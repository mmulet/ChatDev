# Soaring7-2 Instructions
Instructions to run macnet using vllm serve, this way we can swap models easily

Create and activate virtual environment
```sh
uv sync
source .venv/bin/activate
```

Launch the openAI compatible server
```sh
# This will launch the openAI compatible server


CUDA_VISIBLE_DEVICES=0,1,2,3 vllm serve \
  unsloth/Qwen2.5-0.5B-Instruct \ # Change to your desired model
  --dtype auto \
 --api-key token-abc123 \ # set OPENAI_API_KEY to this value
 --port 8000 \ # !!!!!! If 2 people are on the same server, change the port to avoid conflicts !!!!!!
 --served-model-name gpt-4o \ # This will fake the model name to gpt-4o for compatibility, (no need to change config.yaml)
 # Optional usual vllm parameters
 --data-parallel-size 4 \ # Adjust as needed. replicate model over multiple gpus for higher throughput
 --tensor-parallel-size 4 \ # Adjust as needed. split tensor over multiple gpus if out of gpu memory

```
Now to run the chat

Optional
(if you want to change the number of agents or the topology run)

```sh
python generate_graph.py --node_num 5 --topology net 
```
it will save the config to config.yaml


Note to anyone sharing a server
```sh
# !!!! change this port to your own port to avoid conflicts !!!!
BASE_URL="http://localhost:8000/v1" OPENAI_API_KEY=token-abc123 python run.py --task "Develop a cli application that takes in json from std in and output yaml to std out" --name "JSON2YAML Converter"
```

Then your results will be in `WareHouse/JSON2YAML Converter` or whatever name you gave