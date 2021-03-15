import os
from shutil import copyfile

# List of png and pgw files in in folder
try:
    png_files = [f for f in os.listdir("in") if f.endswith(".png")]
    pgw_files = [f for f in os.listdir("in") if f.endswith(".pgw")]
except FileNotFoundError:
    print("There is no \in directory.")
except:
    print("An error occured.")

# If no out_depr folder, create it
if not os.path.exists("out_depr"):
    os.mkdir("out_depr")

# If no out_no_depr folder, create it
if not os.path.exists("out_no_depr"):
    os.mkdir("out_no_depr")

# Copying png files
done_files = 0
total_files = len(png_files)
for f in png_files:
    filename, file_extension = os.path.splitext(f)
    if filename.endswith("_depr"):
        copyfile(("in\\" + f), ("out_depr\\" + f))
    else:
        copyfile(("in\\" + f), ("out_no_depr\\" + f))
    done_files += 1
    print(str(done_files) + " png files done under a total of " + str(total_files))

# Copying pgw files
done_files = 0
total_files = len(pgw_files)
for f in pgw_files:
    filename, file_extension = os.path.splitext(f)
    if filename.endswith("_depr"):
        copyfile(("in\\" + f), ("out_depr\\" + f))
    else:
        copyfile(("in\\" + f), ("out_no_depr\\" + f))
    done_files += 1
    print(str(done_files) + " pgw files done under a total of " + str(total_files))