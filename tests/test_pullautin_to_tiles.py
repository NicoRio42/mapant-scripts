import os

import geojson

import pullautin_to_tiles.helpers as helpers


def test_filter_tile_index():
    pass


def test_delete_folder_content():
    # Create a folder
    if not os.path.exists("test_delete_folder_content"):
        os.mkdir("test_delete_folder_content")
    # Put a file inside
    with open("test_delete_folder_content\\file.txt", "w") as f:
        test_file = f
    # Empty folder
    helpers.delete_folder_content("test_delete_folder_content")
    assert not os.listdir("test_delete_folder_content")
    # Delete folder
    os.rmdir("test_delete_folder_content")


def test_load_geojson_file():
    file_name = "test_files\\border_test.geojson"
    with open(file_name, "r") as read_file:
        polygon = geojson.load(read_file)
    assert type(polygon) == geojson.feature.FeatureCollection


def test_polygon_extrema():
    file_name = "test_files\\border_test.geojson"
    with open(file_name, "r") as read_file:
        polygon = geojson.load(read_file)
    returned_tuple = (6.029314, 6.142241, 46.387207, 46.4233)
    assert returned_tuple == helpers.polygon_extrema(polygon)


def test_wgs84_to_tile_num():
    assert helpers.wgs84_to_tile_num(46.387207, 6.029314, 15) == (16932, 11606)


def test_tile_num_to_wgs84():
    assert helpers.tile_num_to_wgs84(16932, 11606, 15) == (
        6.0205078125,
        46.392411189814645,
    )


def test_int_to_str_add_zeros():
    assert helpers.int_to_str_add_zeros(64) == "000064"
