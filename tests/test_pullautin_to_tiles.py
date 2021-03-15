import geojson

import pullautin_to_tiles.helpers as helpers

def test_polygon_extrema():
    file_name = "test_files\\border_test.geojson"
    with open(file_name, "r") as read_file:
        polygon = geojson.load(read_file)
    returned_tuple = (6.029314, 6.142241, 46.387207, 46.4233)
    assert returned_tuple == helpers.polygon_extrema(polygon)