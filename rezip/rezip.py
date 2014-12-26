#!/usr/bin/env python3

import argparse
import os
import zipfile


# Search a directory recursively for files newer than timestamp
def is_newer_than(directory, time):
    # Exception if directory's not a directory
    if not os.path.isdir(directory):
        raise ValueError("directory must actually be a directory!")

    # Obviously return if directory itself is newer than timestamp
    if os.path.getmtime(directory) > time:
        return true

    # Go through every file
    content = os.listdir(directory)
    for entry in content:
        entry = directory+"/"+entry
        if os.path.isfile(entry) and os.path.getmtime(entry) > time:
            return True
        elif os.path.isdir(entry) and is_newer_than(entry, time):
            return True

    # If nothing else returned True, than it's False
    return False


# Variables to be used
rezip = False

# Parse for arguments
parser = argparse.ArgumentParser(
    description="Check a directory for files to be newer than an archive "
    + "and compress again if there are.")
parser.add_argument("directory", help="directory to be recursively checked")
parser.add_argument("archive", help="archive to be checked against (zip)")
parser.add_argument("-f", "--force", help="compress anyway", action="store_true")
args = parser.parse_args()

# Read arguments
directory_name = args.directory
archive_name = args.archive
if args.force:
    rezip = True

# Exit if directory doesn't exist
if not os.path.isdir(directory_name):
    print("Directory not found: "+directory_name)
    exit()

# Exit if directory is empty (and compressing is not forced)
if not os.listdir(directory_name) and not rezip:
    print("Directory is empty: "+directory_name)
    exit()

# Exit if archive is a directory
if os.path.isdir(archive_name):
    print("Archive is a directory: "+archive_name)
    exit()

# Exit if archive is not *.zip
if archive_name.lower()[-4:] != ".zip":
    print("Archive does not end with .zip: "+archive_name)
    exit()

# Rezip if archive doesn't exist
if not rezip and not os.path.exists(archive_name):
    rezip = True

# Rezip if directory contains newer files than archive
if not rezip and is_newer_than(directory_name, os.path.getmtime(archive_name)):
    rezip = True

# Exit if nothing to rezip
if not rezip:
    exit()

# Open zip file
archive = zipfile.ZipFile(archive_name, 'w')

# Add everything to archive
directories_toadd = [directory_name]
while directories_toadd:
    directory = directories_toadd[0]
    archive.write(directory)
    content = os.listdir(directory)
    for entry in content:
        entry = directory+"/"+entry
        if os.path.isdir(entry):
            directories_toadd.append(entry)
        else:
            archive.write(entry)
    directories_toadd.remove(directory)

# Finally close
archive.close()