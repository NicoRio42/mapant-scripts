import sys
import os
from shutil import copyfile

import geojson

import helpers as hp

MIN_ZOOM = 6
MAX_ZOOM = 15
BORDER_FILENAME = "border_test.geojson"
LIDAR_INDEX_FILENAME = "lidar_index.geojson"
LIDAR_INDEX_LAMBERT_93_FILENAME = "lidar_index_lambert_93.geojson"
TILES_PIXEL_SIZE = 1183


def make_max_zoom_index(
    max_zoom=15,
    border_filename="border_test.geojson",
    lidar_index_filename="lidar_index.geojson",
):
    """ """

    # Importing the geojson files
    border = hp.load_geojson_file(border_filename)
    lidar_index = hp.load_geojson_file("index_files\\" + lidar_index_filename)

    # Calculate the slipy map extrem tile coordinates
    (min_lon, max_lon, min_lat, max_lat) = hp.polygon_extrema(border_geometry)
    (min_x, max_y) = hp.wgs84_to_tile_num(min_lat, min_lon, max_zoom)
    (max_x, min_y) = hp.wgs84_to_tile_num(max_lat, max_lon, max_zoom)

    features = []
    count = 0

    for x in range(min_x, (max_x + 1)):
        for y in range(min_y, (max_y + 1)):
            # Create tile geometry
            polygon = geojson.Polygon(
                [
                    [
                        hp.tile_num_to_wgs84(x, y, max_zoom),
                        hp.tile_num_to_wgs84(x + 1, y, max_zoom),
                        hp.tile_num_to_wgs84(x + 1, y + 1, max_zoom),
                        hp.tile_num_to_wgs84(x, y + 1, max_zoom),
                        hp.tile_num_to_wgs84(x, y, max_zoom),
                    ]
                ]
            )

            # Fill png list
            png_list = []
            p = polygon.coordinates[0]
            p_min_lon = p[0][0]
            p_max_lon = p[1][0]
            p_min_lat = p[2][1]
            p_max_lat = p[0][1]

            # For every lidar tile, check if an edge of the square is
            # in the slippy map tile
            for lidar in lidar_index.features:
                lidar_geometry = lidar.geometry.coordinates[0][0]

                # Check every edges
                for edge in lidar_geometry:

                    # Check if edge is inside the slippy map tile
                    if (
                        edge[0] > p_min_lon
                        and edge[0] < p_max_lon
                        and edge[1] > p_min_lat
                        and edge[1] < p_max_lat
                    ):
                        png_list.append(lidar["properties"]["TILES_500m"])
                        break

            png_list.sort()
            # create feature
            properties = {
                "png_list": png_list,
                "parent_tiles": [],
                "x_tile": x,
                "y_tile": y,
            }
            feature = geojson.Feature(geometry=polygon, properties=properties)
            if png_list:
                features.append(feature)

    feature_collection = geojson.FeatureCollection(features)
    # write feature into file
    output_file_name = "index_files\\tile_index_" + str(max_zoom) + ".geojson"
    with open(output_file_name, "w") as f:
        geojson.dump(feature_collection, f)


def make_index(zoom_number):
    pass


def make_max_zoom_tiles(
    max_zoom=15,
    lidar_index_filename="lidar_index.geojson",
    lidar_index_lambert_93_filename="lidar_index_lambert_93.geojson",
):
    """ """

    # Load max zoom tile index
    tile_index_max_zoom = load_geojson_file(
        "index_files\\tile_index_" + str(max_zoom) + ".geojson"
    )
    # Load lidar index
    lidar_index = load_geojson_file("index_files\\" + lidar_index_filename)
    # Load lidar index in Lambert 93 projection
    lidar_index = load_geojson_file(
        "index_files\\" + lidar_index_lambert_93_filename
    )

    # Filter tile_index_max_zoom given the png files that are present in the \in folder
    hp.filter_tile_index(tile_index_max_zoom)

    hp.make_dir_if_doesnt_exist("tiles")
    hp.make_dir_if_doesnt_exist("tiles\\" + str(max_zoom))
    hp.make_dir_if_doesnt_exist("temp")

    for tile in tile_index_max_zoom.features:
        png_list = tile["properties"]["png_list"]
        # Copy every png of png_list in temp folder
        for png in png_list:
            png_file = (
                "11555_Grand-Geneve_SemisLidar_"
                + int_to_str_add_zeros(int(png))
                + "_quarter.laz_depr.png"
            )
            pgw_file = (
                "11555_Grand-Geneve_SemisLidar_"
                + int_to_str_add_zeros(int(png))
                + "_quarter.laz_depr.pgw"
            )
            try:
                copyfile(("in\\" + png_file), ("temp\\" + png_file))
                copyfile(("in\\" + png_file), ("temp\\" + png_file))
            except:
                print(
                    "The png or its pgw number "
                    + png
                    + " does'nt exist in the in folder"
                )
        # Fill the smaller png with alpha so it is all the same size
        if hp.png_is_too_small(png_path):
            hp.fill_png_with_alpha(png_path)
        # Merge every png of the temp folder into one
        merge_png(folder)
        # If merged png is not big enouth, fill the space with alpha
        if merged_png_is_too_small(merged_png_path):
            fill_merged_png_with_alpha(merged_png_path)
        # Rotate the merged png
        angle = 0
        rotate_png(angle)
        # Clip the merged png at the size of the tile

        # os.system("magick convert temp\\*.png +append temp\\out.png")
        if not os.path.exists(
            "tiles\\" + str(MAX_ZOOM) + "\\" + str(tile["properties"]["x_tile"])
        ):
            os.mkdir(
                "tiles\\"
                + str(MAX_ZOOM)
                + "\\"
                + str(tile["properties"]["x_tile"])
            )
        first_png = os.listdir("temp")
        if first_png:
            fisrt_png_path = os.path.join("temp", first_png[0])
            copyfile(
                (fisrt_png_path),
                (
                    "tiles\\"
                    + str(MAX_ZOOM)
                    + "\\"
                    + str(tile["properties"]["x_tile"])
                    + "\\"
                    + str(tile["properties"]["y_tile"])
                    + ".png"
                ),
            )
        # copyfile(("temp\\out.png"), ("tiles\\" + str(MAX_ZOOM) + "\\" + str(tile['properties']['x_tile']) + "\\" + str(tile['properties']['y_tile']) + ".png"))
        delete_folder_content("temp")


def make_tiles():
    pass


# Main

if __name__ == "__main__":
    args = sys.argv[1:]
    if (
        len(args) == 4
        and args[0] == "-minzoom"
        and args[2] == "-maxzoom"
        and args[1].isdigit()
        and args[3].isdigit()
    ):
        min_zoom = args[1]
        max_zoom = args[3]
        print(min_zoom)
        print(max_zoom)
    else:
        print("There is a problem with your options.")

    # make_max_zoom_index()
    # make_max_zoom_tiles()
