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
python3 -m venv venv

# Activate the venv
source venv/bin.activate

# Install Docling
pip3 install "docling[vlm]"
```

_Note: if you prefer, use `uv venv` and `uv pip "docling[vlm]"` instead of the commands above._

To verify the installtion, try out the Docling CLI

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

TBA

### Tasks

1. Use Docling for document conversion in Llama Stack
2. Multi-modal RAG
3. Visual grounding


## Part 3 - Agents and Docling

TBA

### Tasks

1. Build a Docling agent and connect it to Llama Stack
2. Deploy your MCP tool in OpenShift
3. Run all-in-one with the Llama Stack Playground UI
