# pestuary
A Python SDK to interact with Estuary nodes

## Usage

Add dir (recursively) to estuary and create a collection around it
```python
add_content('/tmp/my-local-directory', create_collection=True)
```

List content on a collection
```python
my_collection_uuid = "1234-1234-1234-1234"
collection_list_content(my_collection_uuid, "/subdir-on-collection")
```
