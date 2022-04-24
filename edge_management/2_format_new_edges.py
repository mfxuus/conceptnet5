import csv
import os
import sys
import json
import argparse
import pandas as pd

from config import (
    ADDITIONAL_EDGES_CSV,
    ADDITIONAL_EDGES_INPUT,
    ADDITIONAL_EDGES_RETROFIT_CSV,
    #UNIQUE_NODES,
    KGC_EDGES_CSV,
    KGC_EDGES_RETROFIT_CSV,
)

from utils import rel_is_valid


def generate_new_edges(language_code=None, for_retrofit=False, from_kgc=False):
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
    # unique_nodes = set()
    errors = []

    if from_kgc:
        edges_df = pd.read_csv(KGC_EDGES_CSV)
        for i in range(len(edges_df)):
            node_1 = edges_df.loc[i, "head_label"]
            node_2 = edges_df.loc[i, "tail_label"]
            rel_type = edges_df.loc[i, "relation_label"]
            weight = edges_df.loc[i, "score"]
            if weight < 3.4:  # manual threshold
                continue

            if for_retrofit:
                # Retrofitting compatible
                if rel_type.startswith('/r/'):
                    rel_type = rel_type[3:]

                # TODO: temp rescale
                weight = int(weight) / 10.
                edges_to_write.append((
                    node_1, node_2, weight, 'kgc', rel_type
                ))
            else:
                print('There is no implementation for non-retrofitting format for kgc data')
                return
    else:
        with open(ADDITIONAL_EDGES_INPUT, 'r') as f:
            for line in f:
                line_error = []
                node_1, node_2, rel_type, weight = [x.strip() for x in line.split(',')]
                node_1 = node_1.strip().lower().replace(' ', '_')
                node_2 = node_2.strip().lower().replace(' ', '_')

                # unique_nodes.add(node_1)
                # unique_nodes.add(node_2)

                if for_retrofit:
                    # Retrofitting compatible
                    if rel_type.startswith('/r/'):
                        rel_type = rel_type[3:]

                    # TODO: temp rescale
                    weight = float(weight)/10.

                else:
                    # node_1 = node_1.strip().replace(' ', '_').lower()
                    # node_2 = node_2.strip().replace(' ', '_').lower()
                    if not node_1.startswith('/c/en/'):
                        node_1 = f'/c/{language_code}/{node_1}'
                    if not node_2.startswith('/c/en/'):
                        node_2 = f'/c/{language_code}/{node_2}'
                    if not rel_is_valid(rel_type):
                        line_error.append('rel_type')
                    try:
                        weight = round(float(weight), 2)
                    except:
                        line_error.append('weight')
                edge_uri = f'/a/[{rel_type},{node_1}/,{node_2}/]'
                edge_data = json.dumps({'source': 'custom', 'weight': weight})

                if for_retrofit:
                    edges_to_write.append((
                        node_1, node_2, weight, 'stereoset', rel_type
                    ))
                else:
                    edges_to_write.append((
                        edge_uri, rel_type, node_1, node_2, edge_data
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
    out_file = ADDITIONAL_EDGES_RETROFIT_CSV if for_retrofit else ADDITIONAL_EDGES_CSV
    if from_kgc:
        out_file = KGC_EDGES_RETROFIT_CSV
    with open(out_file, 'w', newline='', encoding='utf8') as csvfile:
        datawriter = csv.writer(csvfile, delimiter='\t')
        for row in edges_to_write:
            datawriter.writerow(row)
    #
    # unique_nodes = set(unique_nodes)
    # with open(UNIQUE_NODES, 'w', newline='', encoding='utf8') as csvfile:
    #     datawriter = csv.writer(csvfile, delimiter='\t')
    #     for row in unique_nodes:
    #         datawriter.writerow([row])


if __name__ == '__main__':
    if not os.path.exists(ADDITIONAL_EDGES_INPUT):
        print(f'Please create input file at: {ADDITIONAL_EDGES_INPUT}')
        sys.exit()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--for-retrofit',
        action='store_true',
        default=False,
        help='Generate retrofit-compatible format',
    )
    parser.add_argument(
        '--from-kgc',
        action='store_true',
        default=False,
        help='From knowledge graph completion edges',
    )
    args = parser.parse_args()
    generate_new_edges(for_retrofit=args.for_retrofit, from_kgc=args.from_kgc)
