import math
import geojson
import os
from shutil import copyfile

import numpy as np
from pyproj import Transformer

MIN_ZOOM = 6
MAX_ZOOM = 15
BORDER_FILENAME = "border_test.geojson"
LIDAR_INDEX_FILENAME = "lidar_index.geojson"
LIDAR_INDEX_LAMBERT_93_FILENAME = "lidar_index_lambert_93.geojson"
TILES_PIXEL_SIZE = 1183

def make_max_zoom_index():
    try:
        border = load_geojson_file(BORDER_FILENAME)
    except FileNotFoundError:
        print("Border geojson file does'nt exist.")
    except:
        print("An error occured.")
    try:
        lidar_index = load_geojson_file("index_files\\" + LIDAR_INDEX_FILENAME)
    except FileNotFoundError:
        print("Lidar index geojson file does'nt exist.")
    except:
        print("An error occured.")
    border_geometry = border.features[0].geometry.coordinates[0][0]
    (min_lon, max_lon, min_lat, max_lat) = polygon_extrema(border_geometry)
    (min_x, max_y) = wgs84_to_tile_num(min_lat, min_lon, MAX_ZOOM)
    (max_x, min_y) = wgs84_to_tile_num(max_lat, max_lon, MAX_ZOOM)

    features = []
    range_x = range(min_x, (max_x + 1))
    range_y = range(min_y, (max_y + 1))
    count = 0
    for x in range_x:
        for y in range_y:
            polygon = geojson.Polygon([[
                tile_num_to_wgs84(x, y, MAX_ZOOM),
                tile_num_to_wgs84(x + 1, y, MAX_ZOOM),
                tile_num_to_wgs84(x + 1, y + 1, MAX_ZOOM),
                tile_num_to_wgs84(x, y + 1, MAX_ZOOM),
                tile_num_to_wgs84(x, y, MAX_ZOOM)
            ]]
            )
            # Fill png list
            png_list= []
            p = polygon.coordinates[0]
            p_min_lon = p[0][0]
            p_max_lon = p[1][0]
            p_min_lat = p[2][1]
            p_max_lat = p[0][1]
            # For every lidar tile, check if an edge of the square is in the slippy map tile
            for lidar in lidar_index.features:
                lidar_geometry = lidar.geometry.coordinates[0][0]
                # Check every edges
                for edge in lidar_geometry:
                    # Check if edge is inside the slippy map tile
                    if edge[0] > p_min_lon and edge[0] < \
                        p_max_lon and edge[1] > p_min_lat and edge[1] < \
                        p_max_lat:
                        png_list.append(lidar['properties']['TILES_500m'])
                        break
            png_list.sort()
            # create feature
            properties = {
                'png_list': png_list,
                'parent_tiles': [],
                'x_tile': x,
                'y_tile': y
            }
            feature = geojson.Feature(geometry=polygon, properties=properties)
            if png_list:
                features.append(feature)
            # add feature to feature collection
            # add feature collection to geojson
    feature_collection = geojson.FeatureCollection(features)
    # Fill png_list
    # Delete feature when png_list is empty
    # write feature into file
    output_file_name = 'index_files\\tile_index_' + str(MAX_ZOOM) + '.geojson'
    with open(output_file_name, 'w') as f:
        geojson.dump(feature_collection, f)

def make_zoom_index(zoom_number):
    pass

