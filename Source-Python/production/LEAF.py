import pandas as pd
import ee
import toolsUtils
import toolsSampling
import eoImage
import toolsNets
import eoImage
import toolsUtils
import dictionariesSL2P 

#makes products for specified region and time period 
def makeProductCollection(colOptions,netOptions,variable,mapBounds,startDate,endDate,maxCloudcover,outputScale,filterSize) :

    # print('makeProductCollection')
    products = []
    tools = colOptions['tools']
    
    # parse the networks
    # check how many different unique networks are available (i.e. by partition class) - this is used for SL2P-CCRS
    numNets = ee.Number(ee.Feature((colOptions["Network_Ind"]).first()).propertyNames().remove('Feature Index').remove('system:index').size())
    # populate the netwoorks for each unique partition class
    SL2P = ee.List.sequence(1,ee.Number(colOptions["numVariables"]),1).map(lambda netNum: toolsNets.makeNetVars(colOptions["Collection_SL2P"],numNets,netNum))
    errorsSL2P = ee.List.sequence(1,ee.Number(colOptions["numVariables"]),1).map(lambda netNum: toolsNets.makeNetVars(colOptions["Collection_SL2Perrors"],numNets,netNum))

    # make products 
    input_collection =  ee.ImageCollection(colOptions['name']) \
                      .filterBounds(mapBounds) \
                      .filterDate(startDate, endDate) \
                      .filterMetadata(colOptions["Cloudcover"],'less_than',maxCloudcover) \
                      .limit(5000) \
                      .map(lambda image: image.clip(mapBounds)) \
                      .map(lambda image: tools.MaskClear(image))  \
                      .map(lambda image: eoImage.attach_Date(image)) \
                      .map(lambda image: eoImage.attach_LonLat(image)) \
                      .map(lambda image: tools.addGeometry(colOptions,image)) 
    
    # print(input_collection.size().getInfo())
    # image = input_collection.first()
    # samples=image.sample(region=image.geometry(), projection=image.select('date').projection(), scale=outputScale,geometries=True, dropNulls = False,numPixels=100)
    # sampleList2= ee.List(image.bandNames().map(lambda bandName: ee.Dictionary({ 'bandName': bandName, 'data': samples.aggregate_array(bandName)})))
    # print(sampleList2.getInfo())   

    # check if there are products
    if (input_collection.size().getInfo() > 0):

        # reproject to output scale based if it differs from nominal scale of first band
        projection = input_collection.first().select(netOptions["inputBands"][3]).projection()
        # print(projection.nominalScale().getInfo())
        # print(outputScale)
        # if ( projection.nominalScale().neq(ee.Number(outputScale))):
        #     print('reprojection')
        input_collection = input_collection.map( lambda image: image.setDefaultProjection(crs=image.select(image.bandNames().slice(0,1)).projection()).reduceResolution(reducer= ee.Reducer.mean(),maxPixels=1024).reproject(crs=projection,scale=outputScale))
                                                
        if variable == "Surface_Reflectance":
            products = input_collection
        else:
            # get partition used to select network
            partition = (colOptions["partition"]).filterBounds(mapBounds).mosaic().clip(mapBounds).rename('partition');
            # pre process input imagery and flag invalid inputs
            input_collection  =  input_collection.map(lambda image: tools.MaskLand(image)).map(lambda image: toolsUtils.scaleBands(netOptions["inputBands"],netOptions["inputScaling"],image)) \
                                                 .map(lambda image: toolsUtils.invalidInput(colOptions["sl2pDomain"],netOptions["inputBands"],image)) 


            ## apply networks to produce mapped parameters                                                
            products =  input_collection.select(['date','QC','longitude','latitude'])            
            estimateSL2P = input_collection.map(lambda image: toolsNets.wrapperNNets(SL2P,partition, netOptions, colOptions,"estimate",variable,image))
            uncertaintySL2P = input_collection.map(lambda image: toolsNets.wrapperNNets(errorsSL2P,partition, netOptions, colOptions,"error",variable,image))

            # Define a boxcar or low-pass kernel.
            if (filterSize > 0 ):
                print('smoothing')
                boxcar = ee.Kernel.square(radius= filterSize, units= 'meters', normalize= True);

                # mask by QC and boxcar filter the estimate andu ncertainty layers
                estimateSL2P = estimateSL2P.map( lambda image: image.addBands(image.updateMask(image.select('QC').eq(0)).select("estimate"+variable).convolve(boxcar)))
                uncertaintySL2P = uncertaintySL2P.map( lambda image: image.addBands(image.updateMask(image.select('QC').eq(0)).select("uncertanity"+variable).convolve(boxcar)))

            products =  products.combine(estimateSL2P).combine(uncertaintySL2P.select("error"+variable))
            # image = estimatesSL2P.first()
            # samples=image.sample(region=miage.geometry(), projection=image.select('date').projection(), scale=outputScale,geometries=True, dropNulls = False)
            # sampleList2= ee.List(productCollection.first().bandNames().map(lambda bandName: ee.Dictionary({ 'bandName': bandName, 'data': samples.aggregate_array(bandName)})))
            # print(sampleList2.getInfo())
    
    return products

