// SL2P
//
// Simplified Level 2 Prototype Processor
// 
// Appies the Simplified Level 2 Prototype Processor (https://step.esa.int/docs/extra/ATBD_S2ToolBox_L2B_V1.1.pdf). ) 
//to satellite image collections to  produce Level 2b products of vegetation biophysical variables.  
//
// Usage:
//
// 
// Arguments:
// collection (FeatureCollection):
// The input collection. One of:
//
// "COPERNICUS_S2_SR"
// "LANDSAT_LC08_C02_T1_L2"
//
// outputName (String)
// The name of the output biophysical variable.  One of:
//
// 'Albedo' : surface albedo
// 'fAPAR' - fraction of absorbed photosynthetically active radiation
// 'FCOVER'- fraction of canopy cover
// 'LAI' - leaf area index
// 'CWC' - canopy water content
// 'CCC' - canopy chloropyll content
// DASF' - directional area scattering factor
////
// Returns: ImageCollection
//
// Collection of images with one:one correspondence to input images.
// Each image has four bands as specified in https://github.com/rfernand387/LEAF-Toolbox/wiki/Export-Outputs
// estimate{outputName}, quality{outputName}, error{outputName}, qualityError{outputName}
//
// Usage: 
//
//    // Sentinel 2 Example
//    var dictionariesSL2P = require('users/richardfernandes/SL2P:dictionaries'); // Specify collection and algorithms
//    var S2 = require('users/richardfernandes/SL2P:toolsS2')                     // Cloud masking and geometry
//    var collectionName = 'COPERNICUS/S2_SR'
//    var colOptions = ee.Dictionary(ee.Dictionary(dictionariesSL2P.make_collection_options()).get(collectionName));
//    var mapBounds= ee.Geometry.Polygon( [[[-75, 45],[-75, 46], [-74, 46],  [-74, 45]]]);
//    var input_collection = ee.ImageCollection(collectionName)
//                           .filterBounds(mapBounds) 
//                           .filterDate('2018-08-01', '2018-09-30') 
//                          .map(S2.S2MaskClear)                                  // Clear sky snow free  land mask
//                          .map(S2.addS2Geometry.bind(null,colOptions))          // Adds geometry bands using metadata
//    var output_collection = applySL2P(input_collection,'LAI');
//    Map.centerObject(output_collection);
//    Map.addLayer(output_collection.select('estimateLAI').max());
//
//    // Landsat 8 example
//    var dictionariesSL2P = require('users/richardfernandes/SL2P:dictionaries');  // Specify collection and algorithms
//    var L08 = require('users/richardfernandes/SL2P:toolsL08');                   // Cloud masking and geometry
//    var collectionName = 'LANDSAT_LC08_C02_T1_L2'
//    var colOptions = ee.Dictionary(ee.Dictionary(dictionariesSL2P.make_collection_options()).get(collectionName));
//    var mapBounds= ee.Geometry.Polygon( [[[-75, 45],[-75, 46], [-74, 46],  [-74, 45]]]);
//    var input_collection = ee.ImageCollection(collectionName)
//                           .filterBounds(mapBounds) 
//                           .filterDate('2018-08-01', '2018-09-30') 
//                          .map(L08.L08MaskClear)                                // Clear sky snow free  land mask
//                          .map(L08.addL08Geometry.bind(null,colOptions))        // Adds geometry bands using metadata
//    var output_collection = applySL2P(input_collection,'LAI');
//    Map.centerObject(output_collection);
//    Map.addLayer(output_collection.select('estimateLAI').max());
//
// Richard Fernandes, Canada Centre for Remote Sensing, 2022, DOI 10.5281/zenodo.4321297.
// Distributed under  https://open.canada.ca/en/open-government-licence-canada
//

var applySL2P = function(inputCollection,outputName) {
  inputCollection = ee.ImageCollection(input_collection);
  outputName = ee.String(outputName);
  
  // bounds for land cover map
  var mapBounds = inputCollection.geometry();
  
  // Import Modules
  var dictionariesSL2P = require('users/richardfernandes/SL2P:dictionaries');  // 
  var ib = require('users/richardfernandes/SL2P:imageBands');
  var wn = require('users/richardfernandes/SL2P:wrapperNets');

  // Identify Collection and make dictionary for parameters
  var collectionName = input_collection.get('system:id')
  var collectionOptions = ee.Dictionary(ee.Dictionary(dictionariesSL2P.make_collection_options()).get(collectionName));
  var netOptions = ee.Dictionary(ee.Dictionary(ee.Dictionary(dictionariesSL2P.make_net_options()).get(outputName)).get(collectionName));

  // Parse prediction networks
  var numNets = ee.Number(ee.Feature(ee.FeatureCollection((collectionOptions.get("Network_Ind"))).first()).propertyNames().remove('Feature Index').remove('system:index').remove('lon').size())
  var SL2P = ee.List.sequence(1,ee.Number(collectionOptions.get("numVariables")),1).map(function (netNum) { return wn.makeNetVars(collectionOptions.get("Collection_SL2P"),numNets,netNum)});
  var errorsSL2P = ee.List.sequence(1,ee.Number(collectionOptions.get("numVariables")),1).map(function (netNum) { return  wn.makeNetVars(collectionOptions.get("Collection_SL2Perrors"),numNets,netNum)});

  // Get partition used to select network
  var partition = ee.ImageCollection(collectionOptions.get("partition")).filterBounds(mapBounds).mosaic().clip(mapBounds).rename('partition');

  // Pre process input imagery and flag invalid inputs
  var scaled_input_collection = input_collection.map(function (image) { return ib.scaleBands(netOptions.get("inputBands"),netOptions.get("inputScaling"),image)}) 
                                            .map(function (image) { return ib.invalidInput(ee.FeatureCollection(collectionOptions.get("sl2pDomain")),netOptions.get("inputBands"),image)});
  
  // Apply networks to produce mapped parameters
  var estimateSL2P = scaled_input_collection.map(function (image) { return wn.wrapperNNets(SL2P, partition, netOptions, collectionOptions, "estimate", image, outputName)});
  var uncertaintySL2P = scaled_input_collection.map(function (image) { return wn.wrapperNNets(errorsSL2P, partition, netOptions, collectionOptions, "error", image, outputName)});

  // Scale and offset mapped parameter bands
  estimateSL2P = estimateSL2P.map(function (image) { return image.addBands({srcImg: image.select("estimate"+outputName).multiply(ee.Image.constant(netOptions.get("outputScale")).add(ee.Image.constant(netOptions.get("outputOffset")))), overwrite: true})});
  uncertaintySL2P = uncertaintySL2P.map(function (image) { return image.addBands({ srcImg: image.select("error"+outputName).multiply(ee.Image.constant(netOptions.get("outputScale")).add(ee.Image.constant(netOptions.get("outputOffset")))), overwrite: true})});
  
  // Return the estimate and uncertainty images
  return(estimateSL2P.combine(uncertaintySL2P));
};
