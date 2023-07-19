import os
import re

def find_imports(root, module):
    # Regular expression to find import statements
    import_re = re.compile(rf"import {module}|from {module} import")

    # Walk the directory
    for dirpath, dirs, files in os.walk(root):
        for filename in files:
            if filename.endswith('.py'):
                # This is a Python file, open it
                with open(os.path.join(dirpath, filename)) as f:
                    contents = f.read()

                    # Check if the module is imported in this file
                    if import_re.search(contents):
                        print(f"Module '{module}' imported in {os.path.join(dirpath, filename)}")

# Use the script
find_imports('.', 'clonal_trees')

