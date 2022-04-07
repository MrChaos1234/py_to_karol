from PIL import Image
import numpy as np
import os


def convert_bmp_to_coords(image_path):
    im = Image.open(image_path).convert('RGB')
    w, h = im.size
    pixels = list(im.getdata())
    hits = []

    i_pixel = 0
    for y in range(h):
        for x in range(w):
            # print(x,y)
            # print(pixels[i_pixel])
            if pixels[i_pixel] != (255, 255, 255) and pixels[i_pixel] != (0, 0, 0):
                # print(f"hit at ({x},{y})")
                hits.append((x, y))
            i_pixel += 1

    return hits


def convert_bmp_to_coords_color(image_path):
    im = Image.open(image_path).convert('RGB')
    w, h = im.size
    pixels = list(im.getdata())
    hits = []

    i_pixel = 0
    for y in range(h):
        for x in range(w):
            # print(x,y)
            # print(pixels[i_pixel])
            if pixels[i_pixel] != (255, 255, 255):
                # print(f"hit at ({x},{y})")
                hits.append((x, y, pixels[i_pixel]))
            i_pixel += 1

    print(hits)
    return hits


def go_to_point(point):
    (x, y) = point
    if x == 0 and y != 0:
        com = f"Schritt({str(y)})\nMarkeSetzen\nLinksDrehen\nLinksDrehen\nSchritt({str(y)})\nLinksDrehen\nLinksDrehen\n"
    elif y == 0 and x != 0:
        com = f"LinksDrehen\nSchritt({str(x)})\nMarkeSetzen\nLinksDrehen\nLinksDrehen\nSchritt({str(x)})\nLinksDrehen\n"
    elif x == 0 and y == 0:
        com = f"MarkeSetzen\n"
    else:
        com = f"Schritt({str(y)})\nLinksDrehen\nSchritt({str(x)})\nMarkeSetzen\nLinksDrehen\nLinksDrehen\nSchritt({str(x)})\nRechtsDrehen\nSchritt({str(y)})\nLinksDrehen\nLinksDrehen\n"

    return com


def go_to_point_optimized(point):
    (x, y) = point
    if x == 0 and y != 0:
        com = f"Schritt({str(y)})\nMarkeSetzen\nLL\nSchritt({str(y)})\nLinksDrehen\nLinksDrehen\n"
    elif y == 0 and x != 0:
        com = f"LinksDrehen\nSchritt({str(x)})\nMLL\nSchritt({str(x)})\nLinksDrehen\n"
    elif x == 0 and y == 0:
        com = f"MarkeSetzen\n"
    else:
        com = f"Schritt({str(y)})\nLinksDrehen\nSchritt({str(x)})\nMLL\nSchritt({str(x)})\nRechtsDrehen\nSchritt({str(y)})\nLL\n"

    return com


def go_to_point_color_optimized(point):
    (x, y, color_in) = point
    (r, g, b) = color_in

    if r > g and r > b:
        color = "rot"
    elif g > r and g > b:
        color = "grün"
    elif b > r and b > g:
        color = "blau"
    elif r == 0 and b == 0 and g == 0:
        color = "schwarz"
    else:
        color = "schwarz"

    if x == 0 and y != 0:
        com = f"Schritt({str(y)})\nMarkeSetzen({color})\nLL\nSchritt({str(y)})\nLinksDrehen\nLinksDrehen\n"
    elif y == 0 and x != 0:
        com = f"LinksDrehen\nSchritt({str(x)})\nMarkeSetzen({color})\nLL\nSchritt({str(x)})\nLinksDrehen\n"
    elif x == 0 and y == 0:
        com = f"MarkeSetzen({color})\n"
    else:
        com = f"Schritt({str(y)})\nLinksDrehen\nSchritt({str(x)})\nMarkeSetzen({color})\nLL\nSchritt({str(x)})\nRechtsDrehen\nSchritt({str(y)})\nLL\n"

    return com


def output_raw(path_to_image, speed):
    if speed == "fast":
        command = "Schnell\n"
    else:
        command = ""

    pixels = convert_bmp_to_coords(path_to_image)

    for point in pixels:
        command = command + (go_to_point(point))

    command = command + "Langsam\n"

    if not os.path.isdir("out_" + image.split(".")[0]):
        os.makedirs("out_" + image.split(".")[0])

    with open("out_" + image.split(".")[0] + "/" + image.split(".")[0] + "_output_raw.txt", "w") as f:
        f.write(command)


def output_optimized(path_to_image, speed):
    command = ""

    mll = "Anweisung MLL\nMarkeSetzen\nLinksDrehen\nLinksDrehen\n*Anweisung\n"
    ll = "Anweisung LL\nLinksDrehen\nLinksDrehen\n*Anweisung\n"
    command = command + mll + ll

    if speed == "fast":
        command = command + "Schnell\n"
    else:
        command = command + ""

    pixels = convert_bmp_to_coords(path_to_image)



    for point in pixels:
        command = command + (go_to_point_optimized(point))

    command = command + "Langsam\n"

    if not os.path.isdir("out_" + image.split(".")[0]):
        os.makedirs("out_" + image.split(".")[0])

    with open("out_" + image.split(".")[0] + "/" + image.split(".")[0] + "_output_optimized.txt", "w") as f:
        f.write(command)


def output_color_optimized(path_to_image, speed):
    command = ""

    ll = "Anweisung LL\nLinksDrehen\nLinksDrehen\n*Anweisung\n"
    command = command + ll

    if speed == "fast":
        command = command + "Schnell\n"
    else:
        command = command + ""

    pixels = convert_bmp_to_coords_color(path_to_image)

    for point in pixels:
        command = command + (go_to_point_color_optimized(point))

    command = command + "Langsam\n"

    if not os.path.isdir("out_" + image.split(".")[0]):
        os.makedirs("out_" + image.split(".")[0])

    with open("out_" + image.split(".")[0] + "/" + image.split(".")[0] + "_color_output_optimized.txt", "w") as f:
        f.write(command)


if __name__ == '__main__':
    image = "bb.bmp"
    output_raw(image, "fast")
    output_optimized(image, "fast")
    output_color_optimized(image, "fast")
    print("Done. Check files..")

    # Optimized:
    # BSP: ph.mbp ->    unoptimized: 1900 Lines
    #                   optimized: 1400 Lines
