import ee  

#land only
def MaskLand(image):
  image = ee.Image(image)
  
  qa = ee.ImageCollection("MODIS/061/MCD43A2").filter(ee.Filter.eq("system:id",image.get("system:id")))  
  mask = qa.select(BRDF_Albedo_LandWaterType).eq(1)

  return image.updateMask(mask)
  
#clear sky snow free ,and
def MaskClear(image):
  image = ee.Image(image)
  
  qa = ee.ImageCollection("MODIS/061/MCD43A2").filter(ee.Filter.eq("system:id",image.get("system:id")))
  mask = qa.select("Snow_BRDF_Albedo").eq(1)
  
  return image.updateMask(mask)


# add MODIS geomtery bands cosine
def addGeometry(image):
  
  szaBand = ee.ImageCollection("MODIS/061/MCD43A2").filter(ee.Filter.eq("system:id",image.get("system:id"))).select("BRDF_Albedo_LocalSolarNoon")

  return image.addBands(ee.Image.constant(1).rename['cosVZA']) \
              .addBands(szaBand.multiply(3.1415).divide(180).cos().multiply(10000).toUint16().rename['cosSZA']) \
              .addBands(ee.Image.constant(1).rename['cosRAA']) 


