# Dictionaries for SL2P
# Richard Fernandes

import ee
import toolsS2
import toolsL8
import toolsL9
import toolsHLS


def make_collection_options(fc): 

    COLLECTION_OPTIONS = {
        # Sentinel 2 using 20 m bands:
        'COPERNICUS/S2_SR_HARMONIZED': {
        "name": 'COPERNICUS/S2_SR_HARMONIZED',
        "description": 'Sentinel 2A',
        "Cloudcover": 'CLOUDY_PIXEL_PERCENTAGE',
        "Watercover": 'WATER_PERCENTAGE',
        "sza": 'MEAN_SOLAR_ZENITH_ANGLE',
        "vza": 'MEAN_INCIDENCE_ZENITH_ANGLE_B8A',
        "saa": 'MEAN_SOLAR_AZIMUTH_ANGLE', 
        "vaa": 'MEAN_INCIDENCE_AZIMUTH_ANGLE_B8A',
        "VIS_OPTIONS": 'VIS_OPTIONS',
        "Collection_SL2P": ee.FeatureCollection(fc.s2_createFeatureCollection_estimates()),
        "Collection_SL2Perrors": ee.FeatureCollection(fc.s2_createFeatureCollection_errors()),  
        "sl2pDomain": ee.FeatureCollection(fc.s2_createFeatureCollection_domains()),
        "Network_Ind": ee.FeatureCollection(fc.s2_createFeatureCollection_Network_Ind()),
        "partition": ee.ImageCollection(fc.s2_createImageCollection_partition()),
        "legend": ee.FeatureCollection(fc.s2_createFeatureCollection_legend()),
        "numVariables": 7,
        "exportRes": 20,
        "tools": toolsS2
        },
        # Sentinel 2 using 10 m bands:
        'COPERNICUS/S2_SR_HARMONIZED_10m': {
        "name": 'COPERNICUS/S2_SR_HARMONIZED',
        "description": 'Sentinel 2A',
        "Cloudcover": 'CLOUDY_PIXEL_PERCENTAGE',
        "Watercover": 'WATER_PERCENTAGE',
        "sza": 'MEAN_SOLAR_ZENITH_ANGLE',
        "vza": 'MEAN_INCIDENCE_ZENITH_ANGLE_B8A',
        "saa": 'MEAN_SOLAR_AZIMUTH_ANGLE', 
        "vaa": 'MEAN_INCIDENCE_AZIMUTH_ANGLE_B8A',
        "VIS_OPTIONS": 'VIS_OPTIONS',
        "Collection_SL2P": ee.FeatureCollection(fc.s2_10m_createFeatureCollection_estimates()),
        "Collection_SL2Perrors": ee.FeatureCollection(fc.s2_10m_createFeatureCollection_errors()),  
        "sl2pDomain": ee.FeatureCollection(fc.s2_10m_createFeatureCollection_domains()),
        "Network_Ind": ee.FeatureCollection(fc.s2_10m_createFeatureCollection_Network_Ind()),
        "partition": ee.ImageCollection(fc.s2_10m_createImageCollection_partition()),
        "legend": ee.FeatureCollection(fc.s2_10m_createFeatureCollection_legend()),
        "numVariables": 7,
        "exportRes": 10,
        "tools": toolsHLS
        },
        'LANDSAT/LC08/C02/T1_L2': {
        "name": 'LANDSAT/LC08/C02/T1_L2',
        "description": 'LANDSAT 8',
        "Cloudcover": 'CLOUD_COVER_LAND',
        "Watercover": 'CLOUD_COVER',
        "sza": 'SZA',
        "vza": 'VZA',
        "saa": 'SAA', 
        "vaa": 'VAA',
        "VIS_OPTIONS": 'VIS_OPTIONS',
        "Collection_SL2P": ee.FeatureCollection(fc.l8_createFeatureCollection_estimates()),
        "Collection_SL2Perrors": ee.FeatureCollection(fc.l8_createFeatureCollection_errors()),
        "sl2pDomain": ee.FeatureCollection(fc.l8_createFeatureCollection_domains()),
        "Network_Ind": ee.FeatureCollection(fc.l8_createFeatureCollection_Network_Ind()),
        "partition": ee.ImageCollection(fc.l8_createImageCollection_partition()),
        "legend": ee.FeatureCollection(fc.l8_createFeatureCollection_legend()),
        "numVariables": 7,
        "exportRes": 30,
        "tools": toolsL8
        },
        'LANDSAT/LC09/C02/T1_L2': {
        "name": 'LANDSAT/LC09/C02/T1_L2',
        "description": 'LANDSAT 8',
        "Cloudcover": 'CLOUD_COVER_LAND',
        "Watercover": 'CLOUD_COVER',
        "sza": 'SZA',
        "vza": 'VZA',
        "saa": 'SAA', 
        "vaa": 'VAA',
        "VIS_OPTIONS": 'VIS_OPTIONS',
        "Collection_SL2P": ee.FeatureCollection(fc.l9_createFeatureCollection_estimates()),
        "Collection_SL2Perrors": ee.FeatureCollection(fc.l9_createFeatureCollection_errors()),
        "sl2pDomain": ee.FeatureCollection(fc.l9_createFeatureCollection_domains()),
        "Network_Ind": ee.FeatureCollection(fc.l9_createFeatureCollection_Network_Ind()),
        "partition": ee.ImageCollection(fc.l9_createImageCollection_partition()),
        "legend": ee.FeatureCollection(fc.l9_createFeatureCollection_legend()),
        "numVariables": 7,
        "exportRes": 30,
        "tools": toolsL9
        },
        'NASA/HLS/HLSL30/v002': {
        "name": 'NASA/HLS/HLSL30/v002',
        "description": 'Harmonized Landsat',
        "Cloudcover": 'CLOUD_COVERAGE',
        "Watercover": 'CLOUD_COVERAGE',
        "sza": 'SZA',
        "vza": 'VZA',
        "saa": 'SAA', 
        "vaa": 'VAA',
        "VIS_OPTIONS": 'VIS_OPTIONS',
        "Collection_SL2P": ee.FeatureCollection(fc.l8_createFeatureCollection_estimates()),
        "Collection_SL2Perrors": ee.FeatureCollection(fc.l8_createFeatureCollection_errors()),
        "sl2pDomain": ee.FeatureCollection(fc.l8_createFeatureCollection_domains()),
        "Network_Ind": ee.FeatureCollection(fc.l8_createFeatureCollection_Network_Ind()),
        "partition": ee.ImageCollection(fc.l8_createImageCollection_partition()),
        "legend": ee.FeatureCollection(fc.l8_createFeatureCollection_legend()),
        "numVariables": 7,
        "exportRes": 30,
        "tools": toolsHLS
        }
    }

    return(COLLECTION_OPTIONS)

