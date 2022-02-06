
// ---------------------------
// NNet calibration functions: 
//---------------------------

//return image with single band named network id corresponding given 
var makeIndexLayer = function(image, legend, Network_Ind) {
    image = ee.Image(image);                          // partition image
    legend = ee.FeatureCollection(legend);            // legend to convert partition numbers to networks
    Network_Ind = ee.FeatureCollection(Network_Ind);  // legend to convert networks to networkIDs
    
    // get lists of valid partitions
    var legend_list = legend.toList(legend.size());
    var landcover = legend_list.map(function (feature) { return ee.Feature(feature).getNumber('Value')});

    // get corresponding networkIDs
    var networkIDs = legend_list.map(function (feature) { return ee.Feature(feature).get('SL2P Network')}) 
                                    .map(function (propertyValue) { return ee.Feature(ee.FeatureCollection(Network_Ind).first()) 
                                    .toDictionary().getNumber(propertyValue)});
    
    return image.remap(landcover, networkIDs, 0).rename('networkID');
};

//read coefficients of a network from csv EE asset
var getCoefs = function(netData, ind)  {
    return((ee.Feature(netData)).getNumber(ee.String('tabledata').cat(ee.Number(ind).int().format())));
};


// parse one row of CSV file for a network into a global variable
// assume a two hidden layer network with tansig functions but allow for variable nodes per layer
var makeNets = function(feature, M)  {
    
    feature = ee.List(feature);
    M = ee.Number(M);
    
    // get the requested network and initialize the created network
    var netData = ee.Feature(feature.get(M.subtract(1)));
    var net = {};
    
    // input slope
    var num = ee.Number(6);
    var start = num.add(1);
    var end = num.add(netData.getNumber(ee.String('tabledata').cat(num.format())));
    net["inpSlope"] = ee.List.sequence(start,end).map(function (ind) { return getCoefs(netData,ind)});
    
    // input offset
    num = end.add(1);
    start = num.add(1);
    end = num.add(netData.getNumber(ee.String('tabledata').cat(num.format())));
    net["inpOffset"] = ee.List.sequence(start,end).map(function (ind) { return getCoefs(netData,ind)});

    // hidden layer 1 weight
    num = end.add(1);
    start = num.add(1);
    end = num.add(netData.getNumber(ee.String('tabledata').cat(num.format())));
    net["h1wt"] = ee.List.sequence(start,end).map(function (ind) { return getCoefs(netData,ind)});

    // hidden layer 1 bias
    num = end.add(1);
    start = num.add(1);
    end = num.add(netData.getNumber(ee.String('tabledata').cat(num.format())));
    net["h1bi"] = ee.List.sequence(start,end).map(function (ind) { return getCoefs(netData,ind)});

    // hidden layer 2 weight
    num = end.add(1);
    start = num.add(1);
    end = num.add(netData.getNumber(ee.String('tabledata').cat(num.format())));
    net["h2wt"] = ee.List.sequence(start,end).map(function (ind) { return getCoefs(netData,ind)});
  
    // hidden layer 2 bias
    num = end.add(1);
    start = num.add(1);
    end = num.add(netData.getNumber(ee.String('tabledata').cat(num.format())));
    net["h2bi"] = ee.List.sequence(start,end).map(function (ind) { return getCoefs(netData,ind)});

    // output slope
    num = end.add(1);
    start = num.add(1);
    end = num.add(netData.getNumber(ee.String('tabledata').cat(num.format())));
    net["outSlope"] = ee.List.sequence(start,end).map(function (ind) { return getCoefs(netData,ind)});
  
    // output offset
    num = end.add(1);
    start = num.add(1);
    end = num.add(netData.getNumber(ee.String('tabledata').cat(num.format())));
    net["outBias"] = ee.List.sequence(start,end).map(function (ind) { return getCoefs(netData,ind)});
    
    return(ee.Dictionary(net));
};


// parse CSV file with list of networks for a selected variable (one network for each landclass partition)
var makeNetVars = function(asset, numNets, variableNum)  {
    
    asset = ee.FeatureCollection(asset);
    numNets = ee.Number(numNets);
    variableNum = ee.Number(variableNum);  

    // get selected network 
    var list_features = asset.flatten();
    var filtered_features = ee.FeatureCollection(asset.filter(ee.Filter.eq('tabledata3', variableNum))).toList(numNets);
    
    return ee.List.sequence(1,numNets).map(function (netNum) { return makeNets(filtered_features,netNum)});
};


