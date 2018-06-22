#!/usr/bin/env python3


from operator import itemgetter

import mapper
import wrapper


### User
# Buy
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
			# Gets the last price stored in the holdings database table for a given ticker_symbol.
			curr_price = mapper.get_last_price(ticker_symbol, username)
			# Calculates the new VWAP based on the current values in the database table and the most recent (last) prices.
			new_vwap = calculate_vwap(curr_price, curr_number_of_shares, last_price, trade_volume)
			# Updates the VWAP in the holdings database table with a new value.
			mapper.update_volume_weighted_average_price(new_vwap, ticker_symbol, username)
			# Updates the holdings database table with the new number of shares after buying stock.
			mapper.update_number_of_shares(new_number_of_shares, ticker_symbol, username)
			# Inserts a new row to the orders database table after buying the stock.
			mapper.insert_orders_row("buy", ticker_symbol, trade_volume, last_price, username)
			return "Stock purchase was successful."
	else:
		# Returns error response.
		return "Error: You do not have enough money in your balance to execute that trade."

# Sell
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
	# Gets needed values from the user and holdings database tables.
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
		# Gets the last price stored in the holdings database table for a given ticker_symbol.
		curr_price = mapper.get_last_price(ticker_symbol, username)
		# Gets the number of shares from holdings database table for the company with ticker_symbol.
		curr_number_of_shares = mapper.get_number_of_shares(ticker_symbol, username)
		# Calculates the new VWAP based on old values in the database table.
		new_vwap = calculate_vwap(curr_price, curr_number_of_shares, last_price, trade_volume)
		# Updates the VWAP in the holdings database table with a new value.
		mapper.update_volume_weighted_average_price(new_vwap, ticker_symbol, username)
		# Updates users database table with the new balance after selling the stock.
		new_balance = balance + balance_to_add
		mapper.update_balance(new_balance, username)
		# Inserts a new row to the orders database table after selling the stock.
		mapper.insert_orders_row("sell", ticker_symbol, trade_volume, last_price, username)
		return "Stock sell was successful."
	else:
		# Returns error response.
		return "Error: You do not have enough shares to sell to complete that trade."

# Calculates the new volume weighted average to update the holdings database table.
def calculate_vwap(curr_price, curr_num_shares, new_price, new_num_shares):
	old = float(curr_price) * float(curr_num_shares)
	new = float(new_price) * float(new_num_shares)
	total_volume = float(curr_num_shares) + float(new_num_shares)
	return (old + new) / total_volume

### Admin
# Calculates new deposit, and handles errors.
def calculate_new_deposit(balance, balance_to_add):
	if balance == "exit":
		return "exit"
	try:
		return balance + abs(float(balance_to_add))
	except (ValueError, TypeError):
		return "exit"

# Calculates new withdraw, and handles errors.
def calculate_new_withdraw(balance, balance_to_add):
	if balance == "exit":
		return "exit"
	try:
		return balance - abs(float(balance_to_add))
	except (ValueError, TypeError):
		return "exit"

# Calculates the new balance to set, and handles errors.
def calculate_new_set(balance, balance_to_set):
	if balance == "exit":
		return "exit"
	try:
		return float(balance_to_set)
	except (ValueError, TypeError):
		return "exit"

# Gets the portfolio earnings for a given username.
def get_earnings(username):
	user_ticker_symbols = mapper.get_ticker_symbols_from_user(username)
	earnings = 0.0
	for t in user_ticker_symbols:
		last_price = wrapper.get_last_price(t) # Current market price
		user_num_shares = mapper.get_number_of_shares(t, username)
		if last_price == "exit":
			earnings += 0.0
		else:
			earnings += float(last_price) * user_num_shares
	return earnings

# Gets a sorted dictionary representing the leaderboard where the key is the username and the value is their earnings.
def get_leaderboard():
	leaderboard = {}
	users = get_users()
	for user in users:
		earnings = get_earnings(user)
		leaderboard[user] = earnings
	sorted_leaderboard = sorted(leaderboard.items(), key=itemgetter(1), reverse=True)
	return sorted_leaderboard

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

def update_balance(new_balance, username):
	return mapper.update_balance(new_balance, username)

### Admin
def get_users():
	return mapper.get_users()
