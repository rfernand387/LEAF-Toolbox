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
