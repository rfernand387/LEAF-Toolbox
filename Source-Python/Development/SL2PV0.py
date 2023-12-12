# Constructors for SL2P LEAF Toolbox algorithms
# Richard Fernandes Feb 19, 2022
# Feacture collections match those use in https://github.com/fqqlsun/LEAF_production/blob/main/LEAFNets.py now   Richard Fernanes Nov 24, 2023

import ee
import eoImage
import toolsNets



# --------------------
# Generic medium resolution functions
# --------------------

# filters a medium resolution image collection 
def filterCollection(imageCollection,colOptions,maxCloudcover,mapBounds,startDate,endDate,tools):

    return imageCollection.filterBounds(mapBounds) \
                      .filterDate(startDate, endDate) \
                      .filterMetadata(colOptions["Cloudcover"],'less_than',maxCloudcover) \
                      .limit(5000) \
                      .map(lambda image: image.clip(mapBounds)) \
                      .map(lambda image: tools.MaskClear(image))  \
                      .map(lambda image: eoImage.attach_Date(image)) \
                      .map(lambda image: eoImage.attach_LonLat(image)) \
                      .map(lambda image: tools.addGeometry(colOptions,image)) 


#make networks using CCRS parsed format to GEE
def makeNets(netName,colOptions):

    # determine nmber of partitons to make networks for
    numNets = ee.Number(ee.Feature((colOptions["Network_Ind"]).first()).propertyNames().remove('lon').remove('Feature Index').remove('system:index').size())

    # populate the netwoorks for each unique partition class
    return ee.List.sequence(1,ee.Number(colOptions["numVariables"]),1).map(lambda netNum: toolsNets.makeNetVars(colOptions[netName],numNets,netNum))


 # --------------------
 # Sentinel2 Functions: 
 # --------------------

def s2_createFeatureCollection_estimates():
    return ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/s2_sl2p_weiss_or_prosail_NNT3_Single_0_1')


def s2_createFeatureCollection_errors():
    return ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/s2_sl2p_weiss_or_prosail_NNT3_Single_0_1_error')


def s2_createFeatureCollection_domains():
    return ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/S2_SL2P_WEISS_ORIGINAL_DOMAIN')


def s2_createFeatureCollection_ranges():
    return ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/weiss_or_prosail3_NNT3_Single_0_1_RANGE')

def s2_createFeatureCollection_Network_Ind():
    return ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/Parameter_file_sl2p')

def s2_createImageCollection_partition_old():
    return ee.ImageCollection('users/rfernand387/NA_NALCMS_2015_tiles') \
              .map(lambda image : image.select("b1").rename("partition") ) \
              .merge(ee.ImageCollection("COPERNICUS/Landcover/100m/Proba-V/Global") \
                        .map( lambda image : image.select("discrete_classification").remap([0,20,30,40,50,60,70,80,90,100,111,112,113,114,115,116,121,122,123,124,125,126,200],[0,8,10,15,17,16,19,18,14,13,1,3,1,5,6,6,2,4,2,5,6,6,18],0).toUint8().rename("partition")))

 # old version that used 2015 NA land cover
 # def s2_createImageCollection_partition():
 #     return ee.ImageCollection('users/rfernand387/NA_NALCMS_2015_tiles') \
 #               .map( lambda image : image.select("b1").rename("partition") }) \
 #               .merge(ee.ImageCollection("COPERNICUS/Landcover/100m/Proba-V/Global") \
 #                         .map(  lambda image : image.select("discrete_classification").remap([0,20,30,40,50,60,70,80,90,100,111,112,113,114,115,116,121,122,123,124,125,126,200],[0,8,10,15,17,16,19,18,14,13,1,3,1,5,6,6,2,4,2,5,6,6,18],0).toUint8().rename("partition")))
 # 

 # New version using 2020 Na land cover Richard Fernandes Nov 2024
