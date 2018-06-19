#!/usr/bin/env bash


if [ ! -f "master.db" ]; then
	python3 schema.py
fi
python3 controller.py
rm -r __pycache__
