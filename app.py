import os
import click
from datetime import datetime
from typing import List
from lightrag import LightRAG, QueryParam
from lightrag.llm import gpt_4o_mini_complete, gpt_4o_complete
from graph_visualizer import visualize_knowledge_graph
from data_ingestor import ingest_data

WORKING_DIR = "./rag_storage/valcon-data"
OUTPUT_DIR = "./outputs"


class LightRAGCLI:
    def __init__(self):
        # Initialize working directory
        if not os.path.exists(WORKING_DIR):
            os.mkdir(WORKING_DIR)

        # Initialize LightRAG
        self.rag = LightRAG(
            working_dir=WORKING_DIR, llm_model_func=gpt_4o_mini_complete
        )

    def ingest_data(self, data_paths: List[str]):
        """
        Ingest data from specified paths.

        Args:
            data_paths: List of directory paths to ingest data from
        """
        # Validate paths exist
        invalid_paths = [path for path in data_paths if not os.path.exists(path)]
        if invalid_paths:
            click.echo(
                f"❌ Error: The following paths do not exist: {', '.join(invalid_paths)}"
            )
            return

        click.echo(f"🔄 Ingesting data from: {', '.join(data_paths)}")
        ingest_data(self.rag, data_paths)
        click.echo("✅ Data ingestion completed successfully!")

    def visualize(self):
        """Generate and save knowledge graph visualization."""
        click.echo("🔄 Generating visualization...")
        graphml_path = os.path.join(WORKING_DIR, "graph_chunk_entity_relation.graphml")
        output_path = os.path.join(OUTPUT_DIR, "knowledge_graph.html")
        visualize_knowledge_graph(graphml_path, output_path)
        click.echo(f"✅ Visualization saved to {output_path}")

    def run_query(self, query_text: str):
        """Run a query and save results."""
        click.echo("🔄 Processing query...")

        # Create outputs directory if it doesn't exist
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        # Generate timestamp for unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(OUTPUT_DIR, f"query_result_{timestamp}.md")

        # Run query and write results
        result = self.rag.query(query_text, param=QueryParam(mode="hybrid"))

        with open(output_file, "w", encoding="utf-8") as f:
            f.write("# Query Results\n\n")
            f.write(f"Query: {query_text}\n\n")
            f.write("---\n\n")
            f.write(result)

        click.echo(f"✅ Query results saved to {output_file}")
        return output_file


@click.group()
def cli():
    """LightRAG CLI - A tool for data ingestion, querying, and visualization."""
    pass


@cli.command()
@click.option(
    "--paths",
    "-p",
    required=True,
    help='Comma-separated list of directory paths to ingest data from (e.g., "./data1,./data2")',
)
def ingest(paths):
    """Ingest data from specified directory paths."""
    # Split the comma-separated paths and strip whitespace
    data_paths = [path.strip() for path in paths.split(",")]
    rag_cli = LightRAGCLI()
    rag_cli.ingest_data(data_paths)


@cli.command()
def visualize():
    """Generate knowledge graph visualization."""
    rag_cli = LightRAGCLI()
    rag_cli.visualize()


@cli.command()
@click.option(
    "--query", "-q", prompt="Enter your query", help="The query text to process"
)
def query(query):
    """Run a query on the ingested data."""
    rag_cli = LightRAGCLI()
    output_file = rag_cli.run_query(query)


if __name__ == "__main__":
    cli()