def s2_createImageCollection_partition():
    return ee.ImageCollection(ee.Image('USGS/NLCD_RELEASES/2020_REL/NALCMS')) \
              .map( lambda image: image.rename("partition")) \
              .merge(ee.ImageCollection("COPERNICUS/Landcover/100m/Proba-V/Global") \
                        .map(  lambda image : image.select("discrete_classification").remap([0,20,30,40,50,60,70,80,90,100,111,112,113,114,115,116,121,122,123,124,125,126,200],[0,8,10,15,17,16,19,18,14,13,1,3,1,5,6,6,2,4,2,5,6,6,18],0).toUint8().rename("partition")))


def s2_createFeatureCollection_legend():
    return ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/Legend_sl2p')




 # Same functions as above using 10 m bands:
def s2_10m_createFeatureCollection_estimates():
    return ee.FeatureCollection('users/kateharvey/s2_sl2p_weiss_or_prosail_10m_NNT1_Single_0_1')


def s2_10m_createFeatureCollection_errors():
    return ee.FeatureCollection('users/kateharvey/s2_sl2p_weiss_or_prosail_10m_NNT1_Single_0_1_errors')


def s2_10m_createFeatureCollection_domains():
    return ee.FeatureCollection('users/kateharvey/s2_sl2p_weiss_or_prosail_10m_domain')


def s2_10m_createFeatureCollection_ranges():
    return ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/weiss_or_prosail3_NNT3_Single_0_1_RANGE')

def s2_10m_createFeatureCollection_Network_Ind():
    return ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/Parameter_file_sl2p')

def s2_10m_createImageCollection_partition_old():
    return ee.ImageCollection('users/rfernand387/NA_NALCMS_2015_tiles') \
              .map( lambda image : image.select("b1").rename("partition") ) \
              .merge(ee.ImageCollection("COPERNICUS/Landcover/100m/Proba-V/Global") \
                        .map(  lambda image : image.select("discrete_classification").remap([0,20,30,40,50,60,70,80,90,100,111,112,113,114,115,116,121,122,123,124,125,126,200],[0,8,10,15,17,16,19,18,14,13,1,3,1,5,6,6,2,4,2,5,6,6,18],0).toUint8().rename("partition")))

 # old version that used 2015 NA land cover
 # def s2_20m_createImageCollection_partition():
 #     return ee.ImageCollection('users/rfernand387/NA_NALCMS_2015_tiles') \
 #               .map( lambda image : image.select("b1").rename("partition") }) \
 #               .merge(ee.ImageCollection("COPERNICUS/Landcover/100m/Proba-V/Global") \
 #                         .map(  lambda image : image.select("discrete_classification").remap([0,20,30,40,50,60,70,80,90,100,111,112,113,114,115,116,121,122,123,124,125,126,200],[0,8,10,15,17,16,19,18,14,13,1,3,1,5,6,6,2,4,2,5,6,6,18],0).toUint8().rename("partition")))
 # 

 # New version using 2020 Na land cover Richard Fernandes Nov 2024
def s2_10m_createImageCollection_partition():
    return ee.ImageCollection(ee.Image('USGS/NLCD_RELEASES/2020_REL/NALCMS')) \
              .map( lambda image: image.rename("partition")) \
              .merge(ee.ImageCollection("COPERNICUS/Landcover/100m/Proba-V/Global") \
                        .map(  lambda image : image.select("discrete_classification").remap([0,20,30,40,50,60,70,80,90,100,111,112,113,114,115,116,121,122,123,124,125,126,200],[0,8,10,15,17,16,19,18,14,13,1,3,1,5,6,6,2,4,2,5,6,6,18],0).toUint8().rename("partition")))


def s2_10m_createFeatureCollection_legend():
    return ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/Legend_sl2p')



 # -------------------
 # Landsat8 Functions:
 # -------------------
def l8_createFeatureCollection_estimates():
    return ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_weiss_or_prosail_NNT1_Single_0_1')

def l8_createFeatureCollection_errors():
    return ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_weiss_or_prosail_NNT1_Single_0_1_incertitudes')

def l8_createFeatureCollection_domains():
    return ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_DOMAIN')

