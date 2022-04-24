import os
import sys
import json
import requests

ESTUARY_URL='http://localhost:3004/'
ESTUARY_KEY=os.getenv('APIKEY')
SHUTTLES = {}
if not ESTUARY_KEY:
    print("$APIKEY environment variable not set")
    sys.exit(1)


def shuttle_create():
    response = requests.post(ESTUARY_URL+'admin/shuttle/init',
                  headers={'Authorization': 'Bearer '+ESTUARY_KEY})
    return response.json()


def autoretrieve_create(private_key, addresses):
    response = requests.post(
        ESTUARY_URL+'admin/autoretrieve/init',
        headers={'Authorization': 'Bearer '+ESTUARY_KEY},
        json={'privateKey': key, 'addresses': addresses},
    )
    return response.json()


def autoretrieve_heartbeat(secret):
    response = requests.post(ESTUARY_URL+'autoretrieve/heartbeat',
                  headers={'Authorization': 'Bearer '+secret})
    return response.json()


def _add_file(path, collection_uuid='', root_collection_path=''):

    # get only relevant parts of path for directory inside collection and filename
    # /tmp/mydir/subdir/current-file -> [collection_path: /subdir/, filename: current-file]
    collection_path = ''
    if collection_uuid:
        if not root_collection_path:
            print(f"empty root collection path")
            return
        collection_path = '/' + os.path.relpath(path, start=root_collection_path)

    file = open(path, "r")
    filename = os.path.basename(os.path.normpath(path))

    response = requests.post(ESTUARY_URL+'content/add',
        headers={'Authorization': 'Bearer '+ESTUARY_KEY},
        files={"data": file},
        data={"name": filename, "collection": collection_uuid, \
            "collectionPath": collection_path},
    )

    file.close()
    return response.json()


def _add_dir(path, collection_uuid='', root_collection_path=''):
    if len(os.listdir(path)) == 0:
        print(f"empty directory '{path}'")
        return

    responses = []
    for entry in os.listdir(path):
        fullpath = os.path.join(path, entry)
        if os.path.isfile(fullpath):
            responses.append(_add_file(fullpath, collection_uuid, root_collection_path))
        else:
            responses += _add_dir(fullpath, collection_uuid, root_collection_path)

    return responses


def add_content(path, create_collection=False):
    if os.path.isfile(path):
        return _add_file(path)

    collection_uuid = ''
    collection = {}
    if create_collection:
        # collection_name is last part of dir path
        # /tmp/foo/bar/cool-pictures/ -> collection_name: cool-pictures
        collection_name = os.path.basename(os.path.normpath(path))
        collection = collection_create(collection_name)
        print(collection)
        if 'error' in collection:
            return collection
        collection_uuid = collection['uuid']
        # TODO: check if collection was properly created

    responses = _add_dir(path, collection_uuid=collection_uuid, \
                    root_collection_path=path)

    if collection and "error" not in collection:
        return responses, collection

    return responses


def collection_create(name, description=''):
    response = requests.post(ESTUARY_URL+'collections/create',
        headers={'Authorization': 'Bearer '+ESTUARY_KEY},
        json={'name': name, 'description': description},
    )
    return response.json()


def collection_list():
    response = requests.get(ESTUARY_URL+'collections/list',
        headers={'Authorization': 'Bearer '+ESTUARY_KEY},
    )
    return response.json()


def collection_fs_list(collection_uuid, collection_path):
    query_params = f'col={collection_uuid}&dir={collection_path}'

    response = requests.get(ESTUARY_URL+f'collections/fs/list?{query_params}',
        headers={'Authorization': 'Bearer '+ESTUARY_KEY},
    )
    return response.json()


def collection_list_content(collection_uuid, collection_path=''):
    if collection_path:
        return collection_fs_list(collection_uuid, collection_path)

    response = requests.get(ESTUARY_URL+f'collections/content/{collection_uuid}',
        headers={'Authorization': 'Bearer '+ESTUARY_KEY},
    )
    return response.json()



def list_content():
    response = requests.get(ESTUARY_URL+f'content/stats',
        headers={'Authorization': 'Bearer '+ESTUARY_KEY},
    )

    # sort in descending id
    return sorted(response.json(), key=lambda k: k['id'])
    # return response.json()


def main():
    responses, collection = add_content('/tmp/dir', create_collection=True)
    # print(json.dumps(list_content(), indent=4))
    # print(collection["uuid"])
    print(json.dumps(collection_list_content(collection['uuid']), indent=4))
    print(json.dumps(collection_list_content(collection["uuid"], "/otherdir"), indent=4))

    # print(shuttle_create())
    # print(autoretrieve_create())
    # print(json.dumps(collection_list(), indent=4))
    # print(json.dumps(add_content('/tmp/file1'), indent=4))


if __name__ == '__main__':
    main()
