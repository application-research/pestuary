import inspect
import tempfile
import click
import os
import sys
import time
import json
import requests
import estuary_client
from estuary_client.rest import ApiException
from pprint import pprint

#ESTUARY_URL='http://localhost:3004'
ESTUARY_URL='https://api.estuary.tech'
ESTUARY_KEY=os.getenv('APIKEY')
SHUTTLES = {}
if not ESTUARY_KEY:
    print("$APIKEY environment variable not set")
    sys.exit(1)

configuration = estuary_client.Configuration()
configuration.api_key['Authorization'] = ESTUARY_KEY
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
configuration.api_key_prefix['Authorization'] = 'Bearer'
configuration.host = ESTUARY_URL

# create an instance of the API class
userApi = estuary_client.UserApi(estuary_client.ApiClient(configuration))
adminApi = estuary_client.AdminApi(estuary_client.ApiClient(configuration))
autoretrieveApi = estuary_client.AutoretrieveApi(estuary_client.ApiClient(configuration))
collectionsApi = estuary_client.CollectionsApi(estuary_client.ApiClient(configuration))
contentApi = estuary_client.ContentApi(estuary_client.ApiClient(configuration))
dealsApi = estuary_client.DealsApi(estuary_client.ApiClient(configuration))
metricsApi = estuary_client.MetricsApi(estuary_client.ApiClient(configuration))
minerApi = estuary_client.MinerApi(estuary_client.ApiClient(configuration))
netApi = estuary_client.NetApi(estuary_client.ApiClient(configuration))
peeringApi = estuary_client.PeeringApi(estuary_client.ApiClient(configuration))
peersApi = estuary_client.PeersApi(estuary_client.ApiClient(configuration))
pinningApi = estuary_client.PinningApi(estuary_client.ApiClient(configuration))
publicApi = estuary_client.PublicApi(estuary_client.ApiClient(configuration))




try:
    # Get API keys for a user
    api_response = userApi.user_api_keys_get()
except ApiException as e:
    print("Exception when calling UserApi->user_api_keys_get: %s\n" % e)





def collection_create(name, description=''):
    body = estuary_client.MainCreateCollectionBody(name=name, description=description)
    return collectionsApi.collections_post(body)


#is this deprecated? I don't see it in the docs
def shuttle_create():
    response = requests.post(ESTUARY_URL+'admin/shuttle/init',
                  headers={'Authorization': 'Bearer '+ESTUARY_KEY})
    return response.json()


def autoretrieve_create(pub_key, addresses):
    return autoretrieveApi.admin_autoretrieve_init_post(addresses, pub_key)

def autoretrieve_list():
    return autoretrieveApi.admin_autoretrieve_list_get()


def autoretrieve_heartbeat(token):
    return autoretrieveApi.autoretrieve_heartbeat_post(token)

def add_string(buffer, filename, coluuid='', dir=''):
    with tempfile.TemporaryDirectory() as tempdir:
        with open(os.path.join(tempdir, filename),'w') as fp:
            fp.write(buffer)
            fp.flush()
            fp.seek(0)
            return contentApi.content_add_post(fp.name, coluuid=coluuid, dir=dir)

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

    responses = _add_dir(path, collection_uuid=collection_uuid, \
                    root_collection_path=path)

    return responses, collection

def collection_list():
    return collectionsApi.collections_get()



#TODO I don't really understand this method 
# I think we want to use this https://github.com/snissn/estuary-swagger-clients/blob/main/python/docs/CollectionsApi.md#collections_coluuid_get
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


#todo what is recursive and how should it be used?
def collection_list_content(collection_uuid, collection_path='', recursive=False):
    return collectionsApi.collections_coluuid_get(collection_uuid, dir=collection_path)


def collection_commit(collection_uuid):
    return collectionsApi.collections_coluuid_commit_post(collection_uuid)

def content_add_ipfs(ipfs):
    body = estuary_client.UtilContentAddIpfsBody(root=ipfs)
    return contentApi.content_add_ipfs_post(body)

# lists all contents for this user
def content_list():
    limit = '0' # seems to be ignored #TODO what is limit
    return collectionsApi.content_stats_get(limit)
    #TODO old version sorted by id, do we need that?

# creates a new pin
def pin_create(cid, name):
    return pinningApi.pinning_pins_post(cid, name)

# list all pins for this user
def pin_list():
    return pinningApi.pinning_pins_get()


def main():
    cli()

if __name__ == '__main__':
    main()
