#!/bin/bash

newvernum=$1
if [ -z $newvernum ]; then
    echo "New version number was not provided"
    exit
fi

echo "Updating version number to $newvernum"

sed -i "s/99.99/$newvernum/g" treebank_parser/version_lal.py