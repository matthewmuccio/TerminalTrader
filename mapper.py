#!/usr/bin/env python3


import hashlib
import sqlite3


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

