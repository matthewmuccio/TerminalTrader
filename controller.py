#!/usr/bin/env python3


import model
import view


def game_loop():
	while True:
		#x = input("What do you want to do?") # This is done in view.py
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

		user_input = view.main_menu()
		if user_input.lower() in acceptable_inputs:
			if user_input.lower() in buy_inputs:
				ticker_symbol, trade_volume = view.buy_menu()
				status = model.buy(ticker_symbol, trade_volume)
				print(status)
				#return status
			elif user_input.lower() in sell_inputs:
				ticker_symbol, trade_volume = view.sell_menu()
				status = model.sell(ticker_symbol, trade_volume)
				print(status)
				#return status
			elif user_input.lower() in lookup_inputs:
				company_name = view.lookup_menu()
				ticker_symbol = model.get_ticker_symbol(company_name)
				print(ticker_symbol)
				#return ticker_symbol
			elif user_input.lower() in quote_inputs:
				ticker_symbol = view.quote_menu()
				last_price = model.get_last_price(ticker_symbol)
				print(last_price)
				#return last_price
			elif user_input.lower() in exit_inputs:
				# TODO: Add exit message in view module.
				break
			else:
				return "Error"


if __name__ == "__main__":
	#print(game_loop())
	game_loop()
