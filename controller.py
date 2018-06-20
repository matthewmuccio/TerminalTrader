#!/usr/bin/env python3


import model
import view


def start_menu():
	# Start menu (create account, log in, exit)
	start_done = False
	while not start_done:
		user_input = view.start_menu()
		if user_input == "1":
			username, password = view.create_account_menu()
			status = model.create_account(username, password)
			print(status)
			if "Success" in status:
				start_done = True
				exit = view.wait("main menu")
				return username
			else:
				exit = view.wait("previous menu")
		elif user_input == "2":
			username, password = view.login_menu()
			status = model.login(username, password)
			print(status)
			if "Success" in status:
				start_done = True
				exit = view.wait("main menu")
				return username
			else:
				exit = view.wait("previous menu")
		elif user_input == "3":
			status = view.exit_message()
			start_done = True
			print(status)
			return "exit"

def game_loop(username):
	# Main menu (buy, sell, lookup, quote, exit)
	main_done = False
	while not main_done:
		balance_inputs = ["a", "balance"]
		buy_inputs = ["b", "buy"]
		sell_inputs = ["s", "sell"]
		lookup_inputs = ["l", "lookup"]
		quote_inputs = ["q", "quote"]
		portfolio_inputs = ["p", "portfolio"]
		exit_inputs = ["e", "exit"]

		acceptable_inputs = balance_inputs\
					+buy_inputs\
					+sell_inputs\
					+lookup_inputs\
					+quote_inputs\
					+portfolio_inputs\
					+exit_inputs

		user_input = view.main_menu(username)
		# If the user input is acceptable.
		if user_input.lower() in acceptable_inputs:
			# Balance
			if user_input.lower() in balance_inputs:
				balance = model.get_balance(username)
				view.balance_menu(balance)
			# Buy
			elif user_input.lower() in buy_inputs:
				ticker_symbol, trade_volume = view.buy_menu()
				res = model.buy(ticker_symbol, trade_volume, username)
				view.display_response(res)
			# Sell
			elif user_input.lower() in sell_inputs:
				ticker_symbol, trade_volume = view.sell_menu()
				res = model.sell(ticker_symbol, trade_volume, username)
				view.display_response(res)
			# Lookup
			elif user_input.lower() in lookup_inputs:
				company_name = view.lookup_menu()
				ticker_symbol = model.get_ticker_symbol(company_name)
				view.display_ticker_symbol(ticker_symbol)
			# Quote
			elif user_input.lower() in quote_inputs:
				ticker_symbol = view.quote_menu()
				last_price = model.get_last_price(ticker_symbol)
				view.display_last_price(last_price)
			# Portfolio (Holdings)
			elif user_input.lower() in portfolio_inputs:
				res = model.display_holdings(username)
			# Exit
			elif user_input.lower() in exit_inputs:
				view.exit_message()
				main_done = True
			# Otherwise
			else:
				return "Error"


if __name__ == "__main__":
	result = start_menu()
	if result != "exit":
		game_loop(result)
