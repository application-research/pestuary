from pestuary import add_content_to_collection, content_add, collection_create, collection_list_content

response = content_add("./test_data/a.csv")
content_id = response.estuary_id

response = collection_create("test collection", "test description")
collection_id = response.uuid

add_content_to_collection(collection_id, [content_id])

response = collection_list_content(collection_id)
print(response)