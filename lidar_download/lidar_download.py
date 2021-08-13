import os
import json
import sys
from ftplib import FTP


def lidar_download(
    ftp_adress, ftp_folder, file_generic_name, file_extention, tiles
):

    "Download a list of lidar files on a ftp server."

    total_number_of_files = len(tiles["features"])
    number_of_downloaded_files = 0
    number_of_skiped_files = 0

    ftp = FTP(ftp_adress)
    ftp.login()
    ftp.cwd(ftp_folder)

    ftp_list = ftp.nlst()

    # Create "in" directory if it don't already exists
    if not os.path.exists(r".\in"):
        os.mkdir(r".\in")

    for tile in tiles["features"]:
        filename = (
            file_generic_name
            + int_to_str_add_zeros(int(tile["properties"]["TILES_500m"]))
            + file_extention
        )
        local_filename = os.path.join(r".\in", filename)

        if os.path.exists(local_filename):
            print("File already in the folder.")
            number_of_skiped_files += 1
            progress_message(
                number_of_skiped_files,
                number_of_downloaded_files,
                total_number_of_files,
            )
            continue

        # Check if the file exists on the server
        if filename in ftp_list:
            lf = open(local_filename, "wb")
            ftp.retrbinary("RETR " + filename, lf.write, 8 * 1024)
            lf.close()
            number_of_downloaded_files += 1
            progress_message(
                number_of_skiped_files,
                number_of_downloaded_files,
                total_number_of_files,
            )
        else:
            print("File does'nt exist on the server")
            number_of_skiped_files += 1
            progress_message(
                number_of_skiped_files,
                number_of_downloaded_files,
                total_number_of_files,
            )


def int_to_str_add_zeros(number):
    """
    Turn an int to a sting and make sure it has 6 digit (add zeros before if
    needed)
    """

    if type(number) != int:
        print("File number should be an integer.\n")
    if number < 0:
        print("File number can't be negative.\n")
    elif number > 999999:
        print("File number can't be longer than 6 digits.\n")
    string = ""
    for i in range(6 - len(str(number))):
        string = string + "0"
    string = string + str(number)
    return string


def progress_message(
    number_of_skiped_files, number_of_downloaded_files, total_number_of_files
):

    print(
        str(number_of_skiped_files)
        + " skiped files and "
        + str(number_of_downloaded_files)
        + " files downloaded under a total of "
        + str(total_number_of_files)
        + "."
    )


def find_part_tiles(filename):
    if getattr(sys, "frozen", False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)
    return os.path.join(datadir, filename)


# Main
# ----

# Parameters import
with open("lidar_download_settings.json", "r") as read_file:
    data = json.load(read_file)

while True:
    try:
        print("Part number ?")
        part_number = input()

        # Tiles geojson list
        # tiles_file = "parts/parts_tiles/part_" + part_number + ".geojson"

        if getattr(sys, "frozen", False):
            # The application is frozen
            tiles_file = "part_" + part_number + ".geojson"
        else:
            # The application is not frozen
            tiles_file = "parts/parts_tiles/part_" + part_number + ".geojson"

        with open(tiles_file, "r") as read_file:
            tiles = json.load(read_file)
        break
    except FileNotFoundError:
        print("Geojson file does'nt exist.")
    except:
        print("An error occured.")

data["tiles"] = tiles
lidar_download(**data)
