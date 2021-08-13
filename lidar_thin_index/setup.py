import sys
from cx_Freeze import setup, Executable

includefiles = ["las2las64.exe", "lasindex64.exe"]
includes = []
excludes = ["tkinter"]

setup(
    name="lidar_thin_index",
    version="0.1",
    description="To thin by a 4 factor lidar data and index it",
    options={
        "build_exe": {
            "includes": includes,
            "excludes": excludes,
            "include_files": includefiles,
        }
    },
    executables=[Executable("lidar_thin_index.py", base=None)],
)
