import ee  
import mosaic

# landsat 8  land mask
# clear and no water, cloud shadow, snow, water
def MaskLand(image):
  image = ee.Image(image)

  qa = image.select('QA_PIXEL').uint16()
  mask = qa.bitwiseAnd(1).eq(0) \
                  .And(qa.bitwiseAnd(1<<4).eq(0)) \
                  .And(qa.bitwiseAnd(1<<5).eq(0)) \
                  .And(qa.bitwiseAnd(1<<7).eq(0))
  return image.updateMask(mask)


def MaskClear(image):
  image = ee.Image(image)
  
  qa = image.select('QA_PIXEL').uint16()
  mask = qa.bitwiseAnd(1).eq(0) \
                  .And(qa.bitwiseAnd(1<<2).eq(0)) \
                  .And(qa.bitwiseAnd(1<<3).eq(0)) \
                  .And(qa.bitwiseAnd(1<<4).eq(0)) \
                  .And(qa.bitwiseAnd(1<<5).eq(0)) 
  return image.updateMask(mask)


# add L8 geomtery bands cosine
def addGeometry(colOptions,image):
  
  geometryBands = ee.ImageCollection("LANDSAT/LC08/C02/T1_TOA").filterMetadata('system:index','equals',image.get('system:index')) .first() 

  return image.addBands(geometryBands.select([colOptions['vza'],colOptions['sza']]).divide(100).multiply(3.1415).divide(180).cos().multiply(10000).toUint16().rename('cosVZA','cosSZA')) \
              .addBands(geometryBands.select(colOptions['vaa']).subtract(geometryBands.select(colOptions['saa'])).divide(100).multiply(3.1415).divide(180).cos().multiply(10000).toUint16().rename('cosRAA')) 


# Simple spec score
def addSpecScore(image,midDate):
  return toolsMosaic.addSpecScore(image,midDate)



