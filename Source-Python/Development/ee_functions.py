import ee
import folium ; from folium import plugins
import time
import numpy as np
import pandas as pd


# --------------------------------------------------------------------
# Earth Engine functions used to verify, display, and export products:
# --------------------------------------------------------------------

# verify status of tasks
def check_ee_tasks(ee_tasks: list=[]):
    for task in ee_tasks:
        taskStatus = ee.data.getTaskStatus(task.id)[0]
        print(taskStatus["description"] + ": " + taskStatus["state"])
    return


# wait loop for Earth Engine tasks to complete
# polls for the task status the specificed number of seconds until it is no longer active
def task_wait_loop(ee_task, wait_interval):
    print(ee.data.getTaskStatus(ee_task.id)[0]["description"] + ":", end = " ")
    prev_task_status = ee.data.getTaskStatus(ee_task.id)[0]["state"]
    print(prev_task_status, end = " ")
    while ee_task.active():
        task_status = ee.data.getTaskStatus(ee_task.id)[0]["state"]
        if(task_status != prev_task_status):
            print(task_status, end = " ")
        prev_task_status = task_status
        time.sleep(wait_interval)
    print(ee.data.getTaskStatus(ee_task.id)[0]["state"])
    return


# ----------------
# Image functions:
# ----------------

# create a folium map object
def displayImage(image, minVal, maxVal, mapBounds):
    center_long = mapBounds.getInfo()['coordinates'][0][0][0]
    center_lat = mapBounds.getInfo()['coordinates'][0][0][1]
    my_map = folium.Map(location=[center_lat, center_long], zoom_start=8, height=700)
    
    vis_params = {
      'min': minVal,
      'max': maxVal}
    
    my_map.add_ee_layer(image, vis_params, 'Image')
        
    # add a layer control panel to the map
    my_map.add_child(folium.LayerControl())

    # add fullscreen button
    plugins.Fullscreen().add_to(my_map)

    # display the map.
    display(my_map)
    return


# define a method for displaying Earth Engine image tiles on a folium map
def add_ee_layer(self, ee_object, vis_params, name):
    try:    
        # display ee.Image()
        if isinstance(ee_object, ee.image.Image):    
            map_id_dict = ee.Image(ee_object).getMapId(vis_params)
            folium.raster_layers.TileLayer(
            tiles = map_id_dict['tile_fetcher'].url_format,
            attr = 'Google Earth Engine',
            name = name,
            overlay = True,
            control = True
            ).add_to(self)
        # display ee.ImageCollection()
        elif isinstance(ee_object, ee.imagecollection.ImageCollection):    
            ee_object_new = ee_object.mosaic()
            map_id_dict = ee.Image(ee_object_new).getMapId(vis_params)
            folium.raster_layers.TileLayer(
            tiles = map_id_dict['tile_fetcher'].url_format,
            attr = 'Google Earth Engine',
            name = name,
            overlay = True,
            control = True
            ).add_to(self)
        # display ee.Geometry()
        elif isinstance(ee_object, ee.geometry.Geometry):    
            folium.GeoJson(
            data = ee_object.getInfo(),
            name = name,
            overlay = True,
            control = True
        ).add_to(self)
        # display ee.FeatureCollection()
        elif isinstance(ee_object, ee.featurecollection.FeatureCollection):  
            ee_object_new = ee.Image().paint(ee_object, 0, 2)
            map_id_dict = ee.Image(ee_object_new).getMapId(vis_params)
            folium.raster_layers.TileLayer(
            tiles = map_id_dict['tile_fetcher'].url_format,
            attr = 'Google Earth Engine',
            name = name,
            overlay = True,
            control = True
        ).add_to(self)
    
    except:
        print("Could not display {}".format(name))
    
# add EE drawing method to folium
folium.Map.add_ee_layer = add_ee_layer



# -----------------
# Export functions:
# -----------------

def export_jpeg(fig_name, outputName):
    fig = fig_name
    outputName = outputName
    
    fig.savefig('Estimated_'+outputName+'.jpeg', bbox_inches = 'tight')
    return


default_asset_location = "users/kateharvey"
def export_collection_to_gee(collection, num_images: int=0, image_names: list=[], asset_folder: str=default_asset_location, scale: float=20, max_pixels: int=1e8, data_type: str="float"):
    collection = ee.ImageCollection(collection)
    image_list = collection.toList(num_images)
    task_list = []
    
    for i in range(num_images):
        image = ee.Image(image_list.get(i))
        name = image_names[i]
        typed_images = {"double": image.toDouble(), "float": image.toFloat(), "byte": image.toByte(), "int": image.toInt()}
        export_task = ee.batch.Export.image.toAsset(image = typed_images[data_type],
                                                      description = name,
                                                      assetId = asset_folder+"/"+name,
                                                      region = image.geometry(),
                                                      scale = scale,
                                                      maxPixels = max_pixels)
        export_task.start()
        task_list.append(export_task)
    
    return task_list


def export_collection_to_drive(collection, num_images: int=0, image_names: list=[], gdrive_folder: str="", scale: float=20, max_pixels: int=1e8,
                               data_type: str="float"):
    collection = ee.ImageCollection(collection)
    image_list = collection.toList(num_images)
    task_list = []

    for i in range(num_images):
        image = ee.Image(image_list.get(i))
        name = image_names[i]
        print(name)
        typed_images = {"double": image.toDouble(), "float": image.toFloat(), "byte": image.toByte(), "int": image.toInt()}
        export_task = ee.batch.Export.image.toDrive(image = typed_images[data_type],
                                                    description = name,
                                                    folder = gdrive_folder,
                                                    fileNamePrefix = name,
                                                    region = image.geometry(),
                                                    scale = scale,
                                                    maxPixels = max_pixels)
        export_task.start()
        task_list.append(export_task)
    
    return task_list