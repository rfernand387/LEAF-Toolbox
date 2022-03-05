// Dictionaries for SL2P - no bugs
// Richard Fernandes

var make_collection_options = function() {

  
var fc = require('users/richardfernandes/SL2P:feature-collections-SL2P');
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
      VIS_OPTIONS: app.VIS_OPTIONS,
      Collection_SL2P: ee.FeatureCollection(app.network.s2_createFeatureCollection_estimates()),
      Collection_SL2Perrors: ee.FeatureCollection(app.network.s2_createFeatureCollection_errors()),  
      sl2pDomain: ee.FeatureCollection(app.network.s2_createFeatureCollection_domains()),
      Network_Ind: ee.FeatureCollection(app.network.s2_createFeatureCollection_Network_Ind()),
      partition: ee.ImageCollection(app.network.s2_createImageCollection_partition()),
      legend:  ee.FeatureCollection(app.network.s2_createFeatureCollection_legend()),
      numVariables: 7,
    },
    'LANDSAT/LC08/C02/T1_L2': {
      name: 'L8',
      description: 'LANDSAT 8',
      visParams: {gamma: 1.3, min: 0, max: 3000, bands: ['SR_B4', 'SR_B3', 'SR_B2']},
      Cloudcover: 'CLOUD_COVER_LAND',
      Watercover: 'CLOUD_COVER',
      sza: 'SZA',
      vza: 'VZA',
      saa: 'SAA', 
      vaa: 'VAA',
      VIS_OPTIONS: app.VIS_OPTIONS,
      Collection_SL2P: ee.FeatureCollection(app.network.l8_createFeatureCollection_estimates()),
      Collection_SL2Perrors: ee.FeatureCollection(app.network.l8_createFeatureCollection_errors()),
      sl2pDomain: ee.FeatureCollection(app.network.l8_createFeatureCollection_domains()),
      Network_Ind: ee.FeatureCollection(app.network.l8_createFeatureCollection_Network_Ind()),
      partition: ee.ImageCollection(app.network.l8_createImageCollection_partition()),
      legend:  ee.FeatureCollection(app.network.l8_createFeatureCollection_legend()),
      numVariables: 7,
    },
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
        outputParams: {gamma: 1.3, min: 0, max: 0.3, bands: ['SR_B4', 'SR_B3', 'SR_B2']},
        inp:      [ 'SR_B1','SR_B2','SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
        },
      'users/rfernand387/L2avalidation': {
        Name: 'Surface_Reflectance',
        description: 'Surface_Reflectance',
        outpuParams: {gamma: 1.3, min: 0, max: 0.3, bands: ['B7', 'B6', 'B4']},
        inp:      [ 'B1','B2','B3','B4', 'B5', 'B6', 'B7', 'B8','B8A','B9','B10','B11','B12'],
        }
      },
    'Albedo': {
      'COPERNICUS/S2_SR': {
        Name: 'Albedo',
        errorName: 'errorAlbedo',
        maskName: 'maskAlbedo',
        description: 'Black sky albedo',
        variable: 6,
        outputParams: { min: 0.1, max: 0.3, palette: app.palettes.misc.jet[7], bands: ['estimateAlbedo']},
        errorParams: { min: -1, max: 1, palette: app.palettes.misc.jet[7], bands: ['errorAlbedo']},
        inputBands:      [ 'cosVZA','cosSZA','cosRAA','B3','B4', 'B5', 'B6', 'B7', 'B8A','B11','B12'],
        inputScaling:      [0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001],
        inputOffset:     [0,0,0,0,0,0,0,0],
        outmin: (ee.Image(ee.Array([[0]]))),
        outmax: (ee.Image(ee.Array([[1]])))
      },
      'LANDSAT/LC08/C02/T1_L2': {
        Name: 'Albedo',
        errorName: 'errorAlbedo',
        maskName: 'maskAlbedo',
        description: 'Black sky albedo',
        variable: 6,
        outputParams: { min: 0, max: 1, palette: app.palettes.misc.jet[7], bands: ['estimateAlbedo']},
        errorParams: { min: -1, max: 1, palette: app.palettes.misc.jet[7], bands: ['errorAlbedo']},
        inputBands:      ['cosVZA','cosSZA','cosRAA','SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
        inputScaling:     [0.0001,0.0001,0.0001,2.75e-05,2.75e-05,2.75e-05,2.75e-05,2.75e-05],
        inputOffset:     [0,0,0,-0.2,-0.2,-0.2,-0.2,-0.2],
        outmin: (ee.Image(ee.Array([[0]]))),
        outmax: (ee.Image(ee.Array([[1]])))
      },
      'users/rfernand387/L2avalidation': {
        Name: 'Albedo',
        errorName: 'errorAlbedo',
        maskName: 'maskAlbedo',
        description: 'Black sky albedo',
        variable: 6,
        outputParams: { min: 0.1, max: 0.3, palette: app.palettes.misc.jet[7], bands: ['estimateAlbedo']},
        errorParams: { min: -1, max: 1, palette: app.palettes.misc.jet[7], bands: ['errorAlbedo']},
        inputBands:      [ 'cosVZA','cosSZA','cosRAA','B3','B4', 'B5', 'B6', 'B7', 'B8A','B11','B12'],
        inputScaling:      [0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001],
        inputOffset:     [0,0,0,0,0,0,0,0],
        outmin: (ee.Image(ee.Array([[0]]))),
        outmax: (ee.Image(ee.Array([[1]])))
      },
    },
    'fAPAR': {
      'COPERNICUS/S2_SR': {
        Name: 'fAPAR',
        errorName: 'errorfAPAR',
        maskName: 'maskfAPAR',
        description: 'Fraction of absorbed photosynthetically active radiation',
        variable: 2,
        outputParams: { min: 0, max: 1, palette: app.palettes.misc.jet[7], bands: ['estimatefAPAR']},
        errorParams: { min: -1, max: 1, palette: app.palettes.misc.jet[7], bands: ['errorfAPAR']},
        inputBands:      [ 'cosVZA','cosSZA','cosRAA','B3','B4', 'B5', 'B6', 'B7', 'B8A','B11','B12'],
        inputScaling:      [0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001],
        inputOffset:     [0,0,0,0,0,0,0,0],
        outmin: (ee.Image(ee.Array([[0]]))),
        outmax: (ee.Image(ee.Array([[1]])))
      },
      'LANDSAT/LC08/C02/T1_L2': {
        Name: 'fAPAR',
        errorName: 'errorfAPAR',
        maskName: 'maskfAPAR',
        description: 'Fraction of absorbed photosynthetically active radiation',
        variable: 2,
        outputParams: { min: 0, max: 1, palette: app.palettes.misc.jet[7], bands: ['estimatefAPAR']},
        errorParams: { min: -1, max: 1, palette: app.palettes.misc.jet[7], bands: ['errorfAPAR']},
        inputBands:      ['cosVZA','cosSZA','cosRAA','SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
        inputScaling:     [0.0001,0.0001,0.0001,2.75e-05,2.75e-05,2.75e-05,2.75e-05,2.75e-05],
        inputOffset:     [0,0,0,-0.2,-0.2,-0.2,-0.2,-0.2],
        outmin: (ee.Image(ee.Array([[0]]))),
        outmax: (ee.Image(ee.Array([[1]]))) 
      },
      'users/rfernand387/L2avalidation': {
        Name: 'fAPAR',
        errorName: 'errorfAPAR',
        maskName: 'maskfAPAR',
        description: 'Fraction of absorbed photosynthetically active radiation',
        variable: 2,
        outputParams: { min: 0, max: 1, palette: app.palettes.misc.jet[7], bands: ['estimatefAPAR']},
        errorParams: { min: -1, max: 1, palette: app.palettes.misc.jet[7], bands: ['errorfAPAR']},
        inputBands:      [ 'cosVZA','cosSZA','cosRAA','B3','B4', 'B5', 'B6', 'B7', 'B8A','B11','B12'],
        inputScaling:      [0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001],
        inputOffset:     [0,0,0,0,0,0,0,0],
        outmin: (ee.Image(ee.Array([[0]]))),
        outmax: (ee.Image(ee.Array([[1]])))
      },
      
    },
    'fCOVER': {
      'COPERNICUS/S2_SR': {
        Name: 'fCOVER',
        errorName: 'errorfCOVER',
        maskName: 'maskfCOVER',
        description: 'Fraction of canopy cover',
        variable: 3,
        outputParams: { min: 0, max: 1, palette: app.palettes.misc.jet[7], bands: ['estimatefCOVER']},
        errorParams: { min: -1, max: 1, palette: app.palettes.misc.jet[7], bands: ['errorfCOVER']},
        inputBands:      [ 'cosVZA','cosSZA','cosRAA','B3','B4', 'B5', 'B6', 'B7', 'B8A','B11','B12'],
        inputScaling:      [0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001],
        inputOffset:     [0,0,0,0,0,0,0,0],
        outmin: (ee.Image(ee.Array([[0]]))),
        outmax: (ee.Image(ee.Array([[1]]))) 
      },
      'LANDSAT/LC08/C02/T1_L2': {
        Name: 'fCOVER',
        errorName: 'errorfCOVER',
        maskName: 'maskfCOVER',
        description: 'Fraction of canopy cover',
        variable: 3,
        outputParams: { min: 0, max: 1, palette: app.palettes.misc.jet[7], bands: ['estimatefCOVER']},
        errorParams: { min: -1, max: 1, palette: app.palettes.misc.jet[7], bands: ['errorfCOVER']},
        inputBands:      ['cosVZA','cosSZA','cosRAA','SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
        inputScaling:     [0.0001,0.0001,0.0001,2.75e-05,2.75e-05,2.75e-05,2.75e-05,2.75e-05],
        inputOffset:     [0,0,0,-0.2,-0.2,-0.2,-0.2,-0.2],
        outmin: (ee.Image(ee.Array([[0]]))),
        outmax: (ee.Image(ee.Array([[1]])))
      },
      'users/rfernand387/L2avalidation': {
        Name: 'fCOVER',
        errorName: 'errorfCOVER',
        maskName: 'maskfCOVER',
        description: 'Fraction of canopy cover',
        variable: 3,
        outputParams: { min: 0, max: 1, palette: app.palettes.misc.jet[7], bands: ['estimatefCOVER']},
        errorParams: { min: -1, max: 1, palette: app.palettes.misc.jet[7], bands: ['errorfCOVER']},
        inputBands:      [ 'cosVZA','cosSZA','cosRAA','B3','B4', 'B5', 'B6', 'B7', 'B8A','B11','B12'],
        inputScaling:      [0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001],
        inputOffset:     [0,0,0,0,0,0,0,0],
        outmin: (ee.Image(ee.Array([[0]]))),
        outmax: (ee.Image(ee.Array([[1]])))  
      },
    },
    'LAI': {
      'COPERNICUS/S2_SR': {
        Name: 'LAI',
        errorName: 'errorLAI',
        maskName: 'maskLAI',
        description: 'Leaf area index',
        variable: 1,
        outputParams: { min: 0, max: 10, palette: app.palettes.misc.jet[7], bands: ['estimateLAI']},
        errorParams: { min: -5, max: 5, palette: app.palettes.misc.jet[7], bands: ['errorLAI']},
        inputBands:      [ 'cosVZA','cosSZA','cosRAA','B3','B4', 'B5', 'B6', 'B7', 'B8A','B11','B12'],
        inputScaling:      [0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001],
        inputOffset:     [0,0,0,0,0,0,0,0],
        outmin: (ee.Image(ee.Array([[0]]))),
        outmax: (ee.Image(ee.Array([[1]]))) 
      },
      'LANDSAT/LC08/C02/T1_L2': {
        Name: 'LAI',
        errorName: 'errorLAI',
        maskName: 'maskLAI',
        description: 'Leaf area index',
        variable: 1,
        outputParams: { min: 0, max: 10, palette: app.palettes.misc.jet[7], bands: ['estimateLAI']},
        errorParams: { min: -5, max: 5, palette: app.palettes.misc.jet[7], bands: ['errorLAI']},
        inputBands:      ['cosVZA','cosSZA','cosRAA','SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
        inputScaling:     [0.0001,0.0001,0.0001,2.75e-05,2.75e-05,2.75e-05,2.75e-05,2.75e-05],
        inputOffset:     [0,0,0,-0.2,-0.2,-0.2,-0.2,-0.2],
        outmin: (ee.Image(ee.Array([[0]]))),
        outmax: (ee.Image(ee.Array([[10]])))
      },
      'users/rfernand387/L2avalidation': {
        Name: 'LAI',
        errorName: 'errorLAI',
        maskName: 'maskLAI',
        description: 'Leaf area index',
        variable: 1,
        outputParams: { min: 0, max: 10, palette: app.palettes.misc.jet[7], bands: ['estimateLAI']},
        errorParams: { min: -5, max: 5, palette: app.palettes.misc.jet[7], bands: ['errorLAI']},
        inputBands:      [ 'cosVZA','cosSZA','cosRAA','B3','B4', 'B5', 'B6', 'B7', 'B8A','B11','B12'],
        inputScaling:      [0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001],
        inputOffset:     [0,0,0,0,0,0,0,0],
        outmin: (ee.Image(ee.Array([[0]]))),
        outmax: (ee.Image(ee.Array([[1]]))) 
      },

    },
    'CCC': {
      'COPERNICUS/S2_SR': {
        Name: 'CCC',
        errorName: 'errorCCC',
        maskName: 'maskCCC',
        description: 'Canopy chloropyll content',
        variable: 4,
        outputParams: { min: 0, max: 1000, palette: app.palettes.misc.jet[7], bands: ['estimateCCC']},
        errorParams: { min: -500, max: 500, palette: app.palettes.misc.jet[7], bands: ['errorCCC']},
        inputBands:      [ 'cosVZA','cosSZA','cosRAA','B3','B4', 'B5', 'B6', 'B7', 'B8A','B11','B12'],
        inputScaling:      [0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001],
        inputOffset:     [0,0,0,0,0,0,0,0],
        outmin: (ee.Image(ee.Array([[0]]))),
        outmax: (ee.Image(ee.Array([[1000]])))
      },
      'LANDSAT/LC08/C02/T1_L2': {
        Name: 'CCC',
        errorName: 'errorCCC',
        maskName: 'maskCCC',
        description: 'Canopy chloropyll content',
        variable: 4,
        outputParams: { min: 0, max: 1000, palette: app.palettes.misc.jet[7], bands: ['estimateCCC']},
        errorParams: { min: -500, max: 500, palette: app.palettes.misc.jet[7], bands: ['errorCCC']},
        inputBands:      ['cosVZA','cosSZA','cosRAA','SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
        inputScaling:     [0.0001,0.0001,0.0001,2.75e-05,2.75e-05,2.75e-05,2.75e-05,2.75e-05],
        inputOffset:     [0,0,0,-0.2,-0.2,-0.2,-0.2,-0.2],
        outmin: (ee.Image(ee.Array([[0]]))),
        outmax: (ee.Image(ee.Array([[1000]])))
      },
      'users/rfernand387/L2avalidation': {
        Name: 'CCC', 
        errorName: 'errorCCC',
        maskName: 'maskCCC',
        description: 'Canopy chloropyll content',
        variable: 4,
        outputParams: { min: 0, max: 1000, palette: app.palettes.misc.jet[7], bands: ['estimateCCC']},
        errorParams: { min: -500, max: 500, palette: app.palettes.misc.jet[7], bands: ['errorCCC']},
        inputBands:      [ 'cosVZA','cosSZA','cosRAA','B3','B4', 'B5', 'B6', 'B7', 'B8A','B11','B12'],
        inputScaling:      [0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001],
        inputOffset:     [0,0,0,0,0,0,0,0],
        outmin: (ee.Image(ee.Array([[0]]))),
        outmax: (ee.Image(ee.Array([[1000]])))
      },

    },
     'CWC': {
       'COPERNICUS/S2_SR': {
        Name: 'CWC',
        errorName: 'errorCWC',
        maskName: 'maskCWC',
        description: 'Canopy water content',
        variable: 5,
        outputParams: { min: 0, max: 100, palette: app.palettes.misc.jet[7], bands: ['estimateCWC']},
        errorParams: { min: -50, max: 50, palette: app.palettes.misc.jet[7], bands: ['errorCWC']},
        inputBands:      [ 'cosVZA','cosSZA','cosRAA','B3','B4', 'B5', 'B6', 'B7', 'B8A','B11','B12'],
        inputScaling:      [0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001],
        inputOffset:     [0,0,0,0,0,0,0,0],
        outmin: (ee.Image(ee.Array([[0]]))),
        outmax: (ee.Image(ee.Array([[100]])))
      },
      'LANDSAT/LC08/C02/T1_L2': {
        Name: 'CWC',
        errorName: 'errorCWC',
        maskName: 'maskCWC',
        description: 'Canopy water content',
        variable: 5,
        outputParams: { min: 0, max: 100, palette: app.palettes.misc.jet[7], bands: ['estimateCWC']},
        errorParams: { min: -50, max: 50, palette: app.palettes.misc.jet[7], bands: ['errorCWC']},
        inputBands:      ['cosVZA','cosSZA','cosRAA','SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
        inputScaling:     [0.0001,0.0001,0.0001,2.75e-05,2.75e-05,2.75e-05,2.75e-05,2.75e-05],
        inputOffset:     [0,0,0,-0.2,-0.2,-0.2,-0.2,-0.2],
        outmin: (ee.Image(ee.Array([[0]]))),
        outmax: (ee.Image(ee.Array([[100]]))) 
      },   
      'users/rfernand387/L2avalidation': {
        Name: 'CWC',
        errorName: 'errorCWC',
        maskName: 'maskCWC',
        description: 'Canopy water content',
        variable: 5,
        outputParams: { min: 0, max: 100, palette: app.palettes.misc.jet[7], bands: ['estimateCWC']},
        errorParams: { min: -50, max: 50, palette: app.palettes.misc.jet[7], bands: ['errorCWC']},
        inputBands:      [ 'cosVZA','cosSZA','cosRAA','B3','B4', 'B5', 'B6', 'B7', 'B8A','B11','B12'],
        inputScaling:      [0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001],
        inputOffset:     [0,0,0,0,0,0,0,0],
        outmin: (ee.Image(ee.Array([[0]]))),
        outmax: (ee.Image(ee.Array([[100]])))
      },

    },
      'DASF' : {
      'COPERNICUS/S2_SR': {
        Name: 'DASF',
        errorname: 'errorDASF',
        maskname: 'maskDASF',
        description: 'Canopy directional scattering factor',
        variable: 7,
        outputParams: { min: 0, max: 1, palette: app.palettes.misc.jet[7], bands: ['estimateDASF']},
        errorParams: { min: -1, max: 1, palette: app.palettes.misc.jet[7], bands: ['errorDASF']},
        inputBands:      [ 'cosVZA','cosSZA','cosRAA','B3','B4', 'B5', 'B6', 'B7', 'B8A','B11','B12'],
        inputScaling:      [0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001],
        inputOffset:     [0,0,0,0,0,0,0,0],
        outmin: (ee.Image(ee.Array([[0]]))),
        outmax: (ee.Image(ee.Array([[2]])))
      },
      'LANDSAT/LC08/C02/T1_L2': {
        Name: 'DASF',
        errorName: 'errorDASF',
        maskName: 'maskDASF',
        description: 'Canopy directional scattering factor',
        variable: 7,
        outputParams: { min: 0, max: 1, palette: app.palettes.misc.jet[7], bands: ['estimateDASF']},
        errorParams: { min: -1, max: 1, palette: app.palettes.misc.jet[7], bands: ['errorDASF']},
        inputBands:      ['cosVZA','cosSZA','cosRAA','SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
        inputScaling:     [0.0001,0.0001,0.0001,2.75e-05,2.75e-05,2.75e-05,2.75e-05,2.75e-05],
        inputOffset:     [0,0,0,-0.2,-0.2,-0.2,-0.2,-0.2],
        outmin: (ee.Image(ee.Array([[0]]))),
        outmax: (ee.Image(ee.Array([[2]])))
      },   
      'users/rfernand387/L2avalidation': {
        Name: 'DASF',
        errorname: 'errorDASF',
        maskname: 'maskDASF',
        description: 'Canopy directional scattering factor',
        variable: 7,
        outputParams: { min: 0, max: 1, palette: app.palettes.misc.jet[7], bands: ['estimateDASF']},
        errorParams: { min: -1, max: 1, palette: app.palettes.misc.jet[7], bands: ['errorDASF']},
        inputBands:      [ 'cosVZA','cosSZA','cosRAA','B3','B4', 'B5', 'B6', 'B7', 'B8A','B11','B12'],
        inputScaling:      [0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001],
        inputOffset:     [0,0,0,0,0,0,0,0],
        outmin: (ee.Image(ee.Array([[0]]))),
        outmax: (ee.Image(ee.Array([[2]])))
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
