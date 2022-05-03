import os
import sys
import time
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
        json={'privateKey': private_key, 'addresses': addresses},
    )
    return response.json()


def autoretrieve_list():
    response = requests.get(
        ESTUARY_URL+'admin/autoretrieve/list',
        headers={'Authorization': 'Bearer '+ESTUARY_KEY},
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


def content_add(path, create_collection=False):
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


def collection_fs_list(collection_uuid, collection_path, recursive=False):
    query_params = f'col={collection_uuid}&dir={collection_path}'

    response = requests.get(ESTUARY_URL+f'collections/fs/list?{query_params}',
        headers={'Authorization': 'Bearer '+ESTUARY_KEY},
    )

    if not recursive:
        return response.json()

    responses = []
    for entry in response.json():
        responses.append(entry)
        if entry["type"] == "directory":
            responses[-1]["contents"] = collection_fs_list(collection_uuid, collection_path+"/"+entry["name"])

    return responses


def collection_list_content(collection_uuid, collection_path='', recursive=False):
    if recursive or collection_path:
        if not collection_path:
            collection_path = '/'
        return collection_fs_list(collection_uuid, collection_path, recursive)

    response = requests.get(ESTUARY_URL+f'collections/content/{collection_uuid}',
        headers={'Authorization': 'Bearer '+ESTUARY_KEY},
    )
    return response.json()


def collection_commit(collection_uuid):
    response = requests.post(ESTUARY_URL+f'collections/{collection_uuid}/commit',
        headers={'Authorization': 'Bearer '+ESTUARY_KEY},
    )
    return response.json()


# lists all contents for this user
def content_list():
    response = requests.get(ESTUARY_URL+f'content/stats',
        headers={'Authorization': 'Bearer '+ESTUARY_KEY},
    )

    # response CID comes like "cid": {"/": "cid_here"}, change to "cid": "cid_here"
    pretty_response = []
    for content in response.json():
        content["cid"] = content["cid"]["/"]
        pretty_response.append(content)

    # sort in descending id order (newer ids appear last)
    return sorted(pretty_response, key=lambda k: k['id'])


# creates a new pin
def pin_create(cid, name, meta):
    response = requests.post(ESTUARY_URL+'pinning/pins',
                  headers={'Authorization': 'Bearer '+ESTUARY_KEY},
                     json={"cid": cid, "name": name, "meta": meta})
    return response.json()


# list all pins for this user
def pin_list():
    response = requests.get(ESTUARY_URL+'pinning/pins',
                  headers={'Authorization': 'Bearer '+ESTUARY_KEY})
    return response.json()


def main():
    pass

if __name__ == '__main__':
    main()
