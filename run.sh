#!/usr/bin/env bash


clear
echo "Running TerminalTrader ..."
if [ ! -f "master.db" ]; then
	echo "Creating database and schema ..."
	python3 schema.py
fi
echo "Database loaded ..."
python3 controller.py
rm -r __pycache__
