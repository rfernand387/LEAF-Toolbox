import ee  

# landsat 8  land mask
# clear and no water, cloud shadow, snow, water
def MaskLand(image):
  image = ee.Image(image)

  qa = image.select('Fmask')
  mask = qa.bitwiseAnd(1).eq(0) \
                  .And(qa.bitwiseAnd(1<<1).eq(0)) \
                  .And(qa.bitwiseAnd(1<<2).eq(0)) \
                  .And(qa.bitwiseAnd(1<<3).eq(0)) \
                  .And(qa.bitwiseAnd(1<<4).eq(0)) \
                  .And(qa.bitwiseAnd(1<<5).eq(0))

  return image.updateMask(mask)



def MaskClear(image):
  image = ee.Image(image)
  
  qa = image.select('Fmask')
  mask = qa.bitwiseAnd(1).eq(0) \
                  .And(qa.bitwiseAnd(1<<1).eq(0)) \
                  .And(qa.bitwiseAnd(1<<2).eq(0)) \
                  .And(qa.bitwiseAnd(1<<3).eq(0))
  return image.updateMask(mask)



# add HLS geomtery bands cosine
def addGeometry(colOptions,image):
  
  geometryBands = image

  return image.addBands(geometryBands.select([colOptions.vza]).divide(1).multiply(3.1415).divide(180).cos().multiply(10000).toUint16().rename('cosVZA')) \
              .addBands(geometryBands.select([colOptions.sza]).divide(1).multiply(3.1415).divide(180).cos().multiply(10000).toUint16().rename('cosSZA')) \
              .addBands(geometryBands.select(colOptions.vaa).subtract(geometryBands.select(colOptions.saa)).divide(1).multiply(3.1415).divide(180).cos().multiply(10000).toUint16().rename('cosRAA'))


# Simple spec score
def addSpecScore(midDate,image):
  return image.addBands(ee.Image(2).subtract(image.select('B1')).rename('spec_score'))
