#!/usr/bin/env python3


import hashlib
import sqlite3
import time

import pandas as pd


# Encrypt a plaintext string (password) with SHA-512 cryptographic hash function.
def encrypt_password(password):
	return hashlib.sha512(str.encode(password)).hexdigest()

# Creates an account in users database table.
def create_account(username, password):
	if account_exists(username, password):
		return "Sorry, an account with that username and password already exists in our database. \nLog in with those credentials to access your account."
	elif username_exists(username):
		return "Sorry, the username you entered is already taken."
	password = encrypt_password(password)
	default_balance = 100000.00
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute(
		"""INSERT INTO users(
			username,
			password,
			balance
			) VALUES(?,?,?);
		""", (username, password, default_balance,)
	)
	connection.commit()
	cursor.close()
	connection.close()
	return "Success: Your account has been created!"

# Logs in to account in users database table.
def login(username, password):
	if not username_exists(username):
		return "Sorry, there is no account with that username in our database."
	elif not account_exists(username, password):
		return "Sorry, the password you entered was incorrect."
	password = encrypt_password(password)
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password,))
	result = len(cursor.fetchall()) == 1
	cursor.close()
	connection.close()
	return "Success: You have been logged in to your account!"

### SELECT (GET)

# Checks if a username exists in a row in the users database table.
def username_exists(username):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM users WHERE username=?", (username,))
	result = len(cursor.fetchall()) == 1
	cursor.close()
	connection.close()
	return result

# Checks if an account (username and password) exists in a row in the users database table.
def account_exists(username, password):
	password = encrypt_password(password)
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password,))
	result = len(cursor.fetchall()) == 1
	cursor.close()
	connection.close()
	return result

# Gets the balance value from the row in the users database table for the given username.
def get_balance(username):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("SELECT balance FROM users WHERE username=?", (username,))
	# Error handling for an unknown username.
	try:
		balance = cursor.fetchall()[0][0]
	except IndexError:
		balance = "exit"
	cursor.close()
	connection.close()
	return balance

# Gets the ticker symbols of the holdings of the user with the given username.
def get_ticker_symbols(ticker_symbol, username):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("SELECT ticker_symbol FROM holdings WHERE ticker_symbol=? AND username=?", (ticker_symbol.upper(), username,))
	ticker_symbols = cursor.fetchall()
	cursor.close()
	connection.close()
	return ticker_symbols

# Gets the number of shares for the given username from holdings database table.
def get_number_of_shares(ticker_symbol, username):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("SELECT number_of_shares FROM holdings WHERE ticker_symbol=? AND username=?", (ticker_symbol.upper(), username,))
	number_of_shares = cursor.fetchall()[0][0]
	cursor.close()
	connection.close()
	return number_of_shares

# Gets the last price stored in the holdings database table for a given ticker_symbol.
def get_last_price(ticker_symbol, username):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("SELECT volume_weighted_average_price FROM holdings WHERE ticker_symbol=? AND username=?", (ticker_symbol.upper(), username,))
	last_price = cursor.fetchall()[0][0]
	cursor.close()
	connection.close()
	return last_price

# Gets a list of all Terminal Traders users in the users database table.
def get_users():
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("SELECT username FROM users WHERE username NOT LIKE 'admin'")
	users = cursor.fetchall() # List of tuples
	users_list = [str(user[0]) for user in users] # List of strings
	cursor.close()
	connection.close()
	return users_list

# Gets all the ticker symbols in a given user's portfolio.
def get_ticker_symbols_from_user(username):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("SELECT ticker_symbol FROM holdings WHERE username=?", (username,))
	ticker_symbols = cursor.fetchall() # List of tuples
	ticker_symbols_list = [str(t[0]) for t in ticker_symbols]
	cursor.close()
	connection.close()
	return ticker_symbols_list

# Creates a new pandas DataFrame that contains the rows in holdings database table for the given user.
def get_holdings_dataframe(username):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	df = pd.read_sql_query("SELECT * FROM holdings WHERE username=?", connection, params=[username])
	return df

### UPDATE / INSERT

# Updates the user's balance in the users database table.
def update_balance(new_balance, username):
	if new_balance != "exit":
		connection = sqlite3.connect("master.db", check_same_thread=False)
		cursor = connection.cursor()
		cursor.execute("UPDATE users SET balance=? WHERE username=?", (new_balance, username,))
		connection.commit()
		cursor.close()
		connection.close()

# Updates the number of shares in the holdings database table with a new number of shares.
def update_number_of_shares(new_number_of_shares, ticker_symbol, username):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("UPDATE holdings SET number_of_shares=? WHERE ticker_symbol=? AND username=?", (new_number_of_shares, ticker_symbol.upper(), username,))
	connection.commit()
	cursor.close()
	connection.close()

# Updates the volume weighted average price in the holdings database table with a new value.
def update_volume_weighted_average_price(new_vwap, ticker_symbol, username):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("UPDATE holdings SET volume_weighted_average_price=? WHERE ticker_symbol=? AND username=?", (new_vwap, ticker_symbol.upper(), username,))
	connection.commit()
	cursor.close()
	connection.close()

# Inserts a new row in the holdings database table.
def insert_holdings_row(ticker_symbol, trade_volume, price, username):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("""INSERT INTO holdings(
				ticker_symbol,
				number_of_shares,
				volume_weighted_average_price,
				username
			) VALUES(?,?,?,?);""", (ticker_symbol.upper(), trade_volume, price, username,)
	)
	connection.commit()
	cursor.close()
	connection.close()

# Inserts a new row in the orders database table.
def insert_orders_row(transaction_type, ticker_symbol, trade_volume, price, username):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	unix_time = round(time.time(), 2)
	cursor.execute("""INSERT INTO orders(
				unix_time,
				transaction_type,
				ticker_symbol,
				trade_volume,
				last_price,
				username
			) VALUES(?,?,?,?,?,?);""", (unix_time, transaction_type, ticker_symbol.upper(), trade_volume, price, username,)
	)
	connection.commit()
	cursor.close()
	connection.close()

### DELETE

# Deletes the row from holdings database table that contains a given ticker symbol.
def delete_holdings_row(ticker_symbol):
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	cursor.execute("DELETE FROM holdings WHERE ticker_symbol=?", (ticker_symbol.upper(),))
	connection.commit()
	cursor.close()
	connection.close()
