#!/usr/bin/env python3


import os


def display_header():
	os.system("clear")
	print("-".center(30, "-"))
	print("Terminal Trader".center(30, " "))
	print("-".center(30, "-"))

def buy_menu():
	display_header()
	ticker_symbol = input("Ticker symbol: ")
	trade_volume = input("Trade volume: ")
	return ticker_symbol, trade_volume

def sell_menu():
	display_header()
	ticker_symbol = input("Ticker symbol: ")
	trade_volume = input("Trade volume: ")
	return ticker_symbol, trade_volume

def main_menu():
	display_header()
	user_input = input("What do you want to do? ")
	return user_input

def lookup_menu():
	display_header()
	company_name = input("Company name: ")
	return company_name

def quote_menu():
	display_header()
	ticker_symbol = input("Ticker Symbol: ")
	return ticker_symbol

def exit_message():
	return "Thanks for playing!"


if __name__ == "__main__":
	print(buy_menu())
