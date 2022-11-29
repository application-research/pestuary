import os

from pestuary import utils, versioned_uploads

if __name__ == '__main__':
    uploads = versioned_uploads.VersionedUploads()
    name = 'e.txt'
    url = 'https://shuttle-8.estuary.tech/gw/ipfs/bafkqaetbmjrwizlgbjtwq2lknmfgy3lon5ya/'
    utils.download_dataset_from_url(name, url, data_directory='.')

    response = uploads.add_with_version(name)
    print(response)
    os.remove(name)

