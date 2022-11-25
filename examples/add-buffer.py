from pestuary.content import add_string

def example_add_string():
    buffer = "The contents of my file to upload"
    print(add_string(buffer, "testfile.txt"))


if __name__ == '__main__':
    test_add_string()