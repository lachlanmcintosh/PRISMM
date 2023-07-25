# this is a program file that runs all tests in this subdirectory
import glob
import re
import unittest

# get all .py files in the current directory
all_py_files = glob.glob('*.py')

# use a regular expression to match 'test*.py' but not 'test*_IO.py'
pattern = re.compile(r"^test(?!.*_IO\.py$).*\.py$")

# filter the files using the pattern
matching_files = [file for file in all_py_files if pattern.match(file)]

# run the tests in each matching file
for file in matching_files:
    # remove '.py' from the file name to get the module name
    module_name = file[:-3]

    # load the tests
    suite = unittest.defaultTestLoader.loadTestsFromName(module_name)

    # run the tests
    unittest.TextTestRunner().run(suite)