# returns lists of sampled values for each band in an image as a new feature property
def sampleProductCollection(productCollection, outputScale, sampleRegion) :

    # print('sampleProductCollection')
    productCollection = ee.ImageCollection(productCollection)
    outputScale= ee.Number(outputScale)
    sampleRegion = ee.Feature(sampleRegion)

    # produce feature collection where each feature a feature collectiion corresponding to a list of samples from a given band from one product image
    # first add a band of ones to the image to account for masked data
    sampleData = productCollection.map(lambda image: image.sample(region=sampleRegion.geometry(), projection=image.select('date').projection(), scale=outputScale,geometries=True, dropNulls = False) ).flatten()
    # print(productCollection.first().bandNames().getInfo())
    # image = productCollection.first()
    # samples=image.sample(region=sampleRegion.geometry(), projection=image.select('date').projection(), scale=outputScale,geometries=True, dropNulls = False)
    # sampleList2= ee.List(productCollection.first().bandNames().map(lambda bandName: ee.Dictionary({ 'bandName': bandName, 'data': samples.aggregate_array(bandName)})))
    # print(sampleList2.getInfo())
    # for each band get a dictionary of sampled values as a property of the sampleRegion feature
    sampleList= ee.List(productCollection.first().bandNames().map(lambda bandName: ee.Dictionary({ 'bandName': bandName, 'data': sampleData.aggregate_array(bandName)})))

    
    return sampleRegion.set('samples',sampleList)

# add dictionary of sampled values from product to a feature
def getSamples(site,variable,collectionOptions,networkOptions,maxCloudcover,bufferSize,outputScale,deltaTime,filterSize):
    
    # define vars
    if ( bufferSize > 0 ):
        site = ee.Feature(site).buffer(bufferSize*2)
    else:
        site = ee.Feature(site)        
    
    # get start and end date for this feature
    startDate = ee.Date(site.get('system:time_start')).advance(deltaTime[0],'day')
    endDate = ee.Date(site.get('system:time_end')).advance(deltaTime[1],'day')
 
    # make collection
    sampleFeature = [];
    productCollection = []
    productCollection = ee.ImageCollection(makeProductCollection(collectionOptions,networkOptions,variable,site.geometry(),startDate,endDate,maxCloudcover,outputScale,filterSize))
    if productCollection :
        if ( ee.ImageCollection(productCollection).size().gt(0) ) :
            sampleFeature = sampleProductCollection(productCollection, outputScale, site.geometry())

    return  sampleFeature

#format samples into a data frame
def samplestoDF(sampleFeature):
    sampleDF = pd.DataFrame()
    sampleList = ee.Dictionary(ee.Feature(sampleFeature).toDictionary()).getInfo()['samples'] 
    # print(len(sampleList[0]))
    for col in sampleList:
        df = pd.DataFrame((col['data']),columns=[col['bandName']])
        if (not(df.empty)) :
            sampleDF = pd.concat([sampleDF,df],axis=1)
    # print(sampleDF)
    return sampleDF.dropna(subset=['date'])

#sample features for LEAF output
def sampleSites(siteList,imageCollectionName,algorithm,variableName,maxCloudcover,filterSize,scaleSize,bufferSize,deltaTime,):
    
    print('\nSTARTING LEAF SITE\n ')

    outputDictionary = {}
    collectionOptions = (dictionariesSL2P.make_collection_options(algorithm))
    networkOptions= dictionariesSL2P.make_net_options()
    for input in siteList:
        
        #Convert the feature collection to a list so we can apply SL2P on features in sequence to avoid time outs on GEE
        sampleRecords =  ee.FeatureCollection(input).sort('system:time_start', False).map(lambda feature: feature.set('timeStart',feature.get('system:time_start')))
        sampleRecords =  sampleRecords.toList(sampleRecords.size())
        print('Site: ',input, ' with ',sampleRecords.size().getInfo(), ' features.')
        result = []
        for n in range(0,sampleRecords.size().getInfo()) : 
            print('Processing feature:',n)
            sampleFeature= getSamples(sampleRecords.get(n),variableName,collectionOptions[imageCollectionName],networkOptions[variableName][imageCollectionName],maxCloudcover,bufferSize,scaleSize,deltaTime,filterSize)
            if sampleFeature :
                result.append({'feature': ee.Dictionary(ee.Feature(sampleRecords.get(n)).toDictionary()).getInfo() , \
                               algorithm.__name__ : samplestoDF(sampleFeature) })
            
        outputDictionary.update({input: result})
        print('\nDONE LEAF SITE\n')
    return outputDictionary
