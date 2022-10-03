import os
import random
import shutil
import json
import string
import pestuary
from pestuary import content_add, collection_list_content

# delete entries from previous tests
try:
    shutil.rmtree('/tmp/test-adddir')
except:
    pass

# create directories with files
# tmp
# ├── test-adddir
# │   ├── subdir-1
# │   ├── subdir-2
# │   └── subdir-3

os.mkdir('/tmp/test-adddir')
os.mkdir('/tmp/test-adddir/subdir-1')
os.mkdir('/tmp/test-adddir/subdir-2')
os.mkdir('/tmp/test-adddir/subdir-3')
dirlist = ['/tmp/test-adddir' ,'/tmp/test-adddir/subdir-1', \
           '/tmp/test-adddir/subdir-2', '/tmp/test-adddir/subdir-3']
for directory in dirlist:
    for i in range(3):
        f = open(directory+f"/file{i}.txt", "w")
        random_content = ''.join(random.choice(string.printable) for _ in range(10))
        f.write(random_content)
        f.close()


# add all the files under /tmp/test-adddir
responses = content_add('/tmp/test-adddir')

# you can also create a dir-like structure
# on estuary using collections
responses, collection = content_add('/tmp/test-adddir', create_collection=True)
if not collection_list_content(collection.uuid):
    print("No collection listed, currenlyt this is due to a problem with the API endpoint https://github.com/application-research/estuary/issues/447")

# you can even list contents recursively!!
#not sure what we want recursive vs non recursive to be
#print(json.dumps(collection_list_content(collection["uuid"], "/", recursive=True), indent=4))

