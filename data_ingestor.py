import os
import glob
from typing import List
from lightrag import LightRAG

def ingest_data(
    rag: LightRAG, data_paths: List[str], file_pattern: str = "*.md"
) -> None:
    """
    Ingest data from multiple directories into LightRAG.

    Args:
        rag: LightRAG instance
        data_paths: List of directory paths containing data files
        file_pattern: Glob pattern for files to ingest (default: "*.md")
    """
    for data_path in data_paths:
        file_path = os.path.join(data_path, file_pattern)
        files = glob.glob(file_path)

        if not files:
            print(f"Warning: No matching files found in {data_path}")
            continue

        print(f"\nProcessing files from: {data_path}")
        for file in files:
            print(f"Ingesting: {file}")
            with open(file) as f:
                content = f.read()
                rag.insert(content) 