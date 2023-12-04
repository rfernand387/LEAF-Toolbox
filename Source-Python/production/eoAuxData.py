######################################################################################################
# Description: The functions in this file can be used to facilitate the usage of some Auxiliary data
#              available in GEE. 
#
######################################################################################################
import ee 


import eoTileGrids as eoTG


NightLight_name  = 'night_light'
RoadDensity_name = 'road_density'


LC_palette = ['033e00',  # 1  Temperate or sub-polar needleleaf forest
              '939b71',  # 2  Sub-polar taiga needleleaf forest
              '196d12',  # 3  Tropical or sub-tropical broadleaf evergreen forest
              '1fab01',  # 4  Tropical or sub-tropical broadleaf deciduous forest
              '5b725c',  # 5  Temperate or sub-polar broadleaf deciduous forest
              '6b7d2c',  # 6  Mixed forest
              'b29d29',  # 7  Tropical or sub-tropical shrubland
              'b48833',  # 8  Temperate or sub-polar shrubland
              'e9da5d',  # 9  Tropical or sub-tropical grassland
              'e0cd88',  # 10  Temperate or sub-polar grassland
              'a07451',  # 11  Sub-polar or polar shrubland-lichen-moss
              'bad292',  # 12  Sub-polar or polar grassland-lichen-moss
              '3f8970',  # 13  Sub-polar or polar barren-lichen-moss
              '6ca289',  # 14  Wetland
              'e6ad6a',  # 15  Cropland
              'a9abae',  # 16  Barren land
              'db2126',  # 17  Urban and built-up
              '4c73a1',  # 18  Water
              'fff7fe']  # 19  Snow and ice 

######################################################################################################
# Description: This function creates a global night-light mosaic image for a targeted year. 
#
# Revision history:  2021-May-06  Lixin Sun  Initial creation
#
######################################################################################################
def get_GlobNLight(target_year, Smooth, Radius):
  '''Create a global night-light mosaic image for a targeted year.
  Arg:
    target_year(string or int): A targeted year of mosaicing;
    Smooth(Boolean): A flag indicating if do smoothing to noght light map;
    inRadius(float): The radius of smoothing if applicable.'''
  year_int     = int(target_year)
  year_str     = str(target_year)
  night_lights = ee.Image(0.0)
  
  # Create a global night lights map 
  if year_int > 1991:
    start = year_str + '-01-01'
    stop  = year_str + '-12-30'
    if year_int >= 2014:
      dataset      = ee.ImageCollection('NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG').filter(ee.Filter.date(start, stop))
      night_lights = dataset.mosaic().select(['avg_rad'], [NightLight_name]) 
    else:  
      dataset = ee.ImageCollection('NOAA/DMSP-OLS/NIGHTTIME_LIGHTS').filter(ee.Filter.date(start, stop))
      night_lights = dataset.mosaic().select(['stable_lights'], [NightLight_name]) 
  else:
    dataset = ee.ImageCollection('NOAA/DMSP-OLS/NIGHTTIME_LIGHTS').filter(ee.Filter.date('1992-01-01', '1992-12-30'))
    night_lights = dataset.mosaic().select(['stable_lights'], [NightLight_name])
  
  #==================================================================================================
  # Smooth the night light map as required
  #==================================================================================================
  if Smooth == True:
    kernel = ee.Kernel.circle(radius = Radius, units = 'pixels', normalize = True)
    night_lights = night_lights.convolve(kernel)
    
  return night_lights





#############################################################################################################
# Description: This function returns a road density mosaic image from an image collection stored on
#              GEE assets.
#
# Revision history:  2021-Jun-30  Lixin Sun  Initial creation
#                    2022-Feb-04  Lixin Sun  Removed road density filtering process.
#############################################################################################################
def get_roadDensity(region):
  '''Creates a road density mosaic image from an image collection stored on GEE assets and filter
     it with a urban area mask. 

     Args:
       region(ee.Geometry): The spatial region of ROI. '''
  CAN_road_density = ee.ImageCollection('users/ORS_code/Canada_road_density')

  #==================================================================================================
  # Give a band name to each road density tile so that they can be mosaiced  
  #==================================================================================================
  def select_road(img):
    return img.select([0], [RoadDensity_name])

  density_ImgColl = CAN_road_density.map(lambda img: select_road(img))
  
  #==================================================================================================
  # Conduct quality mosaic and then clip it with a given region
  #==================================================================================================
  return density_ImgColl.qualityMosaic(RoadDensity_name).clip(region)





