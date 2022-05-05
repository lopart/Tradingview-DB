## Creating an input for tradingview API

import yfinance as yf
import os
import sys
import pandas as pd

## - insert market, stock, strategy and timeframe into input √
## - list and find inputs √
## - check if an input is matching a varaible from the list of stocks/timeframes √
## - delete json rows √
## - crypto √


class InputCheck:
	def __init__(self, ticker, timeframe):
		## monitors ticker from finance!Yahoo for stock exchange only (no cryptocurrencies)
		self.x = str(ticker)
		self.timeframe = str(timeframe)
		self.timeframe_list = ['1','3','5','15','30','45','60','120','180','240','1D','1W','1M','D','W','M']
		
	def check_ticker(self):
		try:
			stock = yf.Ticker(self.x)
			return stock.info
		except:
			print("Wrong ticker, try again.")
					
	def check_timeframe(self):
		if self.timeframe in self.timeframe_list:
			#print('Timeframe accepted')
			return self.timeframe
		else:
			return False

class StrategyCheck:
	def __init__(self, ranking):
		self.path = '/Users/artem_lopatenko/workspace/javascript'
		self.name = 'strategy.json'
		os.chdir(self.path)
		self.df = pd.read_json(self.name)
		self.ranking = int(ranking)
		
	def list_all(self):
		print(self.df)
		
	def select_strategy(self):
		# selecting strategy by its rank
		if self.ranking in self.df['ranking']:
			return self.df.at[self.ranking-1, 'strategy']
		else:
			raise Exception("Wrong ranking or strategy, try again.")

class DatabaseManager:
	def __init__(self):
		# path to json file
		self.path = '/Users/artem_lopatenko/workspace/javascript'
		self.name = 'tradingview_input.json'
		os.chdir(self.path)
		self.df = pd.read_json(self.name)
		super().__init__()
		
	def print_db(self):
		print(self.df)
		
	def add_strategy(self, StrategyCheck, InputCheck):
		if InputCheck.check_timeframe()!=False:
			stock1 = InputCheck.check_ticker()['symbol']
			if "-" in stock1:
                stock1 = stock1.replace("-","",1)
                market1 = 'BINANCE'
            else:
                market1 = InputCheck.check_ticker()['exchange']
			strategy1 = StrategyCheck.select_strategy()
			timeframe1 = int(InputCheck.check_timeframe())
			new_row = {'market':market1, 'stock':stock1, 'strategy':strategy1, 'timeframe':timeframe1}
			
			d = ((self.df['strategy'] == strategy1) & (self.df['stock'] == stock1) & (self.df['timeframe'] == timeframe1)).any()
			if d == True:
				print('The strategy already exists.')
			else:
				self.df = self.df.append(new_row, ignore_index=True)
				self.df.to_json('/Users/artem_lopatenko/workspace/javascript/tradingview_input.json', orient="records")
				print(self.df)

	def delete_strategy(self, index):
		index = int(index)
		if len(self.df) > index:
			self.df = self.df.drop(index)
			self.df.to_json('/Users/artem_lopatenko/workspace/javascript/tradingview_input.json', orient="records")
		else:
			print("Index out of range.")



if __name__ == "__main__":

## --help function: shows help window [ 0 arg ]
## --list function: lists 1) set of inputs and 2) set of strategies [ 1 arg ]
## --add function: adds an input into a set [ 3 args ]
## --delete function: delete an input from a set [ 1 arg ]

	def call_option(option):
		if option == '--help':
			if len(sys.argv) == 2:
				print("... details outputed by help function ...")
			else:
				raise Exception("Too many arguments, try MarketSet.py --help.")
		elif option == '--list':
			if len(sys.argv) == 3 and sys.argv[2] == 'input':
				if sys.argv[2] == 'input':
					new_db = DatabaseManager()
					new_db.print_db()
			else:
				raise Exception("Tipe 'strategy' or 'input' as an argument.")
		elif option == '--add':
			if len(sys.argv) == 5:
				input_row = InputCheck(sys.argv[2], sys.argv[3])
				strategy = StrategyCheck(sys.argv[4])
				new_db = DatabaseManager()
				new_db.add_strategy(strategy, input_row)
			else:
				raise Exception("Missing arguments / too many arguments.")
		elif option == '--delete':
			if len(sys.argv) == 3:
				new_db = DatabaseManager()
				new_db.delete_strategy(sys.argv[2])
			else:
				raise Exception("Missing arguments / too many arguments. Select strategy you want to delete by inserting number. The order of strategies can be found with the command 'MarketSet.py --list input'.")
		else:
			raise Exception("Wrong function. Check MarketSet.py --help.")

	if len(sys.argv) == 1:
		print("Tipe MarketSet.py --help for help")
	else:
		call_option(sys.argv[1])
