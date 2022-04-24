import os
import random
import shutil
import json
import string
from pestuary import add_content, collection_list_content

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
responses = add_content('/tmp/test-adddir')
# print(responses)

# you can also create a dir-like structure
# on estuary using collections
responses, collection = add_content('/tmp/test-adddir', create_collection=True)
# print(responses, collection)
print(json.dumps(collection_list_content(collection["uuid"], "/subdir-1"), indent=4))
print(json.dumps(collection_list_content(collection["uuid"], "/subdir-2"), indent=4))
print(json.dumps(collection_list_content(collection["uuid"], "/subdir-3"), indent=4))

