import os
import tempfile

from estuary_client import UtilContentAddIpfsBody

from .collections import collection_create
from pestuary import Pestuary

pestuary = Pestuary()
contentApi = pestuary.get_content_api()


def add_string(buffer, filename, coluuid='', dir=''):
    with tempfile.TemporaryDirectory() as tempdir:
        with open(os.path.join(tempdir, filename), 'w') as fp:
            fp.write(buffer)
            fp.flush()
            fp.seek(0)
            return contentApi.content_add_post(fp.name, filename=fp.name, coluuid=coluuid, dir=dir)


def _add_file(path, collection_uuid='', root_collection_path=''):
    # get only relevant parts of path for directory inside collection and filename
    # /tmp/mydir/subdir/current-file -> [collection_path: /subdir/, filename: current-file]
    collection_path = ''
    if collection_uuid:
        if not root_collection_path:
            print(f"empty root collection path")
            return
        collection_path = '/' + os.path.relpath(path, start=root_collection_path)
    print("Calling api", path, collection_uuid)
    return contentApi.content_add_post(path, coluuid=collection_uuid, dir=collection_path)


def _add_dir(path, collection_uuid='', root_collection_path=''):
    responses = []
    if len(os.listdir(path)) == 0:
        print(f"empty directory '{path}'")
        return responses

    for entry in os.listdir(path):
        fullpath = os.path.join(path, entry)
        if os.path.isfile(fullpath):
            responses.append(_add_file(fullpath, collection_uuid, root_collection_path))
        else:
            responses += _add_dir(fullpath, collection_uuid, root_collection_path)

    return responses


def content_add(path, create_collection=False):
    print("path", path)
    if os.path.isfile(path):
        return _add_file(path)

    collection_uuid = ''
    collection = {}
    if create_collection:
        # collection_name is last part of dir path
        # /tmp/foo/bar/cool-pictures/ -> collection_name: cool-pictures
        collection_name = os.path.basename(os.path.normpath(path))
        collection = collection_create(collection_name)
        collection_uuid = collection.uuid
    print("collection_uuid", collection_uuid)

    responses = _add_dir(path, collection_uuid=collection_uuid,
                         root_collection_path=path)

    return responses, collection


def content_add_ipfs(ipfs):
    body = UtilContentAddIpfsBody(root=ipfs)
    return contentApi.content_add_ipfs_post(body)
