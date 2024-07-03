
# Constructors for CCRS LEAF Toolbox algorithms
# Richard Fernandes Feb 19, 2022
# Feacture collections match those use in https://github.com/fqqlsun/LEAF_production/blob/main/LEAFNets.py now   Richard Fernanes Nov 24, 2023
import ee

#--------------------------------------------------------------------------------*/
# Landsat 8 Surface_Reflectance SL2P algoirthm - these are correct RF Nov 2023 */                 
#--------------------------------------------------------------------------------*/
def l8_createFeatureCollection_Network_Ind():
  return ee.FeatureCollection('users/rfernand387/Parameter_file_prosail_ccrs_big_clumped2')

#old version that used 2015 NA land cover
# def l8_createImageCollection_partition():
#     return ee.ImageCollection('users/rfernand387/NA_NALCMS_2015_tiles') \
#               .map(lambda image :image.select("b1").rename("partition") ) \
#               .merge(ee.ImageCollection("COPERNICUS/Landcover/100m/Proba-V-C3/Global") \
#                         .map( lambda image :image.select("discrete_classification").remap([0,20,30,40,50,60,70,80,90,100,111,112,113,114,115,116,121,122,123,124,125,126,200],[0,8,10,15,17,16,19,18,14,13,1,3,1,5,6,6,2,4,2,5,6,6,18],0).toUint8().rename("partition")))

def l8_createImageCollection_partition():
    return ee.ImageCollection(ee.Image('USGS/NLCD_RELEASES/2020_REL/NALCMS')) \
              .map(lambda image: image.rename("partition") )\
              .merge(ee.ImageCollection("COPERNICUS/Landcover/100m/Proba-V-C3/Global")\
                        .map( lambda image :image.select("discrete_classification").remap([0,20,30,40,50,60,70,80,90,100,111,112,113,114,115,116,121,122,123,124,125,126,200],[0,8,10,15,17,16,19,18,14,13,1,3,1,5,6,6,2,4,2,5,6,6,18],0).toUint8().rename("partition")))

def l8_createFeatureCollection_legend():
    return ee.FeatureCollection('users/rfernand387/Legend_prosail_ccrs_big_clumped')

def l8_createFeatureCollection_estimates():
    return  ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_weiss_or_prosail_NNT1_Single_0_1') \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_weiss_or_prosail_NNT1_Single_0_1')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_ROF_sobol_prosail_dbf_big_clumpedv3_NNT1_Single_0_1')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_ccrs_sobol_4sail2_enf_NNT1_Single_0_1')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_weiss_or_prosail_NNT1_Single_0_1')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_weiss_or_prosail_NNT1_Single_0_1')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_weiss_or_prosail_NNT1_Single_0_1')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_ROF_sobol_prosail_dbf_big_clumpedv3_NNT1_Single_0_1')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_weiss_or_prosail_NNT1_Single_0_1')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_weiss_or_prosail_NNT1_Single_0_1')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_weiss_or_prosail_NNT1_Single_0_1')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_ccrs_sobol_4sail2_mix_NNT1_Single_0_1')) 

def l8_createFeatureCollection_errors():
    return  ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_weiss_or_prosail_NNT1_Single_0_1_incertitudes') \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_weiss_or_prosail_NNT1_Single_0_1_incertitudes')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_ROF_sobol_prosail_dbf_big_clumpedv3_NNT1_Single_0_1_incertitudes')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_ccrs_sobol_4sail2_enf_NNT1_Single_0_1_incertitudes')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_weiss_or_prosail_NNT1_Single_0_1_incertitudes')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_weiss_or_prosail_NNT1_Single_0_1_incertitudes')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_weiss_or_prosail_NNT1_Single_0_1_incertitudes')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_ROF_sobol_prosail_dbf_big_clumpedv3_NNT1_Single_0_1_incertitudes')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_weiss_or_prosail_NNT1_Single_0_1_incertitudes')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_weiss_or_prosail_NNT1_Single_0_1_incertitudes')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_weiss_or_prosail_NNT1_Single_0_1_incertitudes')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_ccrs_sobol_4sail2_mix_NNT1_Single_0_1_incertitudes')) \

