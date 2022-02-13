#!/usr/bin/env python
import argparse
import glob
import os
import sys
import re
from tqdm import tqdm


# get the flags and parse them
parser = argparse.ArgumentParser()
parser.add_argument("--dir", help="Directory in which the files are located",
                    action="store", default=None)
parser.add_argument("-o", "--output", 
                    help="Directory in which the new files are created",
                    action="store", default='output_script_results')
parser.add_argument("-d",  
                    help="Enter a delimiter, ex: '-d -'",
                    action="store", default='_')
parser.add_argument("-r",  
                    help="Enter a range, ex: '-r 1-4'",
                    action="store", default='2-4')
args = parser.parse_args()

# directory will be overwritten later
directory = ''
output_folder = args.output
delimeter = args.d
my_range = args.r
sub_str = re.compile(r'X{1,}')

# use to exit when there's an exception or the end of the script
def exit_message(number):
    input('\nPress any key to exit!')
    sys.exit(number)

def replace_x(matchobj):
    return 'N' * len(matchobj.group(0))

# check if the user has input a directory
if args.dir is None:
    directory = input('Please input the file directory: ')
else:
    directory = args.dir

# check if the input directory is valid
try:
    os.chdir(directory)
except Exception as ex:
    print('Not a valid directory\n', ex)
    exit_message(1)

# check if the output folder already exists and/or can be created
if os.path.isdir(output_folder) is False:
    try:
        os.mkdir(output_folder)
    except Exception as ex:
        print('Cannot create output directory!\n', ex)
        exit_message(1)

# get all files
files = glob.glob('*.fa')
lines = []

# get the start and end of the range
ranges = my_range.split('-')

# iterate the files and also use tqdm for the progress bar
for file in tqdm(files, desc="Processing...", colour='#cc4722'):
    # split the file in an array and join only the required parts
    new_name = delimeter.join(file.split(delimeter)[int(ranges[0]):int(ranges[1])]).replace('.fa', '')
    try:
    # read the file contents and replace the first line
        with open(file, 'r') as rfile:
            lines = rfile.readlines()
            lines[0] = '>' + new_name + '\n'
        rfile.close()
        read_data = re.sub(sub_str, repl=replace_x, string=''.join(lines))
        # write the amended contents to a new file
        with open(f'{output_folder}/{new_name}.fa', 'w') as wfile:
            wfile.write(read_data)
        wfile.close()
    except Exception as ex:
        print(f'\nCannot process file - {file}\n', ex)