#############################################################################################################
# Description: This function creates a LC map for entire Canada, optionally water bodies can be masked out.
#
# Revision history:  2023-Feb-17  Lixin Sun  Initial creation.
#
#############################################################################################################
def get_CanLC(Year):
  '''Creates a mask that mask out the land outside Canada and optionally water.

     Args:      
       Year(int or string): A target year;
       mask_water(Boolean): Flag indicating if water bodies are masked out as well.'''
  #==========================================================================================================
  # Choose a proper land cover image collection based on a given "Year"
  #==========================================================================================================
  year = int(Year)  
  #ccrs_LC_assets  = 'projects/ccmeo-ag-000007/assets/CanadaLC2020_30m' 
  ccrs_LC_assets  = 'projects/ee-lsunott/assets/CanadaLC2020_30m' 

  if year > 2017:
    #ccrs_LC_assets = 'projects/ccmeo-ag-000007/assets/CanLC2020'
    ccrs_LC_assets  = 'projects/ee-lsunott/assets/CanadaLC2020_30m' 

  #==========================================================================================================
  # Create a CCRS land cover image
  #==========================================================================================================
  return ee.Image(ccrs_LC_assets).rename('partirion')
  





#############################################################################################################
# Description: This function returns a proper land cover mosaic based on a given region and year.
#
# The class mapping between CCRS land cover legend and SL2P class legend: 
#
#            CCRS class legend                     ==>     Biome                    ==>  SL2P class legend
# ===========================================================================================================
# C1: Temperate or sub-polar needleleaf forest     ==>     C7: needleleaf forest    ==>  C3: needleaf forest
# C2: Sub-polar taiga needleleaf forest            ==>     C7: needleleaf forest    ==>  C3: needleaf forest
# C3: Tropical broadleaf evergreen forest          ==>     C5: evergreen forest     ==>  C2: tropical forest
# C4: Tropical broadleaf deciduous forest          ==>     C6: broadleaf forest     ==>  C2: tropical forest
# C5: Temperate broadleaf deciduous forest         ==>     C6: broadleaf forest     ==>  C2: tropical forest
# C6: Mixed forester                               ==>     C7: needleleaf forest    ==>  C11: forest
# C7: Tropical shrubland                           ==>     C2: shrubland            ==>  C8:     
# C8: Temperate or sub-polar shrubland             ==>     C2: shrubland            ==>  C7:     
# C9: Tropical or sub-tropical grassland           ==>     C1: grassland            ==>  C4:     
# C10: Tempearte or sub-polar grassland            ==>     C1: grassland            ==>  C6:     
# C11: Sub-polar or polar shrubland-lichen-moss    ==>     C2: shrubland            ==>  C7:     
# C12: Sub-polar or polar grassland-lichen-moss    ==>     C1: grassland            ==>  C10:     
# C13: Sub-polar or polar barren-lichen-moss       ==>     C1: grassland            ==>  C5:     
# C14: Wetland                                     ==>     C2: shrubland            ==>  C4: wetland    
# C15: Cropland                                    ==>     C3: cropland             ==>  C1: cropland     
# C16: Barren land                                 ==>     C1: grassland            ==>  C9:     
# C17: Urban                                       ==>     C1: grassland            ==>  C0:     
# C18: Water                                       ==>     no class                 ==>  C0:     
# C19: Snow and Ice                                ==>     no class                 ==>  C0:     
#============================================================================================================
# CCRS legend: [1, 3, 4, 17, 7, 8, 5, 11, 9, 15, 13, 2, 14, 10, 12, 18, 16, 19, 6]
# SL2P legend: [3, 2, 2, 0,  8, 7, 2, 7,  4, 1,  5,  3, 4,  6,  10, 0,  9,  0,  11]
# Biome:       [7, 5, 6, 6,  2, 2, 6, 2,  1, 1,  1,  7, 2,  1,  1,  0   1,  0   7] 
#
# Revision history:  2022-Jul-05  Lixin Sun  Initial creation
#                    2022-Sep-29  Lixin Sun  Fixed the issues related to the urban areas in CCRS 2020 LC map
#                    2023-Jan-10  Lixin Sun  Added "IsBiome" option, which determines if a biome map should 
#                                            be returned.
#############################################################################################################  
def get_GlobLC(Year, IsBiome):
  '''Returns a proper land cover mosaic based on a given region and year.

     Args:
       Region(ee.Geometry): A spatial region defining the location of the mosaic;
       Year(int or string): The target year;
       IsBiome(Boolean): Flag indicating if a biome map will be returned. Only when RF model is used'''
  #==========================================================================================================
  # Choose a proper land cover image collection based on a given "Year"
  #==========================================================================================================
  year = int(Year)
  new_name = 'partition'

  if year <= 2017:
    ccrs_LC = ee.ImageCollection('users/rfernand387/NA_NALCMS_2015_tiles') \
              .map(lambda image: image.rename(new_name)) \
              .mosaic()
    
  elif year > 2017:
    ccrs_LC = ee.Image('USGS/NLCD_RELEASES/2020_REL/NALCMS').rename(new_name)
 
  #==========================================================================================================
  # A function for mapping the class IDs of global land cover map to those of CCRS land cover map
  #==========================================================================================================
  def remap_classIDs(Image):
    img = Image.select("discrete_classification").uint8()

    img = img.remap([0,20,30,40,50,60,70,80,90,100,111,112,113,114,115,116,121,122,123,124,125,126,200], \
                    [0,8, 10,15,17,16,19,18,14,13, 1,  3,  1,  5,  6,  6,  2,  4,  2,  5,  6,  6,  18], 0)
    
    return img.rename(new_name)
  
  #==========================================================================================================
  # The given "Region" might already be expended from original region, but here it is necessary to reexpend it
  # so that it can completely cover reprojected output result.    
  #==========================================================================================================  
  global_LC = ee.Image('COPERNICUS/Landcover/100m/Proba-V-C3/Global/2019')  
  global_LC = remap_classIDs(global_LC)  

  #==========================================================================================================
  # Merge two land cover maps together with CCRS' land cover map as basis and then clip it
  #==========================================================================================================  
  #out_map = ccrs_LC.unmask(value = global_LC, sameFootprint = False)   #.clip(region)
  out_map = global_LC.where(ccrs_LC.gte(0), ccrs_LC)

  #==========================================================================================================
  # Biome is valid only when Random Forest model is used for extracting biophysical parameters
  # The mapping from CCRS land cover ID to SL2P land cover will be conducted in "makeIndexLayer" function,
  # which is in "LEAFNets.py" 
  #==========================================================================================================
  if IsBiome == True:
    #out_map = out_map.remap([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19], [0,7,7,5,6,6,7,2,2,1,1,2,1,9,2,3,9,10,0,0])
    out_map = out_map.remap([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19], \
                            [0,7,7,5,6,6,7,2,2,1,1, 2, 1, 1, 2, 3, 1, 1, 0, 0])

  return out_map