def l8_createFeatureCollection_ranges():
    return ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_RANGE')\
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_RANGE')) \
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_RANGE')) \
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_RANGE')) \
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_RANGE')) \
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_RANGE')) \
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_RANGE')) \
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_RANGE')) \
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_RANGE')) \
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_RANGE')) \
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_RANGE')) \
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_RANGE')) 

def l8_createFeatureCollection_domains():
    return  ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_weiss_or_prosail_domain') \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_weiss_or_prosail_domain')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_ROF_sobol_prosail_dbf_big_clumpedv3_domain')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_ROF_sobol_prosail_enf_big_clumpedv2_domain')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_weiss_or_prosail_domain')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_weiss_or_prosail_domain')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_weiss_or_prosail_domain')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_ROF_sobol_prosail_dbf_big_clumpedv3_domain')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_weiss_or_prosail_domain')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_weiss_or_prosail_domain')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_weiss_or_prosail_domain')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_ROF_sobol_prosail_mix_big_clumpedv3_domain')) \

#--------------------------------------------------------------------------------*/
# Landsat 9 Surface_Reflectance SL2P algoirthm - these are correct RF Nov 2023 */                 
#--------------------------------------------------------------------------------*/
def l9_createFeatureCollection_Network_Ind():
  return ee.FeatureCollection('users/rfernand387/Parameter_file_prosail_ccrs_big_clumped2')


# old version that used 2015 NA land cover
# def l8_createImageCollection_partition():
#     return ee.ImageCollection('users/rfernand387/NA_NALCMS_2015_tiles')\
#               .map(lambda image :image.select("b1").rename("partition") )\
#               .merge(ee.ImageCollection("COPERNICUS/Landcover/100m/Proba-V-C3/Global")\
#                         .map( lambda image :image.select("discrete_classification").remap([0,20,30,40,50,60,70,80,90,100,111,112,113,114,115,116,121,122,123,124,125,126,200],[0,8,10,15,17,16,19,18,14,13,1,3,1,5,6,6,2,4,2,5,6,6,18],0).toUint8().rename("partition")))
# 

def l9_createImageCollection_partition():
    return ee.ImageCollection(ee.Image('USGS/NLCD_RELEASES/2020_REL/NALCMS'))\
              .map(lambda image :image.rename("partition"))\
              .merge(ee.ImageCollection("COPERNICUS/Landcover/100m/Proba-V-C3/Global")\
                        .map( lambda image :image.select("discrete_classification").remap([0,20,30,40,50,60,70,80,90,100,111,112,113,114,115,116,121,122,123,124,125,126,200],[0,8,10,15,17,16,19,18,14,13,1,3,1,5,6,6,2,4,2,5,6,6,18],0).toUint8().rename("partition")))


def l9_createFeatureCollection_legend():
    return ee.FeatureCollection('users/rfernand387/Legend_prosail_ccrs_big_clumped')

def l9_createFeatureCollection_estimates():
    return  ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l9_sl2p_weiss_or_prosail_NNT1_Single_0_1') \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l9_sl2p_weiss_or_prosail_NNT1_Single_0_1')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l9_sl2p_ROF_sobol_prosail_dbf_big_clumpedv3_NNT1_Single_0_1')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l9_sl2p_ccrs_sobol_4sail2_enf_NNT1_Single_0_1')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l9_sl2p_weiss_or_prosail_NNT1_Single_0_1')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l9_sl2p_weiss_or_prosail_NNT1_Single_0_1')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l9_sl2p_weiss_or_prosail_NNT1_Single_0_1')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_ROF_sobol_prosail_dbf_big_clumpedv3_NNT1_Single_0_1')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l9_sl2p_weiss_or_prosail_NNT1_Single_0_1')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l9_sl2p_weiss_or_prosail_NNT1_Single_0_1')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l9_sl2p_weiss_or_prosail_NNT1_Single_0_1')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l9_sl2p_ccrs_sobol_4sail2_mix_NNT1_Single_0_1')) 

