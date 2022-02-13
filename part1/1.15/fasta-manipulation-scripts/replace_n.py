#!/usr/bin/env python
import argparse
import glob
import os
import sys
import re
from tqdm import tqdm

# set as global var so the num_contig() can use it
count = 0

def main():
    global count
    replacement = None
    occurances = dict()
    nfile, output, nflag, directory, stat = get_cli_args()

    # check if the user has input the -n flag
    if nflag:
        replacement = return_n
    else:
        replacement = num_contig

    # check if the user has input the -d flag
    if directory:
        change_dir(directory)
        create_output(output)
        files = glob.glob('*.fasta')
        print(f'Processing {len(files)} files: ', end='')
        for i, file in enumerate(tqdm(files, desc="Processing...", colour='#cc4722')):
            # make sure the counter is 0 before each file
            count = 0
            # get the number of occurances in file and put it in a dict
            occurance = str(
                replace_file_contents(file, replacement, output))
            occurances[file] = occurance
    else:
        create_output(output)
        occurance = str(replace_file_contents(nfile, replacement, output))
        occurances[nfile] = occurance

    # check if the user has requested to see the stats
    if stat:
        print('\n\nStats:\n', end='')
        print('File      |      Occurances       ')
        for occ in occurances:
            print(occ + ' | ' + occurances[occ])
    else:
        print('\nDone!')

def get_cli_args():
    """Get the cli args, parse and
    return them as vars.

    Returns:
       nfile (str): path to the file
       output (str): path to output directory
       nflag (bool): flag for replacement text
       directory (str): path to file directory
       stat (bool): flag for stats
    """
    # get the flags and parse them
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="Provide only one file",
                        action="store", default=None)
    parser.add_argument("-o", "--output", 
                        help="A directory which will store the new file/s",
                        action="store", default='output_script_results')
    parser.add_argument("-n", 
                        help="Use 10k x N as the replacement text",
                        action="store_true", default=None)
    parser.add_argument("-d", "--dir", 
                        help="Provide a directory of files",
                        action="store", default=None)
    parser.add_argument("-s", "--stat", 
                        help="Show number of changes per file",
                        action="store_true", default=None)
    args = parser.parse_args()

    # store the values from the flags in vars
    nfile = args.file
    output = args.output
    nflag = args.n
    directory = args.dir
    stat = args.stat

    return nfile, output, nflag, directory, stat


def num_contig(matchobj):
    """Get the match object and use a global counter
    to increment the replacement text.

    Args:
        matchobj (object): match from a regex function

    Returns:
        str: the replacement text
    """
    global count
    count += 1
    return f'\n>Contig_new_{count}\n'


def return_n(matchobj):
    return 'N' * 10000


def replace_file_contents(my_file, replacement, output):
    """Load the file contents, replace the text based on pattern
    and write the new contents to a new file.

    Args:
        my_file (str): path to a file
        replacement (func): the replacement text
        output (str): the output folder

    Returns:
        int: number of occurances of the pattern
    """
    # this will catch groups of two or more Ns
    sub_str = re.compile(r'N{2,}')

    read_data = ''

    # change the new file name, remove any directories if only one file
    new_file = my_file.split('/')[-1].replace('fasta', 'fa')
    
    # try to open the file and load all the data in memory
    try:
        with open(my_file, 'r') as rf:
            read_data = rf.read()
        rf.close()
    except Exception as ex:
        print('Couldn\'t open file\n', ex)
        sys.exit()

    # iterate the data and replace the substring with the new string
    read_data = re.subn(sub_str, repl=replacement, string=read_data)
    
    # write to a file from memory
    try:
        with open(f'{output}/{new_file}', 'w') as wf:
            wf.write(read_data[0])
        wf.close()
    except Exception as ex:
        print('Couldn\'t write to file\n', ex)
        sys.exit()
    
    # return the number of changes per file
    return read_data[1]

def create_output(output):
    """Create the output folder
    check if it already exists first.

    Args:
        output (str): path to the output folder
    """
    # check if the output folder already exists and/or can be created
    if os.path.isdir(output) is False:
        try:
            os.mkdir(output)
        except Exception as ex:
            print('Cannot create output directory!\n', ex)
            sys.exit()


def change_dir(directory):
    """Navigate to the provided directory
    check if it's a valid directory.

    Args:
        directory (str): path to the directory
    """
    try:
        os.chdir(directory)
    except Exception as ex:
        print('Not a valid directory\n', ex)
        sys.exit()

if __name__ == "__main__":
    main()
