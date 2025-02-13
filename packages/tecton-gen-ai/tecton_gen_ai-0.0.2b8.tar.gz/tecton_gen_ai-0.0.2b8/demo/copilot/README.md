To install the dependencies, run:

```bash
pip install -e ".[tecton,openai,dev]"
pip install streamlit-flow-component, black, lancedb, streamlit, snowflake-connector-python, snowflake, matplotlib
```

Before you start the co-pilot, make sure you're logged into a Tecton cluster using:
```bash
    tecton login yourcluster.tecton.ai
```

Set the following environment variables:
```bash
export TECTON_API_KEY=<api key to the dev-gen-ai cluster>
export OPENAI_API_KEY=<api key to openai>
```

To start the co-pilot, run:

```bash
python -m demo/copilot/streamlit run --server.port 3000 ui.py
```
