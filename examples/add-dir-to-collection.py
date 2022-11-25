from pestuary.collections import collection_list_content
from pestuary.content import content_add

from utils import cleanup_test_data_directory, setup_test_data_directory

if __name__ == '__main__':
    directory = 'test-addir'
    setup_test_data_directory(directory)

    responses, collection = content_add('/tmp/test-adddir', create_collection=True)
    print(collection_list_content(collection.uuid))

    cleanup_test_data_directory(directory)
