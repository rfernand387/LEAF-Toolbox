// Dictionaries for SL2P - no bugs
// Richard Fernandes

var make_collection_options = function() {

  
var fc = require('users/richardfernandes/SL2P:feature-collections-SL2P-CCRS');
var COLLECTION_OPTIONS =  {
    'COPERNICUS/S2_SR': {
      name: 'S2',
      description: 'Sentinel 2A',
      visParams: {gamma: 1.3, min: 0, max: 3000, bands: ['B4', 'B3', 'B2']},
      Cloudcover: 'CLOUDY_PIXEL_PERCENTAGE',
      Watercover: 'WATER_PERCENTAGE',
      sza: 'MEAN_SOLAR_ZENITH_ANGLE',
      vza: 'MEAN_INCIDENCE_ZENITH_ANGLE_B8A',
      saa: 'MEAN_SOLAR_AZIMUTH_ANGLE', 
      vaa: 'MEAN_INCIDENCE_AZIMUTH_ANGLE_B8A',
      Collection_SL2P: ee.FeatureCollection(fc.s2_createFeatureCollection_estimates()),
      Collection_SL2Perrors: ee.FeatureCollection(fc.s2_createFeatureCollection_errors()),  
      sl2pDomain: ee.FeatureCollection(fc.s2_createFeatureCollection_domains()),
      Network_Ind: ee.FeatureCollection(fc.s2_createFeatureCollection_Network_Ind()),
      partition: ee.ImageCollection(fc.s2_createImageCollection_partition()),
      legend:  ee.FeatureCollection(fc.s2_createFeatureCollection_legend()),
      numVariables: 7,
    },
    'LANDSAT/LC08/C02/T1_L2': {
      name: 'L8',
      description: 'LANDSAT 8',
      visParams: {gamma: 1.3, min: 0, max: 3000, bands: ['SR_B4', 'SR_B3', 'SR_B2']},
      Cloudcover: 'CLOUD_COVER_LAND',
      Watercover: 'CLOUD_COVER',
      sza: 'SUN_ELEVATION',  // will be converted to zenith angle later
      vza: 'SUN_ELEVATION', // dummy value
      saa: 'SUN_AZIMUTH', 
      vaa: 'SUN_AZIMUTH',
      Collection_SL2P: ee.FeatureCollection(fc.l8_createFeatureCollection_estimates()),
      Collection_SL2Perrors: ee.FeatureCollection(fc.l8_createFeatureCollection_errors()),
      sl2pDomain: ee.FeatureCollection(fc.l8_createFeatureCollection_domains()),
      Network_Ind: ee.FeatureCollection(fc.l8_createFeatureCollection_Network_Ind()),
      partition: ee.ImageCollection(fc.l8_createImageCollection_partition()),
      legend:  ee.FeatureCollection(fc.l8_createFeatureCollection_legend()),
      numVariables: 7,
    }
  };

return(COLLECTION_OPTIONS);

}; 

