#!/bin/bash

pyside6-uic gui/form.ui -o gui/ui_form.py
python3 gui/main.py $@
