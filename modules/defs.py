import datetime
from aiogram import Bot, Dispatcher, executor, types
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
import pandas as pd
from config import *
from database.db import *
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


async def getVol(message, bot, dp):
	try:
		await dp.throttle(message.text, rate=3)
	except Throttled:
		msg = f'<b>Подождите 3 секунды. Нельзя часто использовать эту команду.</b>'
		if getUserStat(message.from_user.id)[5] == 'en':
			msg = "<b>Wait 3 seconds. You can't use this command often.</b>"

		await message.reply(msg)
		await bot.send_message(logs_chat_id, f'<b>Пользователь {message.from_user.username} спамит!\n\n{message.text}</b>\n\n<i>Id: {message.from_user.id}</i>')
	else:
		await bot.send_message(message.from_user.id, 'This feature is still in development')


async def getProfile(message, bot):
	key1 = types.InlineKeyboardButton('🇷🇺Russian', callback_data='langru')
	key2 = types.InlineKeyboardButton('🇬🇧English', callback_data='langen')
	keyboard = types.InlineKeyboardMarkup().add(key1, key2)

	msg = f'<b>⚙️Ваш профиль:</b>\n\n<b>💳Подписка:</b> {None}\n<b>📝Язык:</b> {getUserStat(message.from_user.id)[5]}\n\n<b>🗓Дата регистрации:</b> {getUserStat(message.from_user.id)[2]}\n\n<i>Id: {message.from_user.id}</i>'
	if getUserStat(message.from_user.id)[5] == 'en':
		msg = f'<b>⚙️Your profile:</b>\n\n<b>💳Subscription:</b> {None}\n<b>📝Language:</b> {getUserStat(message.from_user.id)[5]}\n\n<b>🗓Date of registration:</b> {getUserStat(message.from_user.id)[2]}\n\n<i>Id: {message.from_user.id}</i>'

	await bot.send_message(message.from_user.id, msg, reply_markup=keyboard)


def getKeyboard(message, arg):
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

	if arg == 'main':
		if getUserStat(message.from_user.id)[5] == 'en':
			keyboard.row('Profile', 'FAQ')
			keyboard.row('Tools')
		else:
			keyboard.row('Профиль', 'FAQ')
			keyboard.row('Инструменты')
	if arg == 'tools':
		if getUserStat(message.from_user.id)[5] == 'en':
			keyboard.row('Scam', 'Coins', 'Volatility')
			keyboard.row('Algorithm', 'Portfolio', 'Menu')
		else:
			keyboard.row('Скам', 'Койны', 'Волатильность')
			keyboard.row('Алгоритм', 'Портфель', 'Меню')
	if arg == 'logic':
		if getUserStat(message.from_user.id)[5] == 'en':
			keyboard.row('On', 'Off')
			keyboard.row('Options', 'Tools')
		else:
			keyboard.row('Вкл', 'Выкл')
			keyboard.row('Настройки', 'Инструменты')

	return keyboard


def spaces(lst, string):
	string = str(string)
	tmp = []
	for i in range(len(lst)):
		tmp.append(len(str(lst[i])))
	n = max(tmp)
	f = len(string)
	while len(string) < n:
		string += ' '

	return string


async def getCoins(message, bot, value):
	msg = ''

	if value == 'binance':
		client = Client(binance_token, binance_secret)
		tickers = client.get_all_tickers()
		ticker_df = pd.DataFrame(tickers)
		ticker_df.set_index('symbol', inplace=True)

		temp, temp2 = [], []
		msg = f'<b>Всего монет:</b> <i>{len(cmd_coins)}</i>\n<b>Биржа:</b> <i>{value}</i>\n\n'
		if getUserStat(message.from_user.id)[5] == 'en':
			msg = f'<b>Total coins:</b> <i>{len(cmd_coins)}</i>\n<b>Stock Market:</b> <i>{value}</i>\n\n'

		for i in range(len(cmd_coins) // 2):
			temp.append(f'<code>{cmd_coins[i][:-4]}: ${round(float(ticker_df.loc[cmd_coins[i]]["price"]), 3)}</code>')

		for i in range(len(cmd_coins) // 2, len(cmd_coins)):
			temp2.append(f'<code>{cmd_coins[i][:-4]}: ${round(float(ticker_df.loc[cmd_coins[i]]["price"]), 3)}</code>')

		for i in range(len(temp)):
			msg += f'<code>{spaces(temp, temp[i])} {temp2[i]}</code>\n'

	if value == 'bybit':
		prices = getPrice(bybit_coins)
		temp, temp2 = [], []
		msg = f'<b>Всего монет:</b> <i>{len(bybit_coins)}</i>\n<b>Биржа:</b> <i>{value}</i>\n\n'

		for i in range(len(bybit_coins) // 2):
			temp.append(f'<code>{bybit_coins[i][:-4]}: ${prices[i]}</code>')

		for i in range(len(bybit_coins) // 2, len(bybit_coins)):
			temp2.append(f'<code>{bybit_coins[i][:-4]}: ${prices[i]}</code>')

		for i in range(len(temp)):
			msg += f'<code>{spaces(temp, temp[i])} {temp2[i]}</code>\n'

	updateUnick(message.from_user.id, message.from_user.username)
	await bot.send_message(message.from_user.id, msg, reply_markup=getKeyboard(message, 'tools'))


async def getOptions(message, bot):
	msg = ''

	if getUserStat(message.from_user.id)[4]:
		msg = f'<b>Текущие настройки:</b>\n\nИнтервал: {getHours(message.from_user.id)}\nПроцент: {getProcent(message.from_user.id)}\nКод регистрации: /{getCode()}'
		if getUserStat(message.from_user.id)[5] == 'en':
			msg = f'<b>Current options:</b>\n\nInterval: {getHours(message.from_user.id)}\nPercent: {getProcent(message.from_user.id)}\nCode for registration: /{getCode()}'
	else:
		msg = f'<b>Текущие настройки:</b>\n\nИнтервал: {getHours(message.from_user.id)}\nПроцент: {getProcent(message.from_user.id)}'
		if getUserStat(message.from_user.id)[5] == 'en':
			msg = f'<b>Current options:</b>\n\nInterval: {getHours(message.from_user.id)}\nPercent: {getProcent(message.from_user.id)}'

	await bot.send_message(message.from_user.id, msg)


def checkPrice(coin):
	client = Client(binance_token, binance_secret)
	tickers = client.get_all_tickers()
	ticker_df = pd.DataFrame(tickers)
	ticker_df.set_index('symbol', inplace=True)

	try:
		return round(float(ticker_df.loc[str(coin)]["price"]), 3)
	except Exception:
		return 'Error'



# def getKeyboard():
# 	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
# 	keyboard.row('ON✅', 'OFF❌')
# 	keyboard.row('COINS💰', 'OPTIONS⚙️')
#
# 	return keyboard
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
