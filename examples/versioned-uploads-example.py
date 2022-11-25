import os
import tempfile

from pestuary import versioned_uploads

uploads = versioned_uploads.VersionedUploads()

response = uploads.add_with_version('a.txt')
print(response)

