
// ------------------------------------
// Functions for modifying image bands:
// ------------------------------------

// Add a 'date' band: number of days since epoch
var addDate = function(image) {
    return image.addBands(ee.Image.constant(ee.Date(image.date()).millis().divide(86400000)).rename('date').toUint16());
};

// Compute a delta time property for an image
// Add a 'date' band: number of days since epoch
var deltaTime = function(midDate, image) {
    return ee.Image(image.set("deltaTime",ee.Number(image.date().millis()).subtract(ee.Number(midDate)).abs()));
};

// Mask pixels that are not clear sky in a S2 MSI image
// Add a 'date' band: number of days since epoch
var s2MaskClear = function(image) {
    image = ee.Image(image)
    var qa = ee.Image(image.select(['QA60']));
    var mask = qa.bitwiseAnd(1<<10).eq(0).and(qa.bitwiseAnd(1<<11).eq(0));
    return image.updateMask(mask);
};

// add s2 geometry bands scaled by 10000
// Add a 'date' band: number of days since epoch
var addS2Geometry = function(colOptions, image) {
    return (image.addBands(ee.Image.constant(0).multiply(3.1415).divide(180).cos().multiply(10000).toUint16().rename(['cosVZA'])).addBands(image.metadata(colOptions.get("sza")).multiply(3.1415).divide(180).cos().multiply(10000).toUint16().rename(['cosSZA'])).addBands(image.metadata(colOptions.get("saa")).subtract(image.metadata(colOptions.get("saa"))).multiply(3.1415).divide(180).cos().multiply(10000).toUint16().rename(['cosRAA'])));
};

// Sentinel 2 land mask
// Add a 'date' band: number of days since epoch
var s2MaskLand = function(image) {
    return image.updateMask((image.select('SCL').eq(4)).or(image.select('SCL').eq(5)));
};

// return image with selected bands scaled
// Add a 'date' band: number of days since epoch
var scaleBands= function(bandList, scaleList, image) {
    bandList = ee.List(bandList);
    scaleList = ee.List(scaleList);
    return image.addBands({srcImg: image.select(bandList).multiply(ee.Image.constant(scaleList)).rename(bandList), overwrite: true});
};

// determine if inputs fall in domain of algorithm
// need to be updated to allow for the domain to vary with partition
// Add a 'date' band: number of days since epoch
var invalidInput = function(sl2pDomain,bandList,image) {
    sl2pDomain = ee.FeatureCollection(sl2pDomain).aggregate_array("DomainCode").sort();
    bandList = ee.List(bandList).slice(3);
    image = ee.Image(image);

    // code image bands into a single band and compare to valid codes to make QC band
    image = image.addBands(image.select(bandList).multiply(ee.Image.constant(ee.Number(10))).ceil().mod(ee.Number(10)).uint8()
                    .multiply(ee.Image.constant(ee.List.sequence(0,bandList.length().subtract(1)).map(function (value) { return ee.Number(10).pow(ee.Number(value))})))
                    .reduce("sum").remap(sl2pDomain, ee.List.repeat(0, sl2pDomain.length()),1).rename("QC"));
    return image;
};

// reduce all bands of input image to 20 m
// Add a 'date' band: number of days since epoch
var reduceTo20m = function(input_image) {
    image = ee.Image(input_image);
    
    // defauflt image to get scale parameters from

    // set default projection to 20 m resolution
    var defaultCrs = 'EPSG:32611';
    var defaultScale = 20;

    // load a copy of the image and reduce resolution using the above
    var reduced_image = image.setDefaultProjection(crs=defaultCrs, scale=defaultScale);
    var reduced_image = reduced_image.reduceResolution(reducer=ee.Reducer.mean(), bestEffort=True, maxPixels=ee.Number(2));
    
    return reduced_image;
};




// Export functions
exports.addDate = addDate;
exports.deltaTime = deltaTime;
exports.s2MaskClear = s2MaskClear;
exports.addS2Geometry = addS2Geometry;
exports.s2MaskLand = s2MaskLand;
exports.scaleBands= scaleBands;
exports.invalidInput = invalidInput;
exports.reduceTo20m = reduceTo20m;
