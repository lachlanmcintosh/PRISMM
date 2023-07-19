#!/stornext/Home/data/allstaff/l/lmcintosh/mambaforge/bin/python

import subprocess
import sys

# The name of your package
pkg="prismm"

def execute_cmd(cmd):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        print(f"Error: {' '.join(cmd)} failed with status {process.returncode}")
        print(stderr.decode())
        sys.exit(1)

    return stdout.decode()

# Uninstall the existing package
print(execute_cmd([sys.executable, '-m', 'pip', 'uninstall', '-y', pkg]))

# Install the package
print(execute_cmd([sys.executable, '-m', 'pip', 'install', '--ignore-installed', '.']))
