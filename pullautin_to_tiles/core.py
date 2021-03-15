import geojson
import os
from shutil import copyfile

import helpers as hp

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

# Main

if __name__ == "__main__":
    # make_max_zoom_index()
    make_max_zoom_tiles()