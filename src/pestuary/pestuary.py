import os
import sys

import estuary_client


def set_config(url, api_key):
    config = estuary_client.Configuration()
    config.api_key['Authorization'] = api_key
    config.api_key_prefix['Authorization'] = 'Bearer'
    config.host = url

    return config


class Pestuary:
    def __init__(self, estuary_url='https://api.estuary.tech', estuary_key=os.getenv('APIKEY')):
        if not estuary_key:
            print("$APIKEY environment variable not set")
            sys.exit(1)
        self.estuary_url = estuary_url
        self.estuary_key = estuary_key
        self.configuration = set_config(estuary_url, estuary_key)

        # create an instance of the API class
        self._userApi = estuary_client.UserApi(estuary_client.ApiClient(self.configuration))
        self._adminApi = estuary_client.AdminApi(estuary_client.ApiClient(self.configuration))
        self._autoretrieveApi = estuary_client.AutoretrieveApi(estuary_client.ApiClient(self.configuration))
        self._collectionsApi = estuary_client.CollectionsApi(estuary_client.ApiClient(self.configuration))
        self._contentApi = estuary_client.ContentApi(estuary_client.ApiClient(self.configuration))
        self._dealsApi = estuary_client.DealsApi(estuary_client.ApiClient(self.configuration))
        self._metricsApi = estuary_client.MetricsApi(estuary_client.ApiClient(self.configuration))
        self._minerApi = estuary_client.MinerApi(estuary_client.ApiClient(self.configuration))
        self._netApi = estuary_client.NetApi(estuary_client.ApiClient(self.configuration))
        self._peeringApi = estuary_client.PeeringApi(estuary_client.ApiClient(self.configuration))
        self._peersApi = estuary_client.PeersApi(estuary_client.ApiClient(self.configuration))
        self._pinningApi = estuary_client.PinningApi(estuary_client.ApiClient(self.configuration))
        self._publicApi = estuary_client.PublicApi(estuary_client.ApiClient(self.configuration))

    def get_autoretrieve_api(self):
        return self._autoretrieveApi

    def get_collections_api(self):
        return self._collectionsApi

    def get_content_api(self):
        return self._contentApi

    def get_pinning_api(self):
        return self._pinningApi