def make_net_options():

    NET_OPTIONS = {
        'Surface_Reflectance': {
            "COPERNICUS/S2_SR_HARMONIZED": {
                "Name": 'Surface_Reflectance',
                "description": 'Surface_Reflectance',
                "inputBands": ['B4', 'B5', 'B6', 'B7', 'B8A', 'B9', 'B11', 'B12']
            },
            "COPERNICUS/S2_SR_HARMONIZED_10m": {
                "Name": 'Surface_Reflectance',
                "description": 'Surface_Reflectance',
                "inputBands": ['B2', 'B3', 'B4', 'B8']
            },
            'LANDSAT/LC08/C02/T1_L2': {
                "Name": 'Surface_Reflectance',
                "description": 'Surface_Reflectance',
                "inputBands":      [ 'SR_B1','SR_B2','SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
                },
            'LANDSAT/LC09/C02/T1_L2': {
                "Name": 'Surface_Reflectance',
                "description": 'Surface_Reflectance',
                "inputBands":      [ 'SR_B1','SR_B2','SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
                },
            'NASA/HLS/HLSL30/v002': {
                "Name": 'Surface_Reflectance',
                "description": 'Surface_Reflectance',
                "inputBands":      [ 'B1','B2','B3', 'B4', 'B5', 'B6', 'B7'],
                },
            'users/rfernand387/L2avalidation': {
                "Name": 'Surface_Reflectance',
                "description": 'Surface_Reflectance',
                "inputBands":      [ 'B1','B2','B3','B4', 'B5', 'B6', 'B7', 'B8','B8A','B9','B10','B11','B12'],
                }
        },
        'Albedo': {
            "COPERNICUS/S2_SR_HARMONIZED": {
                "Name": 'Albedo',
                "errorName": 'errorAlbedo',
                "maskName": 'maskAlbedo',
                "description": 'Black sky albedo',
                "variable": 6,
                "inputBands":      ['cosVZA', 'cosSZA', 'cosRAA', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8A', 'B11', 'B12'],
                "inputScaling":    [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001],
                "inputOffset":     [0,0,0,0,0,0,0,0,0,0,0],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[1]])))
            },
            "COPERNICUS/S2_SR_HARMONIZED_10m": {
                "Name": 'Albedo',
                "errorName": 'errorAlbedo',
                "maskName": 'maskAlbedo',
                "description": 'Black sky albedo',
                "variable": 6,
                "inputBands":      ['cosVZA', 'cosSZA', 'cosRAA', 'B2', 'B3', 'B4', 'B8'],
                "inputScaling":    [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001],
                "inputOffset":     [0,0,0,0,0,0,0,0],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[1]])))
            },
            'LANDSAT/LC08/C02/T1_L2': {
                "Name": 'Albedo',
                "errorName": 'errorAlbedo',
                "maskName": 'maskAlbedo',
                "description": 'Black sky albedo',
                "variable": 6,
                "inputBands":      ['cosVZA','cosSZA','cosRAA','SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
                "inputScaling":     [0.0001,0.0001,0.0001,2.75e-05,2.75e-05,2.75e-05,2.75e-05,2.75e-05],
                "inputOffset":     [0,0,0,-0.2,-0.2,-0.2,-0.2,-0.2],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[1]])))
            },
            'LANDSAT/LC09/C02/T1_L2': {
                "Name": 'Albedo',
                "errorName": 'errorAlbedo',
                "maskName": 'maskAlbedo',
                "description": 'Black sky albedo',
                "variable": 6,
                "inputBands":      ['cosVZA','cosSZA','cosRAA','SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
                "inputScaling":     [0.0001,0.0001,0.0001,2.75e-05,2.75e-05,2.75e-05,2.75e-05,2.75e-05],
                "inputOffset":     [0,0,0,-0.2,-0.2,-0.2,-0.2,-0.2],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[1]])))
            },
            'NASA/HLS/HLSL30/v002': {
                "Name": 'Albedo',
                "errorName": 'errorAlbedo',
                "maskName": 'maskAlbedo',
                "description": 'Black sky albedo',
                "variable": 6,
                "inputBands":      ['cosVZA','cosSZA','cosRAA','B3', 'B4', 'B5', 'B6', 'B7'],
                "inputScaling":     [0.0001,.0001,.0001,1,1,1,1,1],
                "inputOffset":     [0,0,0,0,0,0,0,0],
                "outmin": (ee.Image(0)),
                "outmax": (ee.Image(1))
            }
        },
        'fAPAR': {
            "COPERNICUS/S2_SR_HARMONIZED": {
                "Name": 'fAPAR',
                "errorName": 'errorfAPAR',
                "maskName": 'maskfAPAR',
                "description": 'Fraction of absorbed photosynthetically active radiation',
                "variable": 2,
                "inputBands":      ['cosVZA', 'cosSZA', 'cosRAA', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8A', 'B11', 'B12'],
                "inputScaling":    [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001],
                "inputOffset":     [0,0,0,0,0,0,0,0,0,0,0],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[1]])))
            },
            "COPERNICUS/S2_SR_HARMONIZED_10m": {
                "Name": 'fAPAR',
                "errorName": 'errorfAPAR',
                "maskName": 'maskfAPAR',
                "description": 'Fraction of absorbed photosynthetically active radiation',
                "variable": 2,
                "inputBands":      ['cosVZA', 'cosSZA', 'cosRAA', 'B2', 'B3', 'B4', 'B8'],
                "inputScaling":    [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001],
                "inputOffset":     [0,0,0,0,0,0,0,0],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[1]])))
            },
            'LANDSAT/LC08/C02/T1_L2': {
                "Name": 'fAPAR',
                "errorName": 'errorfAPAR',
                "maskName": 'maskfAPAR',
                "description": 'Fraction of absorbed photosynthetically active radiation',
                "variable": 2,
                "inputBands":      ['cosVZA','cosSZA','cosRAA','SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
                "inputScaling":     [0.0001,0.0001,0.0001,2.75e-05,2.75e-05,2.75e-05,2.75e-05,2.75e-05],
                "inputOffset":     [0,0,0,-0.2,-0.2,-0.2,-0.2,-0.2],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[1]]))) 
            },
            'LANDSAT/LC09/C02/T1_L2': {
                "Name": 'fAPAR',
                "errorName": 'errorfAPAR',
                "maskName": 'maskfAPAR',
                "description": 'Fraction of absorbed photosynthetically active radiation',
                "variable": 2,
                "inputBands":      ['cosVZA','cosSZA','cosRAA','SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
                "inputScaling":     [0.0001,0.0001,0.0001,2.75e-05,2.75e-05,2.75e-05,2.75e-05,2.75e-05],
                "inputOffset":     [0,0,0,-0.2,-0.2,-0.2,-0.2,-0.2],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[1]]))) 
            },
            'NASA/HLS/HLSL30/v002': {
                "Name": 'fAPAR',
                "errorName": 'errorfAPAR',
                "maskName": 'maskfAPAR',
                "description": 'Fraction of absorbed photosynthetically active radiation',
                "variable": 2,
                "inputBands":      ['cosVZA','cosSZA','cosRAA','B3', 'B4', 'B5', 'B6', 'B7'],
                "inputScaling":     [0.0001,.0001,.0001,1,1,1,1,1],
                "inputOffset":     [0,0,0,0,0,0,0,0],
                "outmin": (ee.Image(0)),
                "outmax": (ee.Image(1))
                }
        },
        'fCOVER': {
            "COPERNICUS/S2_SR_HARMONIZED": {
                "Name": 'fCOVER',
                "errorName": 'errorfCOVER',
                "maskName": 'maskfCOVER',
                "description": 'Fraction of canopy cover',
                "variable": 3,
                "inputBands":      ['cosVZA', 'cosSZA', 'cosRAA', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8A', 'B11', 'B12'],
                "inputScaling":    [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001],
                "inputOffset":     [0,0,0,0,0,0,0,0,0,0,0],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[1]]))) 
            },
            "COPERNICUS/S2_SR_HARMONIZED_10m": {
                "Name": 'fCOVER',
                "errorName": 'errorfCOVER',
                "maskName": 'maskfCOVER',
                "description": 'Fraction of canopy cover',
                "variable": 3,
                "inputBands":      ['cosVZA', 'cosSZA', 'cosRAA', 'B2', 'B3', 'B4', 'B8'],
                "inputScaling":    [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001],
                "inputOffset":     [0,0,0,0,0,0,0,0],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[1]])))
            },
            'LANDSAT/LC08/C02/T1_L2': {
                "Name": 'fCOVER',
                "errorName": 'errorfCOVER',
                "maskName": 'maskfCOVER',
                "description": 'Fraction of canopy cover',
                "variable": 3,
                "inputBands":      ['cosVZA','cosSZA','cosRAA','SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
                "inputScaling":     [0.0001,0.0001,0.0001,2.75e-05,2.75e-05,2.75e-05,2.75e-05,2.75e-05],
                "inputOffset":     [0,0,0,-0.2,-0.2,-0.2,-0.2,-0.2],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[1]]))) 
            },
            'LANDSAT/LC09/C02/T1_L2': {
                "Name": 'fCOVER',
                "errorName": 'errorfCOVER',
                "maskName": 'maskfCOVER',
                "description": 'Fraction of canopy cover',
                "variable": 3,
                "inputBands":      ['cosVZA','cosSZA','cosRAA','SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
                "inputScaling":     [0.0001,0.0001,0.0001,2.75e-05,2.75e-05,2.75e-05,2.75e-05,2.75e-05],
                "inputOffset":     [0,0,0,-0.2,-0.2,-0.2,-0.2,-0.2],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[1]]))) 
            },
            'NASA/HLS/HLSL30/v002': {
                "Name": 'fCOVER',
                "errorName": 'errorfCOVER',
                "maskName": 'maskfCOVER',
                "description": 'Fraction of canopy cover',
                "variable": 3,
                "inputBands":      ['cosVZA','cosSZA','cosRAA','B3', 'B4', 'B5', 'B6', 'B7'],
                "inputScaling":     [0.0001,.0001,.0001,1,1,1,1,1],
                "inputOffset":     [0,0,0,0,0,0,0,0],
                "outmin": (ee.Image(0)),
                "outmax": (ee.Image(1))
                }
        },
        'LAI': {
            "COPERNICUS/S2_SR_HARMONIZED": {
                "Name": 'LAI',
                "errorName": 'errorLAI',
                "maskName": 'maskLAI',
                "description": 'Leaf area index',
                "variable": 1,
                "inputBands":      ['cosVZA', 'cosSZA', 'cosRAA', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8A', 'B11', 'B12'],
                "inputScaling":    [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001],
                "inputOffset":     [0,0,0,0,0,0,0,0,0,0,0],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[10]]))) 
            },
            "COPERNICUS/S2_SR_HARMONIZED_10m": {
                "Name": 'LAI',
                "errorName": 'errorLAI',
                "maskName": 'maskLAI',
                "description": 'Leaf area index',
                "variable": 1,
                "inputBands":      ['cosVZA', 'cosSZA', 'cosRAA', 'B2', 'B3', 'B4', 'B8'],
                "inputScaling":    [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001],
                "inputOffset":     [0,0,0,0,0,0,0,0],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[10]])))
            },
            'LANDSAT/LC08/C02/T1_L2': {
                "Name": 'LAI',
                "errorName": 'errorLAI',
                "maskName": 'maskLAI',
                "description": 'Leaf area index',
                "variable": 1,
                "inputBands":      ['cosVZA','cosSZA','cosRAA','SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
                "inputScaling":     [0.0001,0.0001,0.0001,2.75e-05,2.75e-05,2.75e-05,2.75e-05,2.75e-05],
                "inputOffset":     [0,0,0,-0.2,-0.2,-0.2,-0.2,-0.2],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[10]]))) 
            },
            'LANDSAT/LC09/C02/T1_L2': {
                 "Name": 'LAI',
                "errorName": 'errorLAI',
                "maskName": 'maskLAI',
                "description": 'Leaf area index',
                "variable": 1,
                "inputBands":      ['cosVZA','cosSZA','cosRAA','SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
                "inputScaling":     [0.0001,0.0001,0.0001,2.75e-05,2.75e-05,2.75e-05,2.75e-05,2.75e-05],
                "inputOffset":     [0,0,0,-0.2,-0.2,-0.2,-0.2,-0.2],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[10]]))) 
            },
            'NASA/HLS/HLSL30/v002': {
                "Name": 'LAI',
                "errorName": 'errorLAI',
                "maskName": 'maskLAI',
                "description": 'Leaf area index',
                "variable": 1,
                "inputBands":      ['cosVZA','cosSZA','cosRAA','B3', 'B4', 'B5', 'B6', 'B7'],
                "inputScaling":     [0.0001,.0001,.0001,1,1,1,1,1],
                "inputOffset":     [0,0,0,0,0,0,0,0],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[10]]))) 
                }
        },
        'CCC': {
            "COPERNICUS/S2_SR_HARMONIZED": {
                "Name": 'CCC',
                "errorName": 'errorCCC',
                "maskName": 'maskCCC',
                "description": 'Canopy chlorophyll content',
                "variable": 4,
                "inputBands":      ['cosVZA', 'cosSZA', 'cosRAA', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8A', 'B11', 'B12'],
                "inputScaling":    [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001],
                "inputOffset":     [0,0,0,0,0,0,0,0,0,0,0],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[100]]))) 
            },
            "COPERNICUS/S2_SR_HARMONIZED_10m": {
                "Name": 'CCC',
                "errorName": 'errorCCC',
                "maskName": 'maskCCC',
                "description": 'Canopy chlorophyll content',
                "variable": 4,
                "inputBands":      ['cosVZA', 'cosSZA', 'cosRAA', 'B2', 'B3', 'B4', 'B8'],
                "inputScaling":    [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001],
                "inputOffset":     [0,0,0,0,0,0,0,0],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[100]]))) 
            },
            'LANDSAT/LC08/C02/T1_L2': {
                "Name": 'CCC',
                "errorName": 'errorCCC',
                "maskName": 'maskCCC',
                "description": 'Canopy chlorophyll content',
                "variable": 4,
                "inputBands":      ['cosVZA','cosSZA','cosRAA','SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
                "inputScaling":     [0.0001,0.0001,0.0001,2.75e-05,2.75e-05,2.75e-05,2.75e-05,2.75e-05],
                "inputOffset":     [0,0,0,-0.2,-0.2,-0.2,-0.2,-0.2],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[100]]))) 
            },
            'LANDSAT/LC09/C02/T1_L2': {
                "Name": 'CCC',
                "errorName": 'errorCCC',
                "maskName": 'maskCCC',
                "description": 'Canopy chlorophyll content',
                "variable": 4,
                "inputBands":      ['cosVZA','cosSZA','cosRAA','SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
                "inputScaling":     [0.0001,0.0001,0.0001,2.75e-05,2.75e-05,2.75e-05,2.75e-05,2.75e-05],
                "inputOffset":     [0,0,0,-0.2,-0.2,-0.2,-0.2,-0.2],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[100]]))) 
            },
            'NASA/HLS/HLSL30/v002': {
                "Name": 'CCC',
                "errorName": 'errorCCC',
                "maskName": 'maskCCC',
                "description": 'Canopy chlorophyll content',
                "variable": 4,
                "inputBands":      ['cosVZA','cosSZA','cosRAA','B3', 'B4', 'B5', 'B6', 'B7'],
                "inputScaling":     [0.0001,.0001,.0001,1,1,1,1,1],
                "inputOffset":     [0,0,0,0,0,0,0,0],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[100]]))) 
                }
        },
        'CWC': {
            "COPERNICUS/S2_SR_HARMONIZED": {
                "Name": 'CWC',
                "errorName": 'errorCWC',
                "maskName": 'maskCWC',
                "description": 'Canopy water content',
                "variable": 5,
                "inputBands":      ['cosVZA', 'cosSZA', 'cosRAA', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8A', 'B11', 'B12'],
                "inputScaling":    [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001],
                "inputOffset":     [0,0,0,0,0,0,0,0,0,0,0],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[100]])))
            },
            "COPERNICUS/S2_SR_HARMONIZED_10m": {
                "Name": 'CWC',
                "errorName": 'errorCWC',
                "maskName": 'maskCWC',
                "description": 'Canopy water content',
                "variable": 5,
                "inputBands":      ['cosVZA', 'cosSZA', 'cosRAA', 'B2', 'B3', 'B4', 'B8'],
                "inputScaling":    [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001],
                "inputOffset":     [0,0,0,0,0,0,0,0],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[100]])))
            },
            'LANDSAT/LC08/C02/T1_L2': {
                "Name": 'CWC',
                "errorName": 'errorCWC',
                "maskName": 'maskCWC',
                "description": 'Canopy water content',
                "variable": 5,
                "inputBands":      ['cosVZA','cosSZA','cosRAA','SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
                "inputScaling":     [0.0001,0.0001,0.0001,2.75e-05,2.75e-05,2.75e-05,2.75e-05,2.75e-05],
                "inputOffset":     [0,0,0,-0.2,-0.2,-0.2,-0.2,-0.2],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[1]]))) 
            },  
            'LANDSAT/LC09/C02/T1_L2': {
                "Name": 'CWC',
                "errorName": 'errorCWC',
                "maskName": 'maskCWC',
                "description": 'Canopy water content',
                "variable": 5,
                "inputBands":      ['cosVZA','cosSZA','cosRAA','SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
                "inputScaling":     [0.0001,0.0001,0.0001,2.75e-05,2.75e-05,2.75e-05,2.75e-05,2.75e-05],
                "inputOffset":     [0,0,0,-0.2,-0.2,-0.2,-0.2,-0.2],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[100]])))
            }, 
            'NASA/HLS/HLSL30/v002': {
                "Name": 'CWC',
                "errorName": 'errorCWC',
                "maskName": 'maskCWC',
                "description": 'Canopy water content',
                "variable": 5,
                "inputBands":      ['cosVZA','cosSZA','cosRAA','B3', 'B4', 'B5', 'B6', 'B7'],
                "inputScaling":     [0.0001,.0001,.0001,1,1,1,1,1],
                "inputOffset":     [0,0,0,0,0,0,0,0],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[100]])))
                }
        },
        'DASF': {
            "COPERNICUS/S2_SR_HARMONIZED": {
                "Name": 'DASF',
                "errorName": 'errorDASF',
                "maskName": 'maskDASF',
                "description": 'Directional area scattering factor',
                "variable": 7,
                "inputBands":      ['cosVZA', 'cosSZA', 'cosRAA', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8A', 'B11', 'B12'],
                "inputScaling":    [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001],
                "inputOffset":     [0,0,0,0,0,0,0,0,0,0,0],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[1]]))) 
            },
            "COPERNICUS/S2_SR_HARMONIZED_10m": {
                "Name": 'DASF',
                "errorName": 'errorDASF',
                "maskName": 'maskDASF',
                "description": 'Directional area scattering factor',
                "variable": 7,
                "inputBands":      ['cosVZA', 'cosSZA', 'cosRAA', 'B2', 'B3', 'B4', 'B8'],
                "inputScaling":    [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001],
                "inputOffset":     [0,0,0,0,0,0,0,0],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[1]])))
            },
            'LANDSAT/LC09/C02/T1_L2': {
                "Name": 'DASF',
                "errorName": 'errorDASF',
                "maskName": 'maskDASF',
                "description": 'Directional area scattering factor',
                "variable": 7,
                "inputBands":      ['cosVZA','cosSZA','cosRAA','SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
                "inputScaling":     [0.0001,0.0001,0.0001,2.75e-05,2.75e-05,2.75e-05,2.75e-05,2.75e-05],
                "inputOffset":     [0,0,0,-0.2,-0.2,-0.2,-0.2,-0.2],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[1]]))) 
            }, 
            'NASA/HLS/HLSL30/v002': {
                "Name": 'DASF',
                "errorName": 'errorDASF',
                "maskName": 'maskDASF',
                "description": 'Directional area scattering factor',
                "variable": 7,
                "inputBands":      ['cosVZA','cosSZA','cosRAA','SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
                "inputScaling":     [0.0001,.0001,.0001,1,1,1,1,1],
                "inputOffset":     [0,0,0,0,0,0,0,0],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[1]]))) 
                }, 
            'users/rfernand387/L2avalidation': {
                "Name": 'DASF',
                "errorName": 'errorDASF',
                "maskName": 'maskDASF',
                "description": 'Directional area scattering factor',
                "variable": 7,
                "inputBands":      ['cosVZA','cosSZA','cosRAA','B3', 'B4', 'B5', 'B6', 'B7'],
                "inputScaling":     [0,.0001,.0001,1,1,1,1,1],
                "inputOffset":     [0,0,0,0,0,0,0,0],
                "outmin": (ee.Image(0)),
                "outmax": (ee.Image(1))
            }
        }
    }


    return(NET_OPTIONS)



def make_outputParams():
    # output parameters
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
    return(outputParams)