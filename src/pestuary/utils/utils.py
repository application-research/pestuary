import os
import requests as re


def download_dataset_from_url(name, url, data_directory="data"):
    resp = re.get(url)
    f = open(os.path.join(data_directory, name), 'wb')
    f.write(resp.content)
    f.close()
