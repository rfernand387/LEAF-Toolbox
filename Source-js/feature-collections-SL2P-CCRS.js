
// Constructors for CCRS LEAF Toolbox algorithms
// Richard Fernandes Feb 19, 2022

/*--------------------------------------------------------------------------------*/
/* Landsat 8 Surface_Reflectance SL2P algoirthm - these are incorrect RF Apr 2021 */                 
/*--------------------------------------------------------------------------------*/
var l8_createFeatureCollection_Network_Ind = function(){
  var collection= ee.FeatureCollection('users/hemitshah/Parameter_file_2');
  //print(collection); 
  return(collection);
};

var l8_createImageCollection_partition = function(){
  var collection = ee.ImageCollection('users/rfernand387/NA_NALCMS_2015_tiles')
                     .map(function(image) { return image.select("b1").rename("partition")})
                     .merge(ee.ImageCollection("COPERNICUS/Landcover/100m/Proba-V/Global")
                              .map(function(image) { return image.select("discrete_classification")
                                                                 .remap([0,20,30,40,50,60,70,80,90,100,111,112,113,114,115,116,121,122,123,124,125,126,200],[0,8,10,15,17,16,19,18,14,13,1,3,1,5,6,6,2,4,2,5,6,6,18],0)
                                                                  .toUint8()
                                                                  .rename("partition")}))
                     .mosaic()
  //print(collection); 
  return(collection);
};

var l8_createFeatureCollection_legend = function(){
  var collection= ee.FeatureCollection('users/hemitshah/Legend_csv');
  //print(collection);
  return(collection);
};


var l8_createFeatureCollection_estimates = function(){
  var collection= ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P')
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_CLOSED_CROPLAND_OUTPUT'))
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P'))
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_EVERGREEN_NEEDLEAF_FOREST_OUTPUT'))
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_PASTURE_OUTPUT'))
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_LICHEN_FEATHERMOSS_OUTPUT')) 
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_POLAR_GRASSLAND_OUTPUT'))
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_POLAR_SHRUBLAND_OUTPUT'))
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_SHRUBLAND_OUTPUT')) 
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_SPARSE_CROPLAND_OUTPUT'))
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_SPHAGNUM_FEATHERMOSS_OUTPUT')); 
  //print(collection);
   return(collection);
};

var l8_createFeatureCollection_errors = function(){
  var collection= ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_ERRORS')
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_CLOSED_CROPLAND_ERRORS'))
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_ERRORS'))
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_EVERGREEN_NEEDLEAF_FOREST_ERRORS'))
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_GRASSLAND_PASTURE_ERRORS'))
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_LICHEN_FEATHERMOSS_ERRORS')) 
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_POLAR_GRASSLAND_ERRORS'))
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_POLAR_SHRUBLAND_ERRORS'))
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_SHRUBLAND_ERRORS')) 
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_SPARSE_CROPLAND_ERRORS'))
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_SPHAGNUM_FEATHERMOSS_ERRORS')); 
  //print(collection);
   return(collection);
};

var l8_createFeatureCollection_ranges = function(){
  var collection= ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_RANGE')
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_closed_cropland_RANGE')) 
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_RANGE'))
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_evergreen_needleaf_forest_RANGE')) 
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_grassland_pasture_RANGE')) 
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_lichen_feathermoss_RANGE'))
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_polar_grassland_RANGE')) 
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_polar_shrubland_RANGE')) 
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_shrubland_RANGE')) 
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_sparse_cropland_RANGE')) 
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_sphagnum_feathermoss_RANGE')); 
  //print(collection)
  return(collection);
};

