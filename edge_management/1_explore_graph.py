import argparse
import networkx as nx
import sys

from config import (
    ALL_LANGUAGES
)

from utils import build_gml_filename


def load_graph(
        include_custom=False,
        all_languages=ALL_LANGUAGES):
    GML_PATH = build_gml_filename(all_languages, include_custom)
    G = nx.read_gml(GML_PATH)
    return G


def explore(G, edges_for=None, language_code=None):
    language_code = language_code or 'en'
    if edges_for:
        node_str = edges_for.lower().strip()
        if not node_str.startswith('/c/'):
            node_str = f'/c/{language_code}/{node_str}'
        print('\n')
        print('-----------------------------------------------------')
        print(f'*** Predecessors of {edges_for} (total: {G.in_degree(node_str)}) ***')
        for item in G.predecessors(node_str):
            print(item, node_str, G.edges[item, node_str])
        print(f'*** Successors of {edges_for} (total: {G.out_degree(node_str)}) ***')
        for item in G.successors(node_str):
            print(node_str, item, G.edges[node_str, item])
        print('-----------------------------------------------------')
        print('\n')


def check(G, start_node, end_node, language_code=None):
    language_code = language_code or 'en'
    start_node = start_node.lower().strip()
    if not start_node.startswith('/c/'):
        start_node = f'/c/{language_code}/{start_node}'
    end_node = end_node.lower().strip()
    if not end_node.startswith('/c/'):
        end_node = f'/c/{language_code}/{end_node}'
    print('\n')
    print('-----------------------------------------------------')
    print(f'* Edge from {start_node} and {end_node} exists?')
    if G.has_edge(start_node, end_node):
        print('Yes')
        print(start_node, end_node, G.edges[start_node, end_node])
    else:
        print('No')

    print(f'* Edge from {end_node} and {start_node} exists?')
    if G.has_edge(end_node, start_node):
        print('Yes')
        print(end_node, start_node, G.edges[end_node, start_node])
    else:
        print('No')
    print('-----------------------------------------------------')
    print('\n')


if __name__ == '__main__':

    '''
    python 1_explore_graph.py
    '''

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--include-custom',
        action='store_true',
        default=False,
        help='Reads GML file with official txt file AND custom txt file.',
    )
    parser.add_argument(
        '--all-languages',
        action='store_true',
        default=False,
        help='Reads GML file with ALL language nodes.',
    )

    # parser.add_argument(
    #     '--edges-for',
    #     type=str,
    #     required=False,
    #     help='Get edges related to node',
    # )

    args = parser.parse_args()
    print(args)

    try:
        print('Loading GML file. This may take a while.')
        G = load_graph(
            include_custom=args.include_custom,
            all_languages=args.all_languages,
        )
    except Exception as e:
        print('Error loading GML file:')
        print(e)

    print('Graph loaded. What next?')
    while True:
        print('Choices: explore [e], check [c], quit [q]')
        action = input().lower()
        if action not in ['explore', 'e', 'check', 'c', 'quit', 'q']:
            print('Invalid input.')
            continue
        if action in ['q', 'quit']:
            print('Quitting ...')
            sys.exit()
        if action in ['explore', 'e']:
            node_str = input('Which node to explore?\n').lower()
            if len(node_str) < 1:
                print('Invalid input.')
                continue
            explore(G, node_str)
        elif action in ['check', 'c']:
            print('Which edge to check?')
            node_1 = input('Start node: ').lower()
            node_2 = input('End node: ').lower()
            if len(node_1) < 1 or len(node_2) < 1:
                print('Invalid input.')
                continue
            check(G, node_1, node_2)
