# pestuary
A Python SDK to interact with Estuary nodes

## Installation
Using pip
```bash
$ pip install pestuary
```

## Setup API Key

Initialize the SDK using your API Key

```python

from pestuary import Pestuary

pestuary = Pestuary(YOUR_ESTUARY_API_KEY)
```

## Usage

Add dir (recursively) to estuary and create a collection around it
```python
import pestuary

pestuary.add_content('/tmp/my-local-directory', create_collection=True)
```

List content on a collection
```python
import pestuary

my_collection_uuid = "1234-1234-1234-1234"
pestuary.collection_list_content(my_collection_uuid, "/subdir-on-collection")
```

## Pypi Release

When we create a tag on git we automatically publish a new version to https://pypi.org/project/pestuary/#history

Make sure to increment the version in setup.py before creating the new tag
