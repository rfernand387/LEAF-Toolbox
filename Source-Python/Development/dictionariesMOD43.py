# Dictionaries for MOD43
# Richard Fernandes

import ee
import toolsMOD43


def make_collection_options(): 

    COLLECTION_OPTIONS = {
        # MCD43A3.061 MODIS Albedo Daily 500m
        "MODIS/061/MCD43A3": {
        "name": "MODIS/061/MCD43A3",
        "description": 'MCD43A3.061 MODIS Albedo Daily 500m',
        "maskCollection":"MODIS/061/MCD43A2",
        "Collection_estimate": ee.ImageCollection(fc.MCD43A3_createCollection_estimates()),
        "Collection_errors": ee.ImageCollection(fc.MCD43A3_createCollection_errors()),  
        "Domain": ee.ImageCollection(fc.MCD43A3_createCollection_domains()),
        "Range": ee.ImageCollection(fc.MCD43A3_createCollection_domains()),
        "numVariables": 7,
        "exportRes": 500,
        "tools": toolsMOD43
        },
        # MCD43A4.061 MODIS Nadir BRDF-Adjusted Reflectance Daily 500m
        "MODIS/061/MCD43A4": {
        "name": "MODIS/061/MCD43A4",
        "description": 'MCD43A4.061 MODIS Nadir BRDF-Adjusted Reflectance Daily 500m',
        "maskCollection":"MODIS/061/MCD43A2",
        "Collection_estimate": ee.ImageCollection(fc.MCD43A4_createCollection_estimates()),
        "Collection_errors": ee.ImageCollection(fc.MCD43A4_createCollection_errors()),  
        "Domain": ee.ImageCollection(fc.MCD43A4_createCollection_domains()),
        "Range": ee.ImageCollection(fc.MCD43A4_createCollection_domains()),
        "numVariables": 7,
        "exportRes": 500,
        "tools": toolsMOD43
        }
    }

    return(COLLECTION_OPTIONS)

