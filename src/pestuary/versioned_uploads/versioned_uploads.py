import os
from datetime import date

import estuary_client


def is_different(latest_data, new_data):
    return latest_data['cid'] != new_data['cid']


def get_latest_collection(data_collections):
    collection_names = sorted(data_collections, key=lambda collection: collection['created_at'])
    return collection_names[-1]


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

    def add_with_version(self, data):
        data_collections = self.get_collections(data)

        if not data_collections:
            data_with_version = versioned_data(data)
            response = self.create_collection(name=data_with_version, description='Collection for ' + data_with_version)
            collection_id = response.uuid
            return self.add_content(data=data, collection_id=collection_id)

        latest_collection = get_latest_collection(data_collections)
        latest_collection_id = latest_collection['uuid']
        latest_data = self.get_content(latest_collection_id)

        new_data = self.add_content(data)

        if is_different(latest_data, new_data):
            response = self.create_collection(name=versioned_data(data), description='Collection for ' + data)
            collection_id = response['uuid']
            return self.add_content(data=data, collection_id=collection_id)

    def get_collections(self, name):
        return [
            {'name': collection.name, 'uuid': collection.uuid, 'created_at': collection.created_at}
            for collection in self.all_collections if collection.name.startswith(name)
        ]

    def create_collection(self, name, description):
        body = {'name': name, 'description': description}
        return self.collections_api.collections_post(body)

    def get_content(self, collection_id):
        return self.collections_api.collections_coluuid_get(coluuid=collection_id)

    def add_content(self, data, collection_id=None):
        if collection_id:
            return self.content_api.content_add_post(data=data, filename=data, coluuid=collection_id)
        return self.content_api.content_add_post(data=data, filename=data)
