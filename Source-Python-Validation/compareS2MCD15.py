import ee
import imageBands as ib
import toolsS2 as S2
import SL2Poverwrite as SL2P

# samples S2 images for a MGRS tile for output SL2P products and associated MCD15 products at MCD15 projection and specified outputScale
# to avoid computation limits it samples a specified number of tiles in a covering grid with grid size smaller than the 100kmx100km MGRS_TILE
# and also samples a maximum number of input S2 images in a specified time interval
# the coveringGrid's are selected as those with the highest fraction of pixels exceeding the fraction of valid land cover type
def getSL2PMCD15Samples(S2,ib,SL2P,dictionariesSL2P,outputScale,coveringGridScale,maxGrids,maxImages,startDate,endDate, minUnmaskedArea,maxCLOUDY_PIXEL_PERCENTAGE,minCoveringGridLandCover_PERCENTAGE,minPixelValidFraction,minPixelLandCoverFraction,maxPixelLAICV,tileName) :
    # S2 - functions for processing S2 data
    # ib - functions for processing image bands
    # dictionariesSL2P - function to create SL2P algorithm dictionaries
    outputScale = ee.Number(outputScale)                                                      # scale of aggregated values 
    coveringGridScale = ee.Number(coveringGridScale)                                          # scale of covering grid grid boxes
    maxGrids = ee.Number(maxGrids)                                                            # maximum number of covering grids to sample
    startDate = ee.Date(startDate)                                                                         # start date of S2 sampling period
    endDate = ee.Date(endDate)                                                                         # end date of S2 sampling period
    minUnmaskedArea = ee.Number(minUnmaskedArea)                                             # minimum unmasked area of a grid before processing it
    maxCLOUDY_PIXEL_PERCENTAGE= ee.Number(maxCLOUDY_PIXEL_PERCENTAGE)                        # minimum S2 IMAGE CLOUDY_PIXEL_PERCENTAGE
    minCoveringGridLandCover_PERCENTAGE = ee.Number(minCoveringGridLandCover_PERCENTAGE)     # minimum land cover percentage in covering grid tile
    minPixelValidFraction = ee.Number(minPixelValidFraction )                                # minimum valid pixel fraction in an aggregated pixel                 
    minPixelLandCoverFraction = ee.Number(minPixelLandCoverFraction)                         # minimum land cover fraction in an aggregated pixel
    maxPixelLAICV = ee.Number(maxPixelLAICV)                                                 # maximum coefficient of iation of LAI in an aggregated pixel
    tileName = ee.String(tileName)                                                           # MGRS_TILE name of tile to process

    # specify input collections 
    collectionNameS2 = "COPERNICUS/S2_SR"     
    collectionNameMCD15 ='MODIS/006/MCD15A3H';
    collectionS2 = ee.ImageCollection(collectionNameS2)
    collectionMCD15 = ee.ImageCollection(collectionNameMCD15)
    projectionMCD15 = collectionMCD15.first().projection()

    # make the tile feature and add metadata
    tile = ee.Feature(ee.Geometry(S2.getMGRSTileGeometry(tileName))).set('MGRS_TILE',tileName, \
                                                                      'gridScale',coveringGridScale, \
                                                                      'outputScale',outputScale, \
                                                                      'collectionName',collectionNameS2, \
                                                                      'modisCollection',collectionNameMCD15, \
                                                                      'system:time_start',startDate, \
                                                                      'system:time_end',endDate, \
                                                                      'minArea',minUnmaskedArea, \
                                                                      'maxCLOUDY_PIXEL_PERCENTAGE',maxCLOUDY_PIXEL_PERCENTAGE, \
                                                                      'minLandCover_PERCENTAGE',minCoveringGridLandCover_PERCENTAGE, \
                                                                      'minValidFraction',minPixelValidFraction, \
                                                                      'minLandCoverFraction',minPixelLandCoverFraction, \
                                                                      'numSamples',0)


    # get input S2 imagery that meet criteria and add bands for further processing
    colOptions = ee.Dictionary(ee.Dictionary(dictionariesSL2P.make_collection_options()).get(collectionNameS2))  #dictionaries describing sensors and bands for networks
    inputCollection = ee.ImageCollection(collectionNameS2).filterDate(startDate,endDate) \
                                                 .filterMetadata('MGRS_TILE','equals',tileName) \
                                                 .filterMetadata('CLOUDY_PIXEL_PERCENTAGE','not_greater_than',maxCLOUDY_PIXEL_PERCENTAGE) \
                                                 .map(lambda image: S2.addLandCoverClassBand(ib.getLandCoverClassImage,image))   \    # add band with selected land cover =1
                                                 .map(S2.S2MaskLand)          \                                                                 # Mask no land areas
                                                 .map(S2.S2MaskClear)    \                                                                      # Mask non clear sky areas
                                                 .map(S2.addS2Geometryv2.bind(null,colOptions))   \                                             # add geometry including terrain
                                                 .sort('CLOUDY_PIXEL_PERCENTAGE')   \                                                                           
                                                 .limit(maxImages)
    projectionS2 = inputCollection.first().select('B11').projection()                                                                      # remember the S2 projection for this tile

    # make and subset grids from a covering grid to optimize memory
    coveringGrid = tile.geometry().coveringGrid(projectionMCD15,coveringGridScale) \                                              # make covering grid to optimize memory
                          .map(lambda feature: feature.intersection(tile.geometry(),projectionS2.nominalScale())) \    # clip the grids to the tile
                          .map(lambda feature: feature.set('area',feature.geometry().area())) \                        # update the area of the clopped grid
                          .filterMetadata('area','greater_than',minUnmaskedArea) \                                                  # only retain grids exceeding minimum area
                          .map(lambda feature: ib.addFeatureLandCoverPercentage(ib.getLandCoverClassImage,outputScale,feature)) \# compute and add property of land cover percentage        
                          .filterMetadata('LandCover_PERCENTAGE','greater_than', minCoveringGridLandCover_PERCENTAGE) \                     # select only grids exceeding required land cover percentage in unmasked areas
                          .sort('landCover_PERCENTAGE',False) \                                                                     # sort by descending land cover percentage
                          .limit(maxGrids)                                                                                        # select only up to maxGrids grids


    # aggregate data for each grid and return it as a feature colelction of samples
    result = coveringGrid.map( lambda feature: \
                    feature.set('outputCollection',
                            SL2P.applySL2P(inputCollection.filterBounds(feature.geometry()) \ 
                                                          .map(lambda image: image.clip(feature.geometry())),'LAI',dictionariesSL2P) \            # apply SL2P to estimate LAI
                            .select(['estimateLAI','QC','LandCover'])  \                                                                                     # only keep estimateLAI some bands
                            .combine(SL2P.applySL2P(inputCollection.filterBounds(feature.geometry())  \             
                                                          .map(lambda image: image.clip(feature.geometry())),'fAPAR',dictionariesSL2P) \            # apply SL2P to estimate fAPAR
                            .select(['estimatefAPAR']))  \                                                                                                    # only keep estimatefAPAR assuming QC is same
                            .map(lambda image: \
                            return S2.aggregateS2MCD15(ee.Reducer.mean(),ib.getImageCollectionRange,projectionMCD15,outputScale,feature,image)   \                                 # aggregate bands to mean values at MCD15 pixels
                            .rename(['meanestimateLAI','meanestimatefAPAR','meanLai','meanLaiStdDev','meanFpar','meanFparStdDev','meanLandCover','meanvalidFraction'])  \# rename bands to indicate they are mean values
                            .addBands(S2.aggregateS2MCD15(ee.Reducer.stdDev(),ib.getImageCollectionRange,projectionMCD15,outputScale,feature,image)        \               # aggregate bands to stdDev values at MCD15 pixels
                                    .rename(['stdestimateLAI','stdLandCover','stdestimatefAPAR','stdvalidFraction','stdLai','stdLaiStdDev','stdFpar','stdFparStdDev'])) \# rename bands to indicate they are stdDev values
                            .addBands(ib.getImageCollectionRange(collectionMCD15,image).first().select(['FparLai_QC','FparExtra_QC']))     \                 # add the MODIS QC bands as nearest neighbour resampling
                            ) \
                            .map( lambda image: \
                            return image.updateMask(image.select('meanvalidFraction').gt(minPixelValidFraction))        \                                         # select pixels with minimum valid fraction
                                  .addBands(image.select(['meanestimateLAI','meanestimatefAPAR','stdestimateLAI','stdestimatefAPAR'])    \             # scale the parameters to account for partial valid fraction
                                                 .divide(image.select('meanvalidFraction')),null,True)      \
                                  .updateMask(image.select('meanLandCover').gt(minPixelLandCoverFraction))                                               # select pixelswith minimum land cover fraction
                                  .updateMask(image.select('stdestimateLAI')            \                    \                                          # mask pixels with too high CV of LAI
                                                  .divide(image.select('meanestimateLAI').add(0.1))\
                                                  .lt(maxPixelLAICV))\
                                  .updateMask(image.select('FparLai_QC').bitwiseAnd(1<<0).eq(0))   \                                                   # mask out poor MCD quality
                                  .updateMask(image.select('FparLai_QC').bitwiseAnd(1<<3).eq(0))    \                                                  # mask out poor MCD quality
                                  .updateMask(image.select('FparLai_QC').bitwiseAnd(1<<6).eq(0))   \                                                   # mask out poor MCD quality
                                  .updateMask(image.select('FparLai_QC').bitwiseAnd(1<<7).eq(0))    \                                                  # mask out poor MCD quality
                                  .updateMask(image.select('FparExtra_QC').bitwiseAnd(1<<2).eq(0)) \                                                   # mask out poor MCD quality
                                  .updateMask(image.select('FparExtra_QC').bitwiseAnd(1<<4).eq(0)) \                                                    # mask out poor MCD quality
                                  .updateMask(image.select('FparExtra_QC').bitwiseAnd(1<<5).eq(0))  \                                                  # mask out poor MCD quality
                                  .updateMask(image.select('FparExtra_QC').bitwiseAnd(1<<6).eq(0)) \                                                   # mask out poor MCD quality   
                                  .sample(  \                                                                                                      # sample data at desired outputScale 
                                    region=feature.geometry(), \
                                    scale= outputScale,\
                                    projection= projectionMCD15,\
                                    dropNulls= True, \
                                    tileScale=16, \
                                    geometries= False\
                                  ) \
                            ) \
                        .flatten())   \                                                                                                                     # merge all of the collections across images
                )
 
    # summary statistics
    samples = ee.FeatureCollection(result.aggregate_array('outputCollection')).flatten()                                         # merge all of the collections across grids
    return tile.set('samples',samples,'numSamples',samples.size())                                                                   # add properties to tile corresponding to the samples and the number of samples (to allow for filtering)



