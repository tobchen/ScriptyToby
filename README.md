# ScriptyToby #

A collection of useful scripts by Tobchen (me).

## Tobinary ##

A Python 3 script to convert plain text files to binary files.

Reads a plain text file with values seperated by whitespaces and converts them to char, integers, floats or C strings depending on the first character of the field.

Examples:
- c12 - becomes a character (byte) with value 12
- i144 - becomes an integer (32bit) with value 144
- f-4.5 - becomes a float (32bit) with value -4.5
- sHello - becomes a C string (zero terminated) with value Hello

For more info call: tobinary.py -h

## Rezip ##

A Python 3 script to possibly rezip a directory.

Takes a directory and a zip-archive (or the path where one wants to write one to) and checks recursively if any file in the directory is newer than the archive and archives the directory anew.
