// landsat 8  land mask
// clear and no water, cloud shadow, snow, water
var L08MaskLand = function(image) {
  image = ee.Image(image)

  var qa = image.select('QA_PIXEL');
  var mask = qa.bitwiseAnd(1).eq(0)
                  .and(qa.bitwiseAnd(1<<4).eq(0))
                  .and(qa.bitwiseAnd(1<<5).eq(0))
                  .and(qa.bitwiseAnd(1<<7).eq(0))
  return (image.updateMask(mask));
};


var L08MaskClear = function(image) {
  image = ee.Image(image)
  
  var qa = image.select('QA_PIXEL');
  var mask = qa.bitwiseAnd(1<<1).eq(0)
                  .and(qa.bitwiseAnd(1<<2).eq(0))
                  .and(qa.bitwiseAnd(1<<3).eq(0))
                  .and(qa.bitwiseAnd(1<<4).eq(0))
                  .and(qa.bitwiseAnd(1<<5).eq(0))
  return (image.updateMask(mask));
};







// add L8 geomtery bands cosine
var addL08Geometry = function(colOptions,image) {
  
  var geometryBands = ee.ImageCollection("LANDSAT/LC08/C02/T1_TOA").filterMetadata('system:index','equals',image.get('system:index')) 
                                                                      .first() 

  return image.addBands(geometryBands.select([colOptions.vza,colOptions.sza]).divide(1000).multiply(3.1415).divide(180).cos().multiply(10000).toUint16().rename('cosVZA','cosSZA'))
              .addBands(geometryBands.select(colOptions.vaa).subtract(geometryBands.select(colOptions.saa)).divide(1000).multiply(3.1415).divide(180).cos().multiply(10000).toUint16().rename('cosRAA'))
}      



exports.L08MaskClear = L08MaskClear;
exports.L08MaskLand = L08MaskLand;
exports.addL08Geometry = addL08Geometry;