def getStats(tile):
    tile = ee.Feature(tile)

    sample = ee.FeatureCollection(tile.get('samples'))

    n = sample.size()
    x = sample.aggregate_array('meanestimateLAI')
    y = sample.aggregate_array('meanLai')
    res = ee.Array(y).subtract(ee.Array(x))
    meanS2LAI = x.reduce(ee.Reducer.mean())
    meanMODISLAI = y.reduce(ee.Reducer.mean())
    biasLAI = ee.Number(res.toList().reduce(ee.Reducer.mean()))
    rmseLAI = res.dotProduct(res).divide(n).sqrt()
    maeLAI = res.abs().sort().get([n.divide(2).toUint32()])
    lineLAI = ee.Dictionary(x.zip(y).reduce(ee.Reducer.linearFit()))

    x = sample.aggregate_array('meanestimatefAPAR')
    y = sample.aggregate_array('meanFpar')
    res = ee.Array(y).subtract(ee.Array(x))
    meanS2fAPAR = x.reduce(ee.Reducer.mean())
    meanMODISfAPAR = y.reduce(ee.Reducer.mean())
    biasfAPAR = ee.Number(res.toList().reduce(ee.Reducer.mean()))
    rmsefAPAR = res.dotProduct(res).divide(n).sqrt()
    maefAPAR = res.abs().sort().get([n.divide(2).toUint32()])
    linefAPAR = ee.Dictionary(x.zip(y).reduce(ee.Reducer.linearFit()))

    meanLandCover = sample.aggregate_array('meanLandCover').reduce(ee.Reducer.mean())

    return tile.set('meanS2LAI',meanS2LAI,'meanMODISLAI',meanMODISLAI,'biasLAI',biasLAI,'rmseLAI',rmseLAI,'maeLAI',maeLAI,'lineLAI',lineLAI, \
                  'meanS2fAPAR',meanS2fAPAR,'meanMODISfAPAR',meanMODISfAPAR,'biasfAPAR',biasfAPAR,'rmsefAPAR',rmsefAPAR,'maefAPAR',maefAPAR,'linefAPAR',linefAPAR, \
                  'meanLandCover',meanLandCover, \
                  'sample',sample)