def l9_createFeatureCollection_errors():
    return  ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l9_sl2p_weiss_or_prosail_NNT1_Single_0_1_incertitudes') \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l9_sl2p_weiss_or_prosail_NNT1_Single_0_1_incertitudes')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l9_sl2p_ROF_sobol_prosail_dbf_big_clumpedv3_NNT1_Single_0_1_incertitudes')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l9_sl2p_ccrs_sobol_4sail2_mix_NNT1_Single_0_1_incertitudes')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l9_sl2p_weiss_or_prosail_NNT1_Single_0_1_incertitudes')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l9_sl2p_weiss_or_prosail_NNT1_Single_0_1_incertitudes')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l9_sl2p_weiss_or_prosail_NNT1_Single_0_1_incertitudes')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_ROF_sobol_prosail_dbf_big_clumpedv3_NNT1_Single_0_1_incertitudes')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l9_sl2p_weiss_or_prosail_NNT1_Single_0_1_incertitudes')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l9_sl2p_weiss_or_prosail_NNT1_Single_0_1_incertitudes')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l9_sl2p_weiss_or_prosail_NNT1_Single_0_1_incertitudes')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l9_sl2p_ccrs_sobol_4sail2_mix_NNT1_Single_0_1_incertitudes')) 


def l9_createFeatureCollection_ranges():
  return ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_RANGE')\
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_RANGE')) \
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_RANGE')) \
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_RANGE')) \
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_RANGE')) \
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_RANGE')) \
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_RANGE')) \
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_RANGE')) \
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_RANGE')) \
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_RANGE')) \
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_RANGE')) \
                    .merge(ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_SL2P_RANGE')) 

def l9_createFeatureCollection_domains():
    return  ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l9_sl2p_weiss_or_prosail_domain') \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l9_sl2p_weiss_or_prosail_domain')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_ROF_sobol_prosail_dbf_big_clumpedv3_domain')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_ROF_sobol_prosail_enf_big_clumpedv2_domain')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l9_sl2p_weiss_or_prosail_domain')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l9_sl2p_weiss_or_prosail_domain')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l9_sl2p_weiss_or_prosail_domain')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_ROF_sobol_prosail_dbf_big_clumpedv3_domain'))\
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l9_sl2p_weiss_or_prosail_domain')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l9_sl2p_weiss_or_prosail_domain')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l9_sl2p_weiss_or_prosail_domain')) \
    .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_ROF_sobol_prosail_mix_big_clumpedv3_domain')) 




#--------------------------------------------------------------------------------*/
# Sentinel 2 Surface_Reflectance CCRS algorithm                                 */                 
#--------------------------------------------------------------------------------*/
def s2_createFeatureCollection_Network_Ind():
  return ee.FeatureCollection('users/rfernand387/Parameter_file_prosail_ccrs_big_clumped2')

#old version that used 2015 NA land cover
#def s2_createImageCollection_partition():
#    return ee.ImageCollection('users/rfernand387/NA_NALCMS_2015_tiles')\
#              .map(lambda image: image.select("b1").rename("partition") )\
#              .merge(ee.ImageCollection("COPERNICUS/Landcover/100m/Proba-V-C3/Global")\
#                        .map( lambda image: image.select("discrete_classification").remap([0,20,30,40,50,60,70,80,90,100,111,112,113,114,115,116,121,122,123,124,125,126,200],[0,8,10,15,17,16,19,18,14,13,1,3,1,5,6,6,2,4,2,5,6,6,18],0).toUint8().rename("partition")))
#

