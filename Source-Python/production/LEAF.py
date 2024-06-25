import pandas as pd
import ee
import toolsUtils
import eoImage
import toolsNets
import eoImage
import toolsUtils
import dictionariesSL2P 
from datetime import timedelta
from datetime import datetime
import pickle
import os
from pprint import pprint
import numpy as np
from tqdm import tqdm 


#makes products for specified region and time period 
def makeProductCollection(colOptions,netOptions,variable,mapBounds,startDate,endDate,maxCloudcover,inputScaleSize) :
    # print('makeProductCollection')
    products = []
    tools = colOptions['tools']
    
    # parse the networks
    # check how many different unique networks are available (i.e. by partition class) - this is used for SL2P-CCRS
    numNets = ee.Number(ee.Feature((colOptions["Network_Ind"]).first()).propertyNames().remove('lon').remove('Feature Index').remove('system:index').size())

    # populate the netwoorks for each unique partition class
    net1 = toolsNets.makeNetVars(colOptions["Collection_SL2P"],numNets,1)
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

    # check if there are products
    if (input_collection.size().getInfo() > 0):
        # reproject to output scale based if it differs from nominal scale of first band
        projection = input_collection.first().select(netOptions["inputBands"][3]).projection()
        input_collection = input_collection.map( lambda image: image.setDefaultProjection(crs=image.select(image.bandNames().slice(0,1)).projection()) \
                                                                    .reduceResolution(reducer= ee.Reducer.mean(),maxPixels=1024).reproject(crs=projection,scale=inputScaleSize))
        
        input_collection  =  input_collection.map(lambda image: tools.MaskLand(image)).map(lambda image:toolsUtils.scaleBands(netOptions["inputBands"],netOptions["inputScaling"],netOptions["inputOffset"],image)) 

        partition = (colOptions["partition"]).filterBounds(mapBounds).mosaic().clip(mapBounds).rename('partition');
        input_collection  =  input_collection.map(lambda image: image.addBands(partition))
        ###  add s2cloudness data (For Sentinel-2)
        if colOptions['name'].startswith('COPERNICUS/S2_SR'):
            s2_cloudless_col = (ee.ImageCollection('COPERNICUS/S2_CLOUD_PROBABILITY').filterBounds(mapBounds).filterDate(startDate, endDate))
            s2_cloudless_col = s2_cloudless_col.map( lambda image: image.setDefaultProjection(crs=image.select(image.bandNames().slice(0,1)).projection()) \
                                                                        .reduceResolution(reducer= ee.Reducer.mean(),maxPixels=1024).reproject(crs=projection,scale=inputScaleSize)
                                                                        .rename('s2cloudless_probability'))
            input_collection = input_collection.combine(s2_cloudless_col)
              
    
        if variable == "Surface_Reflectance":
            products = input_collection
        else:
            # get partition used to select network
            #partition = (colOptions["partition"]).filterBounds(mapBounds).mosaic().clip(mapBounds).rename('partition');

            # pre process input imagery and flag invalid inputs
            input_collection  =  input_collection.map(lambda image: toolsUtils.invalidInput(colOptions["sl2pDomain"],netOptions["inputBands"],image)) 
            
            ## apply networks to produce mapped parameters
            if 's2cloudless_probability' in input_collection.first().bandNames().getInfo():
                products =  input_collection.select(['date','QC','longitude','latitude','s2cloudless_probability'])  
            else:
                products =  input_collection.select(['date','QC','longitude','latitude']) 
                
            image = input_collection.first()
            estimateSL2P = input_collection.map(lambda image: toolsNets.wrapperNNets(SL2P,partition, netOptions, colOptions,"estimate",variable,image))
            uncertaintySL2P = input_collection.map(lambda image: toolsNets.wrapperNNets(errorsSL2P,partition, netOptions, colOptions,"error",variable,image))
            products =  products.combine(estimateSL2P).combine(uncertaintySL2P.select("error"+variable))  
    return products

# returns lists of sampled values for each band in an image as a new feature property
def sampleProductCollection(productCollection, sampleRegion, outputScaleSize, factor=1,numPixels=0) :

    productCollection = ee.ImageCollection(productCollection)
    outputScaleSize= ee.Number(outputScaleSize)
    sampleRegion = ee.Feature(sampleRegion)

    # produce feature collection where each feature a feature collectiion corresponding to a list of samples from a given band from one product image
    if (numPixels>0):
        sampleData = productCollection.map(lambda image: image.sample(region=sampleRegion.geometry(), projection=image.select(image.slice(4,5).bandNames()).projection(), scale=outputScaleSize,geometries=True, dropNulls = True, numPixels=numPixels) ).flatten()
    else:
        sampleData = productCollection.map(lambda image: image.sample(region=sampleRegion.geometry(), projection=image.select(image.slice(4,5).bandNames()).projection(), scale=outputScaleSize,geometries=True, dropNulls = True, factor=factor) ).flatten()
    
    # for each band get a dictionary of sampled values as a property of the sampleRegion feature
    sampleList= ee.List(productCollection.first().bandNames().map(lambda bandName: ee.Dictionary({ 'bandName': bandName, 'data': sampleData.aggregate_array(bandName)})))
    
    return sampleRegion.set('samples',sampleList)

