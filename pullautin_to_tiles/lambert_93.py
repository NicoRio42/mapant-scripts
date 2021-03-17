import geojson
import math
import os
from shutil import copyfile

from PIL import Image

import helpers as hp
import image_helpers as im_hp

TILES_PIXEL_SIZE = 1183
ZOOM_NUMBER = 12
(MIN_X, MAX_X, MIN_Y, MAX_Y) = (-343646, 1704354, 5619537, 7667537)
MAX_TILE_SIZE = 500 * math.pow(2, 12)
SLIPPY_MAP_ORIGIN = (MIN_X, MAX_Y)

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

def slippy_map_parameters():
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

def make_max_zoom_tiles():
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
        tile_coord = lambert_93_to_tile_num(point[0], point[1], SLIPPY_MAP_ORIGIN, MAX_TILE_SIZE, 12)
        hp.make_dir_if_doesnt_exist("tiles\\12\\" + str(tile_coord[0]))
        png_path = os.path.join("in", png)
        png_file = Image.open(png_path)
        png_width, png_height = png_file.size
        # print(tile_number)
        # print(tile_coord)

        if png_width == TILES_PIXEL_SIZE and png_height == TILES_PIXEL_SIZE:
            copyfile(png_path, ("tiles\\12\\" + str(tile_coord[0]) + "\\" + str(tile_coord[1]) + ".png"))
        else:
            pgw_path = os.path.splitext(png_path)[0] + ".pgw"
            tile_geometry = tile[0]["geometry"]["coordinates"][0][0]
            filled_png = im_hp.fill_small_png_with_alpha(png_path, pgw_path, TILES_PIXEL_SIZE, 500, tile_geometry)
            filled_png.save(("tiles\\12\\" + str(tile_coord[0]) + "\\" + str(tile_coord[1]) + ".png"), 'PNG')

def get_parent_tile(x_tile, y_tile):
    x_parent = int(x_tile / 2)
    y_parent = int(y_tile / 2)
    return (x_parent, y_parent)

def get_children_tiles(x_tile, y_tile):
    x_children = (x_tile * 2, x_tile * 2 + 1)
    y_children = (y_tile * 2, y_tile * 2 + 1)
    return (x_children, y_children)

def make_tiles(zoom):
    parent_tiles_path = os.path.join("tiles", str(zoom))
    hp.make_dir_if_doesnt_exist(parent_tiles_path)
    children_tiles_path = os.path.join("tiles", (str(zoom + 1)))
    x_list = os.listdir(children_tiles_path)
    for x in x_list:
        x_path = os.path.join(children_tiles_path, str(x))
        y_list = os.listdir(x_path)
        for y in y_list:
            x_parent, y_parent = get_parent_tile(int(x), int(os.path.splitext(y)[0]))
            parent_path = os.path.join(parent_tiles_path, str(x_parent), str(y_parent) + ".png")
            if not os.path.exists(parent_path):
                hp.make_dir_if_doesnt_exist(os.path.join(parent_tiles_path, str(x_parent)))
                children_tiles = get_children_tiles(x_parent, y_parent)
                x0_y0_path = os.path.join(children_tiles_path, str(children_tiles[0][0]), str(children_tiles[1][0]) + ".png")
                x1_y0_path = os.path.join(children_tiles_path, str(children_tiles[0][1]), str(children_tiles[1][0]) + ".png")
                x0_y1_path = os.path.join(children_tiles_path, str(children_tiles[0][0]), str(children_tiles[1][1]) + ".png")
                x1_y1_path = os.path.join(children_tiles_path, str(children_tiles[0][1]), str(children_tiles[1][1]) + ".png")
                if os.path.exists(x0_y0_path):
                    x0_y0 = Image.open(x0_y0_path)
                else:
                    x0_y0 = im_hp.create_transparent_image(TILES_PIXEL_SIZE, TILES_PIXEL_SIZE)
                
                if os.path.exists(x1_y0_path):
                    x1_y0 = Image.open(x1_y0_path)
                else:
                    x1_y0 = im_hp.create_transparent_image(TILES_PIXEL_SIZE, TILES_PIXEL_SIZE)
                
                if os.path.exists(x0_y1_path):
                    x0_y1 = Image.open(x0_y1_path)
                else:
                    x0_y1 = im_hp.create_transparent_image(TILES_PIXEL_SIZE, TILES_PIXEL_SIZE)
                
                if os.path.exists(x1_y1_path):
                    x1_y1 = Image.open(x1_y1_path)
                else:
                    x1_y1 = im_hp.create_transparent_image(TILES_PIXEL_SIZE, TILES_PIXEL_SIZE)
                
                merged_up = im_hp.get_concat_h(x0_y0, x1_y0)
                merged_down = im_hp.get_concat_h(x0_y1, x1_y1)
                merged = im_hp.get_concat_v(merged_up, merged_down)
                merged_resized = merged.resize((TILES_PIXEL_SIZE, TILES_PIXEL_SIZE))
                merged_resized.save(parent_path, 'PNG')


if __name__ == "__main__":
    zoom_list = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    for zoom in zoom_list:
        make_tiles(zoom)