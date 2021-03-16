import geojson
import math
import os
from shutil import copyfile

import helpers as hp

def zoom_number(minimum_tile_size, border_size):
    """Return the number of zooms
    """
    num = math.log(border_size / minimum_tile_size) / math.log(2)
    return num

def max_height_or_width(polygon_extrema):
    height = abs(polygon_extrema[0] - polygon_extrema[1])
    width = abs(polygon_extrema[2] - polygon_extrema[3])
    return max(height, width)

def lambert_93_to_tile_num(x, y, origin, max_size, zoom):
    x_tile = int(((x - origin[0]) / max_size) * math.pow(2, zoom))
    y_tile = int(((origin[1] - y) / max_size) * math.pow(2, zoom))
    return (x_tile, y_tile)


if __name__ == "__main__":
    france_border = hp.load_geojson_file("lambert_93_index_files\\france_border.geojson")
    france_extrema = hp.polygon_extrema(france_border)
    france_size = max_height_or_width(france_extrema)
    zoom_num = zoom_number(500, int(france_size))
    max_tile_size = 500 * math.pow(2, 12)
    center_offset = int((max_tile_size - france_size) / 2)
    min_x = int(france_extrema[0]) - center_offset
    max_x = min_x + max_tile_size
    min_y = int(france_extrema[2]) - center_offset
    max_y = min_y + max_tile_size

    slipy_map_origin = (min_x, max_y) # y is inverted in slipy maps

    tile_exemple = lambert_93_to_tile_num(959500, 6545500, slipy_map_origin, max_tile_size, 12)
    tile_exemple_2 = lambert_93_to_tile_num(960000, 6545000, slipy_map_origin, max_tile_size, 12)

    print(france_extrema)
    print(france_size)
    print(zoom_num)
    print(max_tile_size)
    print(center_offset)
    print(min_x, max_x, min_y, max_y)
    print(max_tile_size/math.pow(2, 12))
    print(tile_exemple)
    print(tile_exemple_2)

    lidar_index_lambert_93 = hp.load_geojson_file("lambert_93_index_files\\lidar_index_lambert_93.geojson")
    try:
        png_files = [f for f in os.listdir("in") if f.endswith(".png")]
        pgw_files = [f for f in os.listdir("in") if f.endswith(".pgw")]
    except FileNotFoundError:
        print("There is no \in directory.")
    except:
        print("An error occured.")
    
    hp.make_dir_if_doesnt_exist("tiles")
    hp.make_dir_if_doesnt_exist("tiles\\12")

    for png in png_files:
        tile_number = int(png[30:36])
        tile = [t for t in lidar_index_lambert_93["features"] if t["properties"]["TILES_500m"] == tile_number]
        point = tile[0]["geometry"]["coordinates"][0][0][0]
        tile_coord = lambert_93_to_tile_num(point[0], point[1], slipy_map_origin, max_tile_size, 12)
        hp.make_dir_if_doesnt_exist("tiles\\12\\" + str(tile_coord[0]))
        copyfile(("in\\" + png), ("tiles\\12\\" + str(tile_coord[0]) + "\\" + str(tile_coord[1]) + ".png"))
        