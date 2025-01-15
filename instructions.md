# LightRAG CLI Instructions

LightRAG CLI is a command-line interface tool for managing and interacting with your RAG (Retrieval-Augmented Generation) system. This document provides detailed instructions for using each command.

## Getting Started

To use the LightRAG CLI, navigate to the project directory and run commands using Python:

```bash
python app.py [COMMAND] [OPTIONS]
```

To see all available commands:

```bash
python app.py --help
```

## Available Commands

### 1. Data Ingestion

The `ingest` command allows you to load data from one or multiple directories into the RAG system.

```bash
# Ingest from a single directory
python app.py ingest -p "./data/directory1"

# Ingest from multiple directories (comma-separated, no spaces)
python app.py ingest -p "./data/directory1,./data/directory2,./data/directory3"

# Using the long form option
python app.py ingest --paths "./data/directory1,./data/directory2"
```

**Options:**

- `-p, --paths`: Required. Comma-separated list of directory paths to ingest data from.

### 2. Knowledge Graph Visualization

The `visualize` command generates an interactive visualization of your knowledge graph.

```bash
python app.py visualize
```

The visualization will be saved as an HTML file in the `lightrag_test_run` directory as `knowledge_graph.html`. You can open this file in any web browser to explore the knowledge graph.

### 3. Running Queries

The `query` command allows you to ask questions about your ingested data.

```bash
# Interactive mode (will prompt for query)
python app.py query

# Direct query mode
python app.py query -q "Your question here"

# Using the long form option
python app.py query --query "Your question here"
```

**Options:**

- `-q, --query`: Optional. The query text. If not provided, you'll be prompted to enter it.

Query results are automatically saved as Markdown files in the `lightrag_test_run/outputs` directory with timestamps in their filenames (e.g., `query_result_20240315_143022.md`).

## Output Directory Structure

The CLI creates and maintains the following directory structure:

```
lightrag_test_run/
├── graph_chunk_entity_relation.graphml  # Knowledge graph data
├── knowledge_graph.html                 # Interactive visualization
└── outputs/                            # Query results
    └── query_result_[timestamp].md     # Individual query results
```

## Error Handling

- The CLI will validate all provided directory paths before ingestion
- Invalid paths will be reported with clear error messages
- All operations provide feedback about their progress and completion status

## Tips

1. When ingesting data from multiple directories, ensure there are no spaces after the commas in the path list
2. Query results are saved in Markdown format for better readability and organization
3. The visualization can be large for complex knowledge graphs - use a modern web browser for best performance
4. Each query generates a new file with a unique timestamp to prevent overwriting previous results
