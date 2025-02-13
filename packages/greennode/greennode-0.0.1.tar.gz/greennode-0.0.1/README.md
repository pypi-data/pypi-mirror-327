# GreenNode Python Library
One-stop Python library for seamless AI model training, deployment and infrastructure management.

## Installation
To install GreenNode Python Library, simply run:
```sh
pip install greennode
```

## Usage

### Authentication

```python
import os
from greennode import GreenNodeAuthen

client = GreenNodeAuthen(client_id=os.environ.get("GREENNODE_CLIENT_ID"),
                         client_secret=os.environ.get("GREENNODE_CLIENT_SECRET"),
                         base_url=os.environ.get("GREENNODE_AUTH_URL"))

response = client.auth.create()
access_token = response.access_token

os.environ["GREENNODE_API_KEY"] = access_token

```

### Chat Completions

```python
import os
from greennode import GreenNode

client = GreenNode(api_key=os.environ.get("GREENNODE_API_KEY"),
                   base_url=os.environ.get("GREENNODE_BASE_URL"))

response = client.chat.completions.create(
    model="meta/llama-3.1-8b-instruct",
    messages=[{"role": "user", "content": "tell me about new york"}],
)
print(response.choices[0].message.content)
```

#### Streaming

```python
import os
from greennode import GreenNode

client = GreenNode(api_key=os.environ.get("GREENNODE_API_KEY"),
                   base_url=os.environ.get("GREENNODE_BASE_URL"))

stream = client.chat.completions.create(
    model="meta/llama-3.1-8b-instruct",
    messages=[{"role": "user", "content": "tell me about new york"}],
    stream=True,
)

for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="", flush=True)
```

### Completions

```python
import os
from greennode import GreenNode

client = GreenNode(api_key=os.environ.get("GREENNODE_API_KEY"),
                   base_url=os.environ.get("GREENNODE_BASE_URL"))

response = client.completions.create(
    model="Qwen/Qwen2.5-1.5B",
    prompt="New York City is",
    stream=False,
)

print(response.choices[0].text)
```

#### Streaming

```python
import os
from greennode import GreenNode

client = GreenNode(api_key=os.environ.get("GREENNODE_API_KEY"),
                   base_url=os.environ.get("GREENNODE_BASE_URL"))

stream = client.completions.create(
    model="Qwen/Qwen2.5-1.5B",
    prompt="New York City is",
    stream=True,
)

for chunk in stream:
    print(chunk.choices[0].text or "", end="", flush=True)
```

### Embeddings

```python
import os
from greennode import GreenNode

client = GreenNode(api_key=os.environ.get("GREENNODE_API_KEY"),
                   base_url=os.environ.get("GREENNODE_BASE_URL"))

response = client.embeddings.create(
      model="BAAI/bge-m3",
      input=["Hello world", "Thank you"],
      encoding_format="float"
)

print(response)
```

### List supported Models

```python
import os
from greennode import GreenNode

client = GreenNode(api_key=os.environ.get("GREENNODE_API_KEY"),
                   base_url=os.environ.get("GREENNODE_BASE_URL"))

response = client.models.list()

print(response)
```