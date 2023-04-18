# -*- coding: utf-8 -*-
import logging
import random
import datetime
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.exceptions import Throttled

from config import *
from modules.defs import *
from database.db import *
from modules.bybit import getPrice
from modules.parse import checkCoinScam


class createCase(StatesGroup):
	coin = State()
	price = State()
	volume = State()


class createScam(StatesGroup):
	check = State()


def getKeyboard():
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.row('ON✅', 'OFF❌')
	keyboard.row('COINS💰', 'OPTIONS⚙️')

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
	await bot.send_message(message.from_user.id, msg)
	await bot.send_message(logs_chat_id, f'<b>Пользователь {message.from_user.username} вызвал команду /coins</b>\n\n<i>Id: {message.from_user.id}</i>')


async def getOptions(message, bot):
	msg = ''

	if getUserStat(message.from_user.id)[4]:
		msg = f'<b>Текущие настройки:</b>\n\nИнтервал: {getHours(message.from_user.id)}\nПроцент: {getProcent(message.from_user.id)}\nКод регистрации: /{getCode()}'
	else:
		msg = f'<b>Текущие настройки:</b>\n\nИнтервал: {getHours(message.from_user.id)}\nПроцент: {getProcent(message.from_user.id)}'

	await bot.send_message(message.from_user.id, f'{msg}')


