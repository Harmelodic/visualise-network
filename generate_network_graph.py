"""
A script to generate a network graph visualisation from CSV data.
"""

import argparse

import networkx
import pandas
from pyvis.network import Network

if __name__ == "__main__":
    # Get arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-csv", type=str, default="data.csv")
    parser.add_argument("--output-html", type=str, default="graph.html")
    args = parser.parse_args()

    input_file = args.input_csv
    output_file = args.output_html

    # Get data from CSV file into a DataFrame:
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html
    dataframe = pandas.read_csv(input_file)

    # Create an in-memory graph to play with:
    # https://networkx.org/documentation/stable/reference/classes/digraph.html
    directed_graph = networkx.DiGraph()

    # Iterate over each row in the DataFrame
    # and add an "edge" (a line) between nodes, into the graph.
    for _, row in dataframe.iterrows():
        source_node = row["source_node"]
        destination_node = row["destination_node"]
        weight = int(row["weight"])
        directed_graph.add_edge(source_node, destination_node, weight=weight)

    # Create a canvas for visualising a Network:
    network_canvas = Network(notebook=False, height="1000px", width="1000px", directed=True)

    # Configure physics of visualisation (don't have to do this)
    network_canvas.repulsion(
        node_distance=400, # This is the range of influence for the repulsion.
        central_gravity=3, # The gravity attractor to pull the entire network to the center.
        spring_length=240, # The rest length of the edges
        spring_strength=0.5, # How strong the edges springs are

        # A value ranging from 0 to 1 of how much of the velocity from the previous
        # physics simulation iteration carries over to the next iteration.
        damping=1
    )

    # We could just load in the networkx directed graph directly into the pyvis Network canvas,
    # but this produces weird results when using big numbers:
    # network_canvas.from_nx(directed_graph)
    # network_canvas.show("direct_from_networkx_graph.html")

    # Get the DegreeView of the graph
    # (node degree = number of edges adjacent (connected to) to node)
    # https://networkx.org/documentation/stable/reference/classes/generated/networkx.DiGraph.degree.html
    graph_degree_view = dict(directed_graph.degree())

    # Find out the max degree available in the degree view.
    MAX_DEGREE = max(graph_degree_view.values()) if graph_degree_view else 1

    # Add the graph nodes to the network canvas.
    for node in directed_graph.nodes():
        network_canvas.add_node(
            str(node),
            # size == relative to the number of edges adjacent to the node.
            size=(graph_degree_view.get(node, 0) / MAX_DEGREE) * 50,
            color="#00b300",
            font={"color": "#333333"}
        )

    # Figure out max weight in the network
    MAX_WEIGHT = max(networkx.get_edge_attributes(directed_graph, "weight").values())\
        if directed_graph.edges() else 1

    # Add the graph "edges" (lines) to the canvas.
    for source_node, destination_node, data in directed_graph.edges(data=True):
        weight = data["weight"]
        network_canvas.add_edge(
            source_node,
            destination_node,
            weight=weight,
            width=(weight / MAX_WEIGHT) * 10, # Relative weight of the edge
            color="#aaaaaa"
        )

    # Render the graph to an HTML file.
    network_canvas.show(output_file, notebook=False)
