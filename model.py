#!/usr/bin/env python3


import json
import sqlite3

import requests

import mapper
import wrapper


def buy(ticker_symbol, trade_volume):
	# Stuff we might need:
	# - Ticker symbol
	# - Trade volume (number of shares)
	# - Market price (via get_last_price())
	# - User's balance for trading
	# TODO: Replace the value for balance with a read operation from our database,
	# which should eventually be in our mapper.
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	# TODO: Write a database read that retrieves the user balance from users table.
	# TODO: Replace the hard-coded value with something that can handle an arbitrary username.
	cursor.execute("SELECT balance FROM users WHERE username=?", ("matthewmuccio",))
	user_balance = cursor.fetchall()[0][0] # fetchall() -> List of tuples of data.
	brokerage_fee = 6.95
	last_price = get_last_price(ticker_symbol)
	transaction_cost = last_price * float(trade_volume) + brokerage_fee
	if transaction_cost < user_balance:
		# State: the user has enough money in their account to execute the trade.
		# TODO: Check if the user already has the stock, in the holdings table, before
		# committing a write to the table.
		cursor.execute("SELECT ticker_symbol FROM holdings WHERE ticker_symbol=?", (ticker_symbol,))
		ticker_symbols = cursor.fetchall()
		if len(ticker_symbols) == 0:
			# State: update the balance in the row in users table with the given username.
			username = "matthewmuccio"
			cursor.execute("SELECT balance FROM users WHERE username=?", (username,))
			new_balance = cursor.fetchall()[0][0] - transaction_cost
			cursor.execute("UPDATE users SET balance=? WHERE username=?", (new_balance, username,))

			cursor.execute("""INSERT INTO holdings(
						ticker_symbol,
						number_of_shares,
						volume_weighted_average_price
					) VALUES(?,?,?);""", (ticker_symbol, trade_volume, last_price,)
			)
			connection.commit()
			return "Trade was successful."
		else:
			# TODO: State: the stock the user bought is already in the database
			# so we need to update the row with the ticker symbol with a new values
			# for trade_volume and last_price.
			cursor.execute("SELECT number_of_shares FROM holdings WHERE ticker_symbol=?", (ticker_symbol,))
			new_number_of_shares = cursor.fetchall()[0][0] + int(trade_volume)
			cursor.execute("UPDATE holdings SET number_of_shares=? WHERE ticker_symbol=?", (new_number_of_shares, ticker_symbol,))
			connection.commit()
			return "Stock purchase was successful."
		cursor.close()
		connection.close()
	else:
		return "Error: You do not have enough money in your balance to execute that trade."

def sell(ticker_symbol, trade_volume):
	# Stuff we might need:
	# - Ticker symbol
	# - Trade volume (number of shares)
	# - Market price (via get_last_price())
	# - User's balance for trading
	# TODO: Replace the value for balance with a read operation from our database,
	# which should eventually be in our mapper.
	connection = sqlite3.connect("master.db", check_same_thread=False)
	cursor = connection.cursor()
	# Check if the user holds any shares with the given ticker symbol.
	cursor.execute("SELECT ticker_symbol FROM holdings WHERE ticker_symbol=?", (ticker_symbol,))
	ticker_symbols = cursor.fetchall()
	if len(ticker_symbols) == 0:
		return "Error: You do not hold any shares from that company."
	# TODO: Replace the hard-coded value with something that can handle an arbitrary username.
	cursor.execute("SELECT balance FROM users WHERE username=?", ("matthewmuccio",))
	user_balance = cursor.fetchall()[0][0] # fetchall() -> List of tuples of data.
	brokerage_fee = 6.95
	cursor.execute("SELECT number_of_shares FROM holdings WHERE ticker_symbol=?", (ticker_symbol,))
	number_of_shares = cursor.fetchall()[0][0]
	new_number_of_shares = number_of_shares - int(trade_volume)
	last_price = get_last_price(ticker_symbol)
	balance_to_add = (last_price * float(trade_volume)) - brokerage_fee
	# If the user does not hold enough shares to complete their trade.
	if int(trade_volume) < number_of_shares:
		username = "matthewmuccio"
		cursor.execute("SELECT balance FROM users WHERE username=?", (username,))
		new_balance = cursor.fetchall()[0][0] + balance_to_add
		cursor.execute("UPDATE users SET balance=? WHERE username=?", (new_balance, username,))
		cursor.execute("UPDATE holdings SET number_of_shares=? WHERE ticker_symbol=?", (new_number_of_shares, ticker_symbol,))
		connection.commit()
		return "Stock sell was successful."
	else:
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