def bot_start():
	logging.basicConfig(level=logging.INFO)
	storage = MemoryStorage()
	bot = Bot(token=telegram_token, parse_mode=types.ParseMode.HTML)
	dp = Dispatcher(bot, storage=storage)




	#
	# Commands for admins
	#




	@dp.message_handler(commands=['admin', 'panel', 'панель'])
	async def admin_panel_cmd(message: types.Message):
		if getUserStat(message.from_user.id) is not None:
			if getUserStat(message.from_user.id)[4]:
				msg = ''\
				'<b>Команды админа:</b>\n\n'\
				'/restart_logic_tf <i>- перезапустить все алгоритмы по тф</i>\n'\
				'/start_logic <i>- запустить все алгоритмы пользователей</i>\n\n'\
				'/users <i>- список всех пользователей</i>\n'\
				'/admins <i>- список всех админов</i>\n'\
				'/guests <i>- список пользователей без прав админа</i>\n\n'\
				'/code код <i>- поменять код регистрации</i>\n\n\n'\
				'<b>Общая статистика:</b>\n\n'\
				f'Кол-во зарег. пользователей: <i>{len(getAllStat())}</i>\n\n'\
				f'Кол-во монет binance: <i>{len(binance_coins)}</i>\n'\
				f'Кол-во монет bybit: <i>{len(bybit_coins)}\n\n\n</i>'\
				'<b>Все тф:</b>\n\n'\
				f'1m - <i>{time_frades_precents[0]}</i>%;\n5m - <i>{time_frades_precents[1]}</i>%;\n15m - <i>{time_frades_precents[2]}</i>%;\n30m - <i>{time_frades_precents[3]}</i>%'

				await bot.send_message(message.from_user.id, msg)
			else:
				await bot.send_message(message.from_user.id, access_denied)


	@dp.message_handler(commands=['start_logic_tf'])
	async def start_logic_tf_cmd(message: types.Message):
		if getUserStat(message.from_user.id) is not None:
			if getUserStat(message.from_user.id)[4]:
				tfs = time_frades
				minutes = time_frades_minutes
				precents = time_frades_precents

				for i in range(len(tfs)):
					os.system(f'start python logic_times.py {tfs[i]} {minutes[i]} {precents[i]}')
			else:
				await bot.send_message(message.from_user.id, access_denied)


	@dp.message_handler(commands=['restart_logic_tf'])
	async def restart_logic_tf_cmd(message: types.Message):
		if getUserStat(message.from_user.id) is not None:
			if getUserStat(message.from_user.id)[4]:
				time_frades_pids = getTfPidsStat()

				for i in time_frades_pids:
					os.system(f'start Taskkill /PID {i} /F')
				for i in time_frades:
					updateTfPid(i, 0)

				tfs = time_frades
				minutes = time_frades_minutes
				precents = time_frades_precents

				for i in range(len(tfs)):
					os.system(f'start python logic_times.py {tfs[i]} {minutes[i]} {precents[i]}')
			else:
				await bot.send_message(message.from_user.id, access_denied)


	@dp.message_handler(commands=['stop_logic_tf'])
	async def stop_logic_tf_cmd(message: types.Message):
		if getUserStat(message.from_user.id) is not None:
			if getUserStat(message.from_user.id)[4]:
				time_frades_pids = getTfPidsStat()

				for i in time_frades_pids:
					os.system(f'start Taskkill /PID {i} /F')
				for i in time_frades:
					updateTfPid(i, 0)
			else:
				await bot.send_message(message.from_user.id, access_denied)


	@dp.message_handler(commands=['start_logic'])
	async def start_logic_cmd(message: types.Message):
		if getUserStat(message.from_user.id) is not None:
			if getUserStat(message.from_user.id)[4]:
				for j in getAllStat():
					if j[3]:
						os.system(f'start python logic.py {j[0]}')
			else:
				await bot.send_message(message.from_user.id, access_denied)


	@dp.message_handler(commands=['set_admin'])
	async def set_admin_cmd(message: types.Message):
		if getUserStat(message.from_user.id) is not None:
			if getUserStat(message.from_user.id)[4]:
				uid = message.text[11:]
				setAdmin(uid, 1)

				await bot.send_message(message.from_user.id, f'<b>Пользователь теперь админ!</b>')
				await bot.send_message(logs_chat_id, f'<b>Админ {message.from_user.username} выдал права админа (id: {uid})</b>\n\n<i>Id: {message.from_user.id}</i>')
			else:
				await bot.send_message(message.from_user.id, access_denied)


	@dp.message_handler(commands=['del_admin'])
	async def del_admin_cmd(message: types.Message):
		if getUserStat(message.from_user.id) is not None:
			if getUserStat(message.from_user.id)[4]:
				uid = message.text[11:]
				if str(uid) != str(owner):
					setAdmin(uid, 0)

					await bot.send_message(message.from_user.id, f'<b>Пользователь больше не админ!</b>')
					await bot.send_message(logs_chat_id, f'<b>Админ {message.from_user.username} снял права админа (id: {uid})</b>\n\n<i>Id: {message.from_user.id}</i>')
				else:
					await bot.send_message(message.from_user.id, access_denied)
			else:
				await bot.send_message(message.from_user.id, access_denied)


	@dp.message_handler(commands=['del_user'])
	async def del_user_cmd(message: types.Message):
		if getUserStat(message.from_user.id) is not None:
			if getUserStat(message.from_user.id)[4]:
				uid = message.text[10:]
				if str(uid) != str(owner):
					delUser(uid)

					await bot.send_message(message.from_user.id, f'<b>Пользователь удален!</b>')
					await bot.send_message(logs_chat_id, f'<b>Админ {message.from_user.username} удалил пользователя (id: {uid})</b>\n\n<i>Id: {message.from_user.id}</i>')
				else:
					await bot.send_message(message.from_user.id, access_denied)
			else:
				await bot.send_message(message.from_user.id, access_denied)


	@dp.message_handler(commands=['code'])
	async def code_cmd(message: types.Message):
		if getUserStat(message.from_user.id) is not None:
			if getUserStat(message.from_user.id)[4]:
				old_code = getCode()
				new_code = message.text[6:]

				if len(new_code) >= 4:
					changeCode(new_code)

					await bot.send_message(message.from_user.id, f'<b>Код успешно изменен!</b>\n\n<b>Старый код:</b> {old_code}\n<b>Новый код:</b> <code>{new_code}</code>')
					await bot.send_message(logs_chat_id, f'<b>Админ {message.from_user.username} поменял код -> <code>{new_code}</code></b>\n\n<i>Id: {message.from_user.id}</i>')
			else:
				await bot.send_message(message.from_user.id, access_denied)


	@dp.message_handler(commands=['accounts', 'users', 'аккаунты'])
	async def accounts_cmd(message: types.Message):
		if getUserStat(message.from_user.id) is not None:
			if getUserStat(message.from_user.id)[4]:
				tmp = getAllStat()
				users = f'<b>Всего {len(tmp)} пользователей</b>\n\n'
				for i in tmp:
					users += f'<b>Ник:</b> {i[1]}\n<b>Id:</b> {i[0]}\n<b>Админ:</b> {itsAdmin(i[4])}\n<b>Дата регистрации:</b> {i[2]}\n\n'

				await bot.send_message(message.from_user.id, users)
			else:
				await bot.send_message(message.from_user.id, access_denied)
		else:
			await bot.send_message(message.from_user.id, access_denied)


	@dp.message_handler(commands=['admins', 'админы'])
	async def admins_cmd(message: types.Message):
		if getUserStat(message.from_user.id) is not None:
			if getUserStat(message.from_user.id)[4]:
				tmp = getAllAdmins()
				users = f'<b>Всего {len(tmp)} админов</b>\n\n'
				for i in tmp:
					users += f'<b>Ник:</b> {i[1]}\n<b>Id:</b> {i[0]}\n<b>Дата регистрации:</b> {i[2]}\n\n'

				await bot.send_message(message.from_user.id, users)
			else:
				await bot.send_message(message.from_user.id, access_denied)
		else:
			await bot.send_message(message.from_user.id, access_denied)


	@dp.message_handler(commands=['guests', 'гости'])
	async def guests_cmd(message: types.Message):
		if getUserStat(message.from_user.id) is not None:
			if getUserStat(message.from_user.id)[4]:
				tmp = getAllGuests()
				users = f'<b>Всего {len(tmp)} обычных пользователей</b>\n\n'
				for i in tmp:
					users += f'<b>Ник:</b> {i[1]}\n<b>Id:</b> {i[0]}\n<b>Дата регистрации:</b> {i[2]}\n\n'

				await bot.send_message(message.from_user.id, users)
			else:
				await bot.send_message(message.from_user.id, access_denied)
		else:
			await bot.send_message(message.from_user.id, access_denied)


	@dp.message_handler(commands=['logs', 'log'])
	async def logs_cmd(message: types.Message):
		if getUserStat(message.from_user.id) is not None:
			if getUserStat(message.from_user.id)[4]:
				await bot.send_message(message.from_user.id, 'https://t.me/+5ufoKN7CYpExMzky')
				await bot.send_message(logs_chat_id, f'<b>Пользователь {message.from_user.username} получил ссылку на логи</b>\n\n<i>Id: {message.from_user.id}</i>')
			else:
				await bot.send_message(message.from_user.id, access_denied)
		else:
			await bot.send_message(message.from_user.id, access_denied)




	#
	# Commands for users
	#


	@dp.message_handler(commands=['time'])
	async def hour_cmd(message: types.Message):
		if getUserStat(message.from_user.id) is not None:
			if int(getUserStat(message.from_user.id)[3]) != 1:
				if (not(message.text[6:].isalpha())) and (message.text[6:] != ''):
					if float(message.text[6:]) > 0.01 and float(message.text[6:]) < 96:
						old_code = getHours(message.from_user.id)
						new_code = message.text[6:]
						updateUinterval(message.from_user.id, new_code)

						await bot.send_message(message.from_user.id, f'<b>Интервал успешно изменен!</b>\n\n<b>Старый интервал:</b> {old_code}\n<b>Новый интервал:</b> {new_code}')
						await bot.send_message(logs_chat_id, f'<b>Пользователь {message.from_user.username} поменял интервал</b>\n\n<i>Id: {message.from_user.id}</i>')
					else:
						await bot.send_message(message.from_user.id, '<b>Недопустимое значение!</b>')
				else:
					await bot.send_message(message.from_user.id, '<b>Недопустимое значение!</b>')
			else:
				await bot.send_message(message.from_user.id, '<b>Для начала выключите алгоритм!</b>')
		else:
			await bot.send_message(message.from_user.id, access_denied)


	@dp.message_handler(commands=['percent'])
	async def procent_cmd(message: types.Message):
		if getUserStat(message.from_user.id) is not None:
			if int(getUserStat(message.from_user.id)[3]) != 1:
				if (not(message.text[9:].isalpha())) and (message.text[9:] != ''):
					if float(message.text[9:]) > 0.01 and float(message.text[9:]) < 100:
						old_code = getProcent(message.from_user.id)
						new_code = message.text[9:]
						updateUprocent(message.from_user.id, new_code)

						await bot.send_message(message.from_user.id, f'<b>Процент успешно изменен!</b>\n\n<b>Старый процент:</b> {old_code}\n<b>Новый процент:</b> {new_code}')
						await bot.send_message(logs_chat_id, f'<b>Пользователь {message.from_user.username} поменял процент</b>\n\n<i>Id: {message.from_user.id}</i>')
					else:
						await bot.send_message(message.from_user.id, '<b>Недопустимое значение!</b>')
				else:
					await bot.send_message(message.from_user.id, '<b>Недопустимое значение!</b>')
			else:
				await bot.send_message(message.from_user.id, '<b>Для начала выключите алгоритм!</b>')
		else:
			await bot.send_message(message.from_user.id, access_denied)


	@dp.message_handler(commands=['keyboard', 'клавиатура', 'клава'])
	async def keyboard_cmd(message: types.Message):
		if getUserStat(message.from_user.id) is not None:
			try:
				await dp.throttle(message.text, rate=time_for_spam_ban)
			except Throttled:
				await message.reply(f'<b>Подождите {time_for_spam_ban} секунд. Нельзя часто использовать эту команду.</b>')
				await bot.send_message(logs_chat_id, f'<b>Пользователь {message.from_user.username} спамит!\n\n{message.text}</b>\n\n<i>Id: {message.from_user.id}</i>')
			else:
				await bot.send_message(message.from_user.id, '<b>Клавиатура обновлена!</b>', reply_markup=getKeyboard())


	@dp.message_handler(commands=['logic_on'])
	async def logic_on_cmd(message: types.Message):
		if getUserStat(message.from_user.id) is not None:
			if int(getUserStat(message.from_user.id)[3]) != 1:
				updateUser(message.from_user.id, 1)

				os.system(f'start python logic.py {message.from_user.id}')

				await bot.send_message(message.from_user.id, '<b>Алгоритм запущен!</b>')
				await bot.send_message(logs_chat_id, f'<b>Пользователь {message.from_user.username} запустил алгоритм</b>\n\n<i>Id: {message.from_user.id}</i>')
			else:
				await bot.send_message(message.from_user.id, '<b>Алгоритм уже запущен!</b>')
		else:
			await bot.send_message(message.from_user.id, access_denied)


	@dp.message_handler(commands=['logic_off'])
	async def logic_off_cmd(message: types.Message):
		if getUserStat(message.from_user.id) is not None:
			if int(getUserStat(message.from_user.id)[3]) != 0:
				updateUser(message.from_user.id, 0)
				os.system(f'start Taskkill /PID {int(getUserStat(message.from_user.id)[8])} /F')
				updateUpid(message.from_user.id, 0)

				await bot.send_message(message.from_user.id, '<b>Алгоритм отключен!</b>')
				await bot.send_message(logs_chat_id, f'<b>Пользователь {message.from_user.username} отключил алгоритм</b>\n\n<i>Id: {message.from_user.id}</i>')
			else:
				await bot.send_message(message.from_user.id, '<b>Алгоритм уже выключен!</b>')
		else:
			await bot.send_message(message.from_user.id, access_denied)


	@dp.message_handler(commands=['options', 'settings', 'настройки', 'опции'])
	async def options_cmd(message: types.Message):
		if getUserStat(message.from_user.id) is not None:
			try:
				await dp.throttle(message.text, rate=time_for_spam_ban)
			except Throttled:
				await message.reply(f'<b>Подождите {time_for_spam_ban} секунд. Нельзя часто использовать эту команду.</b>')
				await bot.send_message(logs_chat_id, f'<b>Пользователь {message.from_user.username} спамит!\n\n{message.text}</b>\n\n<i>Id: {message.from_user.id}</i>')
			else:
				await getOptions(message, bot)
		else:
			await bot.send_message(message.from_user.id, access_denied)


	@dp.message_handler(commands=['coins', 'coin', 'койны', 'койн'])
	async def coins_cmd(message: types.Message):
		if getUserStat(message.from_user.id) is not None:
			try:
				await dp.throttle(message.text, rate=3)
			except Throttled:
				await message.reply(f'<b>Подождите 3 секунды. Нельзя часто использовать эту команду.</b>')
				await bot.send_message(logs_chat_id, f'<b>Пользователь {message.from_user.username} спамит!\n\n{message.text}</b>\n\n<i>Id: {message.from_user.id}</i>')
			else:
				await getCoins(message, bot, 'binance')
		else:
			await bot.send_message(message.from_user.id, access_denied)

	@dp.message_handler(commands=['scam', 'скам'])
	async def scam_cmd(message: types.Message):
		if getUserStat(message.from_user.id) is not None:
			try:
				await dp.throttle(message.text, rate=3)
			except Throttled:
				await message.reply(f'<b>Подождите 3 секунды. Нельзя часто использовать эту команду.</b>')
				await bot.send_message(logs_chat_id, f'<b>Пользователь {message.from_user.username} спамит!\n\n{message.text}</b>\n\n<i>Id: {message.from_user.id}</i>')
			else:
				await bot.send_message(message.from_user.id, '<b>Введите токен для проверки:</b>')
				await createScam.check.set()
		else:
			await bot.send_message(message.from_user.id, access_denied)


	@dp.message_handler(state=createScam.check)
	async def input_check(message: types.Message, state: FSMContext):
		msg = ''
		if checkCoinScam(message.text) == 'true':
			msg = 'Предположительно не скам'
		elif checkCoinScam(message.text) == 'Ошибка соединения!':
			msg = 'Ошибка соединения с сервером'
		else:
			msg = 'Предположительно скам'

		await bot.send_message(message.from_user.id, f'<b>{msg}!</b>')
		await state.finish()


	@dp.message_handler(commands=['case'])
	async def case_cmd(message: types.Message):
		if getUserStat(message.from_user.id) is not None:
			try:
				await dp.throttle(message.text, rate=3)
			except Throttled:
				await message.reply(f'<b>Подождите 3 секунды. Нельзя часто использовать эту команду.</b>')
				await bot.send_message(logs_chat_id, f'<b>Пользователь {message.from_user.username} спамит!\n\n{message.text}</b>\n\n<i>Id: {message.from_user.id}</i>')
			else:
				arg = message.text[6:]

				if arg == 'create':
					await bot.send_message(message.from_user.id, '<b>Введите название торговой пары:</b>')
					await createCase.coin.set()
				else:
					if os.path.exists(f'allcases/{message.from_user.id}.txt'):
						data, msg = [], '<b>Ваш портфель:</b>\n\n'
						with open(f'allcases/{message.from_user.id}.txt', 'r') as f:
							tmp = f.readlines()

							for i in tmp:
								i = i.replace('\n', '')
								data.append(list(i.split(' ')))
						for i in data:
							msg += f'<b>{i[0]}</b> - ${i[1]}<i>({i[2]})</i>\n'
						await bot.send_message(message.from_user.id, msg)
					else:
						await bot.send_message(message.from_user.id, '<b>Портфель еще не создан!</b>\n\n<b>Введите:</b> <code>/case create</code>\n<i>Нажмите, чтобы скопировать.</i>')
		else:
			await bot.send_message(message.from_user.id, access_denied)


	@dp.message_handler(state=createCase.coin)
	async def input_coin(message: types.Message, state: FSMContext):
		if len(message.text) < 3:
			await message.answer('<b>Название должно быть длиннее!</b>')
			return

		async with state.proxy() as data:
			data['coin'] = message.text

		await createCase.next()
		await bot.send_message(message.from_user.id, '<b>Введите цену:</b>')
		await createCase.price.set()


	@dp.message_handler(state=createCase.price)
	async def input_volume(message: types.Message, state: FSMContext):
		async with state.proxy() as data:
			data['price'] = message.text
		await createCase.next()
		await bot.send_message(message.from_user.id, '<b>Введите кол-во:</b>')
		await createCase.volume.set()


	@dp.message_handler(state=createCase.volume)
	async def input_price(message: types.Message, state: FSMContext):
		async with state.proxy() as data:
			with open(f'allcases/{message.from_user.id}.txt', 'w') as f:
				f.write(f'{data["coin"]} {data["price"]} {message.text}')

		await bot.send_message(message.from_user.id, '<b>Ваш портфель успешно создан!</b>')
		await state.finish()


	@dp.message_handler(commands=['about', 'test'])
	async def about_cmd(message: types.Message):
		if getUserStat(message.from_user.id) is not None:
			try:
				await dp.throttle(message.text, rate=time_for_spam_ban)
			except Throttled:
				await message.reply(f'<b>Подождите {time_for_spam_ban} секунд. Нельзя часто использовать эту команду.</b>')
				await bot.send_message(logs_chat_id, f'<b>Пользователь {message.from_user.username} спамит!\n\n{message.text}</b>\n\n<i>Id: {message.from_user.id}</i>')
			else:
				await bot.send_message(message.from_user.id, f'Версия Бота: {bot_version}')


	@dp.callback_query_handler(lambda c: c.data == 'u1m')
	async def u1m_cmd(callback_query: types.CallbackQuery):
		if not(int(getUserStat(callback_query.from_user.id)[9])):
			updateLogicTF(callback_query.from_user.id, 'u1m', 1)

			await bot.answer_callback_query(callback_query.id)
			await bot.send_message(callback_query.from_user.id, '<b>Включена рассылка интервалом 1 минута!</b>')
		else:
			updateLogicTF(callback_query.from_user.id, 'u1m', 0)

			await bot.answer_callback_query(callback_query.id)
			await bot.send_message(callback_query.from_user.id, '<b>Рассылка интервалом 1 минута отключена!</b>')


	@dp.callback_query_handler(lambda c: c.data == 'u5m')
	async def u5m_cmd(callback_query: types.CallbackQuery):
		if not(int(getUserStat(callback_query.from_user.id)[10])):
			updateLogicTF(callback_query.from_user.id, 'u5m', 1)

			await bot.answer_callback_query(callback_query.id)
			await bot.send_message(callback_query.from_user.id, '<b>Включена рассылка интервалом 5 минут!</b>')
		else:
			updateLogicTF(callback_query.from_user.id, 'u5m', 0)

			await bot.answer_callback_query(callback_query.id)
			await bot.send_message(callback_query.from_user.id, '<b>Рассылка интервалом 5 минут отключена!</b>')


	@dp.callback_query_handler(lambda c: c.data == 'u15m')
	async def u15m_cmd(callback_query: types.CallbackQuery):
		if not(int(getUserStat(callback_query.from_user.id)[11])):
			updateLogicTF(callback_query.from_user.id, 'u15m', 1)

			await bot.answer_callback_query(callback_query.id)
			await bot.send_message(callback_query.from_user.id, '<b>Включена рассылка интервалом 15 минут!</b>')
		else:
			updateLogicTF(callback_query.from_user.id, 'u15m', 0)

			await bot.answer_callback_query(callback_query.id)
			await bot.send_message(callback_query.from_user.id, '<b>Рассылка интервалом 15 минут отключена!</b>')


	@dp.callback_query_handler(lambda c: c.data == 'u30m')
	async def u30m_cmd(callback_query: types.CallbackQuery):
		if not(int(getUserStat(callback_query.from_user.id)[12])):
			updateLogicTF(callback_query.from_user.id, 'u30m', 1)

			await bot.answer_callback_query(callback_query.id)
			await bot.send_message(callback_query.from_user.id, '<b>Включена рассылка интервалом 30 минут!</b>')
		else:
			updateLogicTF(callback_query.from_user.id, 'u30m', 0)

			await bot.answer_callback_query(callback_query.id)
			await bot.send_message(callback_query.from_user.id, '<b>Рассылка интервалом 30 минут отключена!</b>')


	@dp.callback_query_handler(lambda c: c.data == 'uallm')
	async def uallm_cmd(callback_query: types.CallbackQuery):
		updateLogicTF(callback_query.from_user.id, 'u1m', 1)
		updateLogicTF(callback_query.from_user.id, 'u5m', 1)
		updateLogicTF(callback_query.from_user.id, 'u15m', 1)
		updateLogicTF(callback_query.from_user.id, 'u30m', 1)

		await bot.answer_callback_query(callback_query.id)
		await bot.send_message(callback_query.from_user.id, '<b>Включена рассылка интервалом 1, 5, 15, 30 минут!</b>')


	@dp.callback_query_handler(lambda c: c.data == 'uoffsm')
	async def uoffsm_cmd(callback_query: types.CallbackQuery):
		updateLogicTF(callback_query.from_user.id, 'u1m', 0)
		updateLogicTF(callback_query.from_user.id, 'u5m', 0)
		updateLogicTF(callback_query.from_user.id, 'u15m', 0)
		updateLogicTF(callback_query.from_user.id, 'u30m', 0)

		await bot.answer_callback_query(callback_query.id)
		await bot.send_message(callback_query.from_user.id, '<b>Все рассылки отключены!</b>')


	@dp.callback_query_handler(lambda c: c.data == 'logic_on')
	async def logic_om_cmd_data(callback_query: types.CallbackQuery):
		if int(getUserStat(callback_query.from_user.id)[3]) != 1:
			updateUser(callback_query.from_user.id, 1)

			os.system(f'start python logic.py {callback_query.from_user.id}')

			await bot.send_message(callback_query.from_user.id, '<b>Алгоритм запущен!</b>')
			await bot.send_message(logs_chat_id, f'<b>Пользователь {callback_query.from_user.username} запустил алгоритм</b>\n\n<i>Id: {callback_query.from_user.id}</i>')
		else:
			await bot.send_message(callback_query.from_user.id, '<b>Алгоритм уже запущен!</b>')


	@dp.callback_query_handler(lambda c: c.data == 'logic_off')
	async def logic_off_cmd_data(callback_query: types.CallbackQuery):
		if int(getUserStat(callback_query.from_user.id)[3]) != 0:
			updateUser(callback_query.from_user.id, 0)

			await bot.send_message(callback_query.from_user.id, '<b>Алгоритм отключен!</b>')
			await bot.send_message(logs_chat_id, f'<b>Пользователь {callback_query.from_user.username} отключил алгоритм</b>\n\n<i>Id: {callback_query.from_user.id}</i>')
		else:
			await bot.send_message(callback_query.from_user.id, '<b>Алгоритм уже выключен!</b>')


	@dp.callback_query_handler(lambda c: c.data == 'upersm')
	async def upersm_cmd(callback_query: types.CallbackQuery):
		msg = '<b>Как создать свой алгоритм? Инструкция:</b>\n\n<b>Настройки:</b>\n<code>/time</code> <i>час</i>  <b>- интервал проверки</b>\n<code>/percent</code> <i>процент</i>  <b>- порог проверки</b>\n\n<b>Запуск:</b>\n<code>/logic_on</code>  <b>- запустить алгоритм</b>\n<code>/logic_off</code>  <b>- выключить алгоритм</b>\n\nПисать все числами, не указывать знаки процента и прочее!\nВ <code>/time</code> указывать строго время в часах\nЕсли число дробное, то писать через точку!'
		key1 = types.InlineKeyboardButton('Включить', callback_data='logic_on')
		key2 = types.InlineKeyboardButton('Выключить', callback_data='logic_off')
		keyboard = types.InlineKeyboardMarkup().add(key1, key2)

		await bot.answer_callback_query(callback_query.id)
		await bot.send_message(callback_query.from_user.id, msg, reply_markup=keyboard)


	@dp.message_handler(commands=['help', 'instruction', 'info', 'помощь', 'хелп', 'инструкция'])
	async def instruction_cmd(message: types.Message):
		if getUserStat(message.from_user.id) is not None:
			try:
				await dp.throttle(message.text, rate=time_for_spam_ban)
			except Throttled:
				await message.reply(f'<b>Подождите {time_for_spam_ban} секунд. Нельзя часто использовать эту команду.</b>')
				await bot.send_message(logs_chat_id, f'<b>Пользователь {message.from_user.username} спамит!\n\n{message.text}</b>\n\n<i>Id: {message.from_user.id}</i>')
			else:
				if getUserStat(message.from_user.id)[4]:
					key = types.InlineKeyboardButton('1 минута', callback_data='u1m')
					key2 = types.InlineKeyboardButton('5 минут', callback_data='u5m')
					key3 = types.InlineKeyboardButton('15 минут', callback_data='u15m')
					key4 = types.InlineKeyboardButton('30 минут', callback_data='u30m')
					key5 = types.InlineKeyboardButton('Включить все', callback_data='uallm')
					key6 = types.InlineKeyboardButton('Создать', callback_data='upersm')
					key7 = types.InlineKeyboardButton('Отключить все', callback_data='uoffsm')
					keyboard = types.InlineKeyboardMarkup().add(key, key2, key3, key4, key5, key6, key7)

					msg = '<b>Вы можете включить/выключить рассылку уведомлений по отклонениям\nВыберите готовый интервал, либо создайте свой:</b>\n\n<i>Полная инструкция -></i> @instruction_crypto_bot'
					await bot.send_message(message.from_user.id, msg, reply_markup=keyboard)
				else:
					key = types.InlineKeyboardButton('1 минута', callback_data='u1m')
					key2 = types.InlineKeyboardButton('5 минут', callback_data='u5m')
					key3 = types.InlineKeyboardButton('15 минут', callback_data='u15m')
					key4 = types.InlineKeyboardButton('30 минут', callback_data='u30m')
					key5 = types.InlineKeyboardButton('Включить все', callback_data='uallm')
					key6 = types.InlineKeyboardButton('Создать', callback_data='upersm')
					key7 = types.InlineKeyboardButton('Отключить все', callback_data='uoffsm')
					keyboard = types.InlineKeyboardMarkup().add(key, key2, key3, key4, key5, key6, key7)

					msg = '<b>Вы можете включить/выключить рассылку уведомлений по отклонениям\nВыберите готовый интервал, либо создайте свой:</b>\n\n<i>Полная инструкция -></i> @crypto_bot_help'
					await bot.send_message(message.from_user.id, msg, reply_markup=keyboard)
		else:
			await bot.send_message(message.from_user.id, '@crypto_bot_help')


	@dp.message_handler(commands=['start'])
	async def start_cmd(message: types.Message):
		if not(getUserStat(message.from_user.id) is not None):
			await bot.send_message(message.from_user.id, text= f'<b>Привет, {message.from_user.username}!</b>\
				\nЧтобы продолжить необходимо зарегистрироваться!\n\nВведите код регистрации:')
		else:
			await bot.send_message(message.from_user.id, access_denied)


	@dp.message_handler(commands=['registration', 'reg', 'регистрация', 'register', 'рег'])
	async def register_cmd(message: types.Message):
		if not(getUserStat(message.from_user.id) is not None):
			await bot.send_message(message.from_user.id, '<b>Введите код:</b>')
		else:
			await bot.send_message(message.from_user.id, access_denied)


	@dp.message_handler(commands=[getCode()])
	async def reg_code_cmd(message: types.Message):
		if not(getUserStat(message.from_user.id) is not None):
			abc, code = 'abcdewjsfkfep41657fapsdadwdbakjsf1865218sd', ''

			regUser(message.from_user.id, message.from_user.username)

			for i in range(7):
				code += abc[random.randint(0, len(abc)-1)]
			changeCode(code)

			await bot.send_message(message.from_user.id, '<b>Регистрация прошла успешно!</b>\nИспользуй клавиатуру, чтобы было удобнее!', reply_markup=getKeyboard())
			await bot.send_message(logs_chat_id, f'<b>Пользователь {message.from_user.username} зарегистрировался!</b>\n\n<i>Id: {message.from_user.id}</i>')
		else:
			await bot.send_message(message.from_user.id, access_denied)


	@dp.message_handler()
	async def echo(message: types.Message):
		if getUserStat(message.from_user.id) is not None:
			msg = message.text.lower()

			if msg == 'on✅':
				try:
					await dp.throttle(message.text, rate=time_for_spam_ban)
				except Throttled:
					await message.reply(f'<b>Подождите {time_for_spam_ban} секунд. Нельзя часто использовать эту команду.</b>')
					await bot.send_message(logs_chat_id, f'<b>Пользователь {message.from_user.username} спамит!\n\n{message.text}</b>\n\n<i>Id: {message.from_user.id}</i>')
				else:
					if int(getUserStat(message.from_user.id)[3]) != 1:
						updateUser(message.from_user.id, 1)

						os.system(f'start python logic.py {message.from_user.id}')

						await bot.send_message(message.from_user.id, '<b>Алгоритм запущен!</b>')
						await bot.send_message(logs_chat_id, f'<b>Пользователь {message.from_user.username} запустил алгоритм</b>\n\n<i>Id: {message.from_user.id}</i>')
					else:
						await bot.send_message(message.from_user.id, '<b>Алгоритм уже запущен!</b>')

			if msg == 'off❌':
				try:
					await dp.throttle(message.text, rate=time_for_spam_ban)
				except Throttled:
					await message.reply(f'<b>Подождите {time_for_spam_ban} секунд. Нельзя часто использовать эту команду.</b>')
					await bot.send_message(logs_chat_id, f'<b>Пользователь {message.from_user.username} спамит!\n\n{message.text}</b>\n\n<i>Id: {message.from_user.id}</i>')
				else:
					if int(getUserStat(message.from_user.id)[3]) != 0:
						updateUser(message.from_user.id, 0)
						os.system(f'start Taskkill /PID {int(getUserStat(message.from_user.id)[8])} /F')
						updateUpid(message.from_user.id, 0)

						await bot.send_message(message.from_user.id, '<b>Алгоритм отключен!</b>')
						await bot.send_message(logs_chat_id, f'<b>Пользователь {message.from_user.username} отключил алгоритм</b>\n\n<i>Id: {message.from_user.id}</i>')
					else:
						await bot.send_message(message.from_user.id, '<b>Алгоритм уже выключен!</b>')

			if msg == 'койны' or msg == 'койн' or msg == 'coins' or msg == 'coin' or msg == 'coins💰' or msg == 'binance':
				try:
					await dp.throttle(message.text, rate=time_for_spam_ban)
				except Throttled:
					await message.reply(f'<b>Подождите {time_for_spam_ban} секунд. Нельзя часто использовать эту команду.</b>')
					await bot.send_message(logs_chat_id, f'<b>Пользователь {message.from_user.username} спамит!\n\n{message.text}</b>\n\n<i>Id: {message.from_user.id}</i>')
				else:
					await getCoins(message, bot, 'binance')

			if msg == 'bybit':
				try:
					await dp.throttle(message.text, rate=time_for_spam_ban)
				except Throttled:
					await message.reply(f'<b>Подождите {time_for_spam_ban} секунд. Нельзя часто использовать эту команду.</b>')
					await bot.send_message(logs_chat_id, f'<b>Пользователь {message.from_user.username} спамит!\n\n{message.text}</b>\n\n<i>Id: {message.from_user.id}</i>')
				else:
					await getCoins(message, bot, 'bybit')

			if msg == 'настройки' or msg == 'options' or msg == 'settings' or msg == 'опции' or msg == 'options⚙️':
				try:
					await dp.throttle(message.text, rate=time_for_spam_ban)
				except Throttled:
					await message.reply(f'<b>Подождите {time_for_spam_ban} секунд. Нельзя часто использовать эту команду.</b>')
					await bot.send_message(logs_chat_id, f'<b>Пользователь {message.from_user.username} спамит!\n\n{message.text}</b>\n\n<i>Id: {message.from_user.id}</i>')
				else:
					await getOptions(message, bot)
		else:
			await bot.send_message(message.from_user.id, access_denied)



	executor.start_polling(dp, skip_updates=True)




while True:
	try:
		print(f'Bot has been started! {str(datetime.datetime.now())[:-10]}\n\n')
		bot_start()
	except:
		print(f'Bot has been restarted! {str(datetime.datetime.now())[:-10]}\n\n')
		bot_start()
