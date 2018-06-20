#!/usr/bin/env python3


import mapper
import wrapper


def buy(ticker_symbol, trade_volume, username):
	last_price = wrapper.get_last_price(ticker_symbol)
	# Error handling: if the user enters a ticker symbol that does not exist.
	if last_price == "exit":
		print("The ticker symbol that you entered does not exist.")
		return "exit"
	balance = mapper.get_balance(username)
	brokerage_fee = 6.95
	# Error handling: if the user enters a trade volume that is not a number.
	try:
		transaction_cost = last_price * float(trade_volume) + brokerage_fee
	except ValueError:
		print("The trade volume you entered is not valid.")
		return "exit"
	# If the user has enough money in their account to execute the trade.
	if transaction_cost < balance:
		ticker_symbols = mapper.get_ticker_symbols(ticker_symbol, username)
		# If the user does not hold any stock from company with ticker_symbol.
		if len(ticker_symbols) == 0:
			new_balance = balance - transaction_cost
			# Updates the user's balance in the users database table.
			mapper.update_balance(new_balance, username)
			# Inserts a new row to the holdings database table after buying the stock.
			mapper.insert_holdings_row(ticker_symbol, trade_volume, last_price, username)
			# Inserts a new row to the orders database table after buying the stock.
			mapper.insert_orders_row("buy", ticker_symbol, trade_volume, last_price, username)
			return "Stock purchase was successful."
		# If the user holds some stock from company with ticker_symbol.
		else:
			# Gets the number of shares from holdings database table for the company with ticker_symbol.
			curr_number_of_shares = mapper.get_number_of_shares(ticker_symbol, username)
			new_number_of_shares = curr_number_of_shares + int(trade_volume)
			# Updates the holdings database table with the new number of shares after buying stock.
			mapper.update_number_of_shares(new_number_of_shares, ticker_symbol, username)
			# Inserts a new row to the orders database table after buying the stock.
			mapper.insert_orders_row("buy", ticker_symbol, trade_volume, last_price, username)
			return "Stock purchase was successful."
	else:
		# Returns error response.
		return "Error: You do not have enough money in your balance to execute that trade."

def sell(ticker_symbol, trade_volume, username):
	last_price = wrapper.get_last_price(ticker_symbol)
	# Error handling: if the user enters a ticker symbol that does not exist.
	if last_price == "exit":
		print("The ticker symbol that you entered does not exist.")
		return "exit"
	brokerage_fee = 6.95
	# Error handling: if the user enters a trade volume that is not a number.
	try:
		balance_to_add = last_price * float(trade_volume) - brokerage_fee
	except ValueError:
		print("The trade volume you entered is not valid.")
		return "exit"
	# Checks if the user holds any stock from the company with ticker_symbol.
	ticker_symbols = mapper.get_ticker_symbols(ticker_symbol, username)
	if len(ticker_symbols) == 0:
		return "Error: You do not hold any shares from that company."
	balance = mapper.get_balance(username)
	number_of_shares = mapper.get_number_of_shares(ticker_symbol, username)
	new_number_of_shares = number_of_shares - int(trade_volume)
	# If the user holds enough shares to complete their trade.
	if int(trade_volume) <= number_of_shares:
		# If the new number of shares would be 0 after the user sells their shares.
		if new_number_of_shares == 0:
			# Deletes the row from holdings database table for company with ticker_symbol.
			mapper.delete_holdings_row(ticker_symbol)
		else:
			# Updates holdings database table with the new number of shares.
			mapper.update_number_of_shares(new_number_of_shares, ticker_symbol, username)
		new_balance = balance + balance_to_add
		# Updates users database table with the new balance after selling the stock.
		mapper.update_balance(new_balance, username)
		# Inserts a new row to the orders database table after selling the stock.
		mapper.insert_orders_row("sell", ticker_symbol, trade_volume, last_price, username)
		return "Stock sell was successful."
	else:
		# Returns error response.
		return "Error: You do not have enough shares to sell to complete that trade."

### Wrapper
def get_ticker_symbol(company_name):
	return wrapper.get_ticker_symbol(company_name)

def get_last_price(ticker_symbol):
	return wrapper.get_last_price(ticker_symbol)

### Mapper
def create_account(username, password):
	return mapper.create_account(username, password)

def login(username, password):
	return mapper.login(username, password)

def get_balance(username):
	return mapper.get_balance(username)

def get_holdings_dataframe(username):
	return mapper.get_holdings_dataframe(username)
