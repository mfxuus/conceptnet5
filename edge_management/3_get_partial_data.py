import argparse
import os
import csv
import json
import networkx as nx
import sys

from config import (
    ALL_LANGUAGES, ORIGINAL_CSV,
    ADDITIONAL_EDGES_CSV,
    ADDITIONAL_EDGES_INPUT,
    EN_CSV
)

def get_partial_data(source_csv_file, destination_csv_file, line_count=None):
    i = 0
    with open(source_csv_file, 'r', encoding="utf8") as source, \
         open(destination_csv_file, 'w') as destination:
        datareader = csv.reader(source, delimiter='\t')
        datawriter = csv.writer(destination, delimiter='\t')
        for row in datareader:
            if i % 100000 == 0 and line_count:
                print(f'Processed {i} out of {line_count} edges.')
            edge_relation = row[1]
            node_1 = row[2]
            node_2 = row[3]
            if not node_1.startswith('/c/en/') or not node_2.startswith('/c/en/'):
                i += 1
                continue

            if args.bias:
                #TODO: partial data related to certain bias
                pass

            datawriter.writerow(row)
            i += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    '''
    python 0_get_partial_data.py
    python 0_get_partial_data.py --bias gender 
    '''

    parser.add_argument(
        '--bias',
        nargs='+',
        help='Determine the bias to explore'
    )

    args = parser.parse_args()

    get_partial_data(ORIGINAL_CSV, EN_CSV, 34074917)