# add dictionary of sampled values from product to a feature
def getSamples(site,variable,collectionOptions,networkOptions,maxCloudcover,bufferSpatialSize,inputScaleSize,startDate,endDate,outputScaleSize,factor=1,numPixels=0):
    
    # Buffer features is requested
    if ( bufferSpatialSize > 0 ):
        site = ee.Feature(site).buffer(bufferSpatialSize)
    else:
        site = ee.Feature(site)        
    
     # make collection
    sampleFeature = []
    productCollection = []
    productCollection = makeProductCollection(collectionOptions,networkOptions,variable,site.geometry(),startDate,endDate,maxCloudcover,inputScaleSize)
    if productCollection :
        if ( ee.ImageCollection(productCollection).size().gt(0) ) :
            sampleFeature = sampleProductCollection(productCollection, site.geometry(),  outputScaleSize,factor,numPixels)

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


    
def samplepartition(siteList,algorithm,bufferSpatialSize=0,outputFileName=None,nlcd=None): 
    if outputFileName==None:
        outputFileName=os.getcwd()
    
    outputDictionary = {}
    collectionOptions = (dictionariesSL2P.make_collection_options(algorithm))
    networkOptions= dictionariesSL2P.make_net_options()
    for input in siteList:  
        ofn='_'.join([os.path.split(os.path.abspath(input))[-1],datetime.now().strftime("%Y_%m_%d_%Hh_%mmn")+'.pkl'])
        outputFileName=os.path.join(outputFileName,ofn)
        ESUs = []
        sampleRecords =  ee.FeatureCollection(input).sort('system:time_start', False).map(lambda feature: feature.set('timeStart',feature.get('system:time_start')))
        sampleRecords =  sampleRecords.toList(sampleRecords.size())
        for n in range(sampleRecords.size().getInfo()) : #sampleRecords.size().getInfo()
            result = []
            site = ee.Feature(sampleRecords.get(n))
            esu=site.get('PLOT_ID').getInfo()
            if esu in ESUs:
                print('Already sampled')
            else:
                print(esu)
                ESUs.append(esu)
            
                imageCollectionName='COPERNICUS/S2_SR_HARMONIZED'
                variableName='LAI'
                sampleFeature= get_partition(site,collectionOptions[imageCollectionName],bufferSpatialSize,)

            # if sampleFeature :
            #                 samplesDF = pd.concat([samplesDF,sampleFeature],ignore_index=True)
            # result.append({'feature': ee.Dictionary(ee.Feature(sampleRecords.get(n)).toDictionary()).getInfo() , \
            #                 algorithm.__name__ : samplesDF })        
    
            #         outputDictionary.update({esu: result})   
            #         with open(outputFileName, "wb") as fp:   #Pickling
            #             pickle.dump(outputDictionary, fp) 
    print('\nDONE LEAF SITE\n')    
    return outputDictionary


