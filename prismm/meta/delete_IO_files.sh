#!/bin/bash

find . -type f -name "*_IO.py" -print

read -rp "Do you want to delete the listed files? (y/n) " response
if [[ $response =~ ^[Yy]$ ]]; then
    find . -type f -name "*_IO.py" -delete
    echo "Deletion completed!"
else
    echo "Deletion cancelled."
fi