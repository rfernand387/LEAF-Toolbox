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
