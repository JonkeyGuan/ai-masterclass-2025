# Unit 2 - Building RAG and Agent Applications with Docling

This unit is focused on using [Docling](https://github.com/docling-project) and integrating it into Llama Stack use cases.

Useful references:

- [Docling Project on GitHub](https://github.com/docling-project)
    - [`docling`](https://github.com/docling-project/docling) repository
    - [`docling-core`](https://github.com/docling-project/docling-core) repository
    - [`docling-serve`](https://github.com/docling-project/docling-serve) repository
- [Documentation](https://docling-project.github.io/docling/)

## Schedule

| Time | Activity |
| -----|----------|
| 9:00-12:00 | Docling |
| | Introduction to Docling |
| | Converting documents with Docling including advanced features |
| 12:00-13:00 | Lunch and discussions |
| 13:00-16:00 | Docling + Llama Stack + Agents |
| | Build your DocumentAI use-case with Llama Stack |
| | Use Docling within your Llama Stack agents |


## Part 1 - Getting started

All the content for this part is available in the Docling docs:
- [Installation](https://docling-project.github.io/docling/installation/)
- [Examples](https://docling-project.github.io/docling/examples/)

In a nutshell, install Docling in a new Python virtual environment.

```shell
# Create a new venv
python -m venv venv

# Activate the venv
source venv/bin/activate

# Install Docling
pip install "docling[vlm]"
```

_Note: if you prefer, use `uv venv` and `uv pip "docling[vlm]"` instead of the commands above._

To verify the installation, try out the Docling CLI

```shell
docling --version
```

### Tasks

1. Install Docling
2. Convert some of your documents
3. Inspect some of the tables
4. Inspect the figures
5. Enable picture classification and description
6. Chunk your document
7. Customize the output


## Part 2 - Llama Stack and Docling


### Setup

Extend your environment with the additional packages required for this part:

```shell
pip install matplotlib pillow rich
```

### Tasks

1. Use Docling for document conversion in Llama Stack
2. Multi-modal RAG
3. Visual grounding

### Playbook

Check out the [advanced RAG notebook](./advanced_rag.ipynb) for a deep dive on using
Docling's powerful capabilities for RAG with Llama Stack.

### Resources

Need more details on some of the underlying concepts? The following resources can
provide useful hints:

- [Hybrid chunking](https://docling-project.github.io/docling/examples/hybrid_chunking/)
- [Serialization](https://docling-project.github.io/docling/examples/serialization/)
- [Picture annotation](https://docling-project.github.io/docling/examples/pictures_description/)

## Part 3 - Agents and Docling

Simple MCP skeleton

```py
from llama_stack_client import LlamaStackClient
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("Docling Documents Ingest")

@mcp.tool()
def ingest_document_to_vectordb(source: str, vector_db_id: str):
    """
    Ingest source documents into the vector database for using them in RAG applications.

    :param source: The http source document to ingest
    :param vector_db_id: The llama stack vector_db_id
    :returns: Filename of the file which has been ingested
    """

    print(f"{source=}")
    print(f"{vector_db_id=}")

    return "filename"


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="sse")
```

_Note: When implementing an MCP tool, the docstring is very important, because it will be used by the LLM to orchestrate the flow._

### Tasks

1. Build a Docling agent and connect it to Llama Stack
    - Add a tool which will perform the "Ingest document XYZ"
    - [Optional] Keep a local cache of converted documents to avoid repeated convert
    - [Optional] Allow metadata search (e.g. publication year or affilition) to select the documents.
2. Deploy your MCP tool in OpenShift
3. Run all-in-one with the Llama Stack Playground UI
