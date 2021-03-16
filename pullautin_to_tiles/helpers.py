import math
import geojson
import os

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

def polygon_extrema(polygon):
    """
    Returns the longitude and latitude extrema from a geojson polygon.
    """
    polygon_geometry = polygon.features[0].geometry.coordinates[0][0]
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

def make_dir_if_doesnt_exist(file_path):
    """ Create a directory if it doesn't already exist at the given 
    path
    """
    if not os.path.exists(file_path):
        os.mkdir(file_path)