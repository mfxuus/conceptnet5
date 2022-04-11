import csv
import os
import sys
import json

from config import (
    ADDITIONAL_EDGES_CSV,
    ADDITIONAL_EDGES_INPUT
)

from utils import rel_is_valid


def generate_new_edges(language_code=None):
    '''
    Takes in file ADDITIONAL_EDGES_INPUT, and make necessary changes to conform to the same
    format as the official assertions.csv
        
        - The URI of the whole edge
        - The relation expressed by the edge
        - The node at the start of the edge
        - The node at the end of the edge
        - A JSON structure of additional information about the edge, such as its weight

    Then output to ADDITIONAL_EDGES_CSV

    '''
    language_code = language_code or 'en'
    edges_to_write = []
    errors = []
    
    with open(ADDITIONAL_EDGES_INPUT, 'r') as f:
        for line in f:
            line_error = []
            node_1, node_2, rel_type, weight = [x.strip() for x in line.split(',')]

            # if not node_1.startswith('/c/en/'):
            #     node_1 = f'/c/{language_code}/{node_1}'
            # if not node_2.startswith('/c/en/'):
            #     node_2 = f'/c/{language_code}/{node_2}'
            # if not rel_is_valid(rel_type):
            #     line_error.append('rel_type')

            # Retrofitting compatible
            if rel_type.startswith('/r/'):
                rel_type = rel_type[3:]
            node_1 = node_1.strip().lower().replace(' ', '_')
            node_2 = node_2.strip().lower().replace(' ', '_')

            #TODO: temp rescale
            weight = float(weight)/10.

            try:
                weight = round(float(weight), 2)
            except:
                line_error.append('weight')
            edge_uri = f'/a/[{rel_type},{node_1}/,{node_2}/]'
            edge_data = json.dumps({'source': 'custom', 'weight': weight})
            edges_to_write.append((
                # edge_uri, rel_type, node_1, node_2, edge_data

                # Retrofitting compatible
                node_1, node_2, weight, 'custom', rel_type
            ))
            if len(line_error) > 0:
                errors.append((line, ','.join(line_error)))

    if len(errors) > 0:
        print('Found errors in input file, please correct.')
        for item in errors:
            print(f'Line: {item[0]}')
            print(f'Errors: {item[1]}')
        return

    # else we write the edges to ADDITIONAL_EDGES_CSV
    with open(ADDITIONAL_EDGES_CSV, 'w', newline='', encoding='utf8') as csvfile:
        datawriter = csv.writer(csvfile, delimiter='\t')
        for row in edges_to_write:
            datawriter.writerow(row)


if __name__ == '__main__':
    if not os.path.exists(ADDITIONAL_EDGES_INPUT):
        print(f'Please create input file at: {ADDITIONAL_EDGES_INPUT}')
        sys.exit()
    generate_new_edges()
