import csv, os
from pestuary import add_content_to_collection, content_add, collection_create, collection_list_content


def setup_test_data(test_file_name='a.csv'):
    with open(test_file_name, 'w') as f:
        writer = csv.writer(f)

        writer.writerow(['number', 'letter'])
        writer.writerow([1, 'a'])
        writer.writerow([2, 'b'])
        writer.writerow([3, 'c'])


def cleanup_test_data(test_file_name='a.csv'):
    os.remove(test_file_name)


def add_data(test_file_name='a.csv'):
    response = content_add(test_file_name)
    content_id = response.estuary_id

    return content_id


if __name__ == '__main__':
    file_name = 'a.csv'
    setup_test_data(file_name)
    content_id = add_data(file_name)

    response = collection_create("test collection", "test description")
    collection_id = response.uuid

    add_content_to_collection(collection_id, [content_id])

    response = collection_list_content(collection_id)
    print(response)
