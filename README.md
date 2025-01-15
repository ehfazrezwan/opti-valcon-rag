# Optimizely Knowledge Graph RAG Implementation

## Background

This project emerged from identifying a critical business need at Optimizely's Value Consulting team: leveraging historical client success data to enhance lead scoring and ROI predictions.

Even though I don't have access to the proprietary data that would allow this tool to shine, with a wealth of customer success stories and product implementation data publicly available, there was an opportunity to create an intelligent system that could analyze patterns and relationships across Optimizely's ecosystem.

The implementation uses advanced RAG (Retrieval Augmented Generation) techniques combined with knowledge graphs to create an AI assistant that understands not just the content, but the relationships between various entities in Optimizely's business context - from products and industries to use cases and success metrics.

## Why LightRAG?

Traditional RAG implementations often treat documents as independent chunks of text, potentially missing important connections between related pieces of information. LightRAG was chosen for this project because it:

1. Implements knowledge graphs to maintain relationships between entities, providing richer context for queries
2. Allows for hybrid search combining semantic similarity with graph-based relevance
3. Provides built-in support for entity extraction and relationship mapping
4. Offers flexible visualization capabilities for knowledge graph exploration
5. Maintains the context of relationships between customers, products, and use cases when responding to queries

## Features

- **Data Ingestion**: Automatically processes and structures data into a knowledge graph
- **Intelligent Querying**: RAG-enhanced chatbot that leverages both semantic search and graph relationships
- **Knowledge Graph Visualization**: Interactive visualization of entity relationships
- **Dual Interfaces**:
  - CLI tool for data ingestion, querying, and visualization
  - StreamLit-based web interface for interactive chat

## Technical Architecture

The system is built using the following core technologies:

- LightRAG for the RAG framework and knowledge graph implementation
- StreamLit for the web interface
- OpenAI's models for LLM capabilities and embeddings
- networkx, pyvis, and streamlit-agraph for graph visualization
- Click for CLI framework

## Setup and Installation

### Prerequisites

- Docker and Docker Compose
- OpenAI API key
- Python 3.8+

### Environment Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd <repository-name>
```

2. Create a `.env` file in the root directory:

```bash
OPENAI_API_KEY=your_api_key_here
```

3. Start the application using Docker Compose:

```bash
docker compose up
```

The web interface will be available at `http://localhost:8501`

### Project Structure

```
.
├── app.py              # CLI implementation
├── Home.py            # StreamLit web interface
├── data/              # Data storage directory
├── rag_storage/       # LightRAG working directory
├── inputs/            # Input data directory
├── outputs/           # Query results and outputs
└── docker-compose.yml # Docker configuration
```

## Usage

### CLI Interface

1. Data Ingestion:

```bash
python app.py ingest --paths "./data1,./data2"
```

2. Generate Knowledge Graph Visualization:

```bash
python app.py visualize
```

3. Query the System:

```bash
python app.py query --query "Your query here"
```

### Web Interface

1. Navigate to `http://localhost:8501`
2. Use the chat interface to interact with the AI assistant
3. Explore the knowledge graph visualization in the dedicated tab

## Data Sources

The system currently incorporates:

- 255+ Optimizely customer case studies
- Detailed product information and specifications
- Industry-specific implementation patterns
- Success metrics and ROI data

## Future Enhancements

- Integration with Neo4j for more advanced graph operations (configuration available in docker-compose.yml)
- Enhanced visualization capabilities
- Additional data source integrations
- Automated data refresh pipeline

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Insert appropriate license information]
