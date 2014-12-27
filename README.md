# ScriptyToby #

A collection of useful scripts by Tobchen (me).

## Tobinary ##

A Python 3 script to convert plain text files to binary files.

Reads a plain text file with values seperated by whitespaces and converts them
to char, integers, floats or C strings depending on the first character of the
field.

Examples:
- c12 - becomes a character (byte) with value 12
- i144 - becomes an integer (32bit) with value 144
- f-4.5 - becomes a float (32bit) with value -4.5
- sHello - becomes a C string (zero terminated) with value Hello

For more info call: tobinary.py -h

## Rezip ##

A Python 3 script to possibly rezip a directory.

Takes a directory and a zip-archive (or the path where one wants to write one
to) and checks recursively if any file in the directory is newer than the
archive and archives the directory anew.

## Spritepack ##

A Python 3 script (using SciPy and NumPy) to compress spritesheets.

Takes a spritesheet and number of frames columns and rows and then packs their
bounding boxes to reduce the amount of space needed. Will then save the
resulting image and a binary file with data for every frame, as specified:

- Frame width: int
- Frame height: int
- Frame count: int
- for every frame:
    - X-position of bounding box in compressed image: int
    - Y-position of bounding box in compressed image: int
    - X-offset from bounding box to original frame origin: int
    - Y-offset from bounding boy to original frame origin: int
    - width of bounding box: int
    - height of bounding box: int

(Note: Integers are 32bit big endian)

So that one can draw a frame at position (40,13) like this:

- Before packing: Draw frame at position (40,13)
- Packed: Draw bounding box from packed image (posX, posY) with size (width, height) at (40+offX, 13+offY)

**Note:** The script is rather slow in finding the bounding boxes - don't worry
if it takes up to 2 minutes to finish.