var make_net_options = function() {

var NET_OPTIONS = {
  
  'Surface_Reflectance': {
      'COPERNICUS/S2_SR': {
        Name: 'Surface_Reflectance',
        description: 'Surface_Reflectance',
        outputParams: {gamma: 1.3, min: 0, max: 0.3, bands: ['B7', 'B6', 'B4']},
        inp:      [ 'B1','B2','B3','B4', 'B5', 'B6', 'B7', 'B8','B8A','B9','B10','B11','B12'],
        },
      'LANDSAT/LC08/C02/T1_L2': {
        Name: 'Surface_Reflectance',
        description: 'Surface_Reflectance',
        outputParams: {gamma: 1.3, min: 0, max: 0.3, bands: ['SR_B7', 'SR_B6', 'SR_B4']},
        inp:      [ 'SR_B1','SR_B2','SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
        },
      },
    'Albedo': {
      'COPERNICUS/S2_SR': {
        Name: 'Albedo',
        errorName: 'errorAlbedo',
        maskName: 'maskAlbedo',
        description: 'Black sky albedo',
        variable: 6,
        inputBands:      [ 'cosVZA','cosSZA','cosRAA','B3','B4', 'B5', 'B6', 'B7', 'B8A','B11','B12'],
        inputScaling:      [0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001],
        outputMin: 0,
        outputMax: 1,
        outputScale: 1000,
        outputOffset: 0
      },
      'LANDSAT/LC08/C02/T1_L2': {
        Name: 'Albedo',
        errorName: 'errorAlbedo',
        maskName: 'maskAlbedo',
        description: 'Black sky albedo',
        variable: 6,
        inputBands:      ['cosVZA','cosSZA','cosRAA','SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
        inputScaling:     [0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001],
        outputMin: 0,
        outputMax: 1,
        outputScale: 1000,
        outputOffset: 0
      },
    },
    'fAPAR': {
      'COPERNICUS/S2_SR': {
        Name: 'fAPAR',
        errorName: 'errorfAPAR',
        maskName: 'maskfAPAR',
        description: 'Fraction of absorbed photosynthetically active radiation',
        variable: 2,
        inputBands:      [ 'cosVZA','cosSZA','cosRAA','B3','B4', 'B5', 'B6', 'B7', 'B8A','B11','B12'],
        inputScaling:      [0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001],
        outputMin: 0,
        outputMax: 1,
        outputScale: 1000,
        outputOffset: 0
      },
      'LANDSAT/LC08/C02/T1_L2': {
        Name: 'fAPAR',
        errorName: 'errorfAPAR',
        maskName: 'maskfAPAR',
        description: 'Fraction of absorbed photosynthetically active radiation',
        variable: 2,
        inputBands:      ['cosVZA','cosSZA','cosRAA','SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
        inputScaling:     [0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001],
        outputMin: 0,
        outputMax: 1,
        outputScale: 1000,
        outputOffset: 0
      },
    },
    'fCOVER': {
      'COPERNICUS/S2_SR': {
        Name: 'fCOVER',
        errorName: 'errorfCOVER',
        maskName: 'maskfCOVER',
        description: 'Fraction of canopy cover',
        variable: 3,
        inputBands:      [ 'cosVZA','cosSZA','cosRAA','B3','B4', 'B5', 'B6', 'B7', 'B8A','B11','B12'],
        inputScaling:      [0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001],
        outputMin: 0,
        outputMax: 1,
        outputScale: 1000,
        outputOffset: 0
      },
      'LANDSAT/LC08/C02/T1_L2': {
        Name: 'fCOVER',
        errorName: 'errorfCOVER',
        maskName: 'maskfCOVER',
        description: 'Fraction of canopy cover',
        variable: 3,
        inputBands:      ['cosVZA','cosSZA','cosRAA','SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
        inputScaling:     [0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001],
        outputMin: 0,
        outputMax: 1,
        outputScale: 1000,
        outputOffset: 0
      },
    },
    'LAI': {
      'COPERNICUS/S2_SR': {
        Name: 'LAI',
        errorName: 'errorLAI',
        maskName: 'maskLAI',
        description: 'Leaf area index',
        variable: 1,
        inputBands:      [ 'cosVZA','cosSZA','cosRAA','B3','B4', 'B5', 'B6', 'B7', 'B8A','B11','B12'],
        inputScaling:      [0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001],
        outputMin: 0,
        outputMax: 15,
        outputScale: 1000,
        outputOffset: 0 
      },
      'LANDSAT/LC08/C02/T1_L2': {
        Name: 'LAI',
        errorName: 'errorLAI',
        maskName: 'maskLAI',
        description: 'Leaf area index',
        variable: 1,
        inputBands:      ['cosVZA','cosSZA','cosRAA','SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
        inputScaling:     [0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001],
        outputMin: 0,
        outputMax: 15,
        outputScale: 1000,
        outputOffset: 0
      },
    },
    'CCC': {
      'COPERNICUS/S2_SR': {
        Name: 'CCC',
        errorName: 'errorCCC',
        maskName: 'maskCCC',
        description: 'Canopy chloropyll content',
        variable: 4,
        inputBands:      [ 'cosVZA','cosSZA','cosRAA','B3','B4', 'B5', 'B6', 'B7', 'B8A','B11','B12'],
        inputScaling:      [0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001],
        outputMin: 0,
        outputMax: 1500,
        outputScale: 10,
        outputOffset: 0
      },
      'LANDSAT/LC08/C02/T1_L2': {
        Name: 'CCC',
        errorName: 'errorCCC',
        maskName: 'maskCCC',
        description: 'Canopy chloropyll content',
        variable: 4,
        inputBands:      ['cosVZA','cosSZA','cosRAA','SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
        inputScaling:     [0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001],
        outputMin: 0,
        outputMax: 1500,
        outputScale: 10,
        outputOffset: 0
      },
    },
     'CWC': {
       'COPERNICUS/S2_SR': {
        Name: 'CWC',
        errorName: 'errorCWC',
        maskName: 'maskCWC',
        description: 'Canopy water content',
        variable: 5,
        inputBands:      [ 'cosVZA','cosSZA','cosRAA','B3','B4', 'B5', 'B6', 'B7', 'B8A','B11','B12'],
        inputScaling:      [0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001],
        outputMin: 0,
        outputMax: 15,
        outputScale: 1000,
        outputOffset: 0
      },
      'LANDSAT/LC08/C02/T1_L2': {
        Name: 'CWC',
        errorName: 'errorCWC',
        maskName: 'maskCWC',
        description: 'Canopy water content',
        variable: 5,
        inputBands:      ['cosVZA','cosSZA','cosRAA','SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
        inputScaling:     [0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001],
        outputMin: 0,
        outputMax: 15,
        outputScale: 1000,
        outputOffset: 0
      },   
    },
      'DASF' : {
      'COPERNICUS/S2_SR': {
        Name: 'DASF',
        errorname: 'errorDASF',
        maskname: 'maskDASF',
        description: 'Canopy directional scattering factor',
        variable: 7,
        inputBands:      [ 'cosVZA','cosSZA','cosRAA','B3','B4', 'B5', 'B6', 'B7', 'B8A','B11','B12'],
        inputScaling:      [0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001],
        outputMin: 0,
        outputMax: 1,
        outputScale: 1000,
        outputOffset: 0
      },
      'LANDSAT/LC08/C02/T1_L2': {
        Name: 'DASF',
        errorName: 'errorDASF',
        maskName: 'maskDASF',
        description: 'Canopy directional scattering factor',
        variable: 7,
        inputBands:      ['cosVZA','cosSZA','cosRAA','SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
        inputScaling:     [0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001],
        outputMin: 0,
        outputMax: 1,
        outputScale: 1000,
        outputOffset: 0
      },   
    },
};


return(NET_OPTIONS);
};


var make_outputParams = function () {
// output parameters
outputParams = {
    'Surface_Reflectance': {
        'outputScale': 0,
        'outputOffset': 0,
        'outputMax': 0
    },
    'Albedo': {
        'outputScale': 1000,
        'outputOffset': 0,
        'outputMax': 0.2
    },
    'fAPAR': {
        'outputScale': 1000,
        'outputOffset': 0,
        'outputMax': 1
    },
    'fCOVER': {
        'outputScale': 1000,
        'outputOffset': 0,
        'outputMax': 1
    },
    'LAI': {
        'outputScale': 1000,
        'outputOffset': 0,
        'outputMax': 8
    },
    'CCC': {
        'outputScale': 1000,
        'outputOffset': 0,
        'outputMax': 6
    },
    'CWC': {
        'outputScale': 1000,
        'outputOffset': 0,
        'outputMax': 0.55
    },
    'DASF': {
        'outputScale': 1000,
        'outputOffset': 0,
        'outputMax': 1
    }
}
return(outputParams);
};

exports.make_collection_options = make_collection_options;
exports.make_net_options = make_net_options;
exports.make_outputParams = make_outputParams;
