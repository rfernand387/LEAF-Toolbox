import ee
import time

# ------------------------------------
# Functions for modifying image bands:
# ------------------------------------

# Add a 'date' band: number of days since epoch
def addDate(image):
    return image.addBands(ee.Image.constant(ee.Date(image.date()).millis().divide(86400000)).rename('date').toUint16())


# Compute a delta time property for an image
def deltaTime(midDate, image):
    return ee.Image(image.set("deltaTime",ee.Number(image.date().millis()).subtract(ee.Number(midDate)).abs()))


# Mask pixels that are not clear sky in a S2 MSI image
def s2MaskClear(image):
    qa = image.select('QA60')
    mask = qa.bitwiseAnd(1<<10).eq(0).And(qa.bitwiseAnd(1<<11).eq(0))
    return image.updateMask(mask)


# add s2 geometry bands scaled by 10000
def addS2Geometry(colOptions, image):
    return (image.addBands(ee.Image.constant(0).multiply(3.1415).divide(180).cos().multiply(10000).toUint16().rename(['cosVZA'])).addBands(image.metadata(colOptions["sza"]).multiply(3.1415).divide(180).cos().multiply(10000).toUint16().rename(['cosSZA'])).addBands(image.metadata(colOptions["saa"]).subtract(image.metadata(colOptions["saa"])).multiply(3.1415).divide(180).cos().multiply(10000).toUint16().rename(['cosRAA'])))


# Sentinel 2 land mask
def s2MaskLand(image):
    return image.updateMask((image.select('SCL').eq(4)).Or(image.select('SCL').eq(5)))


# return image with selected bands scaled
def scaleBands(bandList, scaleList, image):
    bandList = ee.List(bandList)
    scaleList = ee.List(scaleList)
    return image.addBands(image.select(bandList).multiply(ee.Image.constant(scaleList)).rename(bandList), overwrite = True)


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
    
# get image of local zenith angle in degrees give flat earth angles and dem image
# We use the MertiDEM as it is within +/-2 degrees slope and aspect as reference national models in GEE at 3 sigma
    def getZenithAngle(za,aa,elevationImage):
    za = ee.Image(za).divide(180).multiply(3.14159)  # flat earth zenith angke
    aa = ee.Image(aa).divide(180).multiply(3.14159)  # flat earth azimuth angle

    tza = ee.Terrain.slope(elevationImage.clip(aa.geometry())).divide(180).multiply(3.14159)
    taa = ee.Terrain.aspect(elevationImage.clip(aa.geometry())).divide(180).multiply(3.14159)
    
    return za.cos().multiply(tza.cos()).subtract(za.sin().multiply(tza.sin()).multiply(aa.subtract(taa).cos())) \
          .acos() \
          .multiply(180) \
          .divide(3.14159)

# get image of local azimuth angle in degrees give flat earth angles and dem image
# We use the MertiDEM as it is within +/-2 degrees slope and aspect as reference national models in GEE at 3 sigma
def getAzimuthAngle(aa,elevationImage):
    aa = ee.Image(aa).divide(180).multiply(3.14159)  # flat earth azimuth angle

    taa = ee.Terrain.aspect(elevationImage.clip(aa.geometry())).divide(180).multiply(3.14159)
    
    return aa.subtract(taa)





# get band with a single land cover class  image from global land cover collections
# change the remap to select a different class 
# returns a mosaic so be careful to reproject it or add it explictly to an existing band if you want to control its scale and projection
def getLandCoverClassImage(): 
  
  return ee.ImageCollection('users/rfernand387/NA_NALCMS_2015_tiles') \
              .map(lambda image: image.select("b1").rename("partition") ) \
              .merge(ee.ImageCollection("COPERNICUS/Landcover/100m/Proba-V/Global") \
                        .map( lambda image: image.select("discrete_classification").remap([0,20,30,40,50,60,70,80,90,100,111,112,113,114,115,116,121,122,123,124,125,126,200],[0,8,10,15,17,16,19,18,14,13,1,3,1,5,6,6,2,4,2,5,6,6,18],0).toUint8().rename("partition"))) \
              .mosaic() \
              .remap([1,2,3,4,5,6,7,8,14],[1,1,1,1,1,1,1,1,1],0) \
              .rename("LandCover")



# return image collection falling withing for date range of image
def getImageCollectionRange(imageCollection,image):
    imageCollection = ee.ImageCollection(imageCollection)    # image collection to filter
    image = ee.Image(image)                                  # image to match date 

    return imageCollection.map(lambda image: image.set('daterange',ee.DateRange(ee.Date(image.get('system:time_start')),ee.Date(image.get('system:time_end'))))) \
                                                        .filter(ee.Filter.dateRangeContains('daterange', ee.Date(image.get('system:time_start'))))


# add attribute of cover percentage in a feature
def addFeatureLandCoverPercentage(getLandCoverClassImage,scale,feature):
    scale = ee.Number(scale)  # scale tp sample 

    return feature.set('LandCover_PERCENTAGE',
                        getLandCoverClassImage().clip(feature.geometry()) \   
                                     .multiply(100) \ 
                                     .reduceRegion( \
                                          reducer= ee.Reducer.mean(), \
                                          geometry= feature.geometry(), \
                                          scale= scale, \
                                          bestEffort= True, \
                                          tileScale= 16 \
                                        ) \
                                    .get('LandCover') \
                    )