var l8_createFeatureCollection_domains = function(){
  var collection= ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/COPERNICUS_S2_SR_SL2P_DOMAIN')
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/COPERNICUS_S2_SR_SL2P_closed_cropland_DOMAIN')) 
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/COPERNICUS_S2_SR_SL2P_DOMAIN'))
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/COPERNICUS_S2_SR_SL2P_evergreen_needleaf_forest_DOMAIN')) 
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/COPERNICUS_S2_SR_SL2P_grassland_pasture_DOMAIN')) 
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/COPERNICUS_S2_SR_SL2P_lichen_feathermoss_DOMAIN'))
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/COPERNICUS_S2_SR_SL2P_polar_grassland_DOMAIN')) 
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/COPERNICUS_S2_SR_SL2P_polar_shrubland_DOMAIN')) 
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/COPERNICUS_S2_SR_SL2P_shrubland_DOMAIN')) 
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/COPERNICUS_S2_SR_SL2P_sparse_cropland_DOMAIN')) 
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/COPERNICUS_S2_SR_SL2P_sphagnum_feathermoss_DOMAIN')); 

  //print(collection);
  return(collection);
};




/*--------------------------------------------------------------------------------*/
/* Sentinel 2 Surface_Reflectance CCRS algorithm                                 */                 
/*--------------------------------------------------------------------------------*/
var s2_createFeatureCollection_Network_Ind = function(){
  var collection= ee.FeatureCollection('users/hemitshah/Parameter_file_2'); 
  //print(collection); 
  return(collection);
};

var s2_createImageCollection_partition = function(){
  var collection = ee.ImageCollection('users/rfernand387/NA_NALCMS_2015_tiles')
                     .map(function(image) { return image.select("b1").rename("partition")})
                     .merge(ee.ImageCollection("COPERNICUS/Landcover/100m/Proba-V/Global")
                              .map(function(image) { return image.select("discrete_classification")
                                                                 .remap([0,20,30,40,50,60,70,80,90,100,111,112,113,114,115,116,121,122,123,124,125,126,200],[0,8,10,15,17,16,19,18,14,13,1,3,1,5,6,6,2,4,2,5,6,6,18],0)
                                                                  .toUint8()
                                                                  .rename("partition")}));
  return(collection);
};

var s2_createFeatureCollection_legend = function(){
  var collection= ee.FeatureCollection('users/hemitshah/Legend_csv');
  //print(collection);
  return(collection);
};

var s2_createFeatureCollection_estimates = function(){
  var collection= ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/s2_sl2p_weiss_or_prosail_NNT3_Single_0_1') // built up and barren
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/s2_sl2p_weiss_or_prosail_NNT3_Single_0_1'))   // cropland closed
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/s2_sl2p_ROF_sobol_prosail_dbf_big_NNT1_Single_0_1'))  // dbf
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/s2_sl2p_ROF_sobol_prosail_enf_big_NNT1_Single_0_1'))  // enf and mixed
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/s2_sl2p_weiss_or_prosail_NNT3_Single_0_1'))  // wetland
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/s2_sl2p_weiss_or_prosail_NNT3_Single_0_1'))  // dont know
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/s2_sl2p_weiss_or_prosail_NNT3_Single_0_1'))  // grassland
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/s2_sl2p_ROF_sobol_prosail_dbf_big_NNT1_Single_0_1'))  // shrubland
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/s2_sl2p_weiss_or_prosail_NNT3_Single_0_1'))  // cropland open
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/s2_sl2p_weiss_or_prosail_NNT3_Single_0_1')) // dont know
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/s2_sl2p_weiss_or_prosail_NNT3_Single_0_1')); // dont know
  //print(collection);
   return(collection);
};

var s2_createFeatureCollection_errors = function(){
  var collection= ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/s2_sl2p_weiss_or_prosail_NNT3_Single_0_1_error') 
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/s2_sl2p_weiss_or_prosail_NNT3_Single_0_1_error')) 
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/s2_sl2p_ROF_sobol_prosail_dbf_big_NNT1_Single_0_1_errors'))  
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/s2_sl2p_ROF_sobol_prosail_enf_big_NNT1_Single_0_1_errors'))
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/s2_sl2p_weiss_or_prosail_NNT3_Single_0_1)_error'))
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/s2_sl2p_weiss_or_prosail_NNT3_Single_0_1_error'))
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/s2_sl2p_weiss_or_prosail_NNT3_Single_0_1_error'))
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/s2_sl2p_ROF_sobol_prosail_dbf_big_NNT1_Single_0_1_errors'))
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/s2_sl2p_weiss_or_prosail_NNT3_Single_0_1_error'))
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/s2_sl2p_weiss_or_prosail_NNT3_Single_0_1_error'))
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/s2_sl2p_weiss_or_prosail_NNT3_Single_0_1_error')); 
  //print(collection);
   return(collection);
};

