#!/usr/bin/env python3


import sqlite3


connection = sqlite3.connect("master.db", check_same_thread=False)
cursor = connection.cursor()

# Create users table
cursor.execute(
	"""CREATE TABLE users(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		username VARCHAR(16) UNIQUE,
		password VARCHAR(128),
		balance FLOAT
	);"""
)

# Create portfolio/holdings table
cursor.execute(
	"""CREATE TABLE holdings(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		ticker_symbol VARCHAR(5),
		number_of_shares INTEGER,
		volume_weighted_average_price FLOAT,
		username VARCHAR(16),
		FOREIGN KEY(username) REFERENCES users(username)
	);"""
)

# Create orders/transactions table
cursor.execute(
	"""CREATE TABLE orders(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		unix_time FLOAT,
		transaction_type VARCHAR(4),
		ticker_symbol VARCHAR(5),
		trade_volume INTEGER,
		last_price FLOAT,
		username VARCHAR(16),
		FOREIGN KEY(username) REFERENCES users(username)
	);"""
)

cursor.close()
connection.close()
