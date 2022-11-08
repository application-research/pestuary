#curl -X POST "https://api.estuary.tech/collections/" -H "Accept: application/json"  -H "Authorization: Bearer REPLACE_ME_WITH_API_KEY" -d '{"name":"COLLECTION_NAME", "description":"COLLECTION_DESCRIPTION"}'

import os
import random
import string
from pestuary import collection_create


name="Test"
description="Helpful description here"
response = collection_create(name, description)
print(response)
