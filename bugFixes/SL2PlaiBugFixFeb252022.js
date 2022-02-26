// GEE Script to compare SL2P and SNAP Biophysical Processor LAI Estimation from S2
// This has been performed for L2A product from ESA S2A_MSIL2A_20200818T172901_20200818T173624_T14UNV

// SNAP LAI Product
// This has been processed using the SNAP Biophysical Processor for S2 as follows:
// 1. Downloaded S2A_MSIL2A_20200818T172901_20200818T173624_T14UNV L2A product from ESA data hub
// 2. Verified L2A layers EXACTLY match product in GEE 
// 3. Resampled product bands to 20m using bicubic resampling (SNAP L2B processor does not allow different resolutions input)
// 4. Applied SNAP S2 Biophysical processor with options: 20m GEOTIFF output, LAI only
// 5. Uploaded L2B LAI Geotiff into GEE as asset
var laiSNAP = ee.Image('projects/ccmeo-ag-000008/assets/S2A_MSIL2A_20200818T172901_N0214_R055_T14UNV_20200818T201952_resampled_biophysical').rename(['estimateLAI','QC'])  // Use same band names as SL2P
var systemID = '20200818T172901_20200818T173624_T14UNV'                             // GEEsystem ID corresponding to the L2A image

// SL2P LAI Product from LEAF toolbox before and after bug fix
// This has been processed using the JavaScript implementation of LEAF Toolbox found here:
var SL2P = require('users/richardfernandes/SL2P:SL2P')                              // Functions that perform estimation
var S2 = require('users/richardfernandes/SL2P:toolsS2')                             // Cloud masking and geometry for S2
var ib = require('users/richardfernandes/SL2P:imageBands')                          // Functions that perform image band operations except estimation
var collectionName = 'COPERNICUS/S2_SR'                                             // Collection to process

// LEAF Toolbox before Bug fix
var dictionariesSL2P = require('users/richardfernandes/SL2P:dictionaries-SL2P-withbugs');    // Specify collection and algorithms
var colOptions = ee.Dictionary(ee.Dictionary(dictionariesSL2P.make_collection_options()).get(collectionName));  //dictionaries describing sensors and bands for networks
var input_collection = ee.ImageCollection(collectionName)
                           .filterMetadata('system:index','equals',systemID)
                           .map(S2.S2MaskClear)                                // Clear sky snow free  land mask
                           .map(S2.addS2Geometry.bind(null,colOptions))        // Adds geometry bands using metadata
var laiSL2Pbugs = ee.ImageCollection(SL2P.applySL2P(input_collection,'LAI',dictionariesSL2P )).first() ; // will process ALL input scenes but we only have one
var laiSL2Pbugs = laiSL2Pbugs.select(['partition','networkID','QC']).addBands(laiSL2Pbugs.select(['estimateLAI','errorLAI']).divide(1000)) // scale LAI

// LEAF Toolbox after Bug fix
var dictionariesSL2P = require('users/richardfernandes/SL2P:dictionaries-SL2P');    // Specify collection and algorithms
var colOptions = ee.Dictionary(ee.Dictionary(dictionariesSL2P.make_collection_options()).get(collectionName));  //dictionaries describing sensors and bands for networks
var input_collection = ee.ImageCollection(collectionName)
                           .filterMetadata('system:index','equals',systemID)
                           .map(S2.S2MaskClear)                                // Clear sky snow free  land mask
                           .map(S2.addS2Geometry.bind(null,colOptions))        // Adds geometry bands using metadata
var laiSL2P = ee.ImageCollection(SL2P.applySL2P(input_collection,'LAI',dictionariesSL2P )).first(); // will process ALL input scenes
var laiSL2P = laiSL2P.select(['partition','networkID','QC']).addBands(laiSL2P.select(['estimateLAI','errorLAI']).divide(1000)) // scale LAI


Map.centerObject(input_collection);                           // Focus map centre/Map.addLayer(output_collection.select('estimateLAI').max());  // We use maximum value composite for demonstration

// Display the input image, LAI using SL2P from LEAF toolbox and LAI using SNAP
Map.addLayer(input_collection.first(),null,'L2A input')
Map.addLayer(laiSNAP,null,'LAI SNAP')
Map.addLayer(laiSL2Pbugs,null,'LAI SL2P LEAF BUGS');  // We use maximum value composite for demonstration
Map.addLayer(laiSL2P,null,'LAI SL2P LEAF CORRECTED');  // We use maximum value composite for demonstration

// Scatter Plot both estimates vs LAI SNAP
// sample N points from the 2-band image
var values = laiSNAP.select('estimateLAI').rename('SNAPLAI')
                    .addBands(laiSL2Pbugs.select('estimateLAI').rename('SL2PbugsLAI'))
                    .addBands(laiSL2P.select('estimateLAI').rename('SL2PLAI'))
                    .sample({ 'region': laiSNAP.geometry(), 'scale': 20, 'numPixels': 1000,geometries:true}) 
 
Map.addLayer(values.style({ color: 'red', pointSize: 2 }), {}, 'samples')
 
// plot sampled features as a scatter chart
var chart = ui.Chart.feature.byFeature(values,  'SNAPLAI')
  .setChartType('ScatterChart')
  .setOptions({ 'title': 'SL2PLAI bugs vs SNAP','pointSize': 2, 'pointColor': 'red', 'width': 300, 'height': 300, 'titleX': 'SNAPLAI', 'titleY':  ['SL2PbugsLAI','SL2P no bugs LAI'] })
   
print(chart)  
