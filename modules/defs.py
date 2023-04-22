import datetime
#from modules.parse import getnewPrices, getResponse, getAdvInfo
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
import pandas as pd
from config import *
from database.db import *
from logics.async_logic import *
import os

path_coins = 'allcoins/'


def createFile(file_name):
	try:
		f = open(f'{path_coins}{file_name}', 'r', encoding='utf-8')
		f.close()
	except FileNotFoundError:
		f = open(f'{path_coins}{file_name}', 'w', encoding='utf-8')
		f.close()
		getAllCoins(file_name)


def getAllCoins(file_name):
	f = open(f'{path_coins}{file_name}', 'w', encoding='utf-8')

	client = Client(binance_token, binance_secret)
	tickers = client.get_all_tickers()
	ticker_df = pd.DataFrame(tickers)
	ticker_df.set_index('symbol', inplace=True)

	for i in binance_coins:
		num = float(ticker_df.loc[i]['price'])
		f.write(f'{num}\n')

	# coingeko
	#for i in range(len(coins.keys())):
	#	f.write(f'{getnewPrices(list(coins.values())[i])}\n')
	f.close()


def check_procent_stat(proc, vector):
	proc = float(proc)

	if proc <= 3:
		if vector == 'up':
			return '📈'
		else:
			return '📉'
	if 3 < proc <= 6:
		if vector == 'up':
			return '📈📈'
		else:
			return '📉📉'
	if proc > 6:
		if vector == 'up':
			return '📈📈📈'
		else:
			return '📉📉📉'


def defStarting(uprocent, file_name):
	uprocent = float(uprocent)
	client = Client(binance_token, binance_secret)
	tickers = client.get_all_tickers()
	ticker_df = pd.DataFrame(tickers)
	ticker_df.set_index('symbol', inplace=True)
	new = []
	old = []
	res = []

	with open(f'{path_coins}{file_name}', 'r', encoding='utf-8') as file:
		old = [float(line.rstrip()) for line in file]
	for i in binance_coins:
		new.append(float(ticker_df.loc[i]['price']))

	for i in range(len(binance_coins)):
		if abs(round(old[i] - new[i], 6)) >= round(old[i]*(uprocent/100), 6) and float(abs(round(old[i] - new[i], 6))) != 0:
			tmp = ''
			tmp2 = ''
			print(f'Not empty - {str(datetime.datetime.now())[:-10]}')
			if round(old[i] - new[i], 6) > 0:
				tmp = check_procent_stat(round(((abs(round(old[i] - new[i], 4))*100)/old[i]), 1), 'down')
				tmp2 = '-'
			else:
				tmp = check_procent_stat(round(((abs(round(old[i] - new[i], 4))*100)/old[i]), 1), 'up')
				tmp2 = '+'

			#res.append(f'<b>Цена отклонилась на {round(((abs(round(old[i] - new[i], 4))*100)/old[i]), 1)}%</b>\n\n<b>{uprocent}% =</b> {round(old[i]*(uprocent/100), 6)}\n<b>Койн:</b> {list(coins.keys())[i]}\n<b>Старая цена:</b> {old[i]}\n<b>Новая цена:</b> {new[i]}\n<b>Цена {tmp} на</b> {abs((round(old[i] - new[i], 6)))}\n')
			res.append(f'{tmp}<a href="https://www.binance.com/en/trade/{binance_coins[i][:-4]}_BUSD">{binance_coins[i][:-4]}</a> {tmp2}{round(((abs(round(old[i] - new[i], 4))*100)/old[i]), 2)}% / <b>Цена:</b> {new[i]}\n')

	with open(f'{path_coins}{file_name}', 'w', encoding='utf-8') as file:
		for i in range(len(new)):
			file.write(f'{new[i]}\n')

	return res


def itsAdmin(adm):
	adm = int(adm)
	if adm: return 'Да'
	else: return 'Нет'


def getAllOptions(uid):
	uid = int(uid)
	uprocent, uinterval = getUserStat(uid)[6], getUserStat(uid)[7]
	return [uinterval, uprocent]


def getHours(uid):
	return float(getAllOptions(int(uid))[0])


def getProcent(uid):
	return float(getAllOptions(int(uid))[1])


def getCode():
	code = ''
	with open('modules/code.txt', 'r') as f:
		code = f.readline()
	return code


def changeCode(code):
	with open('modules/code.txt', 'w') as f:
		f.write(code)


class createCase(StatesGroup):
	name = State()
	coin = State()
	price = State()
	volume = State()


class updateCase(StatesGroup):
	name = State()
	coin = State()
	price = State()
	volume = State()


class deleteCase(StatesGroup):
	name = State()


class createScam(StatesGroup):
	check = State()


''' Coingeko
def defStarting():
	new = []
	old = []
	res = []

	with open('coins.txt', 'r', encoding='utf-8') as file:
		old = [line.rstrip() for line in file]
	for i in range(len(coins.keys())):
		new.append(getnewPrices(list(coins.values())[i]))

	for i in range(len(coins.keys())):
		if ',' in str(old[i]):
			old[i] = round(float(str(old[i]).replace(',', '.')), 6)
			new[i] = round(float(str(new[i]).replace(',', '.')), 6)
		else:
			old[i] = round(float(str(old[i]).replace(',', '.')), 6)
			new[i] = round(float(str(new[i]).replace(',', '.')), 6)

		if abs(round(old[i] - new[i], 6)) >= round(old[i]*(getProcent()/100), 6) and float(abs(round(old[i] - new[i], 6))) != 0:
			tmp = ''
			#print(f'\n{list(coins.keys())[i]}: Цена отклонилась на {getProcent()}%\n {old[i]} - {new[i]} = {(round(old[i] - new[i], 4))}\n')
			print('Not empty')
			if round(old[i] - new[i], 6) > 0: tmp = 'упала'
			else: tmp = 'поднялась'

			res.append(f'<b>Цена отклонилась на {round(((abs(round(old[i] - new[i], 4))*100)/old[i]), 1)}%</b>\n<b>Объем торгов за 24 часа:</b> ${int(getAdvInfo(list(coins.values())[i]))/1000000} млн\n\n<b>{getProcent()}% =</b> {round(old[i]*(getProcent()/100), 4)}\n<b>Койн:</b> {list(coins.keys())[i]}\n<b>Старая цена:</b> {old[i]}\n<b>Новая цена:</b> {new[i]}\n<b>Цена {tmp} на</b> {abs((round(old[i] - new[i], 4)))}\n')
	#getAllCoins()
	with open('coins.txt', 'w', encoding='utf-8') as file:
		for i in range(len(new)):
			file.write(f'{new[i]}\n')

	return res
'''
