#!/usr/bin/env python3


import mapper
import model
import view


def start_menu():
	# Start menu (create account, log in, exit)
	start_done = False
	while not start_done:
		user_input = view.start_menu()
		if user_input == "1":
			username, password = view.create_account_menu()
			status = mapper.create_account(username, password)
			print(status)
			if "Success" in status:
				start_done = True
				exit = view.wait("main menu")
				return username
			else:
				exit = view.wait("previous menu")
		elif user_input == "2":
			username, password = view.login_menu()
			status = mapper.login(username, password)
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
		buy_inputs = ["b", "buy"]
		sell_inputs = ["s", "sell"]
		lookup_inputs = ["l", "lookup"]
		quote_inputs = ["q", "quote"]
		exit_inputs = ["e", "exit"]

		acceptable_inputs = buy_inputs\
					+sell_inputs\
					+lookup_inputs\
					+quote_inputs\
					+exit_inputs

		user_input = view.main_menu(username)
		if user_input.lower() in acceptable_inputs:
			if user_input.lower() in buy_inputs:
				ticker_symbol, trade_volume = view.buy_menu()
				status = model.buy(ticker_symbol, trade_volume, username)
				print(status)
				exit = view.wait("previous menu")
			elif user_input.lower() in sell_inputs:
				ticker_symbol, trade_volume = view.sell_menu()
				status = model.sell(ticker_symbol, trade_volume, username)
				print(status)
				exit = view.wait("previous menu")
			elif user_input.lower() in lookup_inputs:
				company_name = view.lookup_menu()
				ticker_symbol = model.get_ticker_symbol(company_name)
				print(ticker_symbol)
				exit = view.wait("previous menu")
			elif user_input.lower() in quote_inputs:
				ticker_symbol = view.quote_menu()
				last_price = model.get_last_price(ticker_symbol)
				print(last_price)
				exit = view.wait("previous menu")
			elif user_input.lower() in exit_inputs:
				status = view.exit_message()
				print(status)
				main_done = True
			else:
				return "Error"


if __name__ == "__main__":
	result = start_menu()
	if result != "exit":
		game_loop(result)
