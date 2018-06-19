#!/usr/bin/env python3


import json

import requests

import mapper
import wrapper


def buy(ticker_symbol, trade_volume, username):
	# TODO: Add database support for reading from and writing to the orders (transactions) table.
	balance = mapper.get_balance(username)
	user_id = mapper.get_id(username)
	last_price = get_last_price(ticker_symbol)
	brokerage_fee = 6.95
	transaction_cost = last_price * float(trade_volume) + brokerage_fee
	if transaction_cost < balance:
		# State: the user has enough money in their account to execute the trade.
		ticker_symbols = mapper.get_ticker_symbols(ticker_symbol, username)
		# If the user does not hold any stock from company with ticker_symbol.
		if len(ticker_symbols) == 0:
			# State: update the balance in the row in users table with the given username.
			new_balance = balance - transaction_cost
			# Updates the user's balance in the users database table.
			mapper.update_balance(new_balance, username)
			# Inserts a new row to the holdings database table after buying the stock.
			mapper.insert_holdings_row(ticker_symbol, trade_volume, last_price, username)
			return "Trade was successful."
		# If the user holds some stock from company with ticker_symbol.
		else:
			# Gets the number of shares from holdings database table for the company with ticker_symbol.
			curr_number_of_shares = mapper.get_number_of_shares(ticker_symbol, username)
			new_number_of_shares = curr_number_of_shares + int(trade_volume)
			# Updates the holdings database table with the new number of shares after buying stock.
			mapper.update_number_of_shares(new_number_of_shares, ticker_symbol, username)
			return "Stock purchase was successful."
	else:
		# Returns error response.
		return "Error: You do not have enough money in your balance to execute that trade."

def sell(ticker_symbol, trade_volume, username):
	# TODO: Add database support for reading from and writing to the orders (transactions) table.
	# Checks if the user holds any stock from the company with ticker_symbol.
	ticker_symbols = mapper.get_ticker_symbols(ticker_symbol, username)
	if len(ticker_symbols) == 0:
		return "Error: You do not hold any shares from that company."
	balance = mapper.get_balance(username)
	brokerage_fee = 6.95
	number_of_shares = mapper.get_number_of_shares(ticker_symbol, username)
	new_number_of_shares = number_of_shares - int(trade_volume)
	last_price = get_last_price(ticker_symbol)
	balance_to_add = last_price * float(trade_volume) - brokerage_fee
	# If the user holds enough shares to complete their trade.
	if int(trade_volume) <= number_of_shares:
		# If the new number of shares would be 0 after the user sells their shares.
		if new_number_of_shares == 0:
			# Deletes the row from holdings database table for company with ticker_symbol.
			mapper.delete_holdings_row(ticker_symbol)
		else:
			# Updates holdings database table with the new number of shares.
			mapper.update_number_of_shares(new_number_of_shares, ticker_symbol, username)
		new_balance = balance + balance_to_add
		# Updates users database table with the new balance after selling the stock.
		mapper.update_balance(new_balance, username)
		return "Stock sell was successful."
	else:
		# Returns error response.
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
