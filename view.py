#!/usr/bin/env python3


import getpass
import os

import mapper


def display_header():
	os.system("clear")
	print("=".center(65, "="))
	print("Terminal Trader".center(65, " "))
	print("=".center(65, "="))

def start_menu():
	display_header()
	print("Welcome to Terminal Trader, a simple terminal trading application \nfor buying and selling stocks with real market data.\n")
	print("What do you want to do?")
	print("1: Create a Terminal Trader account.")
	print("2: Log in to your Terminal Trader account.")
	print("3: Exit Terminal Trader.")
	user_input = input()
	return user_input

def create_account_menu():
	display_header()
	print("Create a Terminal Trader account ...")
	username = input("Username: ")
	password = getpass.getpass()
	return username, password

def login_menu():
	display_header()
	print("Log in to your Terminal Trader account ...")
	username = input("Username: ")
	password = getpass.getpass()
	return username, password

def main_menu(username):
	display_header()
	print("What do you want to do?")
	print("Account balance: ${0}".format(format(mapper.get_balance(username), ".2f")))
	print("Buy    / b - Buy stock at the current market price.")
	print("Sell   / s - Sell stock at the current market price.")
	print("Lookup / l - Look up the ticker symbol for a company.")
	print("Quote  / q - Get the current market price for a company's stock.")
	print("Exit   / e - Exit Terminal Trader.")
	user_input = input()
	return user_input

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
	return "Thanks for playing Terminal Trader!\n"

def wait(str):
	x = input("\nPress \"Enter\" to access the {0} ...".format(str))
	return x


if __name__ == "__main__":
	print(buy_menu())
