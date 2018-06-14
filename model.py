#!/usr/bin/env python3


import json

import requests

import wrapper
import mapper


def buy(ticker_symbol, trade_volume):
	# Stuff we might need:
	# - Market price
	# - Volume (how many shares)
	# - check trader's balance
	# - ticker_symbol
	# TODO: Replace the value for balance with a read operation from our database,
	# which should eventually be in our mapper.
	user_balance = 5000.00
	brokerage_fee = 6.95
	transaction_cost = get_last_price(ticker_symbol) * float(trade_volume) + brokerage_fee
	if transaction_cost > user_balance:
		return "You don\'t have enough money!"
	else:
		print(get_last_price(ticker_symbol))
		print(transaction_cost)
		return "Trade was successful."

def sell():
	pass

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
