#!/usr/bin/env python3

import argparse
import os.path
import struct


# Variables to be used
input_name = None
output_name = None
use_bigendian = True

# Parse for arguments
parser = argparse.ArgumentParser(
    description="Create binary file from plain text file, "
    +"supported types: c (char), i (32b integer), f (32b float), s (C string)")
parser.add_argument("file", help="file to read from")
parser.add_argument("-o", "--output", metavar="out", help="specify output filename")
parser.add_argument("-l", "--littleendian", help="use little endian", action="store_true")
args = parser.parse_args()

# Read arguments
input_name = args.file
if args.output:
    output_name = args.output
else:
    output_name = input_name+".bin"
if args.littleendian:
    use_bigendian = False

# Exit if input file does not exist
if not os.path.isfile(input_name):
    print("File not found: "+input_name)
    exit()

# Ask to overwrite or specify new output file if output file exists
while os.path.isfile(output_name):
    print("Output file "+output_name+" already exists!")
    overwrite = input("Overwrite? [y/n]\n")
    if overwrite.lower() in ["y", "yes"]:
        break
    output_name = input("Output file: (leave empty to exit)\n")
    if not output_name:
        exit()

# Read input file and split into parts
input_file = open(input_name)
input_string = input_file.read()
input_file.close()
input_data = input_string.split()

# Write binary output file
endianness = '>'
if not use_bigendian:
    endianness = '<'
output_file = open(output_name, "wb")
for part in input_data:
    field_type = part[0]
    field = part[1:]
    
    if not field and not field_type == 's':
        print("Warning: Empty non-string field found!")
        continue
    
    if field_type == 'c':  # Char
        output_file.write(struct.pack(endianness+field_type, chr(int(field)).encode()))
    elif field_type == 'i':  # Integer
        output_file.write(struct.pack(endianness+field_type, int(field)))
    elif field_type == 'f':  # Float
        output_file.write(struct.pack(endianness+field_type, float(field)))
    elif field_type == 's':  # C string
        for character in field:
            output_file.write(struct.pack(endianness+field_type, character.encode()))
        output_file.write(struct.pack(endianness+field_type, '\0'.encode()))
    else:
        print("Warning: Type " + field_type + " not known!")
output_file.close()