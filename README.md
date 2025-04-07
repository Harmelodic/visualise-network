# visualise-network

A simple script to visualise a network from some data.

Written in Python.

## This uses

- pandas for doing managing data structures: https://pandas.pydata.org/pandas-docs/stable/reference/index.html
- NetworkX for doing network analysis / graphing: https://networkx.org/documentation/stable/reference/index.html
- pyvis for visualising network graphs: https://pyvis.readthedocs.io/en/latest/tutorial.html

## Setup

Ensure Python (3+) is installed on your machine and clone/checkout this repository, then:

```bash
# Setup a virtual environment (venv)
python -m venv ./venv

# Activate the venv
source venv/bin/activate
# Deactivate anytime with
deactivate

# Install dependencies
pip install -r requirements.txt
```

## Running

Run the script:

```bash
python ./generate_network_graph.py 
```
