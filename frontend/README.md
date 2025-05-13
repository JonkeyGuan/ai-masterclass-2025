# Llama Stack Playground

In this directory we create a container image of the [Llama Stack Playground](https://github.com/meta-llama/llama-stack/tree/main/llama_stack/distribution/ui).
Additionally to the original upstream image, here we [patched the UI](https://github.com/meta-llama/llama-stack/compare/main...dolfim-ibm:llama-stack:docling-mcp) for adding an extra argument when calling the `mcp::docling-llamastack` tool.


## Run the image

```shell
podman run -e LLAMA_STACK_ENDPOINT="http://host.containers.internal:8321" -p 8501:8501 quay.io/drl-masterclass/llama-stack-playground
```

## Build the image

```shell
podman build -t quay.io/drl-masterclass/llama-stack-playground .
```