#New version using 2020 Na land cover Richard Fernandes Nov 2024
def s2_createImageCollection_partition():
    return ee.ImageCollection(ee.Image('USGS/NLCD_RELEASES/2020_REL/NALCMS'))\
              .map(lambda image: image.rename("partition") )\
              .merge(ee.ImageCollection("COPERNICUS/Landcover/100m/Proba-V-C3/Global")\
                        .map( lambda image: image.select("discrete_classification").remap([0,20,30,40,50,60,70,80,90,100,111,112,113,114,115,116,121,122,123,124,125,126,200],[0,8,10,15,17,16,19,18,14,13,1,3,1,5,6,6,2,4,2,5,6,6,18],0).toUint8().rename("partition")))

def s2_createFeatureCollection_legend():
    return ee.FeatureCollection('users/rfernand387/Legend_prosail_ccrs_big_clumped')

def s2_createFeatureCollection_estimates():
    return  ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/s2_sl2p_weiss_or_prosail_NNT3_Single_0_1') \
     .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/s2_sl2p_weiss_or_prosail_NNT3_Single_0_1')) \
     .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/s2_sl2p_ROF_sobol_prosail_dbf_big_clumped_NNT1_Single_0_1_v2')) \
     .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/s2_sl2p_ccrs_sobol_4sail2_enf_NNT1_Single_0_1')) \
     .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/s2_sl2p_weiss_or_prosail_NNT3_Single_0_1')) \
     .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/s2_sl2p_weiss_or_prosail_NNT3_Single_0_1')) \
     .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/s2_sl2p_weiss_or_prosail_NNT3_Single_0_1')) \
     .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/s2_sl2p_ROF_sobol_prosail_dbf_big_clumped_NNT1_Single_0_1_v2')) \
     .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/s2_sl2p_weiss_or_prosail_NNT3_Single_0_1')) \
     .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/s2_sl2p_weiss_or_prosail_NNT3_Single_0_1')) \
     .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/s2_sl2p_weiss_or_prosail_NNT3_Single_0_1')) \
     .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/s2_sl2p_ccrs_sobol_4sail2_mix_NNT1_Single_0_1'))



def s2_createFeatureCollection_errors():
    return   ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/s2_sl2p_weiss_or_prosail_NNT3_Single_0_1_error') \
      .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/s2_sl2p_weiss_or_prosail_NNT3_Single_0_1_error')) \
      .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/s2_sl2p_ROF_sobol_prosail_dbf_big_clumped_NNT1_Single_0_1_v2_errors')) \
      .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/s2_sl2p_ccrs_sobol_4sail2_enf_NNT1_Single_0_1_incertitudes')) \
      .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/s2_sl2p_weiss_or_prosail_NNT3_Single_0_1_error')) \
      .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/s2_sl2p_weiss_or_prosail_NNT3_Single_0_1_error')) \
      .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/s2_sl2p_weiss_or_prosail_NNT3_Single_0_1_error')) \
      .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/s2_sl2p_ROF_sobol_prosail_dbf_big_clumped_NNT1_Single_0_1_v2_errors')) \
      .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/s2_sl2p_weiss_or_prosail_NNT3_Single_0_1_error')) \
      .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/s2_sl2p_weiss_or_prosail_NNT3_Single_0_1_error')) \
      .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/s2_sl2p_weiss_or_prosail_NNT3_Single_0_1_error')) \
      .merge(ee.FeatureCollection('projects/ee-modis250/assets/SL2P/s2_sl2p_ccrs_sobol_4sail2_mix_NNT1_Single_0_1_incertitudes')) \


def s2_createFeatureCollection_ranges():
  return   ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_RANGE') \
    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_RANGE')) \
    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_RANGE')) \
    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_RANGE')) \
    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_RANGE')) \
    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_RANGE')) \
    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_RANGE')) \
    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_RANGE')) \
    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_RANGE')) \
    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_RANGE')) \
    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_RANGE')) \
    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_RANGE'))\


def s2_createFeatureCollection_domains():
  return   ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_DOMAIN') \
    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_DOMAIN')) \
    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_DOMAIN')) \
    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_DOMAIN')) \
    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_DOMAIN')) \
    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_DOMAIN')) \
    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_DOMAIN')) \
    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_DOMAIN')) \
    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_DOMAIN')) \
    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_DOMAIN')) \
    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_DOMAIN')) \
    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_DOMAIN'))






