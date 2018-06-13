#!/usr/bin/env python3


import json

import requests

import wrapper
import mapper


def get_last_price(ticker_symbol):
	endpoint = "http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?symbol=" + ticker_symbol
	response = json.loads(requests.get(endpoint).text)
	last_price = response["LastPrice"]
	return last_price
