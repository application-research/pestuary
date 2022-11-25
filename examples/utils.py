import csv
import os
import random
import shutil
import string


def setup_test_data_directory(dir='test-adddir'):
    # create directories with files
    # tmp
    # ├── test-adddir
    # │   ├── subdir-1
    # │   ├── subdir-2
    # │   └── subdir-3

    root_dir = os.path.join('/tmp', dir)
    sub_dirs = []
    for i in range(3):
        sub_dirs.append(os.path.join(root_dir, 'subdir-' + str(i)))

    os.mkdir(root_dir)
    for sub_dir in sub_dirs:
        os.mkdir(sub_dir)
    dirs = [root_dir] + sub_dirs
    for directory in dirs:
        for i in range(3):
            f = open(directory + f"/file{i}.txt", "w")
            random_content = ''.join(random.choice(string.printable) for _ in range(10))
            f.write(random_content)
            f.close()


def setup_test_data_file(test_file_name='a.csv'):
    with open(test_file_name, 'w') as f:
        writer = csv.writer(f)

        writer.writerow(['number', 'letter'])
        writer.writerow([1, 'a'])
        writer.writerow([2, 'b'])
        writer.writerow([3, 'c'])


def cleanup_test_data_directory(dir='test-addir'):
    # delete entries from previous tests
    try:
        shutil.rmtree(os.path.join('/tmp', dir))
    except:
        pass
