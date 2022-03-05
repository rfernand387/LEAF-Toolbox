// Example to run SL2P that works for either S2 or L08 collectionns

// import dictionaries needed to pre process both S2 and L08 data
var dictionariesSL2P = require('users/richardfernandes/SL2P:dictionaries-SL2P'); // Specify collection and algorithms
var S2 = require('users/richardfernandes/SL2P:toolsS2')                     // Cloud masking and geometry for S2
var L08 = require('users/richardfernandes/SL2P:toolsL8');                   // Cloud masking and geometry for L08
var ib = require('users/richardfernandes/SL2P:imageBands')                     // Cloud masking and geometry
var SL2P = require('users/richardfernandes/SL2P:SL2P')                     // Cloud masking and geometry

// chose a collection
//var collectionName = "COPERNICUS/S2_SR"                                    // Uncomment for S2
var collectionName = "LANDSAT/LC08/C02/T1_L2"                               // Uncomment for L08

// filter images based on you mapBouds, date range and then preprocess
var colOptions = ee.Dictionary(ee.Dictionary(dictionariesSL2P.make_collection_options()).get(collectionName));  //dictionaries describing sensors and bands for networks
var mapBounds= ee.Geometry.Polygon( [[[-75, 45],[-75, 46], [-74, 46],  [-74, 45],[-75,45]]]);   // change to your geometry
var input_collection = ee.ImageCollection(collectionName)
                           .filterBounds(mapBounds) 
                           .filterDate('2020-08-01', '2020-08-30')  
switch (collectionName) {
  case "COPERNICUS/S2_SR":
    input_collection = input_collection.map(S2.S2MaskClear)                                // Clear sky snow free  land mask, uncomment for S2
                                       .map(S2.addS2Geometry.bind(null,colOptions))
  break;
  case "LANDSAT/LC08/C02/T1_L2" :
    input_collection = input_collection.map(L08.L08MaskClear)                                // Clear sky snow free  land mask, uncomment for S2
                                       .map(L08.addL08Geometry.bind(null,colOptions))
  break;  
}

//  Apply processor for a selected variable
var varName = 'LAI'
var output_collection = ee.ImageCollection(SL2P.applySL2P(input_collection,varName,dictionariesSL2P)); // will process ALL input scenes
Map.centerObject(input_collection);                           // Focus map centre
Map.addLayer(output_collection.select('estimateLAI').max());  // We use maximum value composite for demonstration
