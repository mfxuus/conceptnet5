## Setup
- Config files
	- Checkout `config.py` and potentially make a `local_config.py`
- Install networkx
	- `pip install -r requirements.txt`
- Download official txt file (assertions.csv) and place in `local_data/`
	- [link](https://github.com/commonsense/conceptnet5/wiki/Downloads)
- Build a networkx directed graph for easier inspection
	- `python 0_build_graph.py`
	- See script for options. Only tried building English subgraph..
- Can interact with the built graph a bit; limited functionality
	- `python 1_explore_graph.py`

## To add new edges
- Modify `new_edges.txt`
	- Each line: node_1, node_2, relation type, weight
- Run script to create formatted csv file
	- `python 2_format_new_edges.py`
- Can build new networkx graph with custom edge included
	- `python 0_build_graph.py --include-custom`
- Interact with graph with custom edges
	- `python 1_explore_graph.py --include-custom`
- When we eventually need to have a single file, can in theory just combine
	`ADDITIONAL_EDGES_CSV` with the official `assertions.csv`
