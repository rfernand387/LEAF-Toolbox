import ee
import time
from datetime import timedelta
from datetime import datetime
import pandas as pd
import eoImage

# ------------------------------------
# Functions for modifying image bands:
# ------------------------------------

# Add a 'date' band: number of days since epoch
def addDate(image):
    return image.addBands(ee.Image.constant(ee.Date(image.date()).millis().divide(86400000)).rename('date').toUint16())


# Compute a delta time property for an image
def deltaTime(midDate, image):
    return ee.Image(image.set("deltaTime",ee.Number(image.date().millis()).subtract(ee.Number(midDate)).abs()))



# return image with selected bands scaled
def scaleBands(bandList, scaleList, offsetList,image):
    bandList = ee.List(bandList)
    scaleList = ee.List(scaleList)
    offsetList = ee.List(offsetList)
    return image.addBands(image.select(bandList).multiply(ee.Image.constant(scaleList)).add(ee.Image.constant(offsetList)).rename(bandList), overwrite = True)


# determine if inputs fall in domain of algorithm
# need to be updated to allow for the domain to vary with partition
def invalidInput(sl2pDomain,bandList,image):
    sl2pDomain = ee.FeatureCollection(sl2pDomain).aggregate_array("DomainCode").sort()
    bandList = ee.List(bandList).slice(3)
    image = ee.Image(image)

    # code image bands into a single band and compare to valid codes to make QC band
    image = image.addBands(image.select(bandList).multiply(ee.Image.constant(ee.Number(10))).ceil().mod(ee.Number(10)).uint8()\
                    .multiply(ee.Image.constant(ee.List.sequence(0,bandList.length().subtract(1)).map(lambda value:
                            ee.Number(10).pow(ee.Number(value)))))\
                    .reduce("sum").remap(sl2pDomain, ee.List.repeat(0, sl2pDomain.length()),1).rename("QC"))
    return image


# reduce all bands of input image to 20 m
def reduceTo20m(input_image):
    image = ee.Image(input_image)
    
    # defauflt image to get scale parameters from

    # set default projection to 20 m resolution
    defaultCrs = 'EPSG:32611'
    defaultScale = 20

    # load a copy of the image and reduce resolution using the above
    reduced_image = image.setDefaultProjection(crs=defaultCrs, scale=defaultScale)
    reduced_image = reduced_image.reduceResolution(reducer=ee.Reducer.mean(), bestEffort=True, maxPixels=ee.Number(2))
    
    return reduced_image


# ------------------------------------
# Functions for determinign date ranges:
# ------------------------------------
def getdateRange(site,bufferTemporalSize):

    site = ee.Feature(site)
    
    # check if the temporal buffer is a date range 
    if (type(bufferTemporalSize[0])==str):
        try: 
            startDate = datetime.strptime(bufferTemporalSize[0],"%Y-%m-%d")
            endDate =  datetime.strptime(bufferTemporalSize[1],"%Y-%m-%d")
            endDatePlusOne = endDate + timedelta(days=1)
            defaultDate=True
        except:
            defaultDate = False
    else:
        defaultDate = False

    # get start and end date for this feature if it 
    if ( defaultDate==False ):
        startDate = datetime.fromtimestamp(ee.Date(site.get('system:time_start')).getInfo()['value']/1000) 
        if ("system:time_end" in site.propertyNames().getInfo()):
            endDate = datetime.fromtimestamp(ee.Date(site.get('system:time_end')).getInfo()['value']/1000) 
        else:
            endDate = datetime.fromtimestamp(ee.Date(site.get('system:time_start')).getInfo()['value']/1000) 
        startDate = startDate + timedelta(days=bufferTemporalSize[0])
        endDate = endDate + timedelta(days=bufferTemporalSize[1])
        endDatePlusOne = endDate + timedelta(days=1)
        
    #do monthly processing 
    if (len(pd.date_range(startDate,endDate,freq='30D')) > 0 ):
        dateRange = pd.DataFrame(pd.date_range(startDate,endDate,freq='30D'),columns=['startDate'])
        dateRange['endDate'] = pd.concat([dateRange['startDate'].tail(-1),pd.DataFrame([endDatePlusOne])],ignore_index=True).values
    else:
        dateRange = pd.DataFrame( {'startDate':[startDate],'endDate':[endDatePlusOne]})

    return dateRange

def rescaleCollection(input_collection,bandName,scale):
        # reproject to output scale based on bandName input projection
        input_collection = ee.ImageCollection(input_collection)
        projection = input_collection.first().select(bandName).projection()
        return input_collection.map( lambda image: image.setDefaultProjection(crs=projection) \
                                                                    .reduceResolution(reducer= ee.Reducer.mean(),maxPixels=1024).reproject(crs=projection,scale=scale))

