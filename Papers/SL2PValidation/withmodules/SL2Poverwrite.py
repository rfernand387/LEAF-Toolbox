# SL2P
#
# Simplified Level 2 Prototype Processor
# 
# Applies the Simplified Level 2 Prototype Processor (https:#step.esa.int/docs/extra/ATBD_S2ToolBox_L2B_V1.1.pdf). ) 
#to satellite image collections to  produce Level 2b products of vegetation biophysical variables.  
#
# Usage:
#
# 
# Arguments:
# collection (FeatureCollection):
# The input collection. One of:
#
# "COPERNICUS_S2_SR"
# "LANDSAT_LC08_C02_T1_L2"
#
# outputName (String)
# The name of the output biophysical variable.  One of:
#
# 'Albedo' : surface albedo
# 'fAPAR' - fraction of absorbed photosynthetically active radiation
# 'FCOVER'- fraction of canopy cover
# 'LAI' - leaf area index
# 'CWC' - canopy water content
# 'CCC' - canopy chloropyll content
# DASF' - directional area scattering factor
##
# Returns: ImageCollection
#
# Collection of images with one:one correspondence to input images.
# Each image has four bands as specified in https:#github.com/rfernand387/LEAF-Toolbox/wiki/Export-Outputs
# estimate{outputName}, quality{outputName}, error{outputName}, qualityError{outputName}
#
# Usage: 
#
# SL2P = require('users/richardfernandes/SL2P:SL2P')                     # Specify collection and algorithms
# output_collection = ee.ImageCollection(SL2P.applySL2P(input_collection,'LAI')) # will process ALL input scenes
#
# The input collection must be augmented with aquisition Geometry bands.
# To see how this is done check out users/richardfernandes/SL2P/example-SL2P
#
# Richard Fernandes, Canada Centre for Remote Sensing, 2022, DOI 10.5281/zenodo.4321297.
# Distributed under  https:#open.canada.ca/en/open-government-licence-canada
#
# Import Modules
import imageBands as ib
import wrapperNets as wn
import dictionariesSL2P 
import ee as ee

def applySL2P(inputCollection,outputName):

  inputCollection = ee.ImageCollection(inputCollection)

  # bounds for land cover map
  mapBounds = inputCollection.map(lambda image:  image.unmask()).union().geometry()



  # Identify Collection and make dictionary for parameters
  collectionName = inputCollection.get('system:id')
  collectionOptions = ee.Dictionary(ee.Dictionary(dictionariesSL2P.make_collection_options()).get(collectionName))
  netOptions = ee.Dictionary(ee.Dictionary(ee.Dictionary(dictionariesSL2P.make_net_options()).get(outputName)).get(collectionName))

  # Parse prediction networks
  numNets = ee.Number(ee.Feature(ee.FeatureCollection((collectionOptions.get("Network_Ind"))).first()).propertyNames().remove('Feature Index').remove('system:index').remove('lon').size())
  SL2P = ee.List.sequence(1,ee.Number(collectionOptions.get("numVariables")),1).map(lambda netNum: wn.makeNetVars(collectionOptions.get("Collection_SL2P"),numNets,netNum))
  errorsSL2P = ee.List.sequence(1,ee.Number(collectionOptions.get("numVariables")),1).map(lambda netNum:  wn.makeNetVars(collectionOptions.get("Collection_SL2Perrors"),numNets,netNum))

  # Get partition used to select network
  partition = ee.ImageCollection(collectionOptions.get("partition")).filterBounds(mapBounds).max().clip(mapBounds).rename('partition')

  # Pre process input imagery and flag invalid inputs
  scaled_inputCollection = inputCollection.map(lambda image:  ib.scaleBands(netOptions.get("inputBands"),netOptions.get("inputScaling"),image)) \
                                            .map(lambda image:  ib.invalidInput(ee.FeatureCollection(collectionOptions.get("sl2pDomain")),netOptions.get("inputBands"),image))

  # Apply networks to produce mapped parameters
  return scaled_inputCollection.map(lambda image:  image.select('B11').multiply(0).add(wn.wrapperNNets(SL2P, partition, netOptions, collectionOptions, "estimate", image, outputName).select('estimate'+outputName)) \
                                                                      .rename('estimate'+outputName) \
                                                                      .addBands(image.select('B11').multiply(0).add(wn.wrapperNNets(SL2P, partition, netOptions, collectionOptions, "error", image, outputName).select('error'+outputName)) \
                                                                      .rename('error'+outputName)) \
                                                                      .set('system:time_start',image.get('system:time_start')) \
                                                                      .set('system:time_end',image.get('system:time_end')) \
                                                                      .addBands(image.select('QC','LandCover'))) 
