from functools import lru_cache
from pathlib import Path
import re
from typing import Optional

from docling.chunking import DocMeta, HybridChunker
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
)
from docling.document_converter import DocumentConverter, FormatOption, PdfFormatOption
from docling_core.transforms.chunker.tokenizer.huggingface import HuggingFaceTokenizer
from llama_stack_client import LlamaStackClient
from mcp.server.fastmcp import FastMCP
from pydantic_settings import BaseSettings, SettingsConfigDict
from transformers import AutoTokenizer
import pandas as pd

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="DOCLING_MCP_",
        env_file=".env",
        extra="allow",
    )

    llama_stack_url: str = "http://localhost:8321"
    vdb_embedding: str = "all-MiniLM-L6-v2"

    data_dir: Path = Path(__file__).parent / "data"


settings = Settings()
mcp = FastMCP("Docling Documents Ingest")

@lru_cache
def get_converter() -> DocumentConverter:
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = False

    format_options: dict[InputFormat, FormatOption] = {
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options),
    }

    return DocumentConverter(format_options=format_options)


@lru_cache
def get_llama_stack_client():
    client = LlamaStackClient(
        base_url=settings.llama_stack_url,
    )
    return client


@lru_cache
def get_metadata_table():
    pattern = re.compile(r"([0-9]{4})/([a-zA-Z]+)/(.+)")
    metadata = []
    for filename in settings.data_dir.glob("**/*.pdf"):
        match = pattern.search(str(filename))
        metadata.append({
            "uri": f"file://{filename.absolute()}",
            "year": int(match.group(1)),
            "affiliation": match.group(2),
            "name": match.group(3),
        })

    return pd.DataFrame(metadata)


@mcp.tool()
def search_files_metadata(year: Optional[int]=None, affiliation: Optional[str]=None):
    """
    List the source files which are matching the provided criteria.
    The returned files can be used for search after they are processed witht the ingest_to_vectordb(source) tool.

    :param year: The publication year. This parameter is optional, if not provided all years are matched.
    :param affiliation: The affiliation of the authors. This parameter is optional, if not provided all affiliations are matched.
    :returns: List of files matching the criteria
    """

    print(f"search_files_metadata: {year=}, {affiliation=}")

    df_meta = get_metadata_table()

    df_selection = df_meta
    if year is not None:
        df_selection = df_selection[df_selection["year"] == year]
    if affiliation is not None:
        df_selection = df_selection[df_selection["affiliation"] == affiliation]

    files = df_selection["uri"].to_list()
    print(f"{files=}")
    return files


@mcp.tool()
def ingest_document_to_vectordb(source: str, vector_db_id: str):
    """
    Ingest source documents into the vector database for using them in RAG applications.

    :param source: The http source document to ingest
    :param vector_db_id: The llama stack vector_db_id
    # :returns: Filename of the file which has been ingested
    """

    print(f"{source=}")
    print(f"{vector_db_id=}")

    if source.startswith("file://"):
        source = Path(source.replace("file://", ""))
    converter = get_converter()
    result = converter.convert(source)
    doc = result.document
    print(f"{result.status=}")

    tokenizer = HuggingFaceTokenizer(
        tokenizer=AutoTokenizer.from_pretrained(
            pretrained_model_name_or_path=f"sentence-transformers/{settings.vdb_embedding}"
        )
    )
    chunker = HybridChunker(tokenizer=tokenizer)

    chunk_iter = chunker.chunk(dl_doc=doc)

    ls_chunks = []
    for i, chunk in enumerate(chunk_iter):
        meta = DocMeta.model_validate(chunk.meta)

        enriched_text = chunker.contextualize(chunk=chunk)

        token_count = tokenizer.count_tokens(enriched_text)
        chunk_dict = {
            "content": enriched_text,
            "mime_type": "text/plain",
            "metadata": {
                "document_id": f"{doc.origin.binary_hash}",
                "token_count": token_count,
                "doc_items": [item.self_ref for item in meta.doc_items],
            },
        }
        ls_chunks.append(chunk_dict)

    client = get_llama_stack_client()
    client.vector_io.insert(
        vector_db_id=vector_db_id,
        chunks=ls_chunks,
    )

    return result.input.file.name


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="sse")
