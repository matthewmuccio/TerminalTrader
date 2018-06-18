#!/usr/bin/env bash


rm master.db
python3 schema.py
python3 controller.py
rm -r __pycache__
