
// landsat 8  land mask
// clear and no water, cloud shadow, snow, water
var L08MaskLand = function(image) {
  image = ee.Image(image)

  var qa = image.select('QA_PIXEL');
  var mask = qa.bitwiseAnd(1).eq(0)
                  .and(qa.bitwiseAnd(1<<6).eq(1))
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




// add L8 geomtery bands
var addL08Geometry = function(colOptions,image) {
  colOptions = ee.Dictionary(colOptions)
  image = ee.Image(image)
  
  var sza = ee.Image.constant(180).subtract(ee.Image(image.metadata(colOptions.get("sza"))));
  
  return image.addBands(ee.Image.constant(0).multiply(3.1415).divide(180).cos().rename(['cosVZA']))
              .addBands(sza .multiply(3.1415).divide(180).cos().rename(['cosSZA']))
              .addBands(image.metadata(colOptions.get("saa")).subtract(image.metadata(colOptions.get("saa"))).multiply(3.1415).divide(180).cos().rename(['cosRAA']))
              .addBands(image.select('date'));
}
exports.L08MaskClear = L08MaskClear;
exports.L08MaskLand = L08MaskLand;
exports.addL08Geometry = addL08Geometry;
