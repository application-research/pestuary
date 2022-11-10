# pestuary
A Python SDK to interact with Estuary nodes

## Installation
Using pip
```bash
$ pip install pestuary
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
