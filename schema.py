#!/usr/bin/env python3


import sqlite3


connection = sqlite3.connect("master.db", check_same_thread=False)
cursor = connection.cursor()

# Create users table
cursor.execute(
	"""CREATE TABLE users(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		username VARCHAR(16),
		password VARCHAR(32),
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
		user_id INTEGER,
		FOREIGN KEY(user_id) REFERENCES users(id)
	);"""
)

# Create orders/transactions table
cursor.execute(
	"""CREATE TABLE orders(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		unix_time FLOAT,
		transaction_type VARCHAR(4),
		ticker_symbol VARCHAR(5),
		last_price FLOAT,
		trade_volume INTEGER,
		user_id INTEGER,
		FOREIGN KEY(user_id) REFERENCES users(id)
	);"""
)

cursor.close()
connection.close()
