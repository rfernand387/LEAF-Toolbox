# Constructors for MCD43 LEAF Toolbox algorithms
# Richard Fernandes December, 2023

import ee
import toolsNets
import toolsUtils
import dictionariesMCD43
import eoImage

# --------------------
# Generic Functions: 
# --------------------
#simple algorithm class
class algorithm:

    def __init__(self, variableName,collectionName):
        self.cc = self.collectionConstructors()
        self.networkOptions= dictionariesMCD43.make_net_options()[variableName][collectionName]
        self.collectionOptions= dictionariesMCD43.make_collection_options(self.cc)[collectionName]
        self.tools = self.collectionOptions["tools"]
 
    #applies a network corresponding to an image 
    #the network corresponds to a polynomial where each coefficient is specified by a network band and each 
    #term is a non-linear function of the inputs specified by the network bandName (yes this means the band name is a long math function!)
    #the polynominal is further transformed by a network property "outputFunction" to allow for a nonlinear output
    #and weighted by a network "weight" property as there can be multiple network estimators that are later weighted
    #
    #the operations are scale dependent so make sure to reproject both image and network to the scale required in the networkOptions
    #before you call this function
    def __applyNetwork(self,image,network):
        image = ee.Image(image)
        network= ee.Image(network)
        return ee.ImageCollection(network.bandNames() \
                                  .map( lambda bandName: ee.Image(network.select(bandName).multiply(image.expression(ee.String(bandName))))).sum()\
                                  .map( lambda estimate: estimate.expression(network.get("outputFunction")) \
                                  .map( lambda estimate: network.get("weight").multiply(estimate))))


    def createInput(self,mapBounds,startDate,endDate,maxCloudcover):
        return  ee.ImageCollection(self.collectionOptions['name']) \
                        .filterBounds(mapBounds) \
                        .filterDate(startDate, endDate) \
                        .limit(5000) \
                        .map(lambda image: image.clip(mapBounds)) \
                        .map(lambda image: self.tools.MaskClear(image))  \
                        .map(lambda image: eoImage.attach_Date(image)) \
                        .map(lambda image: eoImage.attach_LonLat(image)) \
                        .map(lambda image: self.tools.addGeometry(image)) \

    def fit(self):
        return 

    def fitUncertainty(self):
        return

    # pre process input imagery into and flag invalid inputs
    def preprocessInput(self,input_collection):
        return input_collection.map(lambda image: self.tools.MaskLand(image)).map(lambda image: \
                        toolsUtils.scaleBands(self.networkOptions["inputBands"],self.networkOptions["inputScaling"],self.networkOptions["inputOffset"],image)) \
                                .map(lambda image: toolsUtils.invalidInput(self.collectionOptions["MCD43Domain"],self.networkOptions["inputBands"],image)) 

    #apply errors networks for the selected variable at the scale they were calibrated 
    #the network is simply the linear regression coefficients in separate bands
    def predict(self,name,image):
        
        image = ee.Image(image).reproject({"crs": image.projection(),"scale":self.networkOptions["scale"]})

        networks = ee.ImageCollection(self.collectionOptions['Collection_estimates']) \
                                .collectionEstimates.filter(ee.Filter.eq('variable',variableNumber)) \
                                .clip(image.geometry()) \
                                .map(lambda image: image.reproject({"crs": image.projection(),"scale":self.networkOptions["scale"]}))
                                
        
        variableNumber = self.networkOptions['variable']
        
        # apply each network to produce an estimate and return a weigted sum
        return networks.map(lambda network: self.applyNetwork(image,network)).sum().divide(networks.aggregate_sum("weights"))
                                        

    #apply errors networks for the selected variable at the scale they were calibrated 
    #the network is simply the linear regression coefficients
    def predictUncertainty(self,name,variable,image):
        image = ee.Image(image).reproject({"crs": image.projection(),"scale":self.networkOptions["scale"]})
        networks = ee.ImageCollection(self.collectionOptions['Collection_errorss']) \
                                .collectionEstimates.filter(ee.Filter.eq('variable',variableNumber)) \
                                .clip(image.geometry()) \
                                .map(lambda image: image.reproject({"crs": image.projection(),"scale":self.networkOptions["scale"]}))
        
        variableNumber = self.networkOptions['variable']
        
        # apply each network to produce an estimate and return a weigted sum
        return networks.map(lambda network: self.applyNetwork(image,network)).sum().divide(networks.aggregate_sum("weights"))

    class collectionConstructors():

        def __init__(self):
            self.Name = 'MCD43'       
        # --------------------
        # MCD43A3
        # --------------------

        def MCD43A3_createCollection_estimates(self):
            return ee.ImageCollection([ \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var1estimate1MCD43A3'), \
                            ee.Image('projects/ee-modis250/MCD43/var1estimate2MCD43A3') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var2estimate1MCD43A3'), \
                            ee.Image('projects/ee-modis250/MCD43/var2estimate2MCD43A3') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var3estimate1MCD43A3'), \
                            ee.Image('projects/ee-modis250/MCD43/var3estimate2MCD43A3') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var4estimate1MCD43A3'), \
                            ee.Image('projects/ee-modis250/MCD43/var4estimate2MCD43A3') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var5estimate1MCD43A3'), \
                            ee.Image('projects/ee-modis250/MCD43/var5estimate2MCD43A3') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var6estimate1MCD43A3'), \
                            ee.Image('projects/ee-modis250/MCD43/var6estimate2MCD43A3') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var7estimate1MCD43A3'), \
                            ee.Image('projects/ee-modis250/MCD43/var7estimate2MCD43A3') \
                            ]) \
                        ])

        def MCD43A3_createCollection_errors(self):
            return ee.ImageCollection([ \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var1errors1MCD43A3'), \
                            ee.Image('projects/ee-modis250/MCD43/var1errors2MCD43A3') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var2errors1MCD43A3'), \
                            ee.Image('projects/ee-modis250/MCD43/var2errors2MCD43A3') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var3errors1MCD43A3'), \
                            ee.Image('projects/ee-modis250/MCD43/var3errors2MCD43A3') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var4errors1MCD43A3'), \
                            ee.Image('projects/ee-modis250/MCD43/var4errors2MCD43A3') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var5errors1MCD43A3'), \
                            ee.Image('projects/ee-modis250/MCD43/var5errors2MCD43A3') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var6errors1MCD43A3'), \
                            ee.Image('projects/ee-modis250/MCD43/var6errors2MCD43A3') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var7errors1MCD43A3'), \
                            ee.Image('projects/ee-modis250/MCD43/var7errors2MCD43A3') \
                            ]) \
                        ])


        def MCD43A3_createCollection_domain(self):
            return ee.ImageCollection([ \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var1domain1MCD43A3'), \
                            ee.Image('projects/ee-modis250/MCD43/var1domain2MCD43A3') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var2domain1MCD43A3'), \
                            ee.Image('projects/ee-modis250/MCD43/var2domain2MCD43A3') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var3domain1MCD43A3'), \
                            ee.Image('projects/ee-modis250/MCD43/var3domain2MCD43A3') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var4domain1MCD43A3'), \
                            ee.Image('projects/ee-modis250/MCD43/var4domain2MCD43A3') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var5domain1MCD43A3'), \
                            ee.Image('projects/ee-modis250/MCD43/var5domain2MCD43A3') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var6domain1MCD43A3'), \
                            ee.Image('projects/ee-modis250/MCD43/var6domain2MCD43A3') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var7domain1MCD43A3'), \
                            ee.Image('projects/ee-modis250/MCD43/var7domain2MCD43A3') \
                            ]) \
                        ])

 

        def MCD43A3_createCollection_range(self):
            return ee.ImageCollection([ \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var1range1MCD43A3'), \
                            ee.Image('projects/ee-modis250/MCD43/var1range2MCD43A3') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var2range1MCD43A3'), \
                            ee.Image('projects/ee-modis250/MCD43/var2range2MCD43A3') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var3range1MCD43A3'), \
                            ee.Image('projects/ee-modis250/MCD43/var3range2MCD43A3') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var4range1MCD43A3'), \
                            ee.Image('projects/ee-modis250/MCD43/var4range2MCD43A3') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var5range1MCD43A3'), \
                            ee.Image('projects/ee-modis250/MCD43/var5range2MCD43A3') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var6range1MCD43A3'), \
                            ee.Image('projects/ee-modis250/MCD43/var6range2MCD43A3') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var7range1MCD43A3'), \
                            ee.Image('projects/ee-modis250/MCD43/var7range2MCD43A3') \
                            ]) \
                        ])
        # --------------------
        # MCD43A4
        # --------------------

        def MCD43A4_createCollection_estimates(self):
            return ee.ImageCollection([ \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var1estimate1MCD43A4'), \
                            ee.Image('projects/ee-modis250/MCD43/var1estimate2MCD43A4') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var2estimate1MCD43A4'), \
                            ee.Image('projects/ee-modis250/MCD43/var2estimate2MCD43A4') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var3estimate1MCD43A4'), \
                            ee.Image('projects/ee-modis250/MCD43/var3estimate2MCD43A4') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var4estimate1MCD43A4'), \
                            ee.Image('projects/ee-modis250/MCD43/var4estimate2MCD43A4') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var5estimate1MCD43A4'), \
                            ee.Image('projects/ee-modis250/MCD43/var5estimate2MCD43A4') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var6estimate1MCD43A4'), \
                            ee.Image('projects/ee-modis250/MCD43/var6estimate2MCD43A4') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var7estimate1MCD43A4'), \
                            ee.Image('projects/ee-modis250/MCD43/var7estimate2MCD43A4') \
                            ]) \
                        ])

        def MCD43A4_createCollection_errors(self):
            return ee.ImageCollection([ \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var1errors1MCD43A4'), \
                            ee.Image('projects/ee-modis250/MCD43/var1errors2MCD43A4') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var2errors1MCD43A4'), \
                            ee.Image('projects/ee-modis250/MCD43/var2errors2MCD43A4') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var3errors1MCD43A4'), \
                            ee.Image('projects/ee-modis250/MCD43/var3errors2MCD43A4') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var4errors1MCD43A4'), \
                            ee.Image('projects/ee-modis250/MCD43/var4errors2MCD43A4') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var5errors1MCD43A4'), \
                            ee.Image('projects/ee-modis250/MCD43/var5errors2MCD43A4') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var6errors1MCD43A4'), \
                            ee.Image('projects/ee-modis250/MCD43/var6errors2MCD43A4') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var7errors1MCD43A4'), \
                            ee.Image('projects/ee-modis250/MCD43/var7errors2MCD43A4') \
                            ]) \
                        ])


        def MCD43A4_createCollection_domain(self):
            return ee.ImageCollection([ \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var1domain1MCD43A4'), \
                            ee.Image('projects/ee-modis250/MCD43/var1domain2MCD43A4') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var2domain1MCD43A4'), \
                            ee.Image('projects/ee-modis250/MCD43/var2domain2MCD43A4') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var3domain1MCD43A4'), \
                            ee.Image('projects/ee-modis250/MCD43/var3domain2MCD43A4') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var4domain1MCD43A4'), \
                            ee.Image('projects/ee-modis250/MCD43/var4domain2MCD43A4') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var5domain1MCD43A4'), \
                            ee.Image('projects/ee-modis250/MCD43/var5domain2MCD43A4') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var6domain1MCD43A4'), \
                            ee.Image('projects/ee-modis250/MCD43/var6domain2MCD43A4') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var7domain1MCD43A4'), \
                            ee.Image('projects/ee-modis250/MCD43/var7domain2MCD43A4') \
                            ]) \
                        ])

 

        def MCD43A4_createCollection_range(self):
            return ee.ImageCollection([ \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var1range1MCD43A4'), \
                            ee.Image('projects/ee-modis250/MCD43/var1range2MCD43A4') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var2range1MCD43A4'), \
                            ee.Image('projects/ee-modis250/MCD43/var2range2MCD43A4') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var3range1MCD43A4'), \
                            ee.Image('projects/ee-modis250/MCD43/var3range2MCD43A4') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var4range1MCD43A4'), \
                            ee.Image('projects/ee-modis250/MCD43/var4range2MCD43A4') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var5range1MCD43A4'), \
                            ee.Image('projects/ee-modis250/MCD43/var5range2MCD43A4') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var6range1MCD43A4'), \
                            ee.Image('projects/ee-modis250/MCD43/var6range2MCD43A4') \
                            ]), \
                        ee.ImageCollection([ \
                            ee.Image('projects/ee-modis250/MCD43/var7range1MCD43A4'), \
                            ee.Image('projects/ee-modis250/MCD43/var7range2MCD43A4') \
                            ]) \
                        ])