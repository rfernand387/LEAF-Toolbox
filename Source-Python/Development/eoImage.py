import ee


import math
# import eoAuxData as eoAD


UNKNOWN_sensor = 0
LS5_sensor     = 5
LS7_sensor     = 7
LS8_sensor     = 8
LS9_sensor     = 9
MAX_LS_CODE    = 20
S2A_sensor     = 21
S2B_sensor     = 22

MOD_sensor     = 50

TOA_ref        = 1
sur_ref        = 2

DPB_band       = 0
BLU_band       = 1
GRN_band       = 2
RED_band       = 3
NIR_band       = 4
SW1_band       = 5
SW2_band       = 6
RED1_band      = 7
RED1_band      = 8
RED1_band      = 9
WV_band        = 10


pix_score       = 'pix_score'
score_target    = 'score_target'
pix_date        = 'date'
neg_blu_score   = 'neg_blu_score'
Texture_name    = 'texture'
mosaic_ssr_code = 'ssr_code'
PARAM_NDVI      = 'ndvi'



SSR_META_DICT = {
  'S2_SR': { 'NAME': 'S2_SR',
             'SSR_CODE': S2A_sensor,
             'DATA_UNIT': sur_ref,
             'GAIN': 0.0001,
             'OFFSET': 0,
             'ALL_BANDS': ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B8A', 'B9', 'B11', 'B12'],
             'OUT_BANDS': ['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B8A', 'B11', 'B12'], 
             '10M_BANDS': ['B2', 'B3', 'B4', 'B8'],
             'SIX_BANDS': ['B2', 'B3', 'B4', 'B8A', 'B11', 'B12'],
             'NoA_BANDS': ['B4', 'B5', 'B6', 'B7', 'B8', 'B8A', 'B11', 'B12'],
             'GEE_NAME': 'COPERNICUS/S2_SR_HARMONIZED',
             'CLOUD': 'CLOUDY_PIXEL_PERCENTAGE',
             'SZA': 'MEAN_SOLAR_ZENITH_ANGLE',
             'VZA': 'MEAN_INCIDENCE_ZENITH_ANGLE_B8A',
             'SAA': 'MEAN_SOLAR_AZIMUTH_ANGLE', 
             'VAA': 'MEAN_INCIDENCE_AZIMUTH_ANGLE_B8A',
             'BLU': 'B2',
             'GRN': 'B3',
             'RED': 'B4',
             'NIR': 'B8A',
             'SW1': 'B11',
             'SW2': 'B12'},

  'S2_TOA': {'NAME': 'S2_TOA',
             'SSR_CODE': S2A_sensor,
             'DATA_UNIT': TOA_ref,
             'GAIN': 0.0001,
             'OFFSET': 0,
             'ALL_BANDS': ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B8A', 'B9', 'B11', 'B12'],
             'OUT_BANDS': ['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B8A', 'B11', 'B12'], 
             '10M_BANDS': ['B2', 'B3', 'B4', 'B8'],
             'SIX_BANDS': ['B2', 'B3', 'B4', 'B8A', 'B11', 'B12'],
             'NoA_BANDS': ['B4', 'B5', 'B6', 'B7', 'B8', 'B8A', 'B11', 'B12'],
             'GEE_NAME': 'COPERNICUS/S2_HARMONIZED',
             "CLOUD": 'CLOUDY_PIXEL_PERCENTAGE',
             "SZA": 'MEAN_SOLAR_ZENITH_ANGLE',
             "VZA": 'MEAN_INCIDENCE_ZENITH_ANGLE_B8A',
             "SAA": 'MEAN_SOLAR_AZIMUTH_ANGLE', 
             "VAA": 'MEAN_INCIDENCE_AZIMUTH_ANGLE_B8A',
             'BLU': 'B2',
             'GRN': 'B3',
             'RED': 'B4',
             'NIR': 'B8A',
             'SW1': 'B11',
             'SW2': 'B12'},

  'L8_SR': {'NAME': 'L8_SR',
            'SSR_CODE': LS8_sensor,
            'DATA_UNIT': sur_ref,
            'GAIN': 0.0000275,
            'OFFSET': -0.2,
            'ALL_BANDS': ['SR_B1', 'SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
            'OUT_BANDS': ['SR_B1', 'SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'], 
            'SIX_BANDS': ['SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
            'NoA_BANDS': ['SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
            'GEE_NAME': 'LANDSAT/LC08/C02/T1_L2',
            "CLOUD": 'CLOUD_COVER',
            "SZA": 'SUN_ELEVATION',
            "SAA": 'SUN_AZIMUTH', 
            "VZA": 'SUN_ELEVATION',            
            "VAA": 'SUN_AZIMUTH',
            'BLU': 'SR_B2',
            'GRN': 'SR_B3',
            'RED': 'SR_B4',
            'NIR': 'SR_B5',
            'SW1': 'SR_B6',
            'SW2': 'SR_B7'},

  'L9_SR': {'NAME': 'L9_SR',
            'SSR_CODE': LS9_sensor,
            'DATA_UNIT': sur_ref,
            'GAIN': 0.0000275,
            'OFFSET': -0.2,
            'ALL_BANDS': ['SR_B1', 'SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
            'OUT_BANDS': ['SR_B1', 'SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'], 
            'SIX_BANDS': ['SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
            'NoA_BANDS': ['SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
            'GEE_NAME': 'LANDSAT/LC09/C02/T1_L2',
            "CLOUD": 'CLOUD_COVER',
            "SZA": 'SUN_ELEVATION',
            "VZA": 'SUN_ELEVATION',
            "SAA": 'SUN_AZIMUTH', 
            "VAA": 'SUN_AZIMUTH',
            'BLU': 'SR_B2',
            'GRN': 'SR_B3',
            'RED': 'SR_B4',
            'NIR': 'SR_B5',
            'SW1': 'SR_B6',
            'SW2': 'SR_B7'},

  'L7_SR': {'NAME': 'L7_SR',
            'SSR_CODE': LS7_sensor,
            'DATA_UNIT': sur_ref,
            'GAIN': 0.0000275,
            'OFFSET': -0.2,
            'ALL_BANDS': ['SR_B1', 'SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B7'],
            'OUT_BANDS': ['SR_B1', 'SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B7'], 
            'SIX_BANDS': ['SR_B1', 'SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B7'],
            'NoA_BANDS': ['SR_B3', 'SR_B4', 'SR_B5', 'SR_B7'],
            'GEE_NAME': 'LANDSAT/LE07/C02/T1_L2',
            "CLOUD": 'CLOUD_COVER',
            "SZA": 'SUN_ELEVATION',
            "SAA": 'SUN_AZIMUTH', 
            "VZA": 'SUN_ELEVATION',            
            "VAA": 'SUN_AZIMUTH',
            'BLU': 'SR_B1',
            'GRN': 'SR_B2',
            'RED': 'SR_B3',
            'NIR': 'SR_B4',
            'SW1': 'SR_B5',
            'SW2': 'SR_B7'},

  'L5_SR': {'NAME': 'L5_SR',
            'SSR_CODE': LS5_sensor,
            'DATA_UNIT': sur_ref,
            'GAIN': 0.0000275,
            'OFFSET': -0.2,
            'ALL_BANDS': ['SR_B1', 'SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B7'],
            'OUT_BANDS': ['SR_B1', 'SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B7'], 
            'SIX_BANDS': ['SR_B1', 'SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B7'],
            'NoA_BANDS': ['SR_B3', 'SR_B4', 'SR_B5', 'SR_B7'],
            'GEE_NAME': 'LANDSAT/LT05/C02/T1_L2', 
            "CLOUD": 'CLOUD_COVER',
            "SZA": 'SUN_ELEVATION',
            "SAA": 'SUN_AZIMUTH', 
            "VZA": 'SUN_ELEVATION',            
            "VAA": 'SUN_AZIMUTH',
            'BLU': 'SR_B1',
            'GRN': 'SR_B2',
            'RED': 'SR_B3',
            'NIR': 'SR_B4',
            'SW1': 'SR_B5',
            'SW2': 'SR_B7'},

  'L8_TOA': {'NAME': 'L8_TOA',
             'SSR_CODE': LS8_sensor,
             'DATA_UNIT': TOA_ref,
             'GAIN': 1,
             'OFFSET': 0,
             'ALL_BANDS': ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7'],
             'OUT_BANDS': ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7'], 
             'SIX_BANDS': ['B2', 'B3', 'B4', 'B5', 'B6', 'B7'],
             'NoA_BANDS': ['B4', 'B5', 'B6', 'B7'],
             'GEE_NAME': 'LANDSAT/LC08/C02/T1_TOA',
             "CLOUD": 'CLOUD_COVER',
             "SZA": 'SUN_ELEVATION',
             "VZA": 'SUN_ELEVATION',
             "SAA": 'SUN_AZIMUTH', 
             "VAA": 'SUN_AZIMUTH',
             'BLU': 'B2',
             'GRN': 'B3',
             'RED': 'B4',
             'NIR': 'B5',
             'SW1': 'B6',
             'SW2': 'B7'},

  'L9_TOA': {'NAME': 'L9_TOA',
             'SSR_CODE': LS9_sensor,
             'DATA_UNIT': TOA_ref,
             'GAIN': 1,
             'OFFSET': 0,
             'ALL_BANDS': ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7'],
             'OUT_BANDS': ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7'], 
             'SIX_BANDS': ['B2', 'B3', 'B4', 'B5', 'B6', 'B7'],
             'NoA_BANDS': ['B4', 'B5', 'B6', 'B7'],
             'GEE_NAME': 'LANDSAT/LC09/C02/T1_TOA',
             "CLOUD": 'CLOUD_COVER',
             "SZA": 'SUN_ELEVATION',
             "VZA": 'SUN_ELEVATION',
             "SAA": 'SUN_AZIMUTH', 
             "VAA": 'SUN_AZIMUTH',
             'BLU': 'B2',
             'GRN': 'B3',
             'RED': 'B4',
             'NIR': 'B5',
             'SW1': 'B6',
             'SW2': 'B7'},
  'L7_TOA': {'NAME': 'L7_TOA',
            'SSR_CODE': LS7_sensor,
            'DATA_UNIT': TOA_ref,
            'GAIN': 1,
            'OFFSET': 0,
            'ALL_BANDS': ['B1', 'B2', 'B3', 'B4', 'B5', 'B7'],
            'OUT_BANDS': ['B1', 'B2', 'B3', 'B4', 'B5', 'B7'], 
            'SIX_BANDS': ['B1', 'B2', 'B3', 'B4', 'B5', 'B7'],
            'NoA_BANDS': ['B3', 'B4', 'B5', 'B7'],
            'GEE_NAME': 'LANDSAT/LE07/C02/T1_TOA',
            "CLOUD": 'CLOUD_COVER',
            "SZA": 'SUN_ELEVATION',
            "SAA": 'SUN_AZIMUTH', 
            "VZA": 'SUN_ELEVATION',            
            "VAA": 'SUN_AZIMUTH',
            'BLU': 'B1',
            'GRN': 'B2',
            'RED': 'B3',
            'NIR': 'B4',
            'SW1': 'B5',
            'SW2': 'B7'},
           
  'MOD_SR': {'NAME': 'MOD09_SR',
             'SSR_CODE': MOD_sensor,
             'DATA_UNIT': sur_ref,
             'GAIN': 0.0001,
             'OFFSET': 0,
             'ALL_BANDS': ['sur_refl_b03', 'sur_refl_b04', 'sur_refl_b01', 'sur_refl_b02', 'sur_refl_b05', 'sur_refl_b06', 'sur_refl_b07'],
             'OUT_BANDS': ['sur_refl_b03', 'sur_refl_b04', 'sur_refl_b01', 'sur_refl_b02', 'sur_refl_b05', 'sur_refl_b06', 'sur_refl_b07'], 
             'SIX_BANDS': ['sur_refl_b03', 'sur_refl_b04', 'sur_refl_b01', 'sur_refl_b02', 'sur_refl_b06', 'sur_refl_b07'],
             'NoA_BANDS': ['sur_refl_b01', 'sur_refl_b02', 'sur_refl_b06', 'sur_refl_b07'],
             'GEE_NAME': 'MODIS/061/MOD09A1', #Terra Surface Refklectance 8-day Global 500m
             "CLOUD": 'CLOUD_COVER',
             "SZA": 'SolarZenith',
             "SAA": 'SolarAzimuth', 
             "VZA": 'SensorZenith',             
             "VAA": 'SensorAzimuth',
             'BLU': 'sur_refl_b03',
             'GRN': 'sur_refl_b04',
             'RED': 'sur_refl_b01',
             'NIR': 'sur_refl_b02',
             'SW1': 'sur_refl_b06',
             'SW2': 'sur_refl_b07'}
}


DATA_TYPE   = ['S2_SR', 'LS8_SR', 'LS9_SR', 'LS7_SR', 'LS5_SR', 'S2_TOA', 'LS8_TOA', 'LS9_TOA', 'LS7_TOA', 'LS5_TOA']
STD_6_BANDS = ['blue', 'green', 'red', 'nir', 'swir1', 'swir2']
MONTH_NAMES = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']





#############################################################################################################
# Description: This function returns sensor_code, tile_name and acquisition date according to a given 
#              Image ID string.   
# 
# Samples: (1) Landsat image ID string:    LC08_034010_20230727    
#          (2) Sentinel-2 image ID string: 20220806T173909_20220806T173907_T17WMU
#
# Revision history:  2023-Nov-20  Lixin Sun  Initial creation
#
#############################################################################################################
def parse_ImgID(ImgID_str):
  tokens = ImgID_str.split('_')
  ssr_code = UNKNOWN_sensor
  tile_name = ''
  acq_date  = ''

  if len(tokens) > 2:
    # Determine the sensor type based on the first token
    if tokens[0].find('LC') > -1:  # is a Landsat scene
      if tokens[0].find('8'):
        ssr_code = LS8_sensor
      elif tokens[0].find('9'):
        ssr_code = LS9_sensor
      elif tokens[0].find('7'):
        ssr_code = LS7_sensor  
      elif tokens[0].find('5'):
        ssr_code = LS5_sensor

      # Determine tile name and acquisition date
      tile_name = tokens[1] 
      acq_date  = tokens[2]
    else: # is a Sentinel-2 scene
      ssr_code  = S2A_sensor
      tile_name = tokens[2]
      acq_date  = tokens[0][0:8]
  
  return ssr_code, tile_name, acq_date





#############################################################################################################
# Description: This function returns a key for retrieving a sensor data dictionary from "SSR_META_DICT" based
#              on a sensor code and a data unit.
#             
# Revision history:  2022-Nov-20  Lixin Sun  Initial creation
#
#############################################################################################################
def get_SsrData_key(SsrCode, DataUnit):
  if DataUnit == sur_ref:
    if SsrCode == LS8_sensor:
      return 'L8_SR'
    elif SsrCode == LS9_sensor:
      return 'L9_SR'
    elif SsrCode == S2A_sensor or SsrCode == S2B_sensor:
      return 'S2_SR'
    elif SsrCode == LS7_sensor:
      return 'L7_SR'
  elif DataUnit == TOA_ref:
    if SsrCode == LS8_sensor:
      return 'L8_TOA'
    elif SsrCode == LS9_sensor:
      return 'L9_TOA'
    elif SsrCode == S2A_sensor or SsrCode == S2B_sensor:
      return 'S2_TOA'
  else:
    print('<get_SsrData> Wrong sensor code or data unit provided!')
    return ''




###################################################################################################
# Description: This function returns a cloud coverage percentage based on a given region and 
#              sensor type code.
#
# Revision history:  2021-June-09  Lixin Sun  Initial creation
#
###################################################################################################
def get_cloud_rate(SsrData, Region):
  '''Returns a cloud coverage percentage based on the given location and sensor type. 
     Args:
        SsrData(Dictionary): A Dictionary containing metadata associated with a sensor and data unit;
        Polygon(ee.Geometry): A geospatial region of ROI.'''
  ssr_code = ee.Number(SsrData['SSR_CODE'])
  region   = ee.Geometry(Region)
  
  # Determine the centre point of the given geographical region
  centre   = region.centroid()
  latitude = ee.Number(centre.coordinates().get(1))
  
  # Determine cloud coverage percentage based on sensor type and location
  ST2_rate = ee.Algorithms.If(latitude.lt(55), 85, 70)
  LS_rate  = 90

  return ee.Algorithms.If(ssr_code.gt(MAX_LS_CODE), ST2_rate, LS_rate)






###################################################################################################
# Description: This function returns rescaling factors for converting the pixel values of an image
#              (either TOA or surface rflectance) to a range either between 0 and 100 or between 
#              0 and 1.
#
# Note:        The gain and offset for diffrent sensors and different data units are gathered from
#              GEE Data Catalog and summarized as follows:
#
#    Sensor  |  TOA reflectance  |  surface reflectance | TOA reflectance  |  surface reflectance |
#            | out range [0,100] | out range [1,100]    | out range [0,1]  | out range [1,1]      | 
#  ------------------------------------------------------------------------------------------------
#   coeffs   |    gain  offset   |    gain     offset   |  gain  offset   |  gain      offset     |             
#   S2       |    0.01   +0      |    0.01       +0     | 0.0001   0.0    | 0.0001       0.0      | 
#   L9 coll2 |    100    +0      |    0.00275    -20    | 1.0      0.0    | 0.0000275   -0.2      |
#   L8 coll2 |    100    +0      |    0.00275    -20    | 1.0      0.0    | 0.0000275   -0.2      |
#   L7 coll2 |    100    +0      |    0.00275    -20    | 1.0      0.0    | 0.0000275   -0.2      |
#   L5 coll2 |    100    +0      |    0.00275    -20    | 1.0      0.0    | 0.0000275   -0.2      |
#  ------------------------------------------------------------------------------------------------
#
# Revision history:  2021-May-10  Lixin Sun  Converted from Lixin's JavaScript code
#                    2022-Mar-24  Lixin Sun  Renamed the function from "get_rescale" to 
#                                            "get_gain_offset" since Landsat Collection-2 data uses
#                                            gain/scale and offset, instead of just scale only. 
#                    2022-Mar-29  Lixin Sun  Add 'MaxRef' parameter so that proper scaling factors
#                                            for different reflectance value ranges (either [0 to 1]
#                                            or [0 to 100]) are returned.  
###################################################################################################
def get_gain_offset(SsrData, MaxRef):
  '''Returns a rescaling factor based on given sensor code and data unit.

     Args:        
        SsrData(Dictionary): A Dictionary containing metadata associated with a sensor and data unit;
        MaxRef: The maximum output reflectance value (1 or 100)''' 
  max_ref = ee.Number(MaxRef)
  gain    = max_ref.multiply(SsrData['GAIN'])
  offset  = max_ref.multiply(SsrData['OFFSET'])

  return gain, offset  





###################################################################################################
# Description: This function applys gain and offset to the optical bands of a given image.
#
# Revision history:  2022-Mar-24  Lixin Sun  Initial creation
#                    2022-Mar-28  Lixin Sun  Add 'MaxRef' parameter so that different reflectance
#                                            ranges ([0 to 1] or [0 to 100]) can be handled.  
###################################################################################################
def apply_gain_offset(Image, SsrData, MaxRef, all_bands):
  '''Returns a rescaling factor based on given sensor code and data unit.

     Args:        
       image(ee.Image): A given ee.Image object to which gain and offset will be applied  
       SsrData(Dictionary): A Dictionary containing metadata associated with a sensor and data unit;
       MaxREF: The maximum reflectance value (1 or 100);
       all_bands(Boolean): A flag indicating if apply gain and offset to all bands or not.''' 
  image = ee.Image(Image)
  
  gain, offset = get_gain_offset(SsrData, MaxRef)
  #print('<apply_gain_offset> Rescaling gain and offset = \n',gain_offset[0], gain_offset[1])
  
  if all_bands == True:
    return image.multiply(gain).add(offset)
  else:
    opti_names = SsrData['ALL_BANDS']                 # Get the names of all optical bands
    opti_img   = image.select(opti_names)             # Extract all optical bands from the given image
    opti_img   = opti_img.multiply(gain).add(offset)  # Apply gain and offset

    return image.addBands(opti_img, opti_names, True) # Put back the rescaled optical bands into original image






###################################################################################################
# Description: This function returns a list of standard band names to be used in a classification
#
# Revision history:  2021-Jun-30  Lixin Sun  Initial creation
###################################################################################################
# def get_STD_classf_bands():
#   return ['green', 'red', 'nir', 'swir1', 'swir2', eoAD.NightLight_name, eoAD.RoadDensity_name]





###################################################################################################
# Description: This function attaches a date band to the given ee.Image object.
#
# Revision history:  2020-Juy-10  Lixin Sun  Initial creation
#                    2021-May-10  Lixin Sun  Converted from Lixin's JavaScript code
#                    2023-Dec-01  Richard Fernandes Name changed to attach_Doy from attach_Date

#
###################################################################################################
def attach_Doy(inImg):
  '''Attaches an image acquisition day of year  band to a given image
  Args:
    Img(ee.Image): A given ee.Image object.'''
  
  #86,400,000 is the milliseconds of one day
  ImgDate  = ee.Date(inImg.date()) 
  DOY_1st  = ee.Date.fromYMD(ImgDate.get('year'), 1, 1).millis().divide(86400000)
  DOY      = ImgDate.millis().divide(86400000).subtract(DOY_1st)
  
  date_img = ee.Image.constant(DOY).rename(pix_date).toUint16()
  return inImg.addBands(date_img)

###################################################################################################
# Description: This function attaches a date band to the given ee.Image object.
#
# Revision history:  2023_Dec-01  Richard Fernandes Initial creation
#
###################################################################################################
def attach_LonLat(inImg):
  '''Attaches an image acquisition date band to a given image ini milliseconds since Jan 1, 1970
  Args:
    Img(ee.Image): A given ee.Image object.'''

  return inImg.addBands(ee.Image.pixelLonLat()) 


###################################################################################################
# Description: This function attaches a a date band in milliseconds since Jan 1, 1970
#
# Revision history:  2023_Dec-01  Richard Fernandes Initial creation

#
###################################################################################################
def attach_Date(inImg):
  '''Attaches an image acquisition date band to a given image ini milliseconds since Jan 1, 1970
  Args:
    Img(ee.Image): A given ee.Image object.'''

  return inImg.addBands(ee.Image.constant(inImg.date().millis()).rename('date') )
  

###################################################################################################
# Description: This function adds three angle bands to a satellite SURFACE reflectance image
#
# Note:        This function is mainly used by LEAF tool
#  
# Revision history:  2021-May-19  Lixin Sun  Initial creation
#                    2021-May-10  Lixin Sun  Converted from Lixin's JavaScript code
#                    2022-Jun-22  Lixin Sun  Removed scaling factor
#
###################################################################################################
def attach_S2AngleBands(Image, SsrData):
  '''Attaches three angle bands to a satallite SURFACE REFLECTANCE image
  Args:    
    Image(ee.Image): A given Sentinel-2 surface reflectance image;
    SsrData(Dictionary): A Dictionary containing metadata associated with a sensor and data unit.'''  
  rad     = ee.Number(math.pi/180.0)  

  vza_rad = ee.Image.constant(Image.getNumber(SsrData['VZA']).multiply(rad))
  sza_rad = ee.Image.constant(Image.getNumber(SsrData['SZA']).multiply(rad))

  raa     = Image.getNumber(SsrData['SAA']).subtract(Image.getNumber(SsrData['VAA']))
  raa_rad = ee.Image.constant(raa.multiply(rad))
  
  return (Image.addBands(vza_rad.cos().rename(['cosVZA'])) \
               .addBands(sza_rad.cos().rename(['cosSZA'])) \
               .addBands(raa_rad.cos().rename(['cosRAA'])))               
  


###################################################################################################
# Description: This function attach a NDVI band to a given image.
#  
# Revision history:  2022-Aug-10  Lixin Sun  Initial creation
#
###################################################################################################
def attach_NDVIBand(Image, SsrData):
  '''Attaches three angle bands to a satallite SURFACE REFLECTANCE image
  Args:
    Image(ee.Image): A given Sentinel-2 surface reflectance image;
    SsrData(Dictionary): A Dictionary containing metadata associated with a sensor and data unit.'''  

  gain, offset = get_gain_offset(SsrData, 100)  
  
  red = Image.select(SsrData['RED']).multiply(gain).add(offset)
  nir = Image.select(SsrData['NIR']).multiply(gain).add(offset)
    
  ndvi  = nir.subtract(red).divide(nir.add(red)).rename(PARAM_NDVI)
  return Image.addBands(ndvi)




###################################################################################################
# Description: This function returns a month name string according to a month number integer.
#  
# Revision history:  2022-Aug-10  Lixin Sun  Initial creation
#
###################################################################################################
def get_MonthName(month_numb):
  month = int(month_numb)

  if month > 0 and month < 13:
    return MONTH_NAMES[month-1]
  else:
    return 'Mone'





###################################################################################################
# Description: This function normalizes the spectral values with the sum of corresponding spectrum. 
#
# Revision history:  2022-Jun-10  Lixin Sun  Initial creation
#
###################################################################################################
def normalize_pixValues(Image, ValScale):
  '''Attaches three angle bands to a satallite SURFACE REFLECTANCE image
  Args:
    Image(ee.Image): A given ee.Image object;
    ValScale(float): A given value scaling factor to be applied to normalized values.'''
  # Cast the input parameters to right type
  image = ee.Image(Image)
  scale = float(ValScale)
  
  img_sum = image.reduce(ee.Reducer.sum()) 
 
  return image.divide(img_sum).multiply(ee.Image(scale))
 





###################################################################################################
# Description: This function creates a spectral angle map based on two given ee.Image objects
#              covering the same ground area. 
#
# Revision history:  2022-Jun-10  Lixin Sun  Initial creation
#
###################################################################################################
def CVA_SAM(Image1, Image2, ValScale):
  '''Attaches three angle bands to a satallite SURFACE REFLECTANCE image
  Args:
    Image1(ee.Image): The first given ee.Image object;
    Image2(ee.Image): The second given ee.Image object;
    ValScale(float): A given value scaling factor to be applied to normalized values.'''
  # Cast the input parameters to right type
  image1 = ee.Image(Image1)
  image2 = ee.Image(Image2)
  scale  = float(ValScale)

  #Conduct pixel value normalization if "scale" is greater than 1
  if scale > 1:
    image1 = normalize_pixValues(image1, scale)
    image2 = normalize_pixValues(image2, scale)
  
  #Calculate numerate and denominator of spectral angle formula
  numerate     = image1.multiply(image2).reduce(ee.Reducer.sum()) 
  
  denominator1 = image1.multiply(image1).reduce(ee.Reducer.sum())
  denominator2 = image2.multiply(image2).reduce(ee.Reducer.sum())
  denominator  = denominator1.multiply(denominator2).sqrt()
  
  #Create spectral angle map
  SAM_map =  numerate.divide(denominator).acos()

  return SAM_map.where(SAM_map.lt(ee.Image(0.35)), ee.Image(0))





###################################################################################################
# Description: This function returns a superpixel ee.Image object corresponding to a give image
#
# Revision history:  2022-Apr-01  Lixin Sun  Initial creation
#
###################################################################################################
def superpixel_img(inImage): 
  all_bands = inImage.bandNames().getInfo()

  seg_mosaic = ee.Algorithms.Image.Segmentation.SNIC(inImage, 3, 0.01, 8, 10)
  
  seg_bands = []
  for band in all_bands:
    seg_bands.append(band + '_mean')

  return seg_mosaic.select(seg_bands, all_bands)




#############################################################################################################
# Description: This function manages a list of exporting tasks
#
# Revision history:  2022-Feb-10  Lixin Sun  Initial creation 
#
#############################################################################################################
def manage_tasks(manage_type, filter):
  '''This function manages a list of exporting tasks.
     Args:
       manage_type(string): a string representing a task type, such as 'status' or 'cancel';
       filter(string): a string for filtering task names. '''
  #==========================================================================================================
  # Get a list of exporting tasks
  #==========================================================================================================  
  task_list = ee.data.listOperations()

  if manage_type.find('status') > -1:
    for task in task_list:
      if task['metadata']['description'].find(filter) > -1: 
        print(task['metadata']['description']+': ' + task['metadata']['state'])
    
  elif manage_type.find('cancel') > -1:
    for task in task_list:
      if task['metadata']['description'].find(filter) > -1:         
        ee.data.cancelOperation(task['name'])
        print(task['metadata']['description'] + ' has been cancelled.')
    
  elif manage_type.find('list') > -1:  
    print('<manage_tasks> the list of all exporting tasks:', ee.data.listOperations())
  
  elif manage_type.find('count') > -1:
    print('<manage_tasks> the number of tasks = ', len(task_list))

  elif manage_type.find('meta') > -1:
    for task in task_list:
      if task['metadata']['description'].find(filter) > -1: 
        print(task['metadata'])


        
 