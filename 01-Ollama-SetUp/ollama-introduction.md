# Introduction to Ollama

## Ollama command line

Show model information

```
> ollama show qwen3.6
  Model
    architecture        qwen35moe
    parameters          36.0B
    context length      262144
    embedding length    2048
    quantization        Q4_K_M

  Capabilities
    completion
    vision
    tools
    thinking

  Parameters
    top_p               0.95
    min_p               0
    presence_penalty    1.5
    repeat_penalty      1
    temperature         1
    top_k               20

  License
    Apache License
    Version 2.0, January 2004
    ...
```

## Create a customized model

```model file```:

```docker
FROM qwen3.6:latest

PARAMETER temperature 0.5

SYSTEM You are a football commenter. Response to the question in a footballistic way.
```

then run

```bash
$ ollama create custom-model -f <model_file>
```

## Ollama Raw API

generate
```bash
$ curl http://localhost:11434/api/generate -d '{
  "model": "qwen3:30b-a3b-thinking-2507-q4_K_M",
  "prompt": "Why is the sky blue?", "stream": false, "think": false
}'
```

chat

```bash
$ curl http://localhost:11434/api/chat -d '{
  "model": "qwen3:30b-a3b-thinking-2507-q4_K_M",
  "messages": [
    {
        "role": "user",
        "content": "Why is the sky blue?"
    }
  ],
  "stream": false,
  "think": false
}'

{"model":"qwen3:30b-a3b-thinking-2507-q4_K_M","created_at":"2026-05-25T16:57:19.001464Z","message":{"role":"assistant","content":"Okay, the user is asking why ...
},"done":true,"done_reason":"stop","total_duration":17299774833,"load_duration":2852093667,"prompt_eval_count":16,"prompt_eval_duration":71145042,"eval_count":1495,"eval_duration":14172655347}%
```


## Ollama load GGUF models from HuggingFace