// return dictionary with image masked so the networkID band equals the netIndex and the corresponding network
var selectNet = function(image, netList, inputNames, netIndex) {
    
    image = ee.Image(image);
    netList = ee.List(netList);
    inputNames = ee.List(inputNames);
    netIndex = ee.Number(netIndex).int();
    
    return ee.Dictionary()  
            .set("Image", ee.Image(image.updateMask(image.select('networkID').eq(netIndex)).select(inputNames))) 
            .set("Network", ee.List(netList.get(netIndex)));
};


// apply two-layer neural network within input and output scaling
var applyNet = function(outputName, netDict)  {
    outputName = ee.String(outputName);
    netDict = ee.Dictionary(netDict);
    
    // extract image and network
    var inp = ee.Image(netDict.get('Image'));
    var net = ee.Dictionary(netDict.get('Network'));
    
    // input scaling
    var l1inp2D = inp.multiply(ee.Image(net.toArray(ee.List(['inpSlope']),0).transpose()).arrayProject([0]) 
                        .arrayFlatten([inp.bandNames()])) 
                        .add(ee.Image(net.toArray(ee.List(['inpOffset']),0).transpose()) 
                        .arrayProject([0]).arrayFlatten([inp.bandNames()]));
    
    // hidden layers
    var l12D = ee.Image(net.toArray(ee.List(['h1wt']),0).reshape([ee.List(net.get('h1bi')).length(),ee.List(net.get('inpOffset')).length()])) 
              .matrixMultiply(l1inp2D.toArray().toArray(1)) 
              .add(ee.Image(net.toArray(ee.List(['h1bi']),0).transpose())) 
              .arrayProject([0]).arrayFlatten([['h1w1','h1w2','h1w3','h1w4','h1w5']]);
    
    // apply tansig 2/(1+exp(-2*n))-1
    var l2inp2D = ee.Image(2).divide(ee.Image(1).add((ee.Image(-2).multiply(l12D)).exp())).subtract(ee.Image(1));
    
    // purlin hidden layers
    var l22D = l2inp2D.multiply(ee.Image(net.toArray(ee.List(['h2wt']),0).transpose()) 
                                          .arrayProject([0]) 
                                          .arrayFlatten([['h2w1','h2w2','h2w3','h2w4','h2w5']])) 
                    .reduce('sum') 
                    .add(ee.Image(net.toArray(ee.List(['h2bi']),0))) 
                                          .arrayProject([0]) 
                                          .arrayFlatten([['h2bi']]);
    
    // output scaling 
    var outputBand = l22D.subtract(ee.Image(ee.Number(net.get('outBias')))).divide(ee.Image(ee.Number(net.get('outSlope')))) ;
    
    // return network output
    return (outputBand.rename(outputName));
};


// return image with single band named networkid corresponding given 
// input partition image remapped to networkIDs
// apply a set of shallow networks to an image based on a provided partition image band
var wrapperNNets = function(network, partition, netOptions, colOptions, suffixName, imageInput, outputName)  {

    // typecast function parameters
    network = ee.List(network);
    partition = ee.Image(partition);
    netOptions = netOptions;
    colOptions = colOptions;
    suffixName = suffixName;
    imageInput = ee.Image(imageInput);
    outputName = outputName;

    // parse partition  used to identify network to use
    var partition = partition.clip(imageInput.geometry()).select(['partition']);

    // determine networks based on collection
    var netList = ee.List(network.get(ee.Number(netOptions.get("variable")).subtract(1)));
    
    // parse land cover into network index and add to input image
    var imageInput = imageInput.addBands(makeIndexLayer(partition,colOptions.get("legend"),colOptions.get("Network_Ind")));

    // define list of input names
    return ee.ImageCollection(ee.List.sequence(0, netList.size().subtract(1)) 
                                                    .map(function (netIndex) { return selectNet(imageInput,netList,netOptions.get("inputBands"),netIndex)}) 
                                                    .map(function (netDict) { return applyNet(suffixName+outputName,netDict)})) 
                                                    .max().addBands(partition).addBands(imageInput.select('networkID'));
};




// ---------------------------
// Export functions:
//---------------------------

exports.makeIndexLayer = makeIndexLayer;
exports.getCoefs = getCoefs;
exports.makeNets = makeNets;
exports.makeNetVars = makeNetVars;
exports.selectNet = selectNet;
exports.applyNet = applyNet;
exports.wrapperNNets = wrapperNNets

