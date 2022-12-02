from estuary_client import MainCreateCollectionBody

from pestuary import Pestuary

pestuary = Pestuary()
collectionsApi = pestuary.get_collections_api()


def collection_create(name, description=''):
    body = MainCreateCollectionBody(name=name, description=description)
    return collectionsApi.collections_post(body)


def add_content_to_collection(coluuid, content_ids):
    return collectionsApi.collections_coluuid_post(coluuid, content_ids)


def collection_list():
    return collectionsApi.collections_get()


# todo what is recursive and how should it be used?
def collection_list_content(collection_uuid, collection_path='', recursive=False):
    return collectionsApi.collections_coluuid_get(collection_uuid, dir=collection_path)


def collection_commit(collection_uuid):
    return collectionsApi.collections_coluuid_commit_post(collection_uuid)


# lists all contents for this user
def content_list():
    limit = '0'  # seems to be ignored #TODO what is limit
    return collectionsApi.content_stats_get(limit)
    # TODO old version sorted by id, do we need that?
