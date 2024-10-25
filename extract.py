from exiftool import ExifToolHelper
import argparse
from pathlib import Path
import json
import threading
import signal
import numpy as np

import logging

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', help='The directory of images',
                        required=True)
    parser.add_argument('-o', '--output', help='The file name to write. Regardless of extension, output will be in json.',
                        default='out.json')
    return parser.parse_args()

def slice_files_into_16(files_list):
    files = np.array(files_list)
    
    split_indices = np.array_split(np.arange(len(files)), 16)
    files_lists = [files[indices] for indices in split_indices]
    
    return files_lists

def extract(files, output):
    print(files)
    logging.basicConfig(level=logging.DEBUG)
    with ExifToolHelper(logger=logging.getLogger(__name__)) as et:
        metadata = et.get_metadata(files)

        # opens in "append" mode
        with open(output, 'a') as out_file:
            out_file.write('[\n')

            for i, d in enumerate(metadata):
                out_file.write(json.dumps(d, indent=2))

                if i < len(metadata) - 1:
                    out_file.write(",\n")
                else:
                    out_file.write("\n")

            out_file.write(']\n')

def main():
    args = parse_arguments()
    all_files = [str(path) for path in Path(args.directory).rglob("*.jpg")]
    file_groups = slice_files_into_16(all_files)
    
    extract(file_groups[0], args.output)
    

if __name__ == '__main__':
    main()
