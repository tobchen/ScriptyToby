#!/usr/bin/env python3

import argparse
import os.path
import matplotlib.image as mpimg
import numpy
import functools
import struct


# Class for frames
class Frame:
    def __init__(self, frame_x: int, frame_y: int, left: int, top: int,
                 right: int, bottom: int):
        self.frame_x = frame_x
        self.frame_y = frame_y
        self.off_x = left
        self.off_y = top
        self.width = right + 1 - left
        self.height = bottom + 1 - top
        self.pos_x = 0
        self.pos_y = 0


def comp_frames(f1: Frame, f2: Frame) -> bool:
    if f1.height > f2.height:
        return -1
    elif f1.height < f2.height:
        return +1
    else:
        if f1.width > f2.width:
            return -1
        elif f1.width < f2.width:
            return +1
        else:
            return 0


# algorithm no. 1 from http://cgi.csc.liv.ac.uk/~epa/surveyhtml.html
def try_pack(frames: list, width: int, height: int):
    tmp = list(frames)

    top = 0

    while len(tmp):
        first = tmp[0]
        tmp.remove(first)
        first.pos_x = 0
        first.pos_y = top

        left = first.width

        if left > width or top + first.height > height:
            return False

        while True:
            found = None
            for frame in tmp:
                if left + frame.width <= width:
                    found = frame
                    break

            if found:
                tmp.remove(found)
                found.pos_x = left
                found.pos_y = top

                left += found.width
            else:
                break

        top += first.height

    return True


# Parse for arguments
parser = argparse.ArgumentParser(description="Compress a sprite sheet")
parser.add_argument("image", help="image to be compressed")
parser.add_argument("frames", help="columns and rows of frames, e.g. 10x5")
parser.add_argument("-o", "--output", metavar="out",
                    help="specify output filename (without extension)")
args = parser.parse_args()

# Read arguments
input_name = args.image
output_name = None
if args.output:
    output_name = args.output
else:
    output_name = input_name + "_packed"

# Exit if image does not exist
if not os.path.isfile(input_name):
    print("Image not found: "+input_name)
    exit()

# Read frame columns and rows
cols = 0
rows = 0
if args.frames.find("x") < 0:
    print("Frames must be of form <columns>x<rows>, e.g.: 10x5")
    exit()
try:
    cols = int(args.frames[:args.frames.find("x")])
    rows = int(args.frames[args.frames.find("x")+1:])
except ValueError:
    print("Frames must be of form <columns>x<rows>, e.g. 10x5")
    exit()

# Load image
input_img = mpimg.imread(input_name)

# Exit if image has no alpha channel
if input_img.shape[2] != 4:
    print("For now only images with alpha are supported!")
    exit()

# Check if columns and rows are correctly given
if input_img.shape[1] % cols != 0:
    print("Columns value seems to be wrong!")
    exit()
if input_img.shape[0] % rows != 0:
    print("Rows value seems to be wrong!")
    exit()

# Get frame width and height
frame_width = int(input_img.shape[1] / cols)
frame_height = int(input_img.shape[0] / rows)

# Build list of frames
frames = []
for frame_y in range(0, rows):
    for frame_x in range(0, cols):
        left = frame_width
        right = 0
        top = frame_height
        bottom = 0

        for x in range(0, frame_width):
            for y in range(0, frame_height):
                if not numpy.isclose(input_img[(frame_y * frame_height) + y][(frame_x * frame_width) + x][3], 0):
                    if x > right:
                        right = x
                    if y > bottom:
                        bottom = y
                    if x < left:
                        left = x
                    if y < top:
                        top = y

        if right < left or bottom < top:
            print("Frame ", frame_x, "x", frame_y, " has no pixels!")
            exit()

        frames.append(Frame(frame_x, frame_y, left, top, right, bottom))

# Sort frames by height, then width - also use a new list
sorted_frames = sorted(frames, key=functools.cmp_to_key(comp_frames))

# Now try pack until it succeeds
new_width = 1
new_height = 1
success = False
while not success:
    if new_width == new_height:
        new_width *= 2
    elif new_width > new_height:
        new_width = int(new_width / 2)
        new_height *= 2
    else:
        new_width *= 2

    success = try_pack(sorted_frames, new_width, new_height)

# Create new image
output_img = numpy.zeros((new_height, new_width, 4))
for frame in frames:
    for x in range(0, frame.width):
        for y in range(0, frame.height):
            for i in range(0, 4):
                output_img[frame.pos_y+y][frame.pos_x+x][i] =\
                    input_img[(frame.frame_y * frame_height)+frame.off_y+y][(frame.frame_x * frame_width)+frame.off_x+x][i]
mpimg.imsave(output_name+".png", output_img, format="png")

# Save binary file
output_file = open(output_name+".bin", "wb")
output_file.write(struct.pack(">i", int(frame_width)))
output_file.write(struct.pack(">i", int(frame_height)))
output_file.write(struct.pack(">i", int(len(frames))))
for frame in frames:
    output_file.write(struct.pack(">i", int(frame.pos_x)))
    output_file.write(struct.pack(">i", int(frame.pos_y)))
    output_file.write(struct.pack(">i", int(frame.off_x)))
    output_file.write(struct.pack(">i", int(frame.off_y)))
    output_file.write(struct.pack(">i", int(frame.width)))
    output_file.write(struct.pack(">i", int(frame.height)))

# File specification:
# frame_width: int, frame_height: int, frame_count: int
# for every frame:
#   frame.pos_x, frame.pos_y,
#   frame.off_x: int, frame.off_y: int,
#   frame.width: int, frame.height: int
#
# Ints are 32bit big endian