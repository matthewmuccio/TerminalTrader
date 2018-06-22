#!/usr/bin/env python3


import getpass
import os


def display_header():
	os.system("clear")
	print("=".center(65, "="))
	print("Terminal Trader".center(65, " "))
	print("=".center(65, "="))

### Menus
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
	done = False
	while not done:
		display_header()
		print("Create a Terminal Trader account ...")
		username = input("Username: ")
		password1 = getpass.getpass()
		password2 = getpass.getpass()
		if password1 == password2:
			done = True
		else:
			print("The passwords you entered did not match, please try again.")
			exit = wait("menu again")
			os.system("clear")
	return username, password1

def login_menu():
	done = False
	while not done:
		display_header()
		print("Log in to your Terminal Trader account ...")
		username = input("Username: ")
		password1 = getpass.getpass()
		password2 = getpass.getpass()
		if password1 == password2:
			done = True
		else:
			print("The passwords you entered did not match, please try again.")
			exit = wait("menu again")
			os.system("clear")
	return username, password1

def admin_menu():
	display_header()
	print("Hello Mr. Admin, what do you want to do?")
	print("Balance   / a - Check a user's account balance.")
	print("Deposit   / d - Deposit into a user's account balance.")
	print("Withdraw  / w - Withdraw from a user's account balance.")
	print("Buy       / b - Buy stock for a user's account.")
	print("Sell      / s - Sell stock for a user's account.")
	print("Portfolio / p - Display all holdings in a user's portfolio.")
	print("Exit      / e - Exit Terminal Trader.")
	user_input = input()
	return user_input

def main_menu(username):
	display_header()
	print("Hello {0}, what do you want to do?".format(username))
	print("Balance   / a - Check your account balance.")
	print("Buy       / b - Buy stock at the current market price.")
	print("Sell      / s - Sell stock at the current market price.")
	print("Lookup    / l - Look up the ticker symbol for a company.")
	print("Quote     / q - Get the current market price for a company's stock.")
	print("Portfolio / p - Displays all holdings in your portfolio.")
	print("Exit      / e - Exit Terminal Trader.")
	user_input = input()
	return user_input

def balance_menu(balance):
	display_header()
	print("Account Balance: ${0}".format(format(balance, ".2f")))
	exit = wait("previous menu")

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
	print("Thanks for playing Terminal Trader!\n")

def display_dataframe(df):
	display_header()
	if df.empty:
		print("There is no portfolio to display.")
		print("You must make a trade first.")
	else:
		print(df)
	exit = wait("previous menu")

def wait(str):
	x = input("\nPress \"Enter\" to access the {0} ...".format(str))
	return x

### Error handling/displaying
def display_response(res):
	if res != "exit":
		print(res)
	exit = wait("previous menu")

def display_ticker_symbol(ticker_symbol):
	if ticker_symbol == "exit":
		print("The company name that you entered does not exist.")
	else:
		print(ticker_symbol)
	exit = wait("previous menu")

def display_last_price(last_price):
	if last_price == "exit":
		print("The ticker symbol that you entered does not exist.")
	else:
		print(last_price)
	exit = wait("previous menu")
