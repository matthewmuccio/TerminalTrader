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

def admin_loop(username):
	# Admin menu (balance, deposit, withdraw, set, portfolio, leaderboard, users, exit)
	admin_done = False
	while not admin_done:
		balance_inputs = ["a", "balance"]
		deposit_inputs = ["d", "deposit"]
		withdraw_inputs = ["w", "withdraw"]
		set_inputs = ["t", "set"]
		portfolio_inputs = ["p", "portfolio"]
		leaderboard_inputs = ["l", "leaderboard"]
		users_inputs = ["u", "users"]
		exit_inputs = ["e", "exit"]

		acceptable_inputs = balance_inputs\
					+deposit_inputs\
					+withdraw_inputs\
					+set_inputs\
					+portfolio_inputs\
					+leaderboard_inputs\
					+users_inputs\
					+exit_inputs

		user_input = view.admin_menu()
		# If the user input is acceptable.
		if user_input.lower() in acceptable_inputs:
			# Balance
			if user_input.lower() in balance_inputs:
				username = view.admin_balance_menu()
				balance = model.get_balance(username)
				view.admin_display_balance(username, balance)
			# Deposit
			elif user_input.lower() in deposit_inputs:
				username, balance_to_add = view.admin_deposit_menu()
				balance = model.get_balance(username)
				new_balance = model.calculate_new_deposit(balance, balance_to_add)
				model.update_balance(new_balance, username)
				view.admin_display_new_balance(username, balance, new_balance)
			# Withdraw
			elif user_input.lower() in withdraw_inputs:
				username, balance_to_subtract = view.admin_withdraw_menu()
				balance = model.get_balance(username)
				new_balance = model.calculate_new_withdraw(balance, balance_to_subtract)
				model.update_balance(new_balance, username)
				view.admin_display_new_balance(username, balance, new_balance)
			# Set
			elif user_input.lower() in set_inputs:
				username, balance_to_set = view.admin_set_menu()
				balance = model.get_balance(username)
				new_balance = model.calculate_new_set(balance, balance_to_set)
				model.update_balance(new_balance, username)
				view.admin_display_new_balance(username, balance, new_balance)
			# Portfolio
			elif user_input.lower() in portfolio_inputs:
				username = view.admin_portfolio_menu()
				df = model.get_holdings_dataframe(username)
				balance = model.get_balance(username)
				earnings = model.get_earnings(username)
				view.display_dataframe(df, balance, earnings, username)
			# Leaderboard
			elif user_input.lower() in leaderboard_inputs:
				view.admin_leaderboard_wait()
				leaderboard = model.get_leaderboard()
				view.admin_display_leaderboard(leaderboard)
			# Users
			elif user_input.lower() in users_inputs:
				users = model.get_users()
				view.admin_display_users(users)
			# Exit
			elif user_input.lower() in exit_inputs:
				view.exit_message()
				admin_done = True
			# Otherwise
			else:
				return "Error"

def game_loop(username):
	# Main menu (balance, buy, sell, lookup, quote, portfolio, exit)
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
				df = model.get_holdings_dataframe(username)
				balance = model.get_balance(username)
				earnings = model.get_earnings(username)
				view.display_dataframe(df, balance, earnings, username)
			# Exit
			elif user_input.lower() in exit_inputs:
				view.exit_message()
				main_done = True
			# Otherwise
			else:
				return "Error"


if __name__ == "__main__":
	# result will either store the user's username if they log in/create an account,
	# or "exit" if the user chooses to exit the terminal.
	result = start_menu()
	if result != "exit":
		if result == "admin":
			admin_loop(result)
		else:
			game_loop(result)
