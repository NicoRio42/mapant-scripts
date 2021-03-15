import os
from shutil import copyfile

# List of png files in out_depr folder
try:
    png_files = [f for f in os.listdir("out_depr") if f.endswith(".png")]
    pgw_files = [f for f in os.listdir("out_depr") if f.endswith(".pgw")]
except FileNotFoundError:
    print("There is no \out_depr directory.")
except:
    print("An error occured.")

# If no out_depr_quarter folder, create it
if not os.path.exists("out_depr_quarter"):
    os.mkdir("out_depr_quarter")

# Copying png files
done_files = 0
total_files = len(png_files)
for f in png_files:
    filename, file_extension = os.path.splitext(f)
    if filename.endswith("_quarter.laz_depr"):
        copyfile(("out_depr\\" + f), ("out_depr_quarter\\" + f))
    else:
        pass
    done_files += 1
    print(str(done_files) + " png files done under a total of " + str(total_files))

# Copying pgw files
done_files = 0
total_files = len(pgw_files)
for f in pgw_files:
    filename, file_extension = os.path.splitext(f)
    if filename.endswith("_quarter.laz_depr"):
        copyfile(("out_depr\\" + f), ("out_depr_quarter\\" + f))
    else:
        pass
    done_files += 1
    print(str(done_files) + " pgw files done under a total of " + str(total_files))