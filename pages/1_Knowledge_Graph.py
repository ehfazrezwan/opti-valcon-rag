import streamlit as st
import networkx as nx
from streamlit_agraph import agraph, Node, Edge, Config
import os

# Set page config
st.set_page_config(page_title="Knowledge Graph", page_icon="🕸️", layout="wide")

st.title("Knowledge Graph Visualization")

st.markdown(
    """
## Interactive Knowledge Graph

This visualization shows the knowledge graph representation of your documents, including:
- Document chunks as nodes
- Entities extracted from the text
- Relationships between different pieces of information

You can:
- Drag nodes to rearrange the graph
- Zoom in/out using the mouse wheel
- Click on nodes to see more details
"""
)

# Add control sidebar
with st.sidebar:
    st.header("Graph Controls")
    physics_enabled = st.toggle("Enable Physics", value=True)
    show_labels = st.toggle("Show Edge Labels", value=True)
    graph_height = st.slider(
        "Graph Height", min_value=400, max_value=1000, value=600, step=50
    )

    st.markdown("---")
    st.header("Node Types")
    node_colors = {
        "ORGANIZATION": "#4CAF50",
        "CONCEPT": "#2196F3",
        "CATEGORY": "#9C27B0",
        "EVENT": "#FF5722",
        "PERSON": "#E91E63",
        "PRODUCT": "#FFC107",
        "FEATURE": "#00BCD4",
        "INDUSTRY": "#795548",
        "TECHNOLOGY": "#607D8B",
    }

    # Display color legend
    for node_type, color in node_colors.items():
        st.markdown(
            f'<span style="color:{color}">●</span> {node_type}', unsafe_allow_html=True
        )


def load_and_convert_graph():
    working_dir = "./valcon-data"
    graphml_path = os.path.join(working_dir, "graph_chunk_entity_relation.graphml")

    if not os.path.exists(graphml_path):
        raise FileNotFoundError(f"Knowledge graph file not found at {graphml_path}")

    # Load the GraphML file
    G = nx.read_graphml(graphml_path)

    # Convert to agraph format
    nodes = []
    edges = []

    # Add nodes
    for node_id in G.nodes():
        node_data = G.nodes[node_id]
        # Debug: Print node data
        # print(f"Node ID: {node_id}, Data: {node_data}")  # Debug statement

        node_type = node_data.get("entity_type", "unknown")
        print("node type")
        print(node_type)

        # Determine node size based on type
        if node_type in ["ORGANIZATION", "INDUSTRY"]:
            size = 35
        elif node_type in ["PRODUCT", "TECHNOLOGY", "CONCEPT"]:
            size = 30
        elif node_type in ["PERSON", "EVENT"]:
            size = 25
        else:
            size = 20

        # Create tooltip with formatted text
        tooltip = [f"Type: {node_type}"]
        for key, value in node_data.items():
            if key != "d0" and value:
                tooltip.append(f"{key}: {value}")

        # Get display label (use 'text' attribute if available, otherwise use node_id)
        display_label = node_data.get("text", str(node_id))
        if len(display_label) > 30:  # Truncate long labels
            display_label = display_label[:27] + "..."

        nodes.append(
            Node(
                id=node_id,
                label=display_label,
                size=size,
                color=node_colors.get(node_type, "#999999"),
                title="\n".join(tooltip),
            )
        )

    # Debug: Print number of nodes created
    print(f"Total nodes created: {len(nodes)}")  # Debug statement

    # Add edges
    for source, target, data in G.edges(data=True):
        edge_label = data.get("relation", "") if show_labels else ""
        edges.append(
            Edge(
                source=source,
                target=target,
                label=edge_label,
                type="",
            )
        )

    return nodes, edges


st.info(
    "Loading the knowledge graph is resource-intensive due to the large number of nodes. Please provide upto 5 minutes to load the graph, and give it some time after it is visible."
)


# Load and convert the graph
if st.button("Load Knowledge Graph"):
    try:
        with st.spinner("Loading knowledge graph..."):
            nodes, edges = load_and_convert_graph()

            # Debug: Print nodes and edges
            print(f"Nodes: {nodes}")  # Debug statement
            print(f"Edges: {edges}")  # Debug statement

            # Configure the graph visualization
            config = Config(
                width="100%",
                height=graph_height,
                directed=True,
                physics={
                    "enabled": physics_enabled,
                    "solver": "forceAtlas2Based",
                    "forceAtlas2Based": {
                        "gravitationalConstant": -50,
                        "centralGravity": 0.01,
                        "springLength": 100,
                        "springConstant": 0.08,
                    },
                },
                nodes={
                    "font": {"size": 12},
                    "borderWidth": 1,
                    "borderWidthSelected": 2,
                    "shape": "dot",
                    "scaling": {"min": 20, "max": 35},
                },
                edges={
                    "font": {"size": 8},
                    "smooth": {"type": "continuous"},
                    "arrows": {"to": {"enabled": True}},
                    "color": {"inherit": False},
                    "width": 1,
                },
                interaction={
                    "hover": True,
                    "navigationButtons": True,
                    "multiselect": True,
                },
                layout={"improvedLayout": True, "randomSeed": 42},
            )

            # Render the graph
            agraph(nodes=nodes, edges=edges, config=config)

            # Display graph statistics
            st.sidebar.markdown("---")
            st.sidebar.header("Graph Statistics")
            st.sidebar.markdown(f"- **Nodes**: {len(nodes)}")
            st.sidebar.markdown(f"- **Edges**: {len(edges)}")

    except FileNotFoundError as e:
        st.error("Knowledge graph file not found.")
        st.info("Please generate a knowledge graph first by processing some documents.")
    except Exception as e:
        st.error(f"Error loading the knowledge graph: {str(e)}")
        st.info(
            "If the error persists, please check the console logs for more details."
        )
