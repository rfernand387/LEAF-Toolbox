import ee
import imageBands as ib

# sentinel 2 land mask
def S2MaskLand(image):
    image = ee.Image(image)
    
    mask = (image.select('SCL').eq(4)).or(image.select('SCL').eq(5))
    
    return (image.updateMask(mask))



# sentinel 2 clear sky mask
def S2MaskClear= function(image):
    image = ee.Image(image)
    
    qa = image.select('QA60')
    mask = qa.bitwiseAnd(1<<10).eq(0) \
              .and(qa.bitwiseAnd(1<<11).eq(0))
    
    return (image.updateMask(mask))


# wrapper to use app.mask.sentinel2 with CCRS s2 data
def ccrsSentinel2(image):
    image = ee.Image(image)

    return image.rename(['B1','B2','B3','B4','B5','B6','B7','B8','B8A','B9','B11','B12','AOT','WVP','SCL','TCI_R','TCI_G','TCI_B','QA10','QA20','QA60','date'])

# add s2 geomtery bands scaled by 10000
def addS2Geometry(colOptions,image):
    colOptions = ee.Dictionary(colOptions)
    image = ee.Image(image)

    return image.addBands(image.select('B2').multiply(0).add(ee.Number(image.get(colOptions.get("vza")))).multiply(3.1415).divide(180).cos().multiply(10000).toUint16().rename('cosVZA')) \
                .addBands(image.select('B2').multiply(0).add(ee.Number(image.get(colOptions.get("sza")))).multiply(3.1415).divide(180).cos().multiply(10000).toUint16().rename('cosSZA')) \
                .addBands(image.select('B2').multiply(0).add(ee.Number(image.get(colOptions.get("saa")))) \
                          .subtract(image.select('B2').multiply(0).add(ee.Number(image.get(colOptions.get("vaa"))))).multiply(3.1415).divide(180).cos().multiply(10000).toInt16().rename('cosRAA'))

# add s2 geometry bands scaled by 10000 for sloped terrain
def addS2Geometryv2(colOptions, image):
    image = ee.Image(image)
  
    vza = image.select('B2').multiply(0).add(image.metadata(colOptions.get("vza")))
    vaa = image.select('B2').multiply(0).add(image.metadata(colOptions.get("vaa")))
    sza = image.select('B2').multiply(0).add(image.metadata(colOptions.get("sza")))
    saa = image.select('B2').multiply(0).add(image.metadata(colOptions.get("saa")))
    
    vza = ib.getZenithAngle(vza,vaa,ee.Image("MERIT/DEM/v1_0_3"))
    vaa = ib.getAzimuthAngle(vaa,ee.Image("MERIT/DEM/v1_0_3"))
    sza = ib.getZenithAngle(sza,saa,ee.Image("MERIT/DEM/v1_0_3"))
    saa = ib.getAzimuthAngle(saa,ee.Image("MERIT/DEM/v1_0_3"))
    
    return image.addBands(vza.multiply(3.1415).divide(180).cos().multiply(10000).toUint16().rename(['cosVZA'])) \
                  .addBands(vaa.multiply(3.1415).divide(180).subtract(saa.multiply(3.1415).divide(180)).cos().multiply(10000).toUint16().rename(['cosRAA'])) \
                  .addBands(sza.multiply(3.1415).divide(180).cos().multiply(10000).toUint16().rename(['cosSZA'])

# add s2 geometry bands scaled by 10000 for sloped terrain except view zenith angle where it uses the baseline estimate
def addS2Geometryv3(colOptions, defaultVZA, image):
    image = ee.Image(image)
  
    vza = image.select('B2').multiply(0).add(defaultVZA)
    vaa = image.select('B2').multiply(0).add(image.metadata(colOptions.get("vaa")))
    sza = image.select('B2').multiply(0).add(image.metadata(colOptions.get("sza")))
    saa = image.select('B2').multiply(0).add(image.metadata(colOptions.get("saa")))
    
    vza = ib.getZenithAngle(vza,vaa,ee.Image("MERIT/DEM/v1_0_3"))
    vaa = ib.getAzimuthAngle(vaa,ee.Image("MERIT/DEM/v1_0_3"))
    sza = ib.getZenithAngle(sza,saa,ee.Image("MERIT/DEM/v1_0_3"))
    saa = ib.getAzimuthAngle(saa,ee.Image("MERIT/DEM/v1_0_3"))
    
    return image.addBands(vza.multiply(3.1415).divide(180).cos().multiply(10000).toUint16().rename(['cosVZA'])) \
                  .addBands(vaa.multiply(3.1415).divide(180).subtract(saa.multiply(3.1415).divide(180)).cos().multiply(10000).toUint16().rename(['cosRAA'])) \
                  .addBands(sza.multiply(3.1415).divide(180).cos().multiply(10000).toUint16().rename(['cosSZA'])) 


# Get geometry of a S2 MGRS_TILE
def getMGRSTileGeometry(tileName):
  tileName = ee.String(tileName)  # tile to get geometry for
  
  return ee.ImageCollection('COPERNICUS/S2_SR').filterDate('2020-01-01','2020-01-20') \
                                               .filterMetadata('MGRS_TILE','equals',tileName) \
                                               .sort('system:asset_size',false) \
                                               .first() \
                                               .geometry()


def  forestCover(): 
    return ee.ImageCollection('users/rfernand387/NA_NALCMS_2015_tiles') \
              .map(lambda image: image.select("b1").rename("partition") ) \
              .merge(ee.ImageCollection("COPERNICUS/Landcover/100m/Proba-V/Global") \
                        .map( lambda image): return image.select("discrete_classification").remap([0,20,30,40,50,60,70,80,90,100,111,112,113,114,115,116,121,122,123,124,125,126,200],[0,8,10,15,17,16,19,18,14,13,1,3,1,5,6,6,2,4,2,5,6,6,18],0).toUint8().rename("partition"))) \
              .mosaic() \
              .remap([1,2,3,4,5,6,7,8,14],[1,1,1,1,1,1,1,1,1],0) \
              .rename("forestCover") 

