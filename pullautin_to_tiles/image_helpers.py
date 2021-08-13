from PIL import Image


def fill_small_png_with_alpha(
    png_path, pgw_path, tile_pixel_size, tile_meter_size, tile_geometry
):
    with open(pgw_path, "r") as f:
        pgw_file = f.read()
    splited_pgw_file = pgw_file.splitlines()
    # png are georeferenced with the up left point
    png_georef_point = [float(splited_pgw_file[4]), float(splited_pgw_file[5])]

    # Tile scale in meters per pixels
    tile_scale = tile_meter_size / tile_pixel_size
    png = Image.open(png_path)
    image_width, image_height = png.size

    png_right_down_point = (
        png_georef_point[0] + image_width * tile_scale,
        png_georef_point[1] - image_height * tile_scale,
    )

    fill_left = False
    fill_right = False
    fill_up = False
    fill_down = False

    if image_width < tile_pixel_size:
        if abs(png_georef_point[0] - tile_geometry[0][0]) > 1:
            fill_left = True
        if abs(png_right_down_point[0] - tile_geometry[2][0]) > 1:
            fill_right = True
    if image_height < tile_pixel_size:
        if abs(png_georef_point[1] - tile_geometry[0][1]) > 1:
            fill_up = True
        if abs(png_right_down_point[1] - tile_geometry[2][1]) > 1:
            fill_down = True

    if fill_left and fill_right:
        left_transparent_width = int(
            abs(png_georef_point[0] - tile_geometry[0][0]) / tile_scale
        )
        right_transparent_width = (
            tile_pixel_size - image_width - left_transparent_width
        )
        left_transparent = create_transparent_image(
            left_transparent_width, image_height
        )
        right_transparent = create_transparent_image(
            right_transparent_width, image_height
        )
        merged_left = get_concat_h(left_transparent, png)
        merged_h = get_concat_h(merged_left, right_transparent)
    elif fill_left and not fill_right:
        left_transparent_width = tile_pixel_size - image_width
        left_transparent = create_transparent_image(
            left_transparent_width, image_height
        )
        merged_h = get_concat_h(left_transparent, png)
    elif not fill_left and fill_right:
        right_transparent_width = tile_pixel_size - image_width
        right_transparent = create_transparent_image(
            right_transparent_width, image_height
        )
        merged_h = get_concat_h(png, right_transparent)

    else:
        merged_h = png

    if fill_up and fill_down:
        up_transparent_height = int(
            abs(png_georef_point[1] - tile_geometry[0][1]) / tile_scale
        )
        down_transparent_height = (
            tile_pixel_size - image_height - up_transparent_height
        )
        up_transparent = create_transparent_image(
            tile_pixel_size, up_transparent_height
        )
        down_transparent = create_transparent_image(
            tile_pixel_size, down_transparent_height
        )
        merged_up = get_concat_v(up_transparent, merged_h)
        merged = get_concat_v(merged_up, down_transparent)
    elif fill_up and not fill_down:
        up_transparent_height = tile_pixel_size - image_height
        up_transparent = create_transparent_image(
            tile_pixel_size, up_transparent_height
        )
        merged = get_concat_v(up_transparent, merged_h)
    elif not fill_up and fill_down:
        down_transparent_height = tile_pixel_size - image_height
        down_transparent = create_transparent_image(
            tile_pixel_size, down_transparent_height
        )
        merged = get_concat_v(merged_h, down_transparent)
    else:
        merged = merged_h

    return merged


def get_concat_h(im1, im2):
    dst = Image.new("RGBA", (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst


def get_concat_v(im1, im2):
    dst = Image.new("RGBA", (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst


def create_transparent_image(width, height):
    img = Image.new("RGBA", (width, height), (255, 0, 0, 0))
    return img
