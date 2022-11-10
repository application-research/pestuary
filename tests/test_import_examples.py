import importlib
import os
import sys
import unittest


current_directory = os.path.dirname(os.path.abspath(__file__))
examples_directory = os.path.join(current_directory, "../examples")
sys.path.append(examples_directory)

#list contents of examples directory and then build and run tests for each file
def get_modules():
    for filename in os.listdir(examples_directory):
        if filename.endswith(".py"):
            yield filename.split(".py")[0]


example_modules = list(get_modules())

def test_template(name):
    return lambda cls: importlib.import_module(name)

class TestPestuary(unittest.TestCase):
    pass


for module_name in example_modules:
    fn = test_template(module_name)
    setattr(TestPestuary, "test_"+module_name, fn)


if __name__ == '__main__':
    unittest.main()