def make_net_options():

    NET_OPTIONS = {
        'Surface_Reflectance': {
             "MODIS/061/MCD43A3": {
                "Name": 'Surface_Reflectance',
                "description": 'White Sky Albedo',
                "inputBands": ['Albedo_WSA_Band1', \
                                'Albedo_WSA_Band2', \
                                'Albedo_WSA_Band3', \
                                'Albedo_WSA_Band4', \
                                'Albedo_WSA_Band5', \
                                'Albedo_WSA_Band6', \
                                'Albedo_WSA_Band7' ]
            },
            "MODIS/061/MCD43A4": {
                "Name": 'Surface_Reflectance',
                "description": 'Nadir BRDF-Adjusted Reflectance',
                "inputBands": ['NADIR_Reflectance_Band1', \
                                'NADIR_Reflectance_Band2', \
                                'NADIR_Reflectance_Band3', \
                                'NADIR_Reflectance_Band4', \
                                'NADIR_Reflectance_Band5', \
                                'NADIR_Reflectance_Band6', \
                                'NADIR_Reflectance_Band7' ]
            }
        },
        'Albedo': {
             "MODIS/061/MCD43A3": {
                "Name": 'Albedo',
                "errorName": 'errorAlbedo',
                "maskName": 'maskAlbedo',
                "description": 'Black sky albedo',
                "variable": 6,
                "inputBands": ['Albedo_WSA_Band1', \
                                'Albedo_WSABand2', \
                                'Albedo_WSA_Band3', \
                                'Albedo_WSA_Band4', \
                                'Albedo_WSA_Band5', \
                                'Albedo_WSA_Band6', \
                                'Albedo_WSA_Band7' ]
                "inputScaling":    [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001],
                "inputOffset":     [0,0,0,0,0,0,0,0],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[1]])))
            }
            "MODIS/061/MCD43A4": {
                "Name": 'Albedo',
                "errorName": 'errorAlbedo',
                "maskName": 'maskAlbedo',
                "description": 'Black sky albedo',
                "variable": 6,
                "inputBands": ['NADIR_Reflectance_Band1', \
                                'NADIR_Reflectance_Band2', \
                                'NADIR_Reflectance_Band3', \
                                'NADIR_Reflectance_Band4', \
                                'NADIR_Reflectance_Band5', \
                                'NADIR_Reflectance_Band6', \
                                'NADIR_Reflectance_Band7' ]
                "inputScaling":    [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001],
                "inputOffset":     [0,0,0,0,0,0,0,0],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[1]])))
            }
        },
        'fAPAR': {
             "MODIS/061/MCD43A3": {
                "Name": 'fAPAR',
                "errorName": 'errorfAPAR',
                "maskName": 'maskfAPAR',
                "description": 'Fraction of absorbed photosynthetically active radiation',
                "variable": 2,
                "inputBands": ['Albedo_WSA_Band1', \
                                'Albedo_WSA_Band2', \
                                'Albedo_WSA_Band3', \
                                'Albedo_WSA_Band4', \
                                'Albedo_WSA_Band5', \
                                'Albedo_WSA_Band6', \
                                'Albedo_WSA_Band7' ]
                "inputScaling":    [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001],
                "inputOffset":     [0,0,0,0,0,0,0,0],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[1]])))
            },
            "MODIS/061/MCD43A4": {
                "Name": 'fAPAR',
                "errorName": 'errorfAPAR',
                "maskName": 'maskfAPAR',
                "description": 'Fraction of absorbed photosynthetically active radiation',
                "variable": 2,
                "inputBands": ['NADIR_Reflectance_Band1', \
                                'NADIR_Reflectance_Band2', \
                                'NADIR_Reflectance_Band3', \
                                'NADIR_Reflectance_Band4', \
                                'NADIR_Reflectance_Band5', \
                                'NADIR_Reflectance_Band6', \
                                'NADIR_Reflectance_Band7' ]
                "inputScaling":    [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001],
                "inputOffset":     [0,0,0,0,0,0,0,0],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[1]])))
            }
        },
        'fCOVER': {
             "MODIS/061/MCD43A3": {
                "Name": 'fCOVER',
                "errorName": 'errorfCOVER',
                "maskName": 'maskfCOVER',
                "description": 'Fraction of canopy cover',
                "variable": 3,
                "inputBands": ['Albedo_WSA_Band1', \
                                'Albedo_WSA_Band2', \
                                'Albedo_WSA_Band3', \
                                'Albedo_WSA_Band4', \
                                'Albedo_WSA_Band5', \
                                'Albedo_WSA_Band6', \
                                'Albedo_WSA_Band7' ]
                "inputScaling":    [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001],
                "inputOffset":     [0,0,0,0,0,0,0,0],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[1]])))
            },
            "MODIS/061/MCD43A4": {
                "Name": 'fCOVER',
                "errorName": 'errorfCOVER',
                "maskName": 'maskfCOVER',
                "description": 'Fraction of canopy cover',
                "variable": 3,
                "inputBands": ['NADIR_Reflectance_Band1', \
                                'NADIR_Reflectance_Band2', \
                                'NADIR_Reflectance_Band3', \
                                'NADIR_Reflectance_Band4', \
                                'NADIR_Reflectance_Band5', \
                                'NADIR_Reflectance_Band6', \
                                'NADIR_Reflectance_Band7' ]
                "inputScaling":    [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001],
                "inputOffset":     [0,0,0,0,0,0,0,0],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[1]])))
            }
        },
        'LAI': {
             "MODIS/061/MCD43A3": {
                "Name": 'LAI',
                "errorName": 'errorLAI',
                "maskName": 'maskLAI',
                "description": 'Leaf area index',
                "variable": 1,
                "inputBands": ['Albedo_WSA_Band1', \
                                'Albedo_WSA_Band2', \
                                'Albedo_WSA_Band3', \
                                'Albedo_WSA_Band4', \
                                'Albedo_WSA_Band5', \
                                'Albedo_WSA_Band6', \
                                'Albedo_WSA_Band7' ]
                "inputScaling":    [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001],
                "inputOffset":     [0,0,0,0,0,0,0,0],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[1]])))
            },
            "MODIS/061/MCD43A4": {
                "Name": 'LAI',
                "errorName": 'errorLAI',
                "maskName": 'maskLAI',
                "description": 'Leaf area index',
                "variable": 1,
                "inputBands": ['NADIR_Reflectance_Band1', \
                                'NADIR_Reflectance_Band2', \
                                'NADIR_Reflectance_Band3', \
                                'NADIR_Reflectance_Band4', \
                                'NADIR_Reflectance_Band5', \
                                'NADIR_Reflectance_Band6', \
                                'NADIR_Reflectance_Band7' ]
                "inputScaling":    [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001],
                "inputOffset":     [0,0,0,0,0,0,0,0],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[1]])))
            }
        },
        'CCC': {
             "MODIS/061/MCD43A3": {
                "Name": 'CCC',
                "errorName": 'errorCCC',
                "maskName": 'maskCCC',
                "description": 'Canopy chlorophyll content',
                "variable": 4,
                "inputBands": ['Albedo_WSA_Band1', \
                                'Albedo_WSA_Band2', \
                                'Albedo_WSA_Band3', \
                                'Albedo_WSA_Band4', \
                                'Albedo_WSA_Band5', \
                                'Albedo_WSA_Band6', \
                                'Albedo_WSA_Band7' ]
                "inputScaling":    [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001],
                "inputOffset":     [0,0,0,0,0,0,0,0],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[1]])))
            },
            "MODIS/061/MCD43A4": {
                "Name": 'CCC',
                "errorName": 'errorCCC',
                "maskName": 'maskCCC',
                "description": 'Canopy chlorophyll content',
                "variable": 4,
                "inputBands": ['NADIR_Reflectance_Band1', \
                                'NADIR_Reflectance_Band2', \
                                'NADIR_Reflectance_Band3', \
                                'NADIR_Reflectance_Band4', \
                                'NADIR_Reflectance_Band5', \
                                'NADIR_Reflectance_Band6', \
                                'NADIR_Reflectance_Band7' ]
                "inputScaling":    [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001],
                "inputOffset":     [0,0,0,0,0,0,0,0],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[1]])))
            }
        },
        'CWC': {
             "MODIS/061/MCD43A3": {
                "Name": 'CWC',
                "errorName": 'errorCWC',
                "maskName": 'maskCWC',
                "description": 'Canopy water content',
                "variable": 5,
                "inputBands": ['Albedo_WSA_Band1', \
                                'Albedo_WSA_Band2', \
                                'Albedo_WSA_Band3', \
                                'Albedo_WSA_Band4', \
                                'Albedo_WSA_Band5', \
                                'Albedo_WSA_Band6', \
                                'Albedo_WSA_Band7' ]
                "inputScaling":    [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001],
                "inputOffset":     [0,0,0,0,0,0,0,0],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[1]])))
            },
            "MODIS/061/MCD43A4": {
                "Name": 'CWC',
                "errorName": 'errorCWC',
                "maskName": 'maskCWC',
                "description": 'Canopy water content',
                "variable": 5,
                "inputBands": ['NADIR_Reflectance_Band1', \
                                'NADIR_Reflectance_Band2', \
                                'NADIR_Reflectance_Band3', \
                                'NADIR_Reflectance_Band4', \
                                'NADIR_Reflectance_Band5', \
                                'NADIR_Reflectance_Band6', \
                                'NADIR_Reflectance_Band7' ]
                "inputScaling":    [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001],
                "inputOffset":     [0,0,0,0,0,0,0,0],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[1]])))
            }
        },
        'DASF': {
             "MODIS/061/MCD43A3": {
                "Name": 'DASF',
                "errorName": 'errorDASF',
                "maskName": 'maskDASF',
                "description": 'Directional area scattering factor',
                "variable": 7,
                "inputBands": ['Albedo_WSA_Band1', \
                                'Albedo_WSA_Band2', \
                                'Albedo_WSA_Band3', \
                                'Albedo_WSA_Band4', \
                                'Albedo_WSA_Band5', \
                                'Albedo_WSA_Band6', \
                                'Albedo_WSA_Band7' ]
                "inputScaling":    [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001],
                "inputOffset":     [0,0,0,0,0,0,0,0],
                "outmin": (ee.Image(ee.Array([[0]]))),
                "outmax": (ee.Image(ee.Array([[1]])))
            },
            "MODIS/061/MCD43A4": {
                "Name": 'DASF',
                "errorName": 'errorDASF',
                "maskName": 'maskDASF',
                "description": 'Directional area scattering factor',
                "variable": 7,
                "inputBands": ['NADIR_Reflectance_Band1', \
                                'NADIR_Reflectance_Band2', \
                                'NADIR_Reflectance_Band3', \
                                'NADIR_Reflectance_Band4', \
                                'NADIR_Reflectance_Band5', \
                                'NADIR_Reflectance_Band6', \
                                'NADIR_Reflectance_Band7' ]
                "inputScaling":    [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001],
                "inputOffset":     [0,0,0,0,0,0,0,0],
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