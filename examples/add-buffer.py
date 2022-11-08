import tempfile
from pestuary import content_add
buffer = "The contents of my file to upload"

temp = tempfile.NamedTemporaryFile()
temp.write(bytes(buffer, 'utf-8'))
temp.flush()

print(temp.name)
print(content_add(temp.name))
