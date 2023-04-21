# Dictionaries for SL2P
# Richard Fernandes

import ee 

def make_collection_options(fc): 

    # import featurecollectionsSL2P as fc
    print("here in file")
    import ee

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
        "numVariables": 7
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
        "Network_Ind": ee.FeatureCollection(fc.s2_createFeatureCollection_Network_Ind()),
        "partition": ee.ImageCollection(fc.s2_createImageCollection_partition()),
        "legend": ee.FeatureCollection(fc.s2_createFeatureCollection_legend()),
        "numVariables": 7
        },
        'LANDSAT/LC08/C01/T1_SR': {
        "name": 'LANDSAT/LC08/C01/T1_SR',
        "description": 'LANDSAT 8',
        "Cloudcover": 'CLOUD_COVER_LAND',
        "Watercover": 'CLOUD_COVER',
        "sza": 'SOLAR_ZENITH_ANGLE',
        "vza": 'SOLAR_ZENITH_ANGLE',
        "saa": 'SOLAR_AZIMUTH_ANGLE', 
        "vaa": 'SOLAR_AZIMUTH_ANGLE',
        "VIS_OPTIONS": 'VIS_OPTIONS',
        "Collection_SL2P": ee.FeatureCollection(fc.l8_createFeatureCollection_estimates()),
        "Collection_SL2Perrors": ee.FeatureCollection(fc.l8_createFeatureCollection_errors()),
        "sl2pDomain": ee.FeatureCollection(fc.l8_createFeatureCollection_domains()),
        "Network_Ind": ee.FeatureCollection(fc.l8_createFeatureCollection_Network_Ind()),
        "partition": ee.ImageCollection(fc.l8_createImageCollection_partition()),
        "legend": ee.FeatureCollection(fc.l8_createFeatureCollection_legend()),
        "numVariables": 7
        }
    }

    return(COLLECTION_OPTIONS)

def make_net_options():

    import ee 

    NET_OPTIONS = {
        'Surface_Reflectance': {
            "COPERNICUS/S2_SR_HARMONIZED": {
                "Name": 'Surface_Reflectance',
                "description": 'Surface_Reflectance',
                "inp": ['B4', 'B5', 'B6', 'B7', 'B8A', 'B9', 'B11', 'B12']
            },
            "COPERNICUS/S2_SR_HARMONIZED_10m": {
                "Name": 'Surface_Reflectance',
                "description": 'Surface_Reflectance',
                "inp": ['B2', 'B3', 'B4', 'B8']
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
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[1]])))
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
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[1]])))
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
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[1]]))) 
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
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[1]])))
            },
            "COPERNICUS/S2_SR_HARMONIZED_10m": {
                "Name": 'LAI',
                "errorName": 'errorLAI',
                "maskName": 'maskLAI',
                "description": 'Leaf area index',
                "variable": 1,
                "inputBands":      ['cosVZA', 'cosSZA', 'cosRAA', 'B2', 'B3', 'B4', 'B8'],
                "inputScaling":    [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[1]])))
            }
        },
        'CCC': {
            "COPERNICUS/S2_SR_HARMONIZED": {
                "Name": 'CCC',
                "errorName": 'errorCCC',
                "maskName": 'maskCCC',
                "description": 'Canopy chlorophyll content',
                "variable": 1,
                "inputBands":      ['cosVZA', 'cosSZA', 'cosRAA', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8A', 'B11', 'B12'],
                "inputScaling":    [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[1000]])))
            },
            "COPERNICUS/S2_SR_HARMONIZED_10m": {
                "Name": 'CCC',
                "errorName": 'errorCCC',
                "maskName": 'maskCCC',
                "description": 'Canopy chlorophyll content',
                "variable": 1,
                "inputBands":      ['cosVZA', 'cosSZA', 'cosRAA', 'B2', 'B3', 'B4', 'B8'],
                "inputScaling":    [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[1000]])))
            }
        },
        'CWC': {
            "COPERNICUS/S2_SR_HARMONIZED": {
                "Name": 'CWC',
                "errorName": 'errorCWC',
                "maskName": 'maskCWC',
                "description": 'Canopy water content',
                "variable": 1,
                "inputBands":      ['cosVZA', 'cosSZA', 'cosRAA', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8A', 'B11', 'B12'],
                "inputScaling":    [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[100]])))
            },
            "COPERNICUS/S2_SR_HARMONIZED_10m": {
                "Name": 'CWC',
                "errorName": 'errorCWC',
                "maskName": 'maskCWC',
                "description": 'Canopy water content',
                "variable": 1,
                "inputBands":      ['cosVZA', 'cosSZA', 'cosRAA', 'B2', 'B3', 'B4', 'B8'],
                "inputScaling":    [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001],
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
                "variable": 1,
                "inputBands":      ['cosVZA', 'cosSZA', 'cosRAA', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8A', 'B11', 'B12'],
                "inputScaling":    [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[1]])))
            },
            "COPERNICUS/S2_SR_HARMONIZED_10m": {
                "Name": 'DASF',
                "errorName": 'errorDASF',
                "maskName": 'maskDASF',
                "description": 'Directional area scattering factor',
                "variable": 1,
                "inputBands":      ['cosVZA', 'cosSZA', 'cosRAA', 'B2', 'B3', 'B4', 'B8'],
                "inputScaling":    [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[1]])))
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