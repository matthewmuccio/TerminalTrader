#!/usr/bin/env python3


import model
import view


def game_loop():
	while True:
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
				exit = view.wait()
			elif user_input.lower() in sell_inputs:
				ticker_symbol, trade_volume = view.sell_menu()
				status = model.sell(ticker_symbol, trade_volume)
				print(status)
				exit = view.wait()
			elif user_input.lower() in lookup_inputs:
				company_name = view.lookup_menu()
				ticker_symbol = model.get_ticker_symbol(company_name)
				print(ticker_symbol)
				exit = view.wait()
			elif user_input.lower() in quote_inputs:
				ticker_symbol = view.quote_menu()
				last_price = model.get_last_price(ticker_symbol)
				print(last_price)
				exit = view.wait()
			elif user_input.lower() in exit_inputs:
				status = view.exit_message()
				print(status)
				break
			else:
				return "Error"


if __name__ == "__main__":
	#print(game_loop())
	game_loop()
