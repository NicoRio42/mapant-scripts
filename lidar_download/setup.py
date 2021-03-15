import sys
from cx_Freeze import setup, Executable

includefiles = [
    'lidar_download_settings.json',
    'parts\parts_tiles\part_1.geojson',
    'parts\parts_tiles\part_2.geojson',
    'parts\parts_tiles\part_3.geojson',
    'parts\parts_tiles\part_4.geojson',
    'parts\parts_tiles\part_5.geojson',
    'parts\parts_tiles\part_6.geojson',
    'parts\parts_tiles_overlap\part_1_overlap.geojson',
    'parts\parts_tiles_overlap\part_2_overlap.geojson',
    'parts\parts_tiles_overlap\part_3_overlap.geojson',
    'parts\parts_tiles_overlap\part_4_overlap.geojson',
    'parts\parts_tiles_overlap\part_5_overlap.geojson',
    'parts\parts_tiles_overlap\part_6_overlap.geojson',]
includes = []
excludes = ['Tkinter']

setup(name = "lidar_download",
    version = "0.1",
    description = "To download lidar files from ftp server",
    options = {'build_exe': {'includes':includes, 'excludes':excludes, 'include_files':includefiles}},
    executables = [Executable("lidar_download.py", base=None)])

"""
    'parts\parts_tiles\part_1.geojson',
    'parts\parts_tiles\part_2.geojson',
    'parts\parts_tiles\part_3.geojson',
    'parts\parts_tiles\part_4.geojson',
    'parts\parts_tiles\part_5.geojson',
    'parts\parts_tiles\part_6.geojson',
    'parts\parts_tiles_overlap\part_1_overlap.geojson',
    'parts\parts_tiles_overlap\part_2_overlap.geojson',
    'parts\parts_tiles_overlap\part_3_overlap.geojson',
    'parts\parts_tiles_overlap\part_4_overlap.geojson',
    'parts\parts_tiles_overlap\part_5_overlap.geojson',
    'parts\parts_tiles_overlap\part_6_overlap.geojson',
"""