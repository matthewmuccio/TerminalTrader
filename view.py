#!/usr/bin/env python3


import getpass
import os


# Displays Terminal Trader header.
def display_header():
	os.system("clear")
	print("=".center(65, "="))
	print("Terminal Trader".center(65, " "))
	print("=".center(65, "="))

### Menus
# Displays start menu of the application.
def start_menu():
	display_header()
	print("Welcome to Terminal Trader, a simple terminal trading application \nfor buying and selling stocks with real market data.\n")
	print("What do you want to do?")
	print("1: Create a Terminal Trader account.")
	print("2: Log in to your Terminal Trader account.")
	print("3: Exit Terminal Trader.")
	user_input = input()
	return user_input

# Displays create account menu and takes in username and password.
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

# Displays login menu and takes in username and password.
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

### Admin
# Main menu for the admin.
def admin_menu():
	display_header()
	print("Hello Mr. Admin, what do you want to do?")
	print("Balance     / a - Check a user's account balance.")
	print("Deposit     / d - Deposit into a user's account balance.")
	print("Withdraw    / w - Withdraw from a user's account balance.")
	print("Set         / t - Set a user's account balance.")
	print("Portfolio   / p - Display all holdings in a user's portfolio.")
	print("Leaderboard / l - Display a list of the top 10 users by portfolio earnings.")
	print("Users       / u - Display a list of all users in our database.")
	print("Exit        / e - Exit Terminal Trader.")
	user_input = input()
	return user_input

# Balance
def admin_balance_menu():
	display_header()
	print("Which user's balance would you like to view?")
	username = input("Username: ")
	return username

def admin_display_balance(username, balance):
	display_header()
	if balance == "exit":
		print("There is no account with username \"{0}\" in our database.".format(username))
	else:
		print("{0}'s balance: ${1}".format(username, format(balance, ".2f")))
	exit = wait("previous menu")

def admin_display_new_balance(username, old_balance, new_balance):
	display_header()
	if old_balance == "exit" or new_balance == "exit":
		print("There was an error with your input. Please try again.")
	else:
		print("{0}'s balance has been updated from ${1} to ${2}.".format(username, format(old_balance, ".2f"), format(new_balance, ".2f")))
	exit = wait("previous menu")

# Deposit
def admin_deposit_menu():
	display_header()
	print("Into which user's balance would you like to deposit?")
	username = input("Username: ")
	print("How much would you like to deposit into {0}'s account?".format(username))
	balance = input("Balance to add: $")
	return username, balance

# Withdraw
def admin_withdraw_menu():
	display_header()
	print("From which user's balance would you like to withdraw?")
	username = input("Username: ")
	print("How much would you like to withdraw from {0}'s account?".format(username))
	balance = input("Balance to subtract: $")
	return username, balance

# Set
def admin_set_menu():
	display_header()
	print("Which user's balance would you like to set?")
	username = input("Username: ")
	print("To what dollar value would you like to set {0}'s account?".format(username))
	balance = input("Balance to set: $")
	return username, balance

# Portfolio
def admin_portfolio_menu():
	display_header()
	print("Which user's portfolio would you like to view?")
	username = input("Username: ")
	return username

# Leaderboard
def admin_display_leaderboard(leaderboard):
	display_header()
	print("List of the Top 10 Users by Portfolio Earnings")
	i = 1
	for user, earnings in leaderboard:
		if i <= 10:
			print("{0}. {1} - ${2}".format(i, user, format(earnings, ".2f")))
			i += 1
		else:
			break
	exit = wait("previous menu")

def admin_leaderboard_wait():
	print("\nCalculating profits for each user ...")

# Users
def admin_display_users(users):
	display_header()
	print("List of Terminal Trader Users")
	i = 1
	for user in sorted(users):
		print("{0}. {1}".format(i, user))
		i += 1
	exit = wait("previous menu")

### User
# Main menu for the user.
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

# Displays the user's balance.
def balance_menu(balance):
	display_header()
	print("Account Balance: ${0}".format(format(balance, ".2f")))
	exit = wait("previous menu")

# Takes in a ticker symbol and trade volume that the user wants to buy.
def buy_menu():
	display_header()
	ticker_symbol = input("Ticker symbol: ")
	trade_volume = input("Trade volume: ")
	return ticker_symbol, trade_volume

# Takes in a ticker symbol and trade volume that the user wants to sell.
def sell_menu():
	display_header()
	ticker_symbol = input("Ticker symbol: ")
	trade_volume = input("Trade volume: ")
	return ticker_symbol, trade_volume

# Takes in a company's name for which to look up the ticker symbol.
def lookup_menu():
	display_header()
	company_name = input("Company name: ")
	return company_name

# Takes in a company's ticker symbol for which to look up the current market price.
def quote_menu():
	display_header()
	ticker_symbol = input("Ticker Symbol: ")
	return ticker_symbol

# Displays the exit message upon a user exit.
def exit_message():
	display_header()
	print("Thanks for playing Terminal Trader!\n")

# Displays the user's portfolio in a pandas DataFrame.
def display_dataframe(df, balance, earnings, username):
	display_header()
	if df.empty:
		print("There is no portfolio to display for {0}.".format(username))
		print("You must make a stock purchase first.")
	else:
		print("{0}'s Portfolio".format(username))
		print("Liquid balance: ${0}".format(format(balance, ".2f")))
		print("Estimated earnings: ${0}".format(format(earnings, ".2f")))
		print(df)
	exit = wait("previous menu")

# Allows for the user to press enter when they are finished reading the output to continue.
def wait(str):
	x = input("\nPress \"Enter\" to access the {0} ...".format(str))
	return x

### Error handling/displaying
# Displays the response from a call to the model, view, or controller.
def display_response(res):
	if res != "exit":
		print(res)
	exit = wait("previous menu")

# Displays the ticker symbol for a company.
def display_ticker_symbol(ticker_symbol):
	if ticker_symbol == "exit":
		print("The company name that you entered does not exist.")
	else:
		print(ticker_symbol)
	exit = wait("previous menu")

# Displays the current market price for a company's stock.
def display_last_price(last_price):
	if last_price == "exit":
		print("The ticker symbol that you entered does not exist.")
	else:
		print(last_price)
	exit = wait("previous menu")
