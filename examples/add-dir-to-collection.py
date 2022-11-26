from pestuary.collections import collection_list_content
from pestuary.content import content_add

from utils import remove_tmp_directory, create_tmp_directory

if __name__ == '__main__':
    directory = 'test-addir'
    create_tmp_directory(directory)

    responses, collection = content_add('/tmp/test-adddir', create_collection=True)
    print(collection_list_content(collection.uuid))

    remove_tmp_directory(directory)