#--------------------------------------------------------------------------------*/
# Sentinel 2 Surface_Reflectance 10m CCRS algorithm                                 */                 
#--------------------------------------------------------------------------------*/
def s2_10m_createFeatureCollection_Network_Ind():
  return ee.FeatureCollection('users/rfernand387/Parameter_file_prosail_ccrs_big_clumped2')



#old version that used 2015 NA land cover
#def s2_createImageCollection_partition():
#    return ee.ImageCollection('users/rfernand387/NA_NALCMS_2015_tiles')\
#              .map(lambda image: image.select("b1").rename("partition") })\
#              .merge(ee.ImageCollection("COPERNICUS/Landcover/100m/Proba-V-C3/Global")\
#                        .map( lambda image: image.select("discrete_classification").remap([0,20,30,40,50,60,70,80,90,100,111,112,113,114,115,116,121,122,123,124,125,126,200],[0,8,10,15,17,16,19,18,14,13,1,3,1,5,6,6,2,4,2,5,6,6,18],0).toUint8().rename("partition")))
#

#New version using 2020 Na land cover Richard Fernandes Nov 2024
def s2_10m_createImageCollection_partition():
    return ee.ImageCollection(ee.Image('USGS/NLCD_RELEASES/2020_REL/NALCMS'))\
              .map(lambda image: image.rename("partition") )\
              .merge(ee.ImageCollection("COPERNICUS/Landcover/100m/Proba-V-C3/Global")\
                        .map( lambda image: image.select("discrete_classification").remap([0,20,30,40,50,60,70,80,90,100,111,112,113,114,115,116,121,122,123,124,125,126,200],[0,8,10,15,17,16,19,18,14,13,1,3,1,5,6,6,2,4,2,5,6,6,18],0).toUint8().rename("partition")))



def s2_10m_createFeatureCollection_legend():
    return ee.FeatureCollection('users/rfernand387/Legend_prosail_ccrs_big_clumped')



def s2_10m_createFeatureCollection_estimates():

    return  ee.FeatureCollection('users/kateharvey/s2_sl2p_weiss_or_prosail_10m_NNT1_Single_0_1') \
     .merge(ee.FeatureCollection('users/kateharvey/s2_sl2p_weiss_or_prosail_10m_NNT1_Single_0_1')) \
     .merge(ee.FeatureCollection('users/kateharvey/s2_sl2p_weiss_or_prosail_10m_NNT1_Single_0_1')) \
     .merge(ee.FeatureCollection('users/kateharvey/s2_sl2p_weiss_or_prosail_10m_NNT1_Single_0_1')) \
     .merge(ee.FeatureCollection('users/kateharvey/s2_sl2p_weiss_or_prosail_10m_NNT1_Single_0_1')) \
     .merge(ee.FeatureCollection('users/kateharvey/s2_sl2p_weiss_or_prosail_10m_NNT1_Single_0_1')) \
     .merge(ee.FeatureCollection('users/kateharvey/s2_sl2p_weiss_or_prosail_10m_NNT1_Single_0_1')) \
     .merge(ee.FeatureCollection('users/kateharvey/s2_sl2p_weiss_or_prosail_10m_NNT1_Single_0_1')) \
     .merge(ee.FeatureCollection('users/kateharvey/s2_sl2p_weiss_or_prosail_10m_NNT1_Single_0_1')) \
     .merge(ee.FeatureCollection('users/kateharvey/s2_sl2p_weiss_or_prosail_10m_NNT1_Single_0_1')) \
     .merge(ee.FeatureCollection('users/kateharvey/s2_sl2p_weiss_or_prosail_10m_NNT1_Single_0_1')) \
     .merge(ee.FeatureCollection('users/kateharvey/s2_sl2p_weiss_or_prosail_10m_NNT1_Single_0_1')) 



