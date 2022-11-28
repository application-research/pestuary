import os
from datetime import date
import json

import estuary_client


def get_latest_collection(data_collections):
    collection_names = sorted(data_collections, key=lambda collection: collection['created_at'])
    return collection_names[-1]


def pick_unique(data_collection):
    assert len(data_collection) == 1
    return data_collection[0]


def _configure_estuary(url, api_key):
    configuration = estuary_client.Configuration()
    configuration.api_key['Authorization'] = api_key
    configuration.api_key_prefix['Authorization'] = 'Bearer'
    configuration.host = url

    return configuration


def versioned_data(data):
    return data + "-" + str(date.today())


class VersionedUploads:
    def __init__(self, url='https://api.estuary.tech', api_key=os.getenv('APIKEY')):
        config = _configure_estuary(url, api_key)
        api_client = estuary_client.ApiClient(config)
        self.content_api = estuary_client.ContentApi(api_client)
        self.collections_api = estuary_client.CollectionsApi(api_client)
        self.all_collections = self.collections_api.collections_get()

    def add_with_version(self, data, filename=None):
        if not filename:
            filename = data
        data_collections = self.get_collections(filename)

        if not data_collections:
            return self.upload_data_to_collection(data, filename)

        latest_cid = self.get_latest_cid(data_collections)
        new_cid = self.get_new_cid(data)

        if latest_cid != new_cid:
            return self.upload_data_to_collection(data, filename)

    def get_new_cid(self, data):
        new_data = self._add_content(data)
        new_cid = new_data.cid
        return new_cid

    def get_latest_cid(self, data_collections):
        latest_collection = get_latest_collection(data_collections)
        latest_collection_id = latest_collection['uuid']
        latest_data = self.get_content(latest_collection_id)
        latest_data = pick_unique(latest_data)
        latest_cid = latest_data['cid']
        return latest_cid

    def upload_data_to_collection(self, data, filename):
        name_with_version = versioned_data(filename)
        response = self.create_collection(name=name_with_version, description='Collection for ' + name_with_version)
        collection_id = response.uuid
        return self._add_content(data=data, filename=filename, collection_id=collection_id)

    def get_collections(self, name):
        return [
            {'name': collection.name, 'uuid': collection.uuid, 'created_at': collection.created_at}
            for collection in self.all_collections if collection.name.startswith(name)
        ]

    def create_collection(self, name, description):
        body = {'name': name, 'description': description}
        return self.collections_api.collections_post(body)

    def get_content(self, collection_id):
        # todo: Need the json.loads because return type is str
        response = self.collections_api.collections_coluuid_get(coluuid=collection_id)
        response = response.replace("'", '"').replace("False", "false").replace("True", "true")
        return json.loads(response)

    def _add_content(self, data, filename=None, collection_id=None):
        if not filename:
            filename = data
        if collection_id:
            return self.content_api.content_add_post(data=data, filename=filename, coluuid=collection_id)
        return self.content_api.content_add_post(data=data, filename=filename)