var s2_createFeatureCollection_ranges = function(){
  var collection= ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/COPERNICUS_S2_SR_SL2P_RANGE')
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/COPERNICUS_S2_SR_SL2P_RANGE')) 
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/COPERNICUS_S2_SR_SL2P_RANGE')) 
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/COPERNICUS_S2_SR_SL2P_RANGE')) 
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/COPERNICUS_S2_SR_SL2P_RANGE')) 
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/COPERNICUS_S2_SR_SL2P_RANGE')) 
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/COPERNICUS_S2_SR_SL2P_RANGE')) 
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/COPERNICUS_S2_SR_SL2P_RANGE')) 
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/COPERNICUS_S2_SR_SL2P_RANGE')) 
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/COPERNICUS_S2_SR_SL2P_RANGE')) 
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/COPERNICUS_S2_SR_SL2P_RANGE')) 
  //print(collection)
  return(collection);
};

var s2_createFeatureCollection_domains = function(){
  var collection= ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_DOMAIN')
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_DOMAIN'))
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_DOMAIN'))
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_DOMAIN'))
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_DOMAIN'))
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_DOMAIN'))
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_DOMAIN'))
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_DOMAIN'))
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_DOMAIN'))
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_DOMAIN'))
                    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_DOMAIN'))

  //print(collection);
  return(collection);
};




exports.l8_createFeatureCollection_Network_Ind  = l8_createFeatureCollection_Network_Ind
exports.l8_createImageCollection_partition  = l8_createImageCollection_partition
exports.l8_createFeatureCollection_legend = l8_createFeatureCollection_legend
exports.l8_createFeatureCollection_estimates = l8_createFeatureCollection_estimates
exports.l8_createFeatureCollection_errors = l8_createFeatureCollection_errors
exports.l8_createFeatureCollection_ranges = l8_createFeatureCollection_ranges
exports.l8_createFeatureCollection_domains = l8_createFeatureCollection_domains


exports.s2_createFeatureCollection_Network_Ind  = s2_createFeatureCollection_Network_Ind
exports.s2_createImageCollection_partition  = s2_createImageCollection_partition
exports.s2_createFeatureCollection_legend = s2_createFeatureCollection_legend
exports.s2_createFeatureCollection_estimates = s2_createFeatureCollection_estimates
exports.s2_createFeatureCollection_errors = s2_createFeatureCollection_errors
exports.s2_createFeatureCollection_ranges = s2_createFeatureCollection_ranges
exports.s2_createFeatureCollection_domains = s2_createFeatureCollection_domains

// export functions

exports.s2_createFeatureCollection_estimates = s2_createFeatureCollection_estimates;
exports.s2_createFeatureCollection_errors = s2_createFeatureCollection_errors;
exports.s2_createFeatureCollection_domains = s2_createFeatureCollection_domains;
exports.s2_createFeatureCollection_ranges = s2_createFeatureCollection_ranges;
exports.s2_createFeatureCollection_Network_Ind = s2_createFeatureCollection_Network_Ind;
exports.s2_createImageCollection_partition = s2_createImageCollection_partition;
exports.s2_createFeatureCollection_legend = s2_createFeatureCollection_legend;
exports.l8_createFeatureCollection_estimates = l8_createFeatureCollection_estimates;
exports.l8_createFeatureCollection_errors = l8_createFeatureCollection_errors;
exports.l8_createFeatureCollection_domains = l8_createFeatureCollection_domains;
exports.l8_createFeatureCollection_ranges = l8_createFeatureCollection_ranges;
exports.l8_createFeatureCollection_Network_Ind = l8_createFeatureCollection_Network_Ind;
exports.l8_createImageCollection_partition = l8_createImageCollection_partition;
exports.l8_createFeatureCollection_legend = l8_createFeatureCollection_legend;
