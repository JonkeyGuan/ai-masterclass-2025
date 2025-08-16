## minimal
```shell
uv run --with "llama-stack" llama stack build --config=distributions/masterclass-minimal/build.yaml
source masterclass_minimal/bin/activate
llama stack run ~/.llama/distributions/masterclass_minimal/masterclass_minimal-run.yaml
```
## agents
```shell
uv run --with "llama-stack" llama stack build --config=distributions/masterclass-agents/build.yaml
source masterclass_agents/bin/activate
```

```shell
vim ~/.llama/distributions/masterclass_agents/masterclass_agents-run.yaml
```

added below to tool_groups
```
tool_groups:
  - toolgroup_id: builtin::websearch
    provider_id: tavily-search
  - toolgroup_id: builtin::rag
    provider_id: rag-runtime
```

```
llama stack run ~/.llama/distributions/masterclass_agents/masterclass_agents-run.yaml
```
