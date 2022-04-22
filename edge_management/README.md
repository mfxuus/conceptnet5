## Setup
- Config files
    - Checkout `config.py` and potentially make a `local_config.py`
- Install networkx
    - `pip install -r requirements.txt`
- Download official txt file (assertions.csv) and place in `local_data/`
    - [link](https://github.com/commonsense/conceptnet5/wiki/Downloads)
- (Optional) Create a smaller dataset that only contains english words
    - Set up an EN_CSV variable
    - `python 3_get_partial_data.py`
    - Then remember to change the input ORIGINAL_CSV in config.py
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

## To predict knowledge graph completion novel edges
- Build formatted subgraph edges for training
    - `python 3_get_partial_data.py --kgc`
- Train model to make predictions
    - Create EMPTY_CSV, just add one row from KGC_CSV to EMPTY_CSV to pass the pykeen pipeline. 
    - `python 4_knowledge_graph_completion_demo.py` train new model then predict
    - `python 4_knowledge_graph_completion_demo.py --eval` load model to make predictions
    
## To evaluate numberbatch embeddings
- Format edges for retrofitting
    - `python 2_format_new_edges.py --for-retrofit` (for external edges)
    - `python 2_format_new_edges.py --from-kgc --for-retrofit` (for KGC edges)
- Apply retrofitting
    - `python 5_run_numberbatch_retrofitting.py` (for external edges)
    - `python 5_run_numberbatch_retrofitting.py --from-kgc` (for KGC edges)
- Evaluation
    - `python 6_run_numberbatch_retrofitting.py` (for external edges)
    - `python 6_run_numberbatch_retrofitting.py --from-kgc` (for KGC edges)


## Available ConceptNet graph completion models
- [Commonsense Knowledge Base Completion with Structural and Semantic Context](https://github.com/allenai/commonsense-kg-completion)
- [Conv-TransE](https://github.com/JD-AI-Research-Silicon-Valley/SACN)
- [InductivE](https://github.com/BinWang28/InductivE)