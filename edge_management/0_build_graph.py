import argparse
import os
import csv
import json
import networkx as nx
import sys
import dgl

from config import (
    ALL_LANGUAGES, ORIGINAL_CSV,
    ADDITIONAL_EDGES_CSV,
    ADDITIONAL_EDGES_INPUT,
    EN_CSV,
)

from utils import build_gml_filename, build_dgl_filename


# where we save the new edges

'''
For now, to examine the current graph, we just need
    - The relation expressed by the edge
    - The node at the start of the edge
    - The node at the end of the edge
    - weight of edge

Can modify script to add in other attributes later if needed
'''

# line_count = 0
# with open(ORIGINAL_CSV, 'r', encoding="utf8") as csvfile:
#     datareader = csv.reader(csvfile, delimiter='\t')
#     for row in datareader:
#         line_count += 1


def add_edge_to_graph_from_file(graph, csv_file, all_languages, line_count=None):
    i = 0
    with open(csv_file, 'r', encoding="utf8") as csvfile:
        datareader = csv.reader(csvfile, delimiter='\t')
        for row in datareader:
            if i % 100000 == 0 and line_count:
                print(f'Processed {i} out of {line_count} edges.')
            edge_relation = row[1]
            node_1 = row[2]
            node_2 = row[3]
            #TODO: not necessary if process english-only data
            if all_languages is False:
                if not node_1.startswith('/c/en/') or not node_2.startswith('/c/en/'):
                    i += 1
                    continue

            weight = json.loads(row[4]).get('weight', -1)
            graph.add_edge(
                node_1,
                node_2,
                weight=weight,
                rel=edge_relation
            )
            i += 1


def build_graph_from_text(include_custom=False, all_languages=ALL_LANGUAGES, build_dgl=False):
    '''
    include_custom:
        - If True, also takes in ADDITIONAL_TXT as input
        - If False, only takes official assertions.csv as input
    all_languages:
        - If False, ignores edges that touches non-english nodes
    build_dgl:
        - If False, skip building DGL model for GNN training
    '''
    # initiate directed graph
    G = nx.DiGraph()
    # build official edges
    add_edge_to_graph_from_file(G, ORIGINAL_CSV, all_languages, 34074917)
    
    if include_custom is True:
        add_edge_to_graph_from_file(G, ADDITIONAL_EDGES_CSV, all_languages)

    OUT_PATH = build_gml_filename(all_languages, include_custom)
    nx.write_gml(G, OUT_PATH)

    if build_dgl:
        print("Building DGL model...")
        dgl_G = dgl.from_networkx(G)
        OUT_PATH = build_dgl_filename(all_languages, include_custom)
        dgl.data.utils.save_graphs(OUT_PATH, [dgl_G])

if __name__ == '__main__':

    '''
    python 0_build_graph.py
    python 0_build_graph.py --include-custom / --all-languages
    '''

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--include-custom',
        action='store_true',
        default=False,
        help='Builds GML file with official txt file AND custom txt file.',
    )
    parser.add_argument(
        '--all-languages',
        action='store_true',
        default=False,
        help='Builds GML file with ALL language nodes.',
    )
    parser.add_argument(
        '--dgl',
        action='store_true',
        default=False,
        help='Builds DGL model from NetworkX graph for GNN training.',
    )

    args = parser.parse_args()

    if args.all_languages:
        res = input('''
                You're trying to build graph with all nodes.
                This would probably go over the memory limit.
                Are you sure you want to proceed? [Y/n]
            ''')
        if res.lower() not in ['y', 'yes']:
            sys.exit()

    if args.include_custom:
        if not os.path.exists(ADDITIONAL_EDGES_CSV):
            print(f'Please create input file at: {ADDITIONAL_EDGES_INPUT}')
            print(f'And then run script 2_format_new_edges.py to generate custom csv file.')
            sys.exit()

    build_graph_from_text(
        include_custom=args.include_custom,
        all_languages=args.all_languages,
        build_dgl=args.dgl,
    )