def s2_10m_createFeatureCollection_errors():
    return   ee.FeatureCollection('users/kateharvey/s2_sl2p_weiss_or_prosail_10m_NNT1_Single_0_1_errors') \
      .merge(ee.FeatureCollection('users/kateharvey/s2_sl2p_weiss_or_prosail_10m_NNT1_Single_0_1_errors')) \
      .merge(ee.FeatureCollection('users/kateharvey/s2_sl2p_weiss_or_prosail_10m_NNT1_Single_0_1_errors')) \
      .merge(ee.FeatureCollection('users/kateharvey/s2_sl2p_weiss_or_prosail_10m_NNT1_Single_0_1_errors')) \
      .merge(ee.FeatureCollection('users/kateharvey/s2_sl2p_weiss_or_prosail_10m_NNT1_Single_0_1_errors')) \
      .merge(ee.FeatureCollection('users/kateharvey/s2_sl2p_weiss_or_prosail_10m_NNT1_Single_0_1_errors')) \
      .merge(ee.FeatureCollection('users/kateharvey/s2_sl2p_weiss_or_prosail_10m_NNT1_Single_0_1_errors')) \
      .merge(ee.FeatureCollection('users/kateharvey/s2_sl2p_weiss_or_prosail_10m_NNT1_Single_0_1_errors')) \
      .merge(ee.FeatureCollection('users/kateharvey/s2_sl2p_weiss_or_prosail_10m_NNT1_Single_0_1_errors')) \
      .merge(ee.FeatureCollection('users/kateharvey/s2_sl2p_weiss_or_prosail_10m_NNT1_Single_0_1_errors')) \
      .merge(ee.FeatureCollection('users/kateharvey/s2_sl2p_weiss_or_prosail_10m_NNT1_Single_0_1_errors')) \
      .merge(ee.FeatureCollection('users/kateharvey/s2_sl2p_weiss_or_prosail_10m_NNT1_Single_0_1_errors')) 


def s2_10m_createFeatureCollection_ranges():
  return   ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_RANGE') \
    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_RANGE')) \
    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_RANGE')) \
    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_RANGE')) \
    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_RANGE')) \
    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_RANGE')) \
    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_RANGE')) \
    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_RANGE')) \
    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_RANGE')) \
    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_RANGE')) \
    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_RANGE')) \
    .merge(ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_RANGE'))


def s2_10m_createFeatureCollection_domains():
  return   ee.FeatureCollection('users/kateharvey/s2_sl2p_weiss_or_prosail_10m_domain') \
    .merge(ee.FeatureCollection('users/kateharvey/s2_sl2p_weiss_or_prosail_10m_domain')) \
    .merge(ee.FeatureCollection('users/kateharvey/s2_sl2p_weiss_or_prosail_10m_domain')) \
    .merge(ee.FeatureCollection('users/kateharvey/s2_sl2p_weiss_or_prosail_10m_domain')) \
    .merge(ee.FeatureCollection('users/kateharvey/s2_sl2p_weiss_or_prosail_10m_domain')) \
    .merge(ee.FeatureCollection('users/kateharvey/s2_sl2p_weiss_or_prosail_10m_domain')) \
    .merge(ee.FeatureCollection('users/kateharvey/s2_sl2p_weiss_or_prosail_10m_domain')) \
    .merge(ee.FeatureCollection('users/kateharvey/s2_sl2p_weiss_or_prosail_10m_domain')) \
    .merge(ee.FeatureCollection('users/kateharvey/s2_sl2p_weiss_or_prosail_10m_domain')) \
    .merge(ee.FeatureCollection('users/kateharvey/s2_sl2p_weiss_or_prosail_10m_domain')) \
    .merge(ee.FeatureCollection('users/kateharvey/s2_sl2p_weiss_or_prosail_10m_domain')) \
    .merge(ee.FeatureCollection('users/kateharvey/s2_sl2p_weiss_or_prosail_10m_domain')) 


