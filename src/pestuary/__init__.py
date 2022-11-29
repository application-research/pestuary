import os
import sys
import estuary_client
from estuary_client.rest import ApiException
from .versioned_uploads import versioned_uploads
from .utils import utils

# ESTUARY_URL='http://localhost:3004'
ESTUARY_URL = 'https://api.estuary.tech'
ESTUARY_KEY = os.getenv('APIKEY')
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

