// Network specification functios 
// Functions are specific to sensor 

// --------------------
// Sentinel2 Functions:
// --------------------

var s2_createFeatureCollection_estimates = function() {
    return ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/s2_sl2p_weiss_or_prosail_NNT3_Single_0_1')
};

var s2_createFeatureCollection_errors = function() {
    return ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/s2_sl2p_weiss_or_prosail_NNT3_Single_0_1_error')
};

var s2_createFeatureCollection_domains = function() {
    return ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/weiss_or_prosail3_NNT3_Single_0_1_DOMAIN')
};



// Same functions as above using 10 m bands:

var s2_10m_createFeatureCollection_estimates = function() {
    return ee.FeatureCollection('users/kateharvey/s2_sl2p_weiss_or_prosail_10m_NNT1_Single_0_1')
};

var s2_10m_createFeatureCollection_errors = function() {
    return ee.FeatureCollection('users/kateharvey/s2_sl2p_weiss_or_prosail_10m_NNT1_Single_0_1_errors')
};

var s2_10m_createFeatureCollection_domains = function() {
    return ee.FeatureCollection('users/kateharvey/s2_sl2p_weiss_or_prosail_10m_domain')
};



// General functions (used for 10 m and 20 m bands)

var s2_createFeatureCollection_range = function() {
    return ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/weiss_or_prosail3_NNT3_Single_0_1_RANGE')
};

var s2_createFeatureCollection_Network_Ind = function() {
    return ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/Parameter_file_sl2p')
};


var s2_createImageCollection_partition = function() {
    return ee.ImageCollection('users/rfernand387/NA_NALCMS_2015_tiles')
              .map(function (image) { return image.select("b1").rename("partition") })
              .merge(ee.ImageCollection("COPERNICUS/Landcover/100m/Proba-V/Global")
                        .map( function (image) { return image.select("discrete_classification").remap([0,20,30,40,50,60,70,80,90,100,111,112,113,114,115,116,121,122,123,124,125,126,200],[0,8,10,15,17,16,19,18,14,13,1,3,1,5,6,6,2,4,2,5,6,6,18],0).toUint8().rename("partition")}))
};

var s2_createFeatureCollection_legend = function() {
    return ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/Legend_sl2p')
};


// -------------------
// Landsat8 Functions:
// -------------------

var l8_createFeatureCollection_estimates = function() {
    return ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_OUTPUT')
};

var l8_createFeatureCollection_errors = function() {
    return ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_ERRORS')
};

var l8_createFeatureCollection_domains = function() {
    return ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_DOMAIN')
};

var l8_createFeatureCollection_range = function() {
    return ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_RANGE')
};

var l8_createFeatureCollection_Network_Ind = function() {
    return ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/Parameter_file_sl2p')
};

var l8_createImageCollection_partition = function() {
    return ee.ImageCollection('users/rfernand387/NA_NALCMS_2015_tiles')
              .map(function (image) { return image.select("b1").rename("partition") })
              .merge(ee.ImageCollection("COPERNICUS/Landcover/100m/Proba-V/Global")
                        .map( function (image) { return image.select("discrete_classification").remap([0,20,30,40,50,60,70,80,90,100,111,112,113,114,115,116,121,122,123,124,125,126,200],[0,8,10,15,17,16,19,18,14,13,1,3,1,5,6,6,2,4,2,5,6,6,18],0).toUint8().rename("partition")}))
};

var l8_createFeatureCollection_legend = function() {
    return ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/Legend_sl2p')
};


// export functions

exports.s2_createFeatureCollection_estimates = s2_createFeatureCollection_estimates;
exports.s2_createFeatureCollection_errors = s2_createFeatureCollection_errors;
exports.s2_createFeatureCollection_domains = s2_createFeatureCollection_domains;
exports.s2_10m_createFeatureCollection_estimates = s2_10m_createFeatureCollection_estimates;
exports.s2_10m_createFeatureCollection_errors = s2_10m_createFeatureCollection_errors;
exports.s2_10m_createFeatureCollection_domains = s2_10m_createFeatureCollection_domains;
exports.s2_createFeatureCollection_range = s2_createFeatureCollection_range;
exports.s2_createFeatureCollection_Network_Ind = s2_createFeatureCollection_Network_Ind;
exports.s2_createImageCollection_partition = s2_createImageCollection_partition;
exports.s2_createFeatureCollection_legend = s2_createFeatureCollection_legend;
exports.l8_createFeatureCollection_estimates = l8_createFeatureCollection_estimates;
exports.l8_createFeatureCollection_errors = l8_createFeatureCollection_errors;
exports.l8_createFeatureCollection_domains = l8_createFeatureCollection_domains;
exports.l8_createFeatureCollection_range = l8_createFeatureCollection_range;
exports.l8_createFeatureCollection_Network_Ind = l8_createFeatureCollection_Network_Ind;
exports.l8_createImageCollection_partition = l8_createImageCollection_partition;
exports.l8_createFeatureCollection_legend = l8_createFeatureCollection_legend;
