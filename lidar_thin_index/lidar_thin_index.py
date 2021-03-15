import os

# List of laz or las files in in folder
try:
    las_laz_files = [f for f in os.listdir("in") if f.endswith((".las",".laz"))]
except FileNotFoundError:
    print("There is no \in directory.")
except:
    print("An error occured.")

# If no out folder, create it
if not os.path.exists("out"):
    os.mkdir("out")

# For files in list, thin every 4 points and index, in out folder
done_files = 0
total_files = len(las_laz_files)
for f in las_laz_files:
    filename, file_extension = os.path.splitext(f)
    output_file = filename + "_quarter" + file_extension
    thin_command = "las2las64 -i in\\" + f + " -keep_every_nth 4 -o out\\" + \
        output_file
    os.system(thin_command)
    index_command = "lasindex64 -i out\\" + output_file
    os.system(index_command)
    done_files += 1
    print(str(done_files) + " files done under a total of " + str(total_files))