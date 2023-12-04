import ee  
import mosaic

# sentinel 2 land mask
def MaskLand(image):
  mask = (image.select('SCL').eq(4)).Or(image.select('SCL').eq(5))
  return image.updateMask(mask)



def MaskClear(image):
  qa = image.select('QA60')
  mask = (qa.bitwiseAnd(1<<10).eq(0)).And(qa.bitwiseAnd(1<<11).eq(0))
  return image.updateMask(mask)


# add s2 geomtery bands scaled by 10000
def addGeometry(colOptions,image):
  return image.addBands(image.metadata(colOptions['vza']).multiply(3.1415).divide(180).cos().multiply(10000).toUint16().rename(['cosVZA'])) \
              .addBands(image.metadata(colOptions['sza']).multiply(3.1415).divide(180).cos().multiply(10000).toUint16().rename(['cosSZA'])) \
              .addBands(image.metadata(colOptions['saa']).subtract(image.metadata(colOptions['vaa'])).multiply(3.1415).divide(180).cos().multiply(10000).toInt16().rename(['cosRAA']))


# spectral score for mosaic
def addSpecScore(image,midDate):
  return toolsMosaic.addSpecScore(image,midDate)



