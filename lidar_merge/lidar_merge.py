""" Special script to fix overlaping problem in the part_2
"""

import os
from shutil import copyfile

from PIL import Image

# If no out folder, create it
if not os.path.exists("out"):
    os.mkdir("out")

png_files_up = [f for f in os.listdir("in_up") if f.endswith(".png")]
png_files_down = [f for f in os.listdir("in_down") if f.endswith(".png")]
pgw_files = [f for f in os.listdir("in_up") if f.endswith(".pgw")]


def get_concat_v(im1, im2):
    dst = Image.new("RGBA", (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst


for i in range(len(png_files_up)):
    png_up = Image.open(os.path.join("in_up", png_files_up[i]))
    png_down = Image.open(os.path.join("in_down", png_files_down[i]))
    png_up_cropped = png_up.crop((0, 0, 1183, 592))
    png_down_cropped = png_down.crop((0, 592, 1183, 1183))
    png_merged = get_concat_v(png_up_cropped, png_down_cropped)
    png_merged.save(os.path.join("out", png_files_up[i]), "PNG")
    copyfile(
        os.path.join("in_up", pgw_files[i]), os.path.join("out", pgw_files[i])
    )
