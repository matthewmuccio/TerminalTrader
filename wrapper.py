#!/usr/bin/env python3


import json

import requests


def get_last_price(ticker_symbol):
	endpoint = "http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?symbol=" + ticker_symbol
	response = json.loads(requests.get(endpoint).text)
	try:
		last_price = response["LastPrice"]
	except KeyError:
		last_price = "exit"
	return last_price

def get_ticker_symbol(company_name):
	endpoint = "http://dev.markitondemand.com/MODApis/Api/v2/Lookup/json?input=" + company_name
	# TODO: Refactor this line so that it does not just take the first element in the
	# iterable that is returned, and assume it's the symbol we want.
	try:
		response = json.loads(requests.get(endpoint).text)[0]
		ticker_symbol = response["Symbol"]
	except (IndexError, KeyError, UnboundLocalError):
		ticker_symbol = "exit"
	return ticker_symbol