def sampleTimeSeries(siteList,imageCollectionName,algorithm,variableName='LAI',maxCloudcover=100,outputScaleSize=30,inputScaleSize=30,bufferSpatialSize=0,bufferTemporalSize=[0,0],subsamplingFraction=1,numPixels=0,outputFileName=None,nlcd=None,plots=None): 
    print('STARTING LEAF IMAGE for ',imageCollectionName)
    if outputFileName==None:
        outputFileName=os.getcwd()
    
    try: 
        startDate = datetime.strptime(bufferTemporalSize[0],"%Y-%m-%d")
        endDate =  datetime.strptime(bufferTemporalSize[1],"%Y-%m-%d")
        endDatePlusOne = endDate + timedelta(days=1)
    except:
        raise ValueError(('Supported EO datasets: %s'%(dictionariesSL2P.make_net_options()[variableName].keys())))  
    outputDictionary = {}
    collectionOptions = (dictionariesSL2P.make_collection_options(algorithm))
    networkOptions= dictionariesSL2P.make_net_options()
    for input in siteList:  
        ofn='_'.join([os.path.split(os.path.abspath(input))[-1],imageCollectionName.replace('/','_'),variableName,nlcd,algorithm.__name__+datetime.now().strftime("%Y_%m_%d_%Hh_%mmn")+'.pkl'])
        outputFileName=os.path.join(outputFileName,ofn)
        sampleRecords =  ee.FeatureCollection(input).sort('system:time_start', False).map(lambda feature: feature.set('timeStart',feature.get('system:time_start')))
        sampleRecords =  sampleRecords.toList(sampleRecords.size())
        for n in plots : #sampleRecords.size().getInfo()
            result = []
            site = ee.Feature(sampleRecords.get(n))
            
            esu=site.get('PLOT_ID').getInfo()
            print(esu)
            dateRange = pd.DataFrame(pd.date_range(startDate,endDate,freq='ME'),columns=['startDate'])
            dateRange['endDate'] = pd.concat([dateRange['startDate'].tail(-1),pd.DataFrame([endDatePlusOne])],ignore_index=True).values
            #dateRange = pd.DataFrame( {'startDate':[startDate],'endDate':[endDatePlusOne]})
            # process one month at a time to prevent GEE memory limits
            samplesDF = pd.DataFrame()
            for index, Dates in dateRange.iterrows():
                sampleFeature= getSamples(site,variableName,collectionOptions[imageCollectionName],networkOptions[variableName][imageCollectionName],maxCloudcover,bufferSpatialSize,inputScaleSize, \
                                     Dates['startDate'],Dates['endDate'],outputScaleSize,subsamplingFraction,numPixels)
                if sampleFeature :
                    samplesDF = pd.concat([samplesDF,samplestoDF(sampleFeature)],ignore_index=True)
            result.append({'feature': ee.Dictionary(ee.Feature(sampleRecords.get(n)).toDictionary()).getInfo() , \
                algorithm.__name__ : samplesDF })        
    
            outputDictionary.update({esu: result})   
            with open(outputFileName, "wb") as fp:   #Pickling
                pickle.dump(outputDictionary, fp) 
    print('\nDONE LEAF SITE\n')    
    return outputDictionary
    
