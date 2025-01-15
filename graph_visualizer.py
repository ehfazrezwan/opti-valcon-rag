import os
import json
import networkx as nx
from pyvis.network import Network


def visualize_knowledge_graph(graphml_path, output_path):
    """
    Create an interactive visualization of the knowledge graph.

    Args:
        graphml_path (str): Path to the GraphML file
        output_path (str): Path where the HTML visualization will be saved
    """
    # Create a Pyvis network
    net = Network(
        height="100vh", notebook=False, bgcolor="#ffffff", font_color="#333333"
    )

    # Load the GraphML file
    G = nx.read_graphml(graphml_path)

    # Convert NetworkX graph to Pyvis network
    net.from_nx(G)

    # Define node colors based on type
    node_colors = {
        "ORGANIZATION": "#4CAF50",  # Green
        "CONCEPT": "#2196F3",  # Blue
        "CATEGORY": "#9C27B0",  # Purple
        "EVENT": "#FF5722",  # Deep Orange
        "PERSON": "#E91E63",  # Pink
        "PRODUCT": "#FFC107",  # Amber
        "FEATURE": "#00BCD4",  # Cyan
        "INDUSTRY": "#795548",  # Brown
        "TECHNOLOGY": "#607D8B",  # Blue Grey
    }

    # Style nodes
    for node in net.nodes:
        node_type = G.nodes[node["id"]].get("entity_type", "unknown")
        node["color"] = node_colors.get(node_type, "#999999")

        # Add size based on type
        if node_type in ["ORGANIZATION", "INDUSTRY"]:
            node["size"] = 35  # Largest nodes for major entities
        elif node_type in ["PRODUCT", "TECHNOLOGY", "CONCEPT"]:
            node["size"] = 30  # Medium-large for key technical entities
        elif node_type in ["PERSON", "EVENT"]:
            node["size"] = 25  # Medium size for specific entities
        else:
            node["size"] = 20  # Default size for other types

        # Add tooltips with metadata
        tooltip = f"Type: {node_type}\n"
        for key, value in G.nodes[node["id"]].items():
            if key != "node_type" and value:
                tooltip += f"{key}: {value}\n"
        node["title"] = tooltip

    # Get the network data
    network_data = {
        "nodes": net.nodes,
        "edges": net.edges,
    }

    # Create custom HTML using f-string instead of % formatting
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Knowledge Graph Visualization</title>
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.2/dist/vis-network.min.js"></script>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.2/dist/dist/vis-network.min.css" rel="stylesheet" type="text/css" />
        <style type="text/css">
            #mynetwork {{
                width: 100%;
                height: 100vh;
                background-color: #ffffff;
            }}
            body {{
                margin: 0;
                padding: 0;
            }}
        </style>
    </head>
    <body>
        <div id="mynetwork"></div>
        <script type="text/javascript">
            var network_data = {json.dumps(network_data)};
            
            var container = document.getElementById('mynetwork');
            var options = {{
                physics: {{
                    forceAtlas2Based: {{
                        springLength: 200,
                        springConstant: 0.05
                    }},
                    minVelocity: 0.75,
                    solver: "forceAtlas2Based"
                }},
                edges: {{
                    smooth: {{
                        type: "continuous",
                        forceDirection: "none"
                    }}
                }}
            }};
            
            var network = new vis.Network(container, network_data, options);
        </script>
    </body>
    </html>
    """

    # Save the HTML file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_template)

    print(f"\nVisualization saved to: {output_path}")


if __name__ == "__main__":
    # Example usage
    working_dir = "./rag_storage/valcon-data"
    graphml_path = os.path.join(working_dir, "graph_chunk_entity_relation.graphml")
    output_path = os.path.join(working_dir, "knowledge_graph.html")

    visualize_knowledge_graph(graphml_path, output_path)
