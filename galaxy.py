"""
This script explores a gigantic json file contained inside a galaxy.json.gz file and prints out the number of rows
contained inside.
"""

import json
import gzip


def main():
    galaxy_file_path = 'galaxy.json.gz'
    with gzip.open(galaxy_file_path, 'rt', encoding='utf-8') as f:
        galaxy_data = json.load(f)

    num_rows = len(galaxy_data)
    print(f'The galaxy.json.gz file contains {num_rows} rows.')


if __name__ == '__main__':
    main()
