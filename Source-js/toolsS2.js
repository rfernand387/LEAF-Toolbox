
// sentinel 2 land mask
var s2MaskLand = function(image) {
  var mask = (image.select('SCL').eq(4)).or(image.select('SCL').eq(5));
  return (image.updateMask(mask));
};



var s2MaskClear= function(image) {
  var qa = image.select('QA60');
  var mask = qa.bitwiseAnd(1<<10).eq(0)
                  .and(qa.bitwiseAnd(1<<11).eq(0));
  return (image.updateMask(mask));
};

// wrapper to use app.mask.sentinel2 with CCRS s2 data
var ccrsSentinel2 = function(image) {
    return image.rename(['B1','B2','B3','B4','B5','B6','B7','B8','B8A','B9','B11','B12','AOT','WVP','SCL','TCI_R','TCI_G','TCI_B','QA10','QA20','QA60','date']);
}
// add s2 geomtery bands scaled by 10000
var addS2Geometry = function(colOptions,image) {


  return (image.addBands(ee.Image.constant(0).multiply(3.1415).divide(180).cos().multiply(10000).toUint16().rename(['cosVZA']))
              .addBands(image.metadata(colOptions.sza).multiply(3.1415).divide(180).cos().multiply(10000).toUint16().rename(['cosSZA']))
              .addBands(image.metadata(colOptions.saa).subtract(image.metadata(colOptions.saa)).multiply(3.1415).divide(180).cos().multiply(10000).toUint16().rename(['cosRAA'])));
}

exports.s2MaskClear = s2MaskClear;
exports.s2MaskLand = s2MaskLand;
exports.ccrsSentinel2 = ccrsSentinel2;
exports.addS2Geometry = addS2Geometry;
