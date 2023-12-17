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
        self.collectionOptions= dictionariesMCD43.make_collection_options(cc)[collectionName]
        self.tools = self.collectionOptions["tools"]

    def __clipPartition(self,image):
        image = ee.Image(image)
        return (self.partition).filterBounds(image.geometry()).mosaic().clip(image.geometry()).rename('partition')
 
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

    #apply first eestimates network to first input feature for the selected variable
    #the network is simply the linear regression coefficients
    def predict(self,name,variable,image):
        image = ee.Image(image)
        collectionEstimates = ee.ImageCollection(self.collectionOptions['Collection_estimates'])
        variableNumber = self.networkOptions['variable']
        
        # dot product of network coefficients and input feature
        image = collectionEstimates.filter(ee.Filter.eq('variable',variableNumber)).first().multiply(image.first().first()).sum()
        return image.rename(name)

    #apply first errors network to first input feature for the selected variable
    #the network is simply the linear regression coefficients
    def predictUncertainty(self,name,variable,image):
        image = ee.Image(image)
        network = ee.ImageCollection(self.collectionOptions['Collection_errors'])
        variableNumber = self.networkOptions['variable']
        
        # dot product of network coefficients and input feature
        image = network.filter(ee.Filter.eq('variable',variableNumber)).first().multiply(image).sum()
        return image.rename(name)

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