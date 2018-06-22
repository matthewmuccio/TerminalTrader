#!/usr/bin/env python3


import json

import requests


def get_last_price(ticker_symbol):
	endpoint = "http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?symbol=" + ticker_symbol
	try:
		response = json.loads(requests.get(endpoint).text)
		last_price = response["LastPrice"]
	except (ValueError, KeyError):
		last_price = "exit"
	return last_price

def get_ticker_symbol(company_name):
	endpoint = "http://dev.markitondemand.com/MODApis/Api/v2/Lookup/json?input=" + company_name
	try:
		response = json.loads(requests.get(endpoint).text)[0]
		ticker_symbol = response["Symbol"]
	except (IndexError, ValueError, KeyError, UnboundLocalError):
		ticker_symbol = "exit"
	return ticker_symbol
