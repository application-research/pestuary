import os

from pestuary.collections import add_content_to_collection, collection_create, collection_list_content
from pestuary.content import content_add
from utils import create_tmp_file


def cleanup_test_data(test_file_name='a.csv'):
    os.remove(test_file_name)


def add_data(test_file_name='a.csv'):
    resp = content_add(test_file_name)
    return resp.estuary_id


if __name__ == '__main__':
    file_name = 'a.csv'
    create_tmp_file(file_name)
    content_id = add_data(file_name)

    response = collection_create("test collection", "test description")
    collection_id = response.uuid

    add_content_to_collection(collection_id, [content_id])

    response = collection_list_content(collection_id)
    print(response)
