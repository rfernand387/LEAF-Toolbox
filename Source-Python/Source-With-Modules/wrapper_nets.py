import ee


# ---------------------------
# NNet calibration functions:
# ---------------------------

# return image with single band named network id corresponding given 
def makeIndexLayer(image, legend, Network_Ind):
    image = ee.Image(image)                          # partition image
    legend = ee.FeatureCollection(legend)            # legend to convert partition numbers to networks
    Network_Ind = ee.FeatureCollection(Network_Ind)  # legend to convert networks to networkIDs
    
    # get lists of valid partitions
    legend_list = legend.toList(legend.size())
    landcover = legend_list.map(lambda feature: ee.Feature(feature).getNumber('Value'))

    # get corresponding networkIDs
    networkIDs = legend_list.map(lambda feature: ee.Feature(feature).get('SL2P Network')) \
                                    .map(lambda propertyValue: ee.Feature(ee.FeatureCollection(Network_Ind).first()) \
                                    .toDictionary().getNumber(propertyValue))
    
    return image.remap(landcover, networkIDs, 0).rename('networkID')


# read coefficients of a network from csv EE asset
def getCoefs(netData, ind):
    return((ee.Feature(netData)).getNumber(ee.String('tabledata').cat(ee.Number(ind).int().format())))


# parse one row of CSV file for a network into a global variable
# assume a two hidden layer network with tansig functions but allow for variable nodes per layer
def makeNets(feature, M):
    
    feature = ee.List(feature)
    M = ee.Number(M)
    
    # get the requested network and initialize the created network
    netData = ee.Feature(feature.get(M.subtract(1)))
    net = {}
    
    # input slope
    num = ee.Number(6)
    start = num.add(1)
    end = num.add(netData.getNumber(ee.String('tabledata').cat(num.format())))
    net["inpSlope"] = ee.List.sequence(start,end).map(lambda ind: getCoefs(netData,ind))
    
    # input offset
    num = end.add(1)
    start = num.add(1)
    end = num.add(netData.getNumber(ee.String('tabledata').cat(num.format())))
    net["inpOffset"] = ee.List.sequence(start,end).map(lambda ind: getCoefs(netData,ind))

    # hidden layer 1 weight
    num = end.add(1)
    start = num.add(1)
    end = num.add(netData.getNumber(ee.String('tabledata').cat(num.format())))
    net["h1wt"] = ee.List.sequence(start,end).map(lambda ind: getCoefs(netData,ind))

    # hidden layer 1 bias
    num = end.add(1)
    start = num.add(1)
    end = num.add(netData.getNumber(ee.String('tabledata').cat(num.format())))
    net["h1bi"] = ee.List.sequence(start,end).map(lambda ind: getCoefs(netData,ind))

    # hidden layer 2 weight
    num = end.add(1)
    start = num.add(1)
    end = num.add(netData.getNumber(ee.String('tabledata').cat(num.format())))
    net["h2wt"] = ee.List.sequence(start,end).map(lambda ind: getCoefs(netData,ind))
  
    # hidden layer 2 bias
    num = end.add(1)
    start = num.add(1)
    end = num.add(netData.getNumber(ee.String('tabledata').cat(num.format())))
    net["h2bi"] = ee.List.sequence(start,end).map(lambda ind: getCoefs(netData,ind))

    # output slope
    num = end.add(1)
    start = num.add(1)
    end = num.add(netData.getNumber(ee.String('tabledata').cat(num.format())))
    net["outSlope"] = ee.List.sequence(start,end).map(lambda ind: getCoefs(netData,ind))
  
    # output offset
    num = end.add(1)
    start = num.add(1)
    end = num.add(netData.getNumber(ee.String('tabledata').cat(num.format())))
    net["outBias"] = ee.List.sequence(start,end).map(lambda ind: getCoefs(netData,ind))
    
    return(ee.Dictionary(net))


# parse CSV file with list of networks for a selected variable (one network for each landclass partition)
def makeNetVars(asset, numNets, variableNum):
    
    asset = ee.FeatureCollection(asset)
    numNets = ee.Number(numNets)
    variableNum = ee.Number(variableNum)  

    # get selected network 
    list_features = asset.flatten()
    filtered_features = ee.FeatureCollection(asset.filter(ee.Filter.eq('tabledata3', variableNum))).toList(numNets)
    
    return ee.List.sequence(1,numNets).map(lambda netNum: makeNets(filtered_features,netNum))


# return dictionary with image masked so the networkID band equals the netIndex and the corresponding network
def selectNet(image, netList, inputNames, netIndex):
    
    image = ee.Image(image)
    netList = ee.List(netList)
    inputNames = ee.List(inputNames)
    netIndex = ee.Number(netIndex).int()
    
    return ee.Dictionary()  \
            .set("Image", ee.Image(image.updateMask(image.select('networkID').eq(netIndex)).select(inputNames))) \
            .set("Network", ee.List(netList.get(netIndex)))


# apply two-layer neural network within input and output scaling
def applyNet(outputName, netDict):
    outputName = ee.String(outputName)
    netDict = ee.Dictionary(netDict)
    inp = ee.Image(netDict.get('Image'))
    net = ee.Dictionary(netDict.get('Network'))
    
    # input scaling
    l1inp2D = inp.multiply(ee.Image(net.toArray(ee.List(['inpSlope']),0).transpose()).arrayProject([0]) \
                        .arrayFlatten([inp.bandNames()])) \
                        .add(ee.Image(net.toArray(ee.List(['inpOffset']),0).transpose()) \
                        .arrayProject([0]).arrayFlatten([inp.bandNames()]))
    
    # hidden layers
    l12D = ee.Image(net.toArray(ee.List(['h1wt']),0).reshape([ee.List(net.get('h1bi')).length(),ee.List(net.get('inpOffset')).length()])) \
              .matrixMultiply(l1inp2D.toArray().toArray(1)) \
              .add(ee.Image(net.toArray(ee.List(['h1bi']),0).transpose())) \
              .arrayProject([0]).arrayFlatten([['h1w1','h1w2','h1w3','h1w4','h1w5']])
    
    # apply tansig 2/(1+exp(-2*n))-1
    l2inp2D = ee.Image(2).divide(ee.Image(1).add((ee.Image(-2).multiply(l12D)).exp())).subtract(ee.Image(1))
    
    # purlin hidden layers
    l22D = l2inp2D.multiply(ee.Image(net.toArray(ee.List(['h2wt']),0).transpose()) \
                                          .arrayProject([0]) \
                                          .arrayFlatten([['h2w1','h2w2','h2w3','h2w4','h2w5']])) \
                    .reduce('sum') \
                    .add(ee.Image(net.toArray(ee.List(['h2bi']),0))) \
                                          .arrayProject([0]) \
                                          .arrayFlatten([['h2bi']])
    
    # output scaling 
    outputBand = l22D.subtract(ee.Image(ee.Number(net.get('outBias')))).divide(ee.Image(ee.Number(net.get('outSlope')))) 
    
    # return network output
    return (outputBand.rename(outputName))


# return image with single band named networkid corresponding given 
# input partition image remapped to networkIDs
# apply a set of shallow networks to an image based on a provided partition image band
def wrapperNNets(network, partition, netOptions, colOptions, suffixName, imageInput, outputName):

    # typecast function parameters
    network = ee.List(network)
    partition = ee.Image(partition)
    netOptions = netOptions
    colOptions = colOptions
    suffixName = suffixName
    imageInput = ee.Image(imageInput)
    outputName = outputName

    # parse partition  used to identify network to use
    partition = partition.clip(imageInput.geometry()).select(['partition'])

    # determine networks based on collection
    netList = ee.List(network.get(ee.Number(netOptions.get("variable")).subtract(1)))
    
    # parse land cover into network index and add to input image
    imageInput = imageInput.addBands(makeIndexLayer(partition,colOptions["legend"],colOptions["Network_Ind"]))

    # define list of input names
    return ee.ImageCollection(ee.List.sequence(0, netList.size().subtract(1)) \
                                                    .map(lambda netIndex: selectNet(imageInput,netList,netOptions["inputBands"],netIndex)) \
                                                    .map(lambda netDict: applyNet(suffixName+outputName,netDict))) \
                                                    .max().addBands(partition).addBands(imageInput.select('networkID'))