#sample features for LEAF output
def sampleSites(siteList,imageCollectionName,algorithm,variableName='LAI',maxCloudcover=100,outputScaleSize=30,inputScaleSize=30,bufferSpatialSize=0,bufferTemporalSize=[0,0],subsamplingFraction=1,numPixels=0,outputPathName=None,feature_range=[0,np.nan]):
    print('STARTING LEAF IMAGE for ',imageCollectionName)
    if outputPathName==None:
        outputPathName=os.getcwd()

    if (type(bufferTemporalSize[0])==str):
        try: 
            startDate = datetime.strptime(bufferTemporalSize[0],"%Y-%m-%d")
            endDate =  datetime.strptime(bufferTemporalSize[1],"%Y-%m-%d")
            endDatePlusOne = endDate + timedelta(days=1)
            defaultDate=True
        except ValueError:
            defaultDate = False
    else:
        defaultDate = False
  
    outputDictionary = {}
    collectionOptions = (dictionariesSL2P.make_collection_options(algorithm))
    networkOptions= dictionariesSL2P.make_net_options()

    ofn='_'.join([os.path.split(os.path.abspath(siteList[0]))[-1],imageCollectionName.replace('/','_'),variableName,str(feature_range[0]),str(feature_range[1]),algorithm.__name__,datetime.now().strftime("%Y_%m_%d_%Hh_%mmn")+'.pkl'])
    outputFileName=os.path.join(outputPathName,ofn)
    print('Output file: %s'%(outputFileName))

    for input in siteList:   
        #Convert the feature collection to a list so we can apply SL2P on features in sequence to avoid time outs on GEE
        sampleRecords =  ee.FeatureCollection(input).sort('system:time_start', False).map(lambda feature: feature.set('timeStart',feature.get('system:time_start')))
        sampleRecords =  sampleRecords.toList(sampleRecords.size())
        print('Site: ',input, ' with ',sampleRecords.size().getInfo(), ' features.')
        feature_range[1]=np.int32(np.nanmin([feature_range[1],sampleRecords.size().getInfo()]))
        
        result = []
        
        #save data search parameters
        params=['input','imageCollectionName','algorithm','variableName','maxCloudcover','outputScaleSize','inputScaleSize','bufferSpatialSize','bufferTemporalSize','subsamplingFraction','feature_range']
        for pp in params:
            if pp == params[0]:
                txt=''
            txt=txt+pp+': %s\n'%(eval(pp))
        with open(outputFileName.replace('.pkl','_metadata.txt'), "a") as fp:   
            fp.write(txt)
            fp.close()
        #######
        
        print('Data sampling for features: from %s to %s'%(feature_range[0],feature_range[1]))
        for n in range(feature_range[0],feature_range[1]) : #sampleRecords.size().getInfo()
            # select feature to process
            site = ee.Feature(sampleRecords.get(n))
            # get start and end date for this feature if it 
            if ( defaultDate==False ):
                time_start = site.get('system:time_start').getInfo()
                if isinstance(time_start, int):
                    startDate = datetime.fromtimestamp(site.get('system:time_start').getInfo()/1000) + timedelta(days=bufferTemporalSize[0])
                else:
                    startDate = datetime.fromtimestamp(ee.Date.parse("dd/MM/YY",site.get('system:time_start'),'Etc/GMT+6').getInfo()['value']/1000) + timedelta(days=bufferTemporalSize[0])

                if ("system:time_end" in site.propertyNames().getInfo()):
                    time_end = site.get('system:time_end').getInfo()
                    if isinstance(time_end, int):
                        endDate = datetime.fromtimestamp(site.get('system:time_end').getInfo()/1000) + timedelta(days=bufferTemporalSize[1])
                    else:
                        endDate = datetime.fromtimestamp(ee.Date.parse("dd/MM/YY",site.get('system:time_end'),'Etc/GMT+6').getInfo()['value']/1000) + timedelta(days=bufferTemporalSize[1])
                else:
                    endDate = startDate - timedelta(days=bufferTemporalSize[0]) + timedelta(days=bufferTemporalSize[1])
                endDatePlusOne = endDate + timedelta(days=1)

            print('Feature n°: %s/%s  -- startDate: %s -- endDate: %s'%(n,feature_range[1],startDate,endDate))
            print('----------------------------------------------------------------------------------------------------------')
            
            #do monthly processing 
            print(startDate,endDate)
            if (len(pd.date_range(startDate,endDate,freq='ME')) > 0 ):
                dateRange = pd.DataFrame(pd.date_range(startDate,endDate,freq='ME'),columns=['startDate'])
                dateRange['endDate'] = pd.concat([dateRange['startDate'].tail(-1),pd.DataFrame([endDatePlusOne])],ignore_index=True).values
            else:
                dateRange = pd.DataFrame( {'startDate':[startDate],'endDate':[endDatePlusOne]})
                
            # process one month at a time to prevent GEE memory limits
            samplesDF = pd.DataFrame()
            for index, Dates in dateRange.iterrows():
                sampleFeature= getSamples(site,variableName,collectionOptions[imageCollectionName],networkOptions[variableName][imageCollectionName],maxCloudcover,bufferSpatialSize,inputScaleSize, \
                                Dates['startDate'],Dates['endDate'],outputScaleSize,subsamplingFraction)
                if sampleFeature :
                    samplesDF = pd.concat([samplesDF,samplestoDF(sampleFeature)],ignore_index=True)

                
            result.append({'feature': ee.Dictionary(ee.Feature(sampleRecords.get(n)).toDictionary()).getInfo() , \
                        algorithm.__name__ : samplesDF })
        
            #dump every 100
            outputDictionary.update({input: result})
            if (( n % 100 ) == 0 ):
                with open(outputFileName.replace('.pkl','_raw.pkl'), "wb") as fpr:   #Pickling
                    pickle.dump(outputDictionary, fpr)

        print('\nDONE LEAF SITE\n')
        if ( outputFileName ):
            with open(outputFileName, "wb") as fp:   #Pickling
                pickle.dump(outputDictionary, fp)
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
            if (len(pd.date_range(startDate,endDate,freq='ME')) > 0 ):
                dateRange = pd.DataFrame(pd.date_range(startDate,endDate,freq='ME'),columns=['startDate'])
                dateRange['endDate'] = pd.concat([dateRange['startDate'].tail(-1),pd.DataFrame([endDatePlusOne])],ignore_index=True).values
            else:
                dateRange = pd.DataFrame( {'startDate':[startDate],'endDate':[endDatePlusOne]})

            # process one month at a time to prevent GEE memory limits
            siteCollection = ee.ImageCollection([])
            for index, Dates in dateRange.iterrows():

                monthlyCollection = getCollection(site,variableName,collectionOptions[imageCollectionName],networkOptions[variableName][imageCollectionName],maxCloudcover,bufferSpatialSize,inputScaleSize, \
                            Dates['startDate'],Dates['endDate'],outputScaleSize,subsamplingFraction)
                if monthlyCollection :
                    siteCollection = siteCollection.merge(monthlyCollection)
                
            result.append({'feature': ee.Dictionary(ee.Feature(sampleRecords.get(n)).toDictionary()).getInfo() , \
                        algorithm.__name__ : siteCollection })
        
        outputDictionary.update({input: result})
        print('\nDONE LEAF IMAGE\n')
    return outputDictionary