def l8_createFeatureCollection_ranges():
    return ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_RANGE')

def l8_createFeatureCollection_Network_Ind():
    return ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/Parameter_file_sl2p')

 # old version that used 2015 NA land cover
 # def l8_createImageCollection_partition():
 #     return ee.ImageCollection('users/rfernand387/NA_NALCMS_2015_tiles') \
 #               .map( lambda image : image.select("b1").rename("partition") }) \
 #               .merge(ee.ImageCollection("COPERNICUS/Landcover/100m/Proba-V/Global") \
 #                         .map(  lambda image : image.select("discrete_classification").remap([0,20,30,40,50,60,70,80,90,100,111,112,113,114,115,116,121,122,123,124,125,126,200],[0,8,10,15,17,16,19,18,14,13,1,3,1,5,6,6,2,4,2,5,6,6,18],0).toUint8().rename("partition")))
 # 

def l8_createImageCollection_partition():
    return ee.ImageCollection(ee.Image('USGS/NLCD_RELEASES/2020_REL/NALCMS')) \
              .map( lambda image: image.rename("partition")) \
              .merge(ee.ImageCollection("COPERNICUS/Landcover/100m/Proba-V/Global") \
                        .map(  lambda image : image.select("discrete_classification").remap([0,20,30,40,50,60,70,80,90,100,111,112,113,114,115,116,121,122,123,124,125,126,200],[0,8,10,15,17,16,19,18,14,13,1,3,1,5,6,6,2,4,2,5,6,6,18],0).toUint8().rename("partition")))

def l8_createFeatureCollection_legend(): 
    return ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/Legend_sl2p') 


 # -------------------
 # Landsat9 Functions:
 # -------------------

def l9_createFeatureCollection_estimates():
    return ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_weiss_or_prosail_NNT1_Single_0_1')

def l9_createFeatureCollection_errors():
    return ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_weiss_or_prosail_NNT1_Single_0_1_incertitudes')

def l9_createFeatureCollection_domains():
    return ee.FeatureCollection('projects/ee-modis250/assets/SL2P/l8_sl2p_weiss_or_prosail_domain')

def l9_createFeatureCollection_ranges():
    return ee.FeatureCollection('users/rfernand387/LANDSAT_LC08_C01_T1_SR/LANDSAT_LC08_C01_T1_SR_RANGE')

def l9_createFeatureCollection_Network_Ind():
    return ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/Parameter_file_sl2p')

 # old version that used 2015 NA land cover
 # def l8_createImageCollection_partition():
 #     return ee.ImageCollection('users/rfernand387/NA_NALCMS_2015_tiles')
 #               .map( lambda image : image.select("b1").rename("partition") }) \
 #               .merge(ee.ImageCollection("COPERNICUS/Landcover/100m/Proba-V/Global") \
 #                         .map(  lambda image : image.select("discrete_classification").remap([0,20,30,40,50,60,70,80,90,100,111,112,113,114,115,116,121,122,123,124,125,126,200],[0,8,10,15,17,16,19,18,14,13,1,3,1,5,6,6,2,4,2,5,6,6,18],0).toUint8().rename("partition")))
 # 

def l9_createImageCollection_partition():
    return ee.ImageCollection(ee.Image('USGS/NLCD_RELEASES/2020_REL/NALCMS')) \
              .map( lambda image: image.rename("partition")) \
              .merge(ee.ImageCollection("COPERNICUS/Landcover/100m/Proba-V/Global") \
                        .map(  lambda image : image.select("discrete_classification").remap([0,20,30,40,50,60,70,80,90,100,111,112,113,114,115,116,121,122,123,124,125,126,200],[0,8,10,15,17,16,19,18,14,13,1,3,1,5,6,6,2,4,2,5,6,6,18],0).toUint8().rename("partition")))

def l9_createFeatureCollection_legend(): 
    return ee.FeatureCollection('users/rfernand387/COPERNICUS_S2_SR/Legend_sl2p') 



