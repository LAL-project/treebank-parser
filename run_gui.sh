#!/bin/bash

echo "Compile GUI"
pyside6-uic gui/form.ui -o gui/ui_form.py

echo "Run GUI"
python3 gui/main.py $@
