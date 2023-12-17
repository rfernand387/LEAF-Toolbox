import pandas as pd
import ee
import toolsUtils
import eoImage
import toolsNets
import eoImage
import toolsUtils
import dictionariesSL2P 
# from datetime import timedelta
# from datetime import datetime
import pickle


#makes products for specified region and time period 
def makeProductCollection(algorithm,colOptions,variableName,mapBounds,startDate,endDate,maxCloudcover,inputScale) :

    # print('makeProductCollection')
    products = []

    #get the input collection
    input_collection = algorithm.createInput(mapBounds,startDate, endDate,maxCloudcover)

    # check if there are input images to process
    if (input_collection.size().getInfo() > 0):
        print('#images:',input_collection.size().getInfo())

        input_collection = toolsUtils.rescaleCollection(input_collection,algorithm.networkOptions["inputBands"][3],inputScale)

        if variableName == "Surface_Reflectance":
            products = input_collection
        else:
          
            # pre process input imagery and flag invalid inputs
            input_collection  =  algorithm.preprocessInput(input_collection)

            ## apply networks to produce mapped parameters                                                
            products =  input_collection.select(['date','QC','longitude','latitude'])            
            estimate = input_collection.map(lambda image: algorithm.predict("estimate",variableName,image))
            uncertainty = input_collection.map(lambda image: algorithm.predictUncertainty( "uncertainty",variableName,image))
            products =  products.combine(estimate).combine(uncertainty.select("uncertainty"+variableName))
            
     
    else:
        print('No images found.')

    
    return products

# returns lists of sampled values for each band in an image as a new feature property
def sampleProductCollection(productCollection, sampleRegion, outputScaleSize, factor=1) :

    productCollection = ee.ImageCollection(productCollection)
    outputScaleSize= ee.Number(outputScaleSize)
    sampleRegion = ee.Feature(sampleRegion)

    # produce feature collection where each feature a feature collectiion corresponding to a list of samples from a given band from one product image
    sampleData = productCollection.map(lambda image: image.sample(region=sampleRegion.geometry(), projection=image.select('date').projection(), scale=outputScaleSize,geometries=True, dropNulls = True, factor=factor) ).flatten()
 
    # for each band get a dictionary of sampled values as a property of the sampleRegion feature
    sampleList= ee.List(productCollection.first().bandNames().map(lambda bandName: ee.Dictionary({ 'bandName': bandName, 'data': sampleData.aggregate_array(bandName)})))
    
    return sampleRegion.set('samples',sampleList)

# add dictionary of sampled values from product to a feature
def getSamples(site,variable,algorithm,collectionOptions,maxCloudcover,bufferSpatialSize,inputScaleSize,startDate,endDate,outputScaleSize,factor=1):
    
    # Buffer features is requested
    if ( bufferSpatialSize > 0 ):
        site = ee.Feature(site).buffer(bufferSpatialSize)
    else:
        site = ee.Feature(site)        
    
     # make collection
    sampleFeature = []
    productCollection = []
    productCollection = makeProductCollection(algorithm,collectionOptions,variable,site.geometry(),startDate,endDate,maxCloudcover,inputScaleSize)
    if productCollection :
        if ( ee.ImageCollection(productCollection).size().gt(0) ) :
            sampleFeature = sampleProductCollection(productCollection, site.geometry(),  outputScaleSize,factor)

    return  sampleFeature

# add dictionary of sampled values from product to a feature
def getCollection(site,variable,collectionOptions,networkOptions,maxCloudcover,bufferSize,outputScaleSize, inputScaleSize,startDate,endDate,factor=1):
    
    # Buffer features is requested
    if ( bufferSpatialSize > 0 ):
        site = ee.Feature(site).buffer(bufferSpatialSize)
    else:
        site = ee.Feature(site)        

    # Make the output collection and rescale it if requested    
    outputCollection = makeProductCollection(collectionOptions,networkOptions,variable,site.geometry(),startDate,endDate,maxCloudcover,inputScaleSize) 
    if ( outputScaleSize != inputScaleSize ):
        outputCollection = outputCollection.reduceResolution({reducer: ee.Reducer.mean(),maxPixels: 1024}) \
                                            .reproject({crs: outputCollection,scale:outputScaleSize});
    return outputCollection



#format samples into a data frame
def samplestoDF(sampleFeature):

    # create empty data frame to hold samples
    sampleDF = pd.DataFrame()
    
    # loop over list of samples and add column for each property sampled to dataframe
    sampleList = ee.Dictionary(ee.Feature(sampleFeature).toDictionary()).getInfo()['samples']
    for col in sampleList:
        df = pd.DataFrame((col['data']),columns=[col['bandName']])
        if (not(df.empty)) :
            sampleDF = pd.concat([sampleDF,df],axis=1) 
    
    if  (not(sampleDF.empty)) :
        sampleDF = sampleDF.dropna(subset=['date'])

    return sampleDF

