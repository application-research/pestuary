import os
import sys
import requests

ESTUARY_URL='http://localhost:3004/'
ESTUARY_KEY=os.getenv('APIKEY')
SHUTTLES = {}
if not ESTUARY_KEY:
    print("$APIKEY environment variable not set")
    sys.exit(1)


def create_shuttle():
    response = requests.post(ESTUARY_URL+'admin/shuttle/init',
                  headers={'Authorization': 'Bearer '+ESTUARY_KEY})
    return response.json()


def _add_file(path):
    response = requests.post(ESTUARY_URL+'content/add',
        headers={'Authorization': 'Bearer '+ESTUARY_KEY},
                             files={'data':path})
    return response.json()


def _add_dir(path):
    if len(os.listdir(path)) == 0:
        print(f"empty directory '{path}', skipping")
        return

    for entry in os.listdir(path):
        fullpath = os.path.join(path, entry)
        if os.path.isfile(fullpath):
            print(_add_file(fullpath))
        else:
            _add_dir(fullpath)


# TODO: implement create_collection
def add_content(path, create_collection=False):
    if os.path.isfile(path):
        return _add_file(path)

    return _add_dir(path)


def main():
    print(create_shuttle())
    add_content('/tmp/file1')
    add_content('/tmp/dir1')


if __name__ == '__main__':
    main()
