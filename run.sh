#!/usr/bin/env bash


clear
echo "Running TerminalTrader ..."
if [ ! -f "master.db" ]; then
	echo "Creating database and schema ..."
	python3 schema.py
	python3 seed.py
fi
echo "Database loaded ..."
echo "Launching TerminalTrader ..."
python3 controller.py
rm -r __pycache__