# make forest cover  band
def getForestCover(image):
    image = ee.Image(image)
    
    return image.addBands(image.select('B11').multiply(0).add(forestCover().clip(image.geometry())).rename('forestCover'))



# add attribute to tile with forest cover percentage
def addCoverPercentage(bandName,image):
    bandName = ee.String(bandName)
    image = ee.Image(image)

    return image.set(bandName.cat('_PERCENTAGE'), \
              image.select(bandName) \
                   .multiply(100) \
                   .reduceRegion( \
                        reducer= ee.Reducer.mean(), \
                        geometry= image.geometry(), \
                        scale= image.select('B3').projection().nominalScale(), \
                        bestEffort= True \
                      ) \
                  .get(bandName)) 


# add attribute of cover percentage in a feature
def addFeatureForestCoverPercentage(scale,feature):
    return feature.set('forestCover_PERCENTAGE', \
                        forestCover().clip(feature.geometry()) \   
                                     .multiply(100) \
                                     .reduceRegion( \
                                          reducer= ee.Reducer.mean(), \
                                          geometry= feature.geometry(), \
                                          scale= scale, \
                                          bestEffort= True, \
                                          tileScale= 16 \
                                        ) \
                                    .get('forestCover') \
                    )


# return image collection falling withing for date range of image
def getImageCollectionRange(imageCollection,image):
    imageCollection = ee.ImageCollection(imageCollection)
    image = ee.Image(image)

    return imageCollection.map(lambda image: image.set('daterange',ee.DateRange(ee.Date(image.get('system:time_start')),ee.Date(image.get('system:time_end'))))) \
                                                            .filter(ee.Filter.dateRangeContains('daterange', ee.Date(image.get('system:time_start'))))
 

# add a land cover band with only one land cover class to a S2 image
# we specifically add it to force resampling as it saves on reprojection
# you can reproject if you want but it may time out depending on the input land cover 
def addLandCoverClassBand(getLandCoverClassImage,image):
    # getLandCoverClassImage - function that returns image with 1 for selected land cover classes only
    image = ee.Image(image) # image to serve as template for new landCover band

    return image.addBands(image.select('B11').multiply(0).add(getLandCoverClassImage().clip(image.geometry())).rename('LandCover'))


# aggregate S2 bands to modis from SL2P output
def aggregateS2MCD15 (reducer,getImageCollectionRange,outputProjection,outputScale,feature,image):
    reducer = ee.Reducer(reducer)
    outputProjection = ee.Projection(outputProjection)
    outputScale = ee.Number(outputScale)
    grid = ee.Feature(feature)
    imahe = ee.Image(image)

    modisCollection = ee.ImageCollection("MODIS/006/MCD15A3H") ;

    return image.addBands(image.select('QC').not().rename('validFraction').updateMask(image.select('QC').mask())) \           # make a band with value=1 is QC is valid
              .unmask() \                                                                                                         # unmask all bands before aggregation , no data values are zero and adjusted later
              .addBands(getImageCollectionRange(modisCollection,image).first().select(['Lai','LaiStdDev']).multiply(0.1)) \       # get the MODIS LAI product containing the S2 image date and add after scaling to real units
              .addBands(getImageCollectionRange(modisCollection,image).first().select(['Fpar','FparStdDev']).multiply(0.01)) \    # get the MODIS Fpar product containing the S2 image date and add after scaling to real units
              .clip(feature.geometry()) \                                                                                         # clip all layers to the grid feature
              .select(['estimateLAI','estimatefAPAR','Lai','LaiStdDev','Fpar','FparStdDev','LandCover','validFraction']) \        # only aggregate the product layers and the land cover and valid fraction
              .reduceResolution( \
                reducer= ee.Reducer.mean(), \
                maxPixels= 1024,    \                                                                                            # we can aggregate at most 1024 pixels or 32x32 fine resolution pixels (e.g. 640m outputScale)
                bestEffort= True   \                                                                                             # our estimate of mean will be statistical if the outputScale is to large
              )   