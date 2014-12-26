# ScriptyToby #

A collection of useful scripts by Tobchen (me).

## Tobinary ##

A python script to convert plain text files to binary files.

Reads a plain text file with values seperated by whitespaces and converts them to char, integers, floats or C strings depending on the first character of the field.

Examples:
- c12 - becomes a character (byte) with value 12
- i144 - becomes an integer (32bit) with value 144
- f-4.5 - becomes a float (32bit) with value -4.5
- cHello - becomes a C string (zero terminated) with value Hello

For more info call: tobinary.py -h