def make_max_zoom_tiles():
    # Load max zoom tile index
    try:
        tile_index_max_zoom = load_geojson_file('index_files\\tile_index_' + str(MAX_ZOOM) + '.geojson')
    except FileNotFoundError:
        print("Tile index geojson file does'nt exist for max zoom. Run make_max_zoom_index() to create it")
    except:
        print("An error occured.")
    # Load lidar index
    try:
        lidar_index = load_geojson_file("index_files\\" + LIDAR_INDEX_FILENAME)
    except FileNotFoundError:
        print("Lidar index geojson file does'nt exist.")
    except:
        print("An error occured.")
    # Load lidar index in Lambert 93 projection
    try:
        lidar_index = load_geojson_file("index_files\\" + LIDAR_INDEX_LAMBERT_93_FILENAME)
    except FileNotFoundError:
        print("Lidar index geojson file does'nt exist.")
    except:
        print("An error occured.")
    
    # Filter tile_index_max_zoom given the png files that are present in the \in folder
    filter_tile_index(tile_index_max_zoom)
    
    if not os.path.exists("tiles"):
        os.mkdir("tiles")
    
    if not os.path.exists("tiles\\" + str(MAX_ZOOM)):
        os.mkdir("tiles\\" + str(MAX_ZOOM))
    
    if not os.path.exists("temp"):
        os.mkdir("temp")

    for tile in tile_index_max_zoom.features:
        png_list = tile['properties']['png_list']
        # Copy every png of png_list in temp folder
        for png in png_list:
            png_file = "11555_Grand-Geneve_SemisLidar_" + int_to_str_add_zeros(int(png)) + "_quarter.laz_depr.png"
            pgw_file = "11555_Grand-Geneve_SemisLidar_" + int_to_str_add_zeros(int(png)) + "_quarter.laz_depr.pgw"
            try:
                copyfile(("in\\" + png_file), ("temp\\" + png_file))
                copyfile(("in\\" + png_file), ("temp\\" + png_file))
            except:
                print("The png or its pgw number ") + png + " does'nt exist in the in folder")
        # Fill the smaller png with alpha so it is all the same size
        if png_is_too_small(png_path):
            fill_png_with_alpha(png_path)
        # Merge every png of the temp folder into one
        merge_png(folder)
        # If merged png is not big enouth, fill the space with alpha
        if merged_png_is_too_small(merged_png_path):
            fill_merged_png_with_alpha(merged_png_path)
        # Rotate the merged png
        angle = 
        rotate_png(angle)
        # Clip the merged png at the size of the tile

        # os.system("magick convert temp\\*.png +append temp\\out.png")
        if not os.path.exists("tiles\\" + str(MAX_ZOOM) + "\\" + str(tile['properties']['x_tile'])):
            os.mkdir("tiles\\" + str(MAX_ZOOM) + "\\" + str(tile['properties']['x_tile']))
        first_png = os.listdir("temp")
        if first_png:
            fisrt_png_path = os.path.join("temp", first_png[0])
            copyfile((fisrt_png_path), ("tiles\\" + str(MAX_ZOOM) + "\\" + str(tile['properties']['x_tile']) + "\\" + str(tile['properties']['y_tile']) + ".png"))
        # copyfile(("temp\\out.png"), ("tiles\\" + str(MAX_ZOOM) + "\\" + str(tile['properties']['x_tile']) + "\\" + str(tile['properties']['y_tile']) + ".png"))
        delete_folder_content("temp")


def make_tiles():
    pass

# Utils

def filter_tile_index(tile_index):
    """
    Look at the png files that are actually present in the /in folder, and 
    remove the png that are missing in png_list of every tile. If a png list 
    become empty, delete the tile.
    """
    pass

def delete_folder_content(folder_path):
    for file_object in os.listdir(folder_path):
        file_object_path = os.path.join(folder_path, file_object)
        if os.path.isfile(file_object_path) or os.path.islink(file_object_path):
            os.unlink(file_object_path)
        else:
            shutil.rmtree(file_object_path)

def load_geojson_file(filename):
    with open(filename, "r") as read_file:
        f = geojson.load(read_file)
    return f

def polygon_extrema(polygon_geometry):
    min_lon = polygon_geometry[0][0]
    max_lon = polygon_geometry[0][0]
    min_lat = polygon_geometry[0][1]
    max_lat = polygon_geometry[0][1]
    for [lon, lat] in polygon_geometry:
        if min_lon > lon:
            min_lon = lon
        if max_lon < lon:
            max_lon = lon
        if min_lat > lat:
            min_lat = lat
        if max_lat < lat:
            max_lat = lat
    return (min_lon, max_lon, min_lat, max_lat)

def wgs84_to_tile_num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return (xtile, ytile)

def tile_num_to_wgs84(xtile, ytile, zoom, invert=True):
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    if invert == True:
        return (lon_deg, lat_deg)
    else:
        return (lat_deg, lon_deg)

def int_to_str_add_zeros(number):
    """
    Turn an int to a sting and make sure it has 6 digit (add zeros before if 
    needed)
    """
    if type(number) != int:
        print("File number should be an integer.\n")
    if number < 0:
        print("File number can't be negative.\n")
    elif number > 999999:
        print("File number can't be longer than 6 digits.\n")
    string = ''
    for i in range(6 - len(str(number))):
        string = string + '0'
    string = string + str(number)
    return string

# Main

if __name__ == "__main__":
    # make_max_zoom_index()
    make_max_zoom_tiles()