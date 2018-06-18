#!/usr/bin/env python3


import json
import sqlite3

import requests

import mapper
import wrapper


def buy(ticker_symbol, trade_volume):
	# TODO: Add database support for reading from and writing to the orders (transactions) table.
	# TODO: Replace the value for balance with a read operation from our database,
	# which should eventually be in our mapper.
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	# TODO: Replace the hard-coded value with something that can handle an arbitrary username.
	cursor.execute("SELECT balance FROM users WHERE username=?", ("matthewmuccio",))
	user_balance = cursor.fetchall()[0][0] # fetchall() -> List of tuples of data.
	last_price = get_last_price(ticker_symbol)
	brokerage_fee = 6.95
	transaction_cost = last_price * float(trade_volume) + brokerage_fee
	if transaction_cost < user_balance:
		# State: the user has enough money in their account to execute the trade.
		cursor.execute("SELECT ticker_symbol FROM holdings WHERE ticker_symbol=?", (ticker_symbol,))
		ticker_symbols = cursor.fetchall()
		# If the user does not hold any stock from company with ticker_symbol.
		if len(ticker_symbols) == 0:
			# State: update the balance in the row in users table with the given username.
			new_user_balance = user_balance - transaction_cost
			# Updates the user's balance in the users database table.
			cursor.execute("UPDATE users SET balance=? WHERE username=?", (new_user_balance, "matthewmuccio",))
			# Inserts a new row to the holdings database table after buying the stock.
			cursor.execute("""INSERT INTO holdings(
						ticker_symbol,
						number_of_shares,
						volume_weighted_average_price
					) VALUES(?,?,?);""", (ticker_symbol, trade_volume, last_price,)
			)
			# Commits changes to the database, closes cursor and connection, and returns successful response.
			connection.commit()
			cursor.close()
			connection.close()
			return "Trade was successful."
		# If the user holds some stock from company with ticker_symbol.
		else:
			# Gets the number of shares from holdings database table for the company with ticker_symbol.
			cursor.execute("SELECT number_of_shares FROM holdings WHERE ticker_symbol=?", (ticker_symbol,))
			new_number_of_shares = cursor.fetchall()[0][0] + int(trade_volume)
			# Updates the holdings database table with the new number of shares after buying stock.
			cursor.execute("UPDATE holdings SET number_of_shares=? WHERE ticker_symbol=?", (new_number_of_shares, ticker_symbol,))
			# Commits changes to the database, closes cursor and connection, and returns successful response.
			connection.commit()
			cursor.close()
			connection.close()
			return "Stock purchase was successful."
	else:
		# Closes cursor and connection, and returns error response.
		cursor.close()
		connection.close()
		return "Error: You do not have enough money in your balance to execute that trade."

def sell(ticker_symbol, trade_volume):
	# TODO: Add database support for reading from and writing to the orders (transactions) table.
	# TODO: Replace the value for balance with a read operation from our database,
	# which should eventually be in our mapper.
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	# Checks if the user holds any stock from the company with ticker_symbol.
	cursor.execute("SELECT ticker_symbol FROM holdings WHERE ticker_symbol=?", (ticker_symbol,))
	ticker_symbols = cursor.fetchall()
	# If the user does not hold any stock from the company with ticker_symbol.
	if len(ticker_symbols) == 0:
		return "Error: You do not hold any shares from that company."
	# TODO: Replace the hard-coded value with something that can handle an arbitrary username.
	cursor.execute("SELECT balance FROM users WHERE username=?", ("matthewmuccio",))
	user_balance = cursor.fetchall()[0][0] # fetchall() -> List of tuples of data.
	brokerage_fee = 6.95
	# Gets the user's number of shares from the company with ticker_symbol.
	cursor.execute("SELECT number_of_shares FROM holdings WHERE ticker_symbol=?", (ticker_symbol,))
	number_of_shares = cursor.fetchall()[0][0]
	new_number_of_shares = number_of_shares - int(trade_volume)
	last_price = get_last_price(ticker_symbol)
	balance_to_add = (last_price * float(trade_volume)) - brokerage_fee
	# If the user holds enough shares to complete their trade.
	if int(trade_volume) <= number_of_shares:
		# If the new number of shares would be 0 after the user sells their shares.
		if new_number_of_shares == 0:
			# Deletes the row from holdings database table for company with ticker_symbol.
			cursor.execute("DELETE FROM holdings WHERE ticker_symbol=?", (ticker_symbol,))
		else:
			# Updates holdings database table with the new number of shares.
			cursor.execute("UPDATE holdings SET number_of_shares=? WHERE ticker_symbol=?", (new_number_of_shares, ticker_symbol,))
		new_user_balance = user_balance + balance_to_add
		# Updates users database table with the new balance after selling the stock.
		cursor.execute("UPDATE users SET balance=? WHERE username=?", (new_user_balance, "matthewmuccio",))
		# Commits changes to the database, closes cursor and connection, and returns successful response.
		connection.commit()
		cursor.close()
		connection.close()
		return "Stock sell was successful."
	else:
		# Closes cursor and connection, and returns error response.
		cursor.close()
		connection.close()
		return "Error: You do not have enough shares to sell to complete that trade."

def get_last_price(ticker_symbol):
	endpoint = "http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?symbol=" + ticker_symbol
	response = json.loads(requests.get(endpoint).text)
	last_price = response["LastPrice"]
	return last_price

def get_ticker_symbol(company_name):
	endpoint = "http://dev.markitondemand.com/MODApis/Api/v2/Lookup/json?input=" + company_name
	# TODO: Refactor this line so that it does not just take the first element in the
	# iterable that is returned, and assume it's the symbol we want.
	response = json.loads(requests.get(endpoint).text)[0]
	ticker_symbol = response["Symbol"]
	return ticker_symbol


if __name__ == "__main__":
	# Test
	# - Buy one share of AT&T at current market price (fair value)
	print(buy("t", 1))
