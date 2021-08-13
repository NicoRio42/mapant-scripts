import os
import json
from shutil import copyfile

# List of png files in in folder
try:
    png_files = [f for f in os.listdir("in") if f.endswith(".png")]
    pgw_files = [f for f in os.listdir("in") if f.endswith(".pgw")]
except FileNotFoundError:
    print("There is no \in directory.")
except:
    print("An error occured.")

# If no out folder, create it
if not os.path.exists("out"):
    os.mkdir("out")

# If no out_overlap folder, create it
if not os.path.exists("out_overlap"):
    os.mkdir("out_overlap")

print("Part number ?")
part_number = input()
tiles_overlap_file = (
    "parts_tiles_overlap\\part_" + part_number + "_overlap.geojson"
)
with open(tiles_overlap_file, "r") as read_file:
    tiles_overlap = json.load(read_file)

# For files in list,
done_files = 0
total_files = len(png_files)
for f in png_files:
    tile_number = int(f[30:36])
    tile = [
        t
        for t in tiles_overlap["features"]
        if t["properties"]["TILES_500m"] == tile_number
    ]

    if tile:
        copyfile(("in\\" + f), ("out_overlap\\" + f))
    else:
        copyfile(("in\\" + f), ("out\\" + f))
    done_files += 1
    print(str(done_files) + " files done under a total of " + str(total_files))

done_files = 0
total_files = len(pgw_files)
for f in pgw_files:
    tile_number = int(f[30:36])
    tile = [
        t
        for t in tiles_overlap["features"]
        if t["properties"]["TILES_500m"] == tile_number
    ]

    if tile:
        copyfile(("in\\" + f), ("out_overlap\\" + f))
    else:
        copyfile(("in\\" + f), ("out\\" + f))
    done_files += 1
    print(str(done_files) + " files done under a total of " + str(total_files))
