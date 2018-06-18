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
	print("What do you want to do?")
	print("Buy    / b - Buy stock at the current market price.")
	print("Sell   / s - Sell stock at the current market price.")
	print("Lookup / l - Look up the ticker symbol for a company.")
	print("Quote  / q - Get the current market price for a company's stock.")
	print("Exit   / e - Exit Terminal Trader.")
	user_input = input()
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
	display_header()
	return "Thanks for playing Terminal Trader!"

def wait():
	x = input("Press \"Enter\" to return to the main menu ...")
	return x


if __name__ == "__main__":
	print(buy_menu())