#sample features for LEAF output
def sampleSites(siteList,imageCollectionName,algorithm,variableName='LAI',maxCloudcover=100,outputScaleSize=30,inputScaleSize=30,bufferSpatialSize=0,bufferTemporalSize=[0,0],subsamplingFraction=1,outputFileName=None):
    
    print('\nSTARTING LEAF IMAGE for ',imageCollectionName,'\n ')
    


    #make a dictionary to hold results for each site
    outputDictionary = {}
    collectionOptions = (dictionariesSL2P.make_collection_options(algorithm))[imageCollectionName]
    networkOptions= dictionariesSL2P.make_net_options()
    algorithmName = algorithm.__name__
    algorithm= algorithm.algorithm(variableName,imageCollectionName)
    algorithm.estimator = algorithm.fit()
    algorithm.uncertainty = algorithm.fitUncertainty()

    for input in siteList:
        
        #Convert the feature collection to a list so we can apply SL2P on features in sequence to avoid time outs on GEE
        sampleRecords =  ee.FeatureCollection(input).sort('system:time_start', False).map(lambda feature: feature.set('timeStart',feature.get('system:time_start')))
        sampleRecords =  sampleRecords.toList(sampleRecords.size())
        print('Site: ',input, ' with ',sampleRecords.size().getInfo(), ' features.')
        result = []
        for n in range(0,sampleRecords.size().getInfo()) : 

            # select feature to process
            
            site = ee.Feature(sampleRecords.get(n))

            # get start and end date for this feature if it 
            dateRange = toolsUtils.getdateRange(site,bufferTemporalSize)
                
            print('Processing feature:',n,' from ', dateRange['startDate'].iloc[0],' to ',dateRange['endDate'].iloc[-1])
           
            # process one month at a time to prevent GEE memory limits
            samplesDF = pd.DataFrame()
            for index, Dates in dateRange.iterrows():
                sampleFeature= getSamples(site,variableName,algorithm,collectionOptions,maxCloudcover,bufferSpatialSize,inputScaleSize, \
                            Dates['startDate'],Dates['endDate'],outputScaleSize,subsamplingFraction)
                if sampleFeature :
                    samplesDF = pd.concat([samplesDF,samplestoDF(sampleFeature)],ignore_index=True)
                
            result.append({'feature': ee.Dictionary(ee.Feature(sampleRecords.get(n)).toDictionary()).getInfo() , \
                        algorithmName : samplesDF })
        

        outputDictionary.update({input: result})
        print('\nDONE LEAF SITE\n')


    return outputDictionary


#sample features for LEAF output
def imageSites(siteList,imageCollectionName,algorithm,variableName='LAI',maxCloudcover=0,outputScaleSize=0,inputScaleSize=30,bufferSpatialSize=0,bufferTemporalSize=[0,0],subsamplingFraction=1):
    
    print('\nSTARTING LEAF IMAGE for ',imageCollectionName,'\n ')

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

            # select feature to process
            
            site = ee.Feature(sampleRecords.get(n))

            # get start and end date for this feature
            startDate = datetime.fromtimestamp(ee.Date(site.get('system:time_start')).advance(bufferTemporalSize[0],'day').getInfo()['value']/1000)
            endDate = datetime.fromtimestamp(ee.Date(site.get('system:time_end')).advance(bufferTemporalSize[1],'day').getInfo()['value']/1000)
            endDatePlusOne = datetime.fromtimestamp(ee.Date(site.get('system:time_end')).advance(bufferTemporalSize[1]+1,'day').getInfo()['value']/1000)
 
            print('Processing feature:',n,' from ', startDate,' to ',endDate)
             #do monthly processing 
            if (len(pd.date_range(startDate,endDate,freq='m')) > 0 ):
                dateRange = pd.DataFrame(pd.date_range(startDate,endDate,freq='m'),columns=['startDate'])
                dateRange['endDate'] = pd.concat([dateRange['startDate'].tail(-1),pd.DataFrame([endDatePlusOne])],ignore_index=True).values
            else:
                dateRange = pd.DataFrame( {'startDate':[startDate],'endDate':[endDatePlusOne]})

            # process one month at a time to prevent GEE memory limits
            siteCollection = ee.ImageCollection([])
            for index, Dates in dateRange.iterrows():
                print(Dates)
                monthlyCollection = getCollection(site,variableName,collectionOptions[imageCollectionName],networkOptions[variableName][imageCollectionName],maxCloudcover,bufferSpatialSize,inputScaleSize, \
                            Dates['startDate'],Dates['endDate'],outputScaleSize,subsamplingFraction)
                if monthlyCollection :
                    siteCollection = siteCollection.merge(monthlyCollection)
                
            result.append({'feature': ee.Dictionary(ee.Feature(sampleRecords.get(n)).toDictionary()).getInfo() , \
                        algorithm.__name__ : siteCollection })
        
        outputDictionary.update({input: result})
        print('\nDONE LEAF IMAGE\n')
    return outputDictionary