#############################################################################################################
# Description: This function returns a specified global DEM mosaic.
# 
# Revision history:  2022-Aug-25  Lixin Sun  Initial creation
#
#############################################################################################################  
def get_GlobDEM(DEM_name):
  '''Returns a DEM covering a specified region.

     Args:
       DEM_name(string): A given DEM name string ('Copernicus', 'ALOS' or 'NASA_SRTM').'''
  
  dem_name = DEM_name.lower()

  if dem_name.find('coperni') > -1:
    glo30 = ee.ImageCollection("projects/sat-io/open-datasets/GLO-30")
    proj  = glo30.first().select(0).projection()
    print('bands in dem:', glo30.first().bandNames().getInfo())

    return glo30.mosaic().setDefaultProjection(proj).rename('dem')    

  elif dem_name.find('alos') > -1:
    ALOS_DEM = ee.ImageCollection('JAXA/ALOS/AW3D30/V3_2')
    proj     = ALOS_DEM.first().select(0).projection()

    # Reproject an image mosaic using a projection from one of the image tiles,
    # rather than using the default projection returned by .mosaic().
    return ALOS_DEM.select('DSM').mosaic().setDefaultProjection(proj).rename('dem')
  
  elif dem_name.find('aster') > -1:
    aster_dataset = ee.Image('projects/sat-io/open-datasets/ASTER/GDEM')

    return aster_dataset.rename('dem')
  
  elif dem_name.find('nasa') > -1 or dem_name.find('usgs') > -1:
    # This DEM data covers partial Canada
    nasa_dataset = ee.Image('USGS/SRTMGL1_003')
    return nasa_dataset.select('elevation').rename('dem')
  


    
#############################################################################################################
# Description: This function returns a specified global slope mosaic.
# 
# Revision history:  2023-Aug-21  Lixin Sun  Initial creation
#
#############################################################################################################  
def get_GlobSlope(DEM_name):
  '''Returns a DEM covering a specified region.

     Args:
       DEM_name(string): A given DEM name string ('Copernicus', 'ALOS' or 'NASA_SRTM').'''
  
  return ee.Terrain.slope(get_GlobDEM(DEM_name))




#############################################################################################################
# Description: This function returns a global tree and building height map.
# 
# Revision history:  2022-Aug-25  Lixin Sun  Initial creation
#
#############################################################################################################  
def get_GlobHeight():
  '''Returns a DEM covering a specified region.

     Args:'''

  glodem30 = ee.ImageCollection("projects/sat-io/open-datasets/GLO-30").mosaic()
  fabdem30 = ee.ImageCollection("projects/sat-io/open-datasets/FABDEM").mosaic()
  
  return glodem30.subtract(fabdem30)





#############################################################################################################
# Description: This function returns a global water mosaic.
# 
# Note: There is another global water map (called JRC Global Surface Water Mapping) in GEE. However it seems 
#       that JRC and forest change water maps are highly consistent.      
#
# Revision history:  2022-Aug-25  Lixin Sun  Initial creation
#                    2022-Sep-23  Lixin Sun  Ensure 1 and 0 represent water and land for every pixel
#    
#############################################################################################################  
def get_GlobWater(OccThresh):
  '''Returns a global water mosaic.
     Args:
       OccThresh(int): A goven occurence threshold.'''

  JRC_water = ee.Image("JRC/GSW1_4/GlobalSurfaceWater")

  return JRC_water.select('occurrence').unmask().gt(OccThresh)