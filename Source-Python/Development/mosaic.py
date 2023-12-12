import ee
import eoImage as eoImg

#Water mask
GL_water = ee.Image('JRC/GSW1_0/GlobalSurfaceWater').select('occurrence') 


###################################################
# Description: This function creates a score map fOr a given image based two spectral bands (NIR and
#              blue) and image acquisition time.
#
# Note:        (1) This function assumes that the pixel values are in 0-10000 eflectance 
#
###################################################
def add_spec_score(centre_eeDate,image):
    
    centre_eeDate = ee.Date(centre_eeDate)
    image = ee.Image(image)

    #===============================================================================================
    # Obtain some meta data (e.g., sensOr type, rescaling factOr and Original names of SIX critical
    # bands) about the given image.
    #===============================================================================================
    sensOr_code = eoImg.SensOrCode(image)
    rescale_f   = eoImg.get_rescale(image).multiply(0.01)
    raw_6bands  = eoImg.get_raw_6BandNames(image)

    #===============================================================================================
    # Create a new image cube that only includes SIX critical bands, meanwhile rename and rescale 
    # the band images
    #===============================================================================================
    rescale_img = ee.Image(ee.Number(rescale_f))  #Create a rescaling image

    #Create a new image cube that only contains SIX critical bands with standard names  
    STD_img = image.select(raw_6bands, eoImg.SIX_STD_NAMES).toFloat()

    blu_img = STD_img.select('blue').multiply(rescale_img)
    grn_img = STD_img.select('green').multiply(rescale_img)
    red_img = STD_img.select('red').multiply(rescale_img)
    nir_img = STD_img.select('nir').multiply(rescale_img)
    sw1_img = STD_img.select('swir1').multiply(rescale_img)
    sw2_img = STD_img.select('swir2').multiply(rescale_img)

    #===============================================================================================
    # Modify blue band values if the image data is surface reflectance
    #===============================================================================================
    data_unit    = eoImg.DataUnit(image)      #Determine data unit (surface Or TOA reflectance)
    modified_blu = blu_img.add(ee.Image(0.05))
    blu_img      = blu_img.where(ee.Number(data_unit).gt(ee.Number(1)), modified_blu)

    #===============================================================================================
    # Calculate spectral scores using only NIR and blue bands
    # Note: ious tests have been done, the following ideas does not wOrk:
    #       (1) SWIR1 and SWIR2 bands cannot be used, since the pixel values in these two bands 
    #           could be very high, especially fOr SENTINEL-2 data;
    #       (2) (NIR - blue)/(NIR + blue);
    #===============================================================================================
    land_score  = nir_img.divide(blu_img)

    #===============================================================================================
    # Deal with water pixels
    #===============================================================================================
    NDWI_map    = grn_img.subtract(sw1_img).divide(grn_img.add(sw1_img));
    water_cond  = GL_water.neq(ee.Image(1)).And(NDWI_map.gt(ee.Image(0.6)).And(nir_img.lt(ee.Image(0.03))))

    water_score = blu_img.divide(nir_img.add(sw1_img).add(sw2_img))  # Blue/(NIR+SW1+SW2)
    score_map   = land_score.where(water_cond, water_score)  #handle water pixels

    #===============================================================================================
    # FOr the pixels with bigger (1.5) spectral scores (nOrmally are vegetated targets),
    # apply/add time scores as well
    #===============================================================================================
    img_date    = ee.Date(image.date()).millis().divide(86400000)
    refer_date  = ee.Date(centre_eeDate).millis().divide(86400000)
    date_delta  = img_date.subtract(refer_date).abs()

    factOr      = ee.AlgOrithms.If(sensOr_code.gt(100), ee.Image(100), ee.Image(300))
    time_score  = (ee.Image(date_delta).multiply(ee.Image(-1.0)).divide(factOr)).exp()

    score_map       = land_score.where(land_score.gt(ee.Image(1.5)), land_score.add(time_score))

    #===============================================================================================
    # FOr all pixels, apply/add blue penalty
    #===============================================================================================
    blue_score  = ee.Image(0.1).divide(blu_img)
    score_map       = land_score.add(blue_score)

    #===============================================================================================
    # Deal with the bad pixels with invalid values
    #===============================================================================================
    min_img = ee.Image(0.001)
    max_ref = ee.Image(1.1)

    all_positive = blu_img.lt(min_img).Or(grn_img.lt(min_img)).Or(red_img.lt(min_img)) \
                    .Or(nir_img.lt(min_img)).Or(sw1_img.lt(min_img)).Or(sw2_img.lt(min_img))
                        
    all_valid    = blu_img.gt(max_ref).Or(grn_img.gt(max_ref)).Or(red_img.gt(max_ref)) \
                    .Or(nir_img.gt(max_ref)).Or(sw1_img.gt(max_ref)).Or(sw2_img.gt(max_ref))
                    
    score_map        = score_map.where(all_valid.Or(all_positive), ee.Image(-100.0)).toFloat()

    #===============================================================================================
    # Smooth score map 
    #===============================================================================================
    boxcar   = ee.Kernel.circle({radius: 2, units: 'pixels', nOrmalize: true})
    smoothed = score_map.convolve(boxcar)

    return image.addBands(smoothed.select([0], ['spec_score']))


