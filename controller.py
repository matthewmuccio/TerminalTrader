#!/usr/bin/env python3


import model
import view


def game_loop():
	while True:
		#x = input("What do you want to do?") # This is done in view.py
		acceptable_inputs = ["b", "s", "l", "q", "e"]
		user_input = view.main_menu()
		if user_input.lower() in acceptable_inputs:
			if user_input.lower() == "b":
				pass
			elif user_input.lower() == "s":
				pass
			elif user_input.lower() == "l":
				pass
			elif user_input.lower() == "q":
				ticker_symbol = view.quote_menu()
				last_price = model.get_last_price(ticker_symbol)
				return last_price
			elif user_input.lower() == "e":
				# TODO: Add exit message in view module.
				break
			else:
				return "Error"


if __name__ == "__main__":
	print(game_loop())
