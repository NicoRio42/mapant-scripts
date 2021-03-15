import os
from shutil import copyfile

# List of png files in in folder
try:
    png_files = [f for f in os.listdir("in") if f.endswith(".png")]
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

while True:
    try:
        print("Part number ?")
        part_number = input()
    
        # Tiles geojson list
        # tiles_file = "parts/parts_tiles/part_" + part_number + ".geojson"

        if getattr(sys, "frozen", False):
            # The application is frozen
            tiles_overlap_file = "part_" + part_number + ".geojson"
        else:
            # The application is not frozen
            tiles_overlap_file = "parts/parts_tiles/part_" + part_number + ".geojson"

        with open(tiles_file, "r") as read_file:
            tiles = json.load(read_file)
        break
    except FileNotFoundError:
        print("Geojson file does'nt exist.")
    except:
        print("An error occured.")

# For files in list, 
done_files = 0
total_files = len(png_files)
for f in png_files:
    filename, file_extension = os.path.splitext(f)
    if filename.endswith("_depr"):
        copyfile(("in\\" + f), ("out_depr\\" + f))
    else:
        copyfile(("in\\" + f), ("out_no_depr\\" + f))
    done_files += 1
    print(str(done_files) + " files done under a total of " + str(total_files))