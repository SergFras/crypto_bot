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




async def getScam(message, bot, dp):
	try:
		await dp.throttle(message.text, rate=3)
	except Throttled:
		msg = f'<b>Подождите 3 секунды. Нельзя часто использовать эту команду.</b>'
		if getUserStat(message.from_user.id)[5] == 'en':
			msg = "<b>Wait 3 seconds. You can't use this command often.</b>"

		await message.reply(msg)
		await bot.send_message(logs_chat_id, f'<b>Пользователь {message.from_user.username} спамит!\n\n{message.text}</b>\n\n<i>Id: {message.from_user.id}</i>')
	else:
		msg = '<b>Введите токен для проверки:</b>'
		if getUserStat(message.from_user.id)[5] == 'en':
			msg = f"<b>Enter the token to verify:</b>"

		await bot.send_message(message.from_user.id, msg)
		await createScam.check.set()


async def getCase(message, bot, dp):
	try:
		await dp.throttle(message.text, rate=3)
	except Throttled:
		msg = f'<b>Подождите 3 секунды. Нельзя часто использовать эту команду.</b>'
		if getUserStat(message.from_user.id)[5] == 'en':
			msg = "<b>Wait 3 seconds. You can't use this command often.</b>"

		await message.reply(msg)
		await bot.send_message(logs_chat_id, f'<b>Пользователь {message.from_user.username} спамит!\n\n{message.text}</b>\n\n<i>Id: {message.from_user.id}</i>')
	else:
		arg = message.text[6:]

		if not(os.path.exists(f'allcases/{message.from_user.id}/')):
			os.mkdir(f'allcases/{message.from_user.id}/')

		if arg == 'create':
			msg = '<b>Введите id портфеля:</b>'
			if getUserStat(message.from_user.id)[5] == 'en':
				msg = "<b>Enter the portfolio id:</b>"

			await bot.send_message(message.from_user.id, msg)
			await createCase.name.set()
		elif arg == 'update':
			msg = '<b>Введите id портфеля:</b>'
			if getUserStat(message.from_user.id)[5] == 'en':
				msg = "<b>Enter the portfolio id:</b>"

			await bot.send_message(message.from_user.id, msg)
			await updateCase.name.set()
		elif arg == 'clear' or arg == 'delete' or arg == 'remove':
			msg = '<b>Введите id портфеля:</b>'
			if getUserStat(message.from_user.id)[5] == 'en':
				msg = "<b>Enter the portfolio id:</b>"

			await bot.send_message(message.from_user.id, msg)
			await deleteCase.name.set()
		elif arg == 'help':
			msg = '<b>Инструкция:</b>\n\n<code>/case create</code> - создать новый портфель\n<code>/case update</code> - добавить новые монеты\n<code>/case delete</code> - удалить портфель\n\n<i>Нажмите, чтобы скопировать.</i>'
			if getUserStat(message.from_user.id)[5] == 'en':
				msg = '<b>Instruction:</b>\n\n<code>/case create</code> - create a new portfolio\n<code>/case update</code> - add new coins\n<code>/case delete</code> - delete portfolio\n\n<i>Click to copy.</i>'

			await bot.send_message(message.from_user.id, msg)
		else:
			filenames = next(os.walk(f'allcases/{message.from_user.id}/'), (None, None, []))[2]

			if len(filenames):
				if len(filenames) <= 5:
					data, msg = [], '<b>📕Ваш портфель:</b>\n\n'

					if getUserStat(message.from_user.id)[5] == 'en':
						msg = '<b>📕Status of your portfolio:</b>\n\n'

					for path in filenames:
						with open(f'allcases/{message.from_user.id}/{path}') as f:
							tmp = [path[:-4], f.readlines()]
							data.append(tmp)

					for info in data:
						values = []
						msg += f'<b>{info[0]}. {info[1][0]}</b>\n'

						for i in info[1]:
							i = i.replace('\n', '')
							values.append(list(i.split(' ')))
						for i in values:
							price = checkPrice(i[0])

							if price != 'Error':
								msg += f'<i>{i[0]}</i>\n<b>📊Price:</b> ${price}\n<b>📉24h:</b> {None}%\n<b>💳Hold:</b> {i[2]} (${round(float(i[2]) * price, 3)})\n<b>⚖️AvgBuy:</b> ${i[1]}\n<b>📈P&L:</b> ${round(price - float(i[1]), 3)} ({None}%)\n\n'

					msg += '\n<code>/case help</code>'

					await bot.send_message(message.from_user.id, msg)
				else:
					msg = '<b>Превышен лимит на количество портфелей!</b>'
					if getUserStat(message.from_user.id)[5] == 'en':
						msg = '<b>Portfolio limit exceeded!</b>'

					await bot.send_message(message.from_user.id, msg)
			else:
				msg = '<b>Портфель еще не создан!</b>\n\n<b>Введите:</b> <code>/case create</code>\n\n<i>Нажмите, чтобы скопировать.</i>'
				if getUserStat(message.from_user.id)[5] == 'en':
					msg = '<b>The portfolio has not been created yet!</b>\n\n<b>Enter:</b> <code>/case create</code>\n\n<i>Click to copy.</i>'

				updateUportid(message.from_user.id, 0)
				await bot.send_message(message.from_user.id, msg)


def bot_start():
	logging.basicConfig(level=logging.INFO)
	storage = MemoryStorage()
	bot = Bot(token=telegram_token, parse_mode=types.ParseMode.HTML, disable_web_page_preview=True)
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
				'/code код <i>- поменять код регистрации</i>\n'\
				'/logs <i>- ссылка на логи</i>\n\n\n'\
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
				await bot.send_message(message.from_user.id, '<b>Алгоритмы запущены!</b>')
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
				await bot.send_message(message.from_user.id, '<b>Алгоритмы запущены!</b>')
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
			try:
				await dp.throttle(message.text, rate=time_for_spam_ban)
			except Throttled:
				msg = f'<b>Подождите {time_for_spam_ban} секунды. Нельзя часто использовать эту команду.</b>'
				if getUserStat(message.from_user.id)[5] == 'en':
					msg = f"<b>Wait {time_for_spam_ban} seconds. You can't use this command often.</b>"

				await message.reply(msg)
				await bot.send_message(logs_chat_id, f'<b>Пользователь {message.from_user.username} спамит!\n\n{message.text}</b>\n\n<i>Id: {message.from_user.id}</i>')
			else:
				if int(getUserStat(message.from_user.id)[3]) != 1:
					if (not(message.text[6:].isalpha())) and (message.text[6:] != ''):
						if float(message.text[6:]) > 0.01 and float(message.text[6:]) < 96:
							old_code = getHours(message.from_user.id)
							new_code = message.text[6:]
							updateUinterval(message.from_user.id, new_code)

							msg = f'<b>Интервал успешно изменен!</b>\n\n<b>Старый интервал:</b> {old_code}\n<b>Новый интервал:</b> {new_code}'
							if getUserStat(message.from_user.id)[5] == 'en':
								msg = f'<b>The interval has been successfully changed!</b>\n\n<b>Old interval:</b> {old_code}\n<b>New interval:</b> {new_code}'

							await bot.send_message(message.from_user.id, msg)
						else:
							msg = '<b>Недопустимое значение!</b>'
							if getUserStat(message.from_user.id)[5] == 'en':
								msg = '<b>Invalid value!</b>'

							await bot.send_message(message.from_user.id, msg)
					else:
						msg = '<b>Недопустимое значение!</b>'
						if getUserStat(message.from_user.id)[5] == 'en':
							msg = '<b>Invalid value!</b>'

						await bot.send_message(message.from_user.id, msg)
				else:
					msg = '<b>Для начала выключите алгоритм!</b>'
					if getUserStat(message.from_user.id)[5] == 'en':
						msg = '<b>First, turn off the algorithm!</b>'

					await bot.send_message(message.from_user.id, msg)
		else:
			await bot.send_message(message.from_user.id, access_denied)


	@dp.message_handler(commands=['percent'])
	async def procent_cmd(message: types.Message):
		if getUserStat(message.from_user.id) is not None:
			try:
				await dp.throttle(message.text, rate=time_for_spam_ban)
			except Throttled:
				msg = f'<b>Подождите {time_for_spam_ban} секунды. Нельзя часто использовать эту команду.</b>'
				if getUserStat(message.from_user.id)[5] == 'en':
					msg = f"<b>Wait {time_for_spam_ban} seconds. You can't use this command often.</b>"

				await message.reply(msg)
				await bot.send_message(logs_chat_id, f'<b>Пользователь {message.from_user.username} спамит!\n\n{message.text}</b>\n\n<i>Id: {message.from_user.id}</i>')
			else:
				if int(getUserStat(message.from_user.id)[3]) != 1:
					if (not(message.text[9:].isalpha())) and (message.text[9:] != ''):
						if float(message.text[9:]) > 0.01 and float(message.text[9:]) < 100:
							old_code = getProcent(message.from_user.id)
							new_code = message.text[9:]
							updateUprocent(message.from_user.id, new_code)

							msg = f'<b>Процент успешно изменен!</b>\n\n<b>Старый процент:</b> {old_code}\n<b>Новый процент:</b> {new_code}'
							if getUserStat(message.from_user.id)[5] == 'en':
								msg = f'<b>The percent has been successfully changed!</b>\n\n<b>Old percent:</b> {old_code}\n<b>New percent:</b> {new_code}'

							await bot.send_message(message.from_user.id, msg)
						else:
							msg = '<b>Недопустимое значение!</b>'
							if getUserStat(message.from_user.id)[5] == 'en':
								msg = '<b>Invalid value!</b>'

							await bot.send_message(message.from_user.id, msg)
					else:
						msg = '<b>Недопустимое значение!</b>'
						if getUserStat(message.from_user.id)[5] == 'en':
							msg = '<b>Invalid value!</b>'

						await bot.send_message(message.from_user.id, msg)
				else:
					msg = '<b>Для начала выключите алгоритм!</b>'
					if getUserStat(message.from_user.id)[5] == 'en':
						msg = '<b>First, turn off the algorithm!</b>'

					await bot.send_message(message.from_user.id, msg)
		else:
			await bot.send_message(message.from_user.id, access_denied)


	@dp.message_handler(commands=['keyboard', 'клавиатура', 'клава'])
	async def keyboard_cmd(message: types.Message):
		if getUserStat(message.from_user.id) is not None:
			try:
				await dp.throttle(message.text, rate=time_for_spam_ban)
			except Throttled:
				msg = f'<b>Подождите {time_for_spam_ban} секунды. Нельзя часто использовать эту команду.</b>'
				if getUserStat(message.from_user.id)[5] == 'en':
					msg = f"<b>Wait {time_for_spam_ban} seconds. You can't use this command often.</b>"

				await message.reply(msg)
				await bot.send_message(logs_chat_id, f'<b>Пользователь {message.from_user.username} спамит!\n\n{message.text}</b>\n\n<i>Id: {message.from_user.id}</i>')
			else:
				msg = '<b>Клавиатура обновлена!</b>'
				if getUserStat(message.from_user.id)[5] == 'en':
					msg = '<b>The keyboard has been updated!</b>'

				await bot.send_message(message.from_user.id, msg, reply_markup=getKeyboard(message, 'tools'))


	@dp.message_handler(commands=['profile', 'профиль', 'me'])
	async def profile_cmd(message: types.Message):
		if getUserStat(message.from_user.id) is not None:
			await getProfile(message, bot)
		else:
			await bot.send_message(message.from_user.id, access_denied)


	@dp.message_handler(commands=['logic_on'])
	async def logic_on_cmd(message: types.Message):
		if getUserStat(message.from_user.id) is not None:
			if int(getUserStat(message.from_user.id)[3]) != 1:
				updateUser(message.from_user.id, 1)

				os.system(f'start python logic.py {message.from_user.id}')

				msg = '<b>Алгоритм запущен!</b>'
				if getUserStat(message.from_user.id)[5] == 'en':
					msg = '<b>Algorithm has been started!</b>'

				await bot.send_message(message.from_user.id, msg)
				await bot.send_message(logs_chat_id, f'<b>Пользователь {message.from_user.username} запустил алгоритм</b>\n\n<i>Id: {message.from_user.id}</i>')
			else:
				msg = '<b>Алгоритм уже запущен!</b>'
				if getUserStat(message.from_user.id)[5] == 'en':
					msg = '<b>The algorithm is already running!</b>'

				await bot.send_message(message.from_user.id, msg)
		else:
			await bot.send_message(message.from_user.id, access_denied)


	@dp.message_handler(commands=['logic_off'])
	async def logic_off_cmd(message: types.Message):
		if getUserStat(message.from_user.id) is not None:
			if int(getUserStat(message.from_user.id)[3]) != 0:
				updateUser(message.from_user.id, 0)
				os.system(f'start Taskkill /PID {int(getUserStat(message.from_user.id)[8])} /F')
				updateUpid(message.from_user.id, 0)

				msg = '<b>Алгоритм отключен!</b>'
				if getUserStat(message.from_user.id)[5] == 'en':
					msg = '<b>Algorithm has been disabled!</b>'

				await bot.send_message(message.from_user.id, msg)
				await bot.send_message(logs_chat_id, f'<b>Пользователь {message.from_user.username} отключил алгоритм</b>\n\n<i>Id: {message.from_user.id}</i>')
			else:
				msg = '<b>Алгоритм уже выключен!</b>'
				if getUserStat(message.from_user.id)[5] == 'en':
					msg = '<b>The algorithm is already disabled!</b>'

				await bot.send_message(message.from_user.id, msg)
		else:
			await bot.send_message(message.from_user.id, access_denied)


	@dp.message_handler(commands=['options', 'settings', 'настройки', 'опции'])
	async def options_cmd(message: types.Message):
		if getUserStat(message.from_user.id) is not None:
			try:
				await dp.throttle(message.text, rate=time_for_spam_ban)
			except Throttled:
				msg = f'<b>Подождите {time_for_spam_ban} секунды. Нельзя часто использовать эту команду.</b>'
				if getUserStat(message.from_user.id)[5] == 'en':
					msg = f"<b>Wait {time_for_spam_ban} seconds. You can't use this command often.</b>"

				await message.reply(msg)
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
				msg = f'<b>Подождите 3 секунды. Нельзя часто использовать эту команду.</b>'
				if getUserStat(message.from_user.id)[5] == 'en':
					msg = f"<b>Wait 3 seconds. You can't use this command often.</b>"

				await message.reply(msg)
				await bot.send_message(logs_chat_id, f'<b>Пользователь {message.from_user.username} спамит!\n\n{message.text}</b>\n\n<i>Id: {message.from_user.id}</i>')
			else:
				await getCoins(message, bot, 'binance')
		else:
			await bot.send_message(message.from_user.id, access_denied)


	@dp.message_handler(commands=['scam', 'скам', 'antiscam'])
	async def scam_cmd(message: types.Message):
		if getUserStat(message.from_user.id) is not None:
			await getScam(message, bot, dp)
		else:
			await bot.send_message(message.from_user.id, access_denied)


	@dp.message_handler(state=createScam.check)
	async def input_check(message: types.Message, state: FSMContext):
		msg = ''
		if checkCoinScam(message.text) == 'true':
			msg = 'Предположительно не скам'
			if getUserStat(message.from_user.id)[5] == 'en':
				msg = 'Presumably not a scam'
		elif checkCoinScam(message.text) == 'Ошибка соединения!':
			msg = 'Ошибка'
			if getUserStat(message.from_user.id)[5] == 'en':
				msg = 'Error'
		else:
			msg = 'Предположительно скам'
			if getUserStat(message.from_user.id)[5] == 'en':
				msg = 'Presumably a scam'

		await bot.send_message(message.from_user.id, f'<b>{msg}!</b>')
		await state.finish()


	@dp.message_handler(commands=['case'])
	async def case_cmd(message: types.Message):
		if getUserStat(message.from_user.id) is not None:
			await getCase(message, bot, dp)
		else:
			await bot.send_message(message.from_user.id, access_denied)


	@dp.message_handler(state=createCase.name)
	async def input_name(message: types.Message, state: FSMContext):
		if len(message.text) < 3:
			msg = '<b>Название должно быть длиннее!</b>'
			if getUserStat(message.from_user.id)[5] == 'en':
				msg = '<b>The name should be longer!</b>'

			await message.answer(msg)
			return

		filenames = next(os.walk(f'allcases/{message.from_user.id}/'), (None, None, []))[2]

		async with state.proxy() as data:
			data['name'] = message.text

		await createCase.next()
		msg = '<b>Введите тикер:</b>'
		if getUserStat(message.from_user.id)[5] == 'en':
			msg = '<b>Enter the ticker:</b>'

		await bot.send_message(message.from_user.id, msg)
		await createCase.coin.set()


	@dp.message_handler(state=createCase.coin)
	async def input_coin(message: types.Message, state: FSMContext):
		if len(message.text) < 3:
			msg = '<b>Название должно быть длиннее!</b>'
			if getUserStat(message.from_user.id)[5] == 'en':
				msg = '<b>The name should be longer!</b>'

			await message.answer(msg)
			return

		async with state.proxy() as data:
			data['coin'] = message.text.upper()

		await createCase.next()
		msg = '<b>Введите цену покупки:</b>'
		if getUserStat(message.from_user.id)[5] == 'en':
			msg = '<b>Enter the purchase price:</b>'

		await bot.send_message(message.from_user.id, msg)
		await createCase.price.set()


	@dp.message_handler(state=createCase.price)
	async def input_volume(message: types.Message, state: FSMContext):
		if message.text.isalpha():
			msg = '<b>Цена должна быть числом!</b>'
			if getUserStat(message.from_user.id)[5] == 'en':
				msg = '<b>The price must be a number</b>!'

			await message.answer(msg)
			return
		else:
			async with state.proxy() as data:
				data['price'] = message.text

			await createCase.next()
			msg = '<b>Введите кол-во:</b>'
			if getUserStat(message.from_user.id)[5] == 'en':
				msg = '<b>Enter the quantity:</b>'

			await bot.send_message(message.from_user.id, msg)
			await createCase.volume.set()


	@dp.message_handler(state=createCase.volume)
	async def input_price(message: types.Message, state: FSMContext):
		async with state.proxy() as data:
			if message.text.isalpha():
				msg = '<b>Объем должна быть числом!</b>'
				if getUserStat(message.from_user.id)[5] == 'en':
					msg = '<b>The volume must be a number</b>!'

				await message.answer(msg)
				return
			else:
				async with state.proxy() as data:
					data['volume'] = message.text

				with open(f'allcases/{message.from_user.id}/{getUserStat(message.from_user.id)[13]}.txt', 'w') as f:
					f.write(f'{data["name"]}\n{data["coin"]} {data["price"]} {data["volume"]}')

				msg = f'<b>Ваш портфель (id: {data["name"]}) успешно создан!</b>'
				if getUserStat(message.from_user.id)[5] == 'en':
					msg = f'<b>Your portfolio (id: {data["name"]}) has been successfully created!</b>'

				await bot.send_message(message.from_user.id, msg)
				updateUportid(message.from_user.id, int(getUserStat(message.from_user.id)[13]) + 1)
				await state.finish()


	@dp.message_handler(state=deleteCase.name)
	async def input_name_open(message: types.Message, state: FSMContext):
		async with state.proxy() as data:
			filenames = next(os.walk(f'allcases/{message.from_user.id}/'), (None, None, []))[2]

			if f'{message.text}.txt' not in filenames:
				msg = '<b>Такого id не существует!</b>'
				if getUserStat(message.from_user.id)[5] == 'en':
					msg = '<b>There is no such id!</b>'

				await message.answer(msg)
			else:
				os.remove(f'allcases/{message.from_user.id}/{message.text}.txt')

				msg = f'<b>Ваш портфель (id: {message.text}) удален!</b>'
				if getUserStat(message.from_user.id)[5] == 'en':
					msg = f'<b>Your portfolio (id: {message.text}) has been deleted!</b>'

				await bot.send_message(message.from_user.id, msg)
			await state.finish()


	@dp.message_handler(state=updateCase.name)
	async def input_coin_update(message: types.Message, state: FSMContext):
		filenames = next(os.walk(f'allcases/{message.from_user.id}/'), (None, None, []))[2]

		if f'{message.text}.txt' not in filenames:
			msg = '<b>Такого id не существует!</b>'
			if getUserStat(message.from_user.id)[5] == 'en':
				msg = '<b>There is no such id!</b>'

			await message.answer(msg)
			await state.finish()
		else:
			async with state.proxy() as data:
				data['name'] = message.text

			await updateCase.next()
			msg = '<b>Введите тикер:</b>'
			if getUserStat(message.from_user.id)[5] == 'en':
				msg = '<b>Enter the ticker:</b>'

			await bot.send_message(message.from_user.id, msg)
			await updateCase.coin.set()


	@dp.message_handler(state=updateCase.coin)
	async def input_coin_update(message: types.Message, state: FSMContext):
		if len(message.text) < 3:
			msg = '<b>Название должно быть длиннее!</b>'
			if getUserStat(message.from_user.id)[5] == 'en':
				msg = '<b>The name should be longer!</b>'

			await message.answer(msg)
			return

		async with state.proxy() as data:
			data['coin'] = message.text.upper()

		await updateCase.next()
		msg = '<b>Введите цену покупки:</b>'
		if getUserStat(message.from_user.id)[5] == 'en':
			msg = '<b>Enter the purchase price:</b>'

		await bot.send_message(message.from_user.id, msg)
		await updateCase.price.set()


	@dp.message_handler(state=updateCase.price)
	async def input_volume_update(message: types.Message, state: FSMContext):
		if message.text.isalpha():
			msg = '<b>Цена должна быть числом!</b>'
			if getUserStat(message.from_user.id)[5] == 'en':
				msg = '<b>The price must be a number</b>!'

			await message.answer(msg)
			return
		else:
			async with state.proxy() as data:
				data['price'] = message.text

			await updateCase.next()
			msg = '<b>Введите кол-во:</b>'
			if getUserStat(message.from_user.id)[5] == 'en':
				msg = '<b>Enter the quantity:</b>'

			await bot.send_message(message.from_user.id, msg)
			await updateCase.volume.set()


	@dp.message_handler(state=updateCase.volume)
	async def input_price_update(message: types.Message, state: FSMContext):
		async with state.proxy() as data:
			if message.text.isalpha():
				msg = '<b>Объем должна быть числом!</b>'
				if getUserStat(message.from_user.id)[5] == 'en':
					msg = '<b>The volume must be a number</b>!'

				await message.answer(msg)
				return
			else:
				old_data = None

				with open(f'allcases/{message.from_user.id}/{getUserStat(message.from_user.id)[13]}.txt', 'r') as f:
					old_data = f.read()

				with open(f'allcases/{message.from_user.id}/{getUserStat(message.from_user.id)[13]}.txt', 'w') as f:
					f.write(f'{old_data}\n{data["coin"]} {data["price"]} {message.text}')

				msg = f'<b>Ваш портфель (id: {data["name"]}) успешно обновлен!</b>'
				if getUserStat(message.from_user.id)[5] == 'en':
					msg = f'<b>Your portfolio (id: {data["name"]}) has been successfully updated!</b>'

				await bot.send_message(message.from_user.id, msg)
				await state.finish()


	@dp.message_handler(commands=['about', 'test'])
	async def about_cmd(message: types.Message):
		if getUserStat(message.from_user.id) is not None:
			try:
				await dp.throttle(message.text, rate=time_for_spam_ban)
			except Throttled:
				msg = f'<b>Подождите {time_for_spam_ban} секунды. Нельзя часто использовать эту команду.</b>'
				if getUserStat(message.from_user.id)[5] == 'en':
					msg = f"<b>Wait {time_for_spam_ban} seconds. You can't use this command often.</b>"

				await message.reply(msg)
				await bot.send_message(logs_chat_id, f'<b>Пользователь {message.from_user.username} спамит!\n\n{message.text}</b>\n\n<i>Id: {message.from_user.id}</i>')
			else:
				await bot.send_message(message.from_user.id, f'Версия Бота: {bot_version}')


	@dp.callback_query_handler(lambda c: c.data == 'u1m')
	async def u1m_cmd(callback_query: types.CallbackQuery):
		if not(int(getUserStat(callback_query.from_user.id)[9])):
			updateLogicTF(callback_query.from_user.id, 'u1m', 1)

			await bot.answer_callback_query(callback_query.id)
			msg = '<b>Включена рассылка интервалом 1 минута!</b>'
			if getUserStat(callback_query.from_user.id)[5] == 'en':
				msg = '<b>Mailing is enabled at 1 minute intervals!</b>'

			await bot.send_message(callback_query.from_user.id, msg)
		else:
			updateLogicTF(callback_query.from_user.id, 'u1m', 0)

			await bot.answer_callback_query(callback_query.id)
			msg = '<b>Рассылка интервалом 1 минута отключена!</b>'
			if getUserStat(callback_query.from_user.id)[5] == 'en':
				msg = '<b>Mailing is disabled at 1 minute intervals!</b>'

			await bot.send_message(callback_query.from_user.id, msg)


	@dp.callback_query_handler(lambda c: c.data == 'u5m')
	async def u5m_cmd(callback_query: types.CallbackQuery):
		if not(int(getUserStat(callback_query.from_user.id)[10])):
			updateLogicTF(callback_query.from_user.id, 'u5m', 1)

			await bot.answer_callback_query(callback_query.id)
			msg = '<b>Включена рассылка интервалом 5 минут!</b>'
			if getUserStat(callback_query.from_user.id)[5] == 'en':
				msg = '<b>Mailing is enabled at 5 minutes intervals!</b>'

			await bot.send_message(callback_query.from_user.id, msg)
		else:
			updateLogicTF(callback_query.from_user.id, 'u5m', 0)

			await bot.answer_callback_query(callback_query.id)
			msg = '<b>Рассылка интервалом 5 минут отключена!</b>'
			if getUserStat(callback_query.from_user.id)[5] == 'en':
				msg = '<b>Mailing is disabled at 5 minutes intervals!</b>'

			await bot.send_message(callback_query.from_user.id, msg)


	@dp.callback_query_handler(lambda c: c.data == 'u15m')
	async def u15m_cmd(callback_query: types.CallbackQuery):
		if not(int(getUserStat(callback_query.from_user.id)[11])):
			updateLogicTF(callback_query.from_user.id, 'u15m', 1)

			await bot.answer_callback_query(callback_query.id)
			msg = '<b>Включена рассылка интервалом 15 минут!</b>'
			if getUserStat(callback_query.from_user.id)[5] == 'en':
				msg = '<b>Mailing is enabled at 15 minutes intervals!</b>'

			await bot.send_message(callback_query.from_user.id, msg)
		else:
			updateLogicTF(callback_query.from_user.id, 'u15m', 0)

			await bot.answer_callback_query(callback_query.id)
			msg = '<b>Рассылка интервалом 15 минут отключена!</b>'
			if getUserStat(callback_query.from_user.id)[5] == 'en':
				msg = '<b>Mailing is disabled at 15 minutes intervals!</b>'

			await bot.send_message(callback_query.from_user.id, msg)


	@dp.callback_query_handler(lambda c: c.data == 'u30m')
	async def u30m_cmd(callback_query: types.CallbackQuery):
		if not(int(getUserStat(callback_query.from_user.id)[12])):
			updateLogicTF(callback_query.from_user.id, 'u30m', 1)

			await bot.answer_callback_query(callback_query.id)
			msg = '<b>Включена рассылка интервалом 30 минут!</b>'
			if getUserStat(callback_query.from_user.id)[5] == 'en':
				msg = '<b>Mailing is enabled at 30 minutes intervals!</b>'

			await bot.send_message(callback_query.from_user.id, msg)
		else:
			updateLogicTF(callback_query.from_user.id, 'u30m', 0)

			await bot.answer_callback_query(callback_query.id)
			msg = '<b>Рассылка интервалом 30 минут отключена!</b>'
			if getUserStat(callback_query.from_user.id)[5] == 'en':
				msg = '<b>Mailing is disabled at 30 minutes intervals!</b>'

			await bot.send_message(callback_query.from_user.id, msg)


	@dp.callback_query_handler(lambda c: c.data == 'uallm')
	async def uallm_cmd(callback_query: types.CallbackQuery):
		updateLogicTF(callback_query.from_user.id, 'u1m', 1)
		updateLogicTF(callback_query.from_user.id, 'u5m', 1)
		updateLogicTF(callback_query.from_user.id, 'u15m', 1)
		updateLogicTF(callback_query.from_user.id, 'u30m', 1)

		await bot.answer_callback_query(callback_query.id)
		msg = '<b>Включена рассылка интервалом 1, 5, 15, 30 минут!</b>'
		if getUserStat(callback_query.from_user.id)[5] == 'en':
			msg = '<b>The newsletter is included in the interval of 1, 5, 15, 30 minutes!</b>'

		await bot.send_message(callback_query.from_user.id, msg)


	@dp.callback_query_handler(lambda c: c.data == 'uoffsm')
	async def uoffsm_cmd(callback_query: types.CallbackQuery):
		updateLogicTF(callback_query.from_user.id, 'u1m', 0)
		updateLogicTF(callback_query.from_user.id, 'u5m', 0)
		updateLogicTF(callback_query.from_user.id, 'u15m', 0)
		updateLogicTF(callback_query.from_user.id, 'u30m', 0)

		await bot.answer_callback_query(callback_query.id)
		msg = '<b>Все рассылки отключены!</b>'
		if getUserStat(callback_query.from_user.id)[5] == 'en':
			msg = '<b>All mailings are disabled!</b>'

		await bot.send_message(callback_query.from_user.id, msg)


	@dp.callback_query_handler(lambda c: c.data == 'logic_on')
	async def logic_om_cmd_data(callback_query: types.CallbackQuery):
		if int(getUserStat(callback_query.from_user.id)[3]) != 1:
			updateUser(callback_query.from_user.id, 1)

			os.system(f'start python logic.py {callback_query.from_user.id}')

			msg = '<b>Алгоритм запущен!</b>'
			if getUserStat(callback_query.from_user.id)[5] == 'en':
				msg = '<b>Algorithm has been started!</b>'

			await bot.send_message(callback_query.from_user.id, msg)
		else:
			msg = '<b>Алгоритм уже запущен!</b>'
			if getUserStat(callback_query.from_user.id)[5] == 'en':
				msg = '<b>Algorithm is already running!</b>'

			await bot.send_message(callback_query.from_user.id, msg)


	@dp.callback_query_handler(lambda c: c.data == 'logic_off')
	async def logic_off_cmd_data(callback_query: types.CallbackQuery):
		if int(getUserStat(callback_query.from_user.id)[3]) != 0:
			updateUser(callback_query.from_user.id, 0)

			msg = '<b>Алгоритм отключен!</b>'
			if getUserStat(callback_query.from_user.id)[5] == 'en':
				msg = '<b>Algorithm has been disabled!</b>'

			await bot.send_message(callback_query.from_user.id, msg)
		else:
			msg = '<b>Алгоритм уже отключен!</b>'
			if getUserStat(callback_query.from_user.id)[5] == 'en':
				msg = '<b>Algorithm is already disabled!</b>'

			await bot.send_message(callback_query.from_user.id, msg)


	@dp.callback_query_handler(lambda c: c.data == 'upersm')
	async def upersm_cmd(callback_query: types.CallbackQuery):
		msg = '<b>Как создать свой алгоритм? Инструкция:</b>\n\n<b>Настройки:</b>\n<code>/time</code> <i>час</i>  <b>- интервал проверки</b>\n<code>/percent</code> <i>процент</i>  <b>- порог проверки</b>\n\n<b>Запуск:</b>\n<code>/logic_on</code>  <b>- запустить алгоритм</b>\n<code>/logic_off</code>  <b>- выключить алгоритм</b>\n\nПисать все числами, не указывать знаки процента и прочее!\nВ <code>/time</code> указывать строго время в часах\nЕсли число дробное, то писать через точку!'
		if getUserStat(callback_query.from_user.id)[5] == 'en':
			msg = '<b>How to create your own algorithm? Instruction manual:</b>\n\n<b>Settings:</b>\n<code>/time</code> <i>hour</i>  <b>- interval for check</b>\n<code>/percent</code> <i>percent</i>  <b>- trigger for check</b>\n\n<b>Start:</b>\n<code>/logic_on</code>  <b>- Enable</b>\n<code>/logic_off</code>  <b>- Disable</b>\n\nWrite everything in numbers, do not specify percent signs and so on!\nOn <code>/time</code> specify strictly the time in hours\nIf the number is fractional, then write through a dot!'
			key1 = types.InlineKeyboardButton('Enable', callback_data='logic_on')
			key2 = types.InlineKeyboardButton('Disable', callback_data='logic_off')
		else:
			key1 = types.InlineKeyboardButton('Включить', callback_data='logic_on')
			key2 = types.InlineKeyboardButton('Выключить', callback_data='logic_off')
		keyboard = types.InlineKeyboardMarkup().add(key1, key2)

		await bot.answer_callback_query(callback_query.id)
		await bot.send_message(callback_query.from_user.id, msg, reply_markup=keyboard)


	@dp.callback_query_handler(lambda c: c.data == 'langru')
	async def langru_cmd(callback_query: types.CallbackQuery):
		msg = '<b>Вы поменяли язык на русский!</b>'
		updateUlang(callback_query.from_user.id, 'ru')

		await bot.answer_callback_query(callback_query.id)
		await bot.send_message(callback_query.from_user.id, msg, reply_markup=getKeyboard(callback_query, 'main'))


	@dp.callback_query_handler(lambda c: c.data == 'langen')
	async def langru_cmd(callback_query: types.CallbackQuery):
		msg = '<b>You have changed the language to English!</b>'
		updateUlang(callback_query.from_user.id, 'en')

		await bot.answer_callback_query(callback_query.id)
		await bot.send_message(callback_query.from_user.id, msg, reply_markup=getKeyboard(callback_query, 'main'))


	@dp.message_handler(commands=['help', 'instruction', 'info', 'помощь', 'хелп', 'инструкция'])
	async def instruction_cmd(message: types.Message):
		if getUserStat(message.from_user.id) is not None:
			try:
				await dp.throttle(message.text, rate=time_for_spam_ban)
			except Throttled:
				msg = f'<b>Подождите {time_for_spam_ban} секунды. Нельзя часто использовать эту команду.</b>'
				if getUserStat(message.from_user.id)[5] == 'en':
					msg = f"<b>Wait {time_for_spam_ban} seconds. You can't use this command often.</b>"

				await message.reply(msg)
				await bot.send_message(logs_chat_id, f'<b>Пользователь {message.from_user.username} спамит!\n\n{message.text}</b>\n\n<i>Id: {message.from_user.id}</i>')
			else:
				msg = '<b>Вы можете включить/выключить рассылку уведомлений по отклонениям\nВыберите готовый интервал, либо создайте свой:</b>\n\n<i>Полная инструкция -></i> @crypto_bot_help'

				if getUserStat(message.from_user.id)[5] == 'en':
					key = types.InlineKeyboardButton('1 minute', callback_data='u1m')
					key2 = types.InlineKeyboardButton('5 minutes', callback_data='u5m')
					key3 = types.InlineKeyboardButton('15 minutes', callback_data='u15m')
					key4 = types.InlineKeyboardButton('30 minutes', callback_data='u30m')
					key5 = types.InlineKeyboardButton('Enable all', callback_data='uallm')
					key6 = types.InlineKeyboardButton('Create own', callback_data='upersm')
					key7 = types.InlineKeyboardButton('Disable all', callback_data='uoffsm')
					msg = '<b>You can enable/disable sending notifications on deviations\nChoose a ready-made interval, or create your own:</b>\n\n<i>Full instruction -></i> @crypto_bot_help'
				else:
					key = types.InlineKeyboardButton('1 минута', callback_data='u1m')
					key2 = types.InlineKeyboardButton('5 минут', callback_data='u5m')
					key3 = types.InlineKeyboardButton('15 минут', callback_data='u15m')
					key4 = types.InlineKeyboardButton('30 минут', callback_data='u30m')
					key5 = types.InlineKeyboardButton('Включить все', callback_data='uallm')
					key6 = types.InlineKeyboardButton('Создать', callback_data='upersm')
					key7 = types.InlineKeyboardButton('Отключить все', callback_data='uoffsm')

				keyboard = types.InlineKeyboardMarkup().add(key, key2, key3, key4, key5, key6, key7)

				await bot.send_message(message.from_user.id, msg, reply_markup=keyboard)
		else:
			await bot.send_message(message.from_user.id, '@crypto_bot_help')


	@dp.message_handler(commands=['start'])
	async def start_cmd(message: types.Message):
		if not(getUserStat(message.from_user.id) is not None):
			await bot.send_message(message.from_user.id, text= f'<b>Hi, {message.from_user.username}!</b>\nTo continue, you need to register!\n\nEnter the registration code:')
		else:
			await bot.send_message(message.from_user.id, access_denied)


	@dp.message_handler(commands=['registration', 'reg', 'регистрация', 'register', 'рег'])
	async def register_cmd(message: types.Message):
		if not(getUserStat(message.from_user.id) is not None):
			await bot.send_message(message.from_user.id, '<b>Enter the registration code:</b>')
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

			await bot.send_message(message.from_user.id, '<b>Registration was successful!</b>\nUse the keyboard to make it more convenient!', reply_markup=getKeyboard(message, 'main'))
			await bot.send_message(logs_chat_id, f'<b>Пользователь {message.from_user.username} зарегистрировался!</b>\n\n<i>Id: {message.from_user.id}</i>')
		else:
			await bot.send_message(message.from_user.id, access_denied)


	@dp.message_handler()
	async def echo(message: types.Message):
		if getUserStat(message.from_user.id) is not None:
			msg = message.text.lower()

			if msg == 'on' or msg == 'вкл':
				try:
					await dp.throttle(message.text, rate=time_for_spam_ban)
				except Throttled:
					msg = f'<b>Подождите {time_for_spam_ban} секунды. Нельзя часто использовать эту команду.</b>'
					if getUserStat(message.from_user.id)[5] == 'en':
						msg = f"<b>Wait {time_for_spam_ban} seconds. You can't use this command often.</b>"

					await message.reply(msg)
					await bot.send_message(logs_chat_id, f'<b>Пользователь {message.from_user.username} спамит!\n\n{message.text}</b>\n\n<i>Id: {message.from_user.id}</i>')
				else:
					if int(getUserStat(message.from_user.id)[3]) != 1:
						updateUser(message.from_user.id, 1)

						os.system(f'start python logic.py {message.from_user.id}')

						msg = '<b>Алгоритм запущен!</b>'
						if getUserStat(message.from_user.id)[5] == 'en':
							msg = '<b>Algorithm has been started!</b>'

						await bot.send_message(message.from_user.id, msg)
					else:
						msg = '<b>Алгоритм уже запущен!</b>'
						if getUserStat(message.from_user.id)[5] == 'en':
							msg = '<b>The algorithm is already running!</b>'

						await bot.send_message(message.from_user.id, msg)

			if msg == 'off' or msg == 'выкл':
				try:
					await dp.throttle(message.text, rate=time_for_spam_ban)
				except Throttled:
					msg = f'<b>Подождите {time_for_spam_ban} секунды. Нельзя часто использовать эту команду.</b>'
					if getUserStat(message.from_user.id)[5] == 'en':
						msg = f"<b>Wait {time_for_spam_ban} seconds. You can't use this command often.</b>"

					await message.reply(msg)
					await bot.send_message(logs_chat_id, f'<b>Пользователь {message.from_user.username} спамит!\n\n{message.text}</b>\n\n<i>Id: {message.from_user.id}</i>')
				else:
					if int(getUserStat(message.from_user.id)[3]) != 0:
						updateUser(message.from_user.id, 0)
						os.system(f'start Taskkill /PID {int(getUserStat(message.from_user.id)[8])} /F')
						updateUpid(message.from_user.id, 0)

						msg = '<b>Алгоритм отключен!</b>'
						if getUserStat(message.from_user.id)[5] == 'en':
							msg = '<b>Algorithm has been disabled!</b>'

						await bot.send_message(message.from_user.id, msg)
					else:
						msg = '<b>Алгоритм уже отключен!</b>'
						if getUserStat(message.from_user.id)[5] == 'en':
							msg = '<b>The algorithm is already disabled!</b>'

						await bot.send_message(message.from_user.id, msg)

			if msg == 'койны' or msg == 'койн' or msg == 'coins' or msg == 'coin' or msg == 'coins💰' or msg == 'binance':
				try:
					await dp.throttle(message.text, rate=time_for_spam_ban)
				except Throttled:
					msg = f'<b>Подождите {time_for_spam_ban} секунды. Нельзя часто использовать эту команду.</b>'
					if getUserStat(message.from_user.id)[5] == 'en':
						msg = f"<b>Wait {time_for_spam_ban} seconds. You can't use this command often.</b>"

					await message.reply(msg)
					await bot.send_message(logs_chat_id, f'<b>Пользователь {message.from_user.username} спамит!\n\n{message.text}</b>\n\n<i>Id: {message.from_user.id}</i>')
				else:
					await getCoins(message, bot, 'binance')

			if msg == 'bybit_test':
				try:
					await dp.throttle(message.text, rate=time_for_spam_ban)
				except Throttled:
					msg = f'<b>Подождите {time_for_spam_ban} секунды. Нельзя часто использовать эту команду.</b>'
					if getUserStat(message.from_user.id)[5] == 'en':
						msg = f"<b>Wait {time_for_spam_ban} seconds. You can't use this command often.</b>"

					await message.reply(msg)
					await bot.send_message(logs_chat_id, f'<b>Пользователь {message.from_user.username} спамит!\n\n{message.text}</b>\n\n<i>Id: {message.from_user.id}</i>')
				else:
					await getCoins(message, bot, 'bybit')

			if msg == 'настройки' or msg == 'options' or msg == 'settings' or msg == 'опции' or msg == 'options⚙️':
				try:
					await dp.throttle(message.text, rate=time_for_spam_ban)
				except Throttled:
					msg = f'<b>Подождите {time_for_spam_ban} секунды. Нельзя часто использовать эту команду.</b>'
					if getUserStat(message.from_user.id)[5] == 'en':
						msg = f"<b>Wait {time_for_spam_ban} seconds. You can't use this command often.</b>"

					await message.reply(msg)
					await bot.send_message(logs_chat_id, f'<b>Пользователь {message.from_user.username} спамит!\n\n{message.text}</b>\n\n<i>Id: {message.from_user.id}</i>')
				else:
					await getOptions(message, bot)

			if msg == 'инструменты' or msg == 'tools':
				try:
					await dp.throttle(message.text, rate=time_for_spam_ban)
				except Throttled:
					msg = f'<b>Подождите {time_for_spam_ban} секунды. Нельзя часто использовать эту команду.</b>'
					if getUserStat(message.from_user.id)[5] == 'en':
						msg = f"<b>Wait {time_for_spam_ban} seconds. You can't use this command often.</b>"

					await message.reply(msg)
					await bot.send_message(logs_chat_id, f'<b>Пользователь {message.from_user.username} спамит!\n\n{message.text}</b>\n\n<i>Id: {message.from_user.id}</i>')
				else:
					msg = '<b>Вы перешли в раздел инструменты!</b>'
					if getUserStat(message.from_user.id)[5] == 'en':
						msg = '<b>You have moved to the tools section!</b>'

					await bot.send_message(message.from_user.id, msg, reply_markup=getKeyboard(message, 'tools'))

			if msg == 'алгоритм' or msg == 'logic' or msg == 'algorithm':
				try:
					await dp.throttle(message.text, rate=time_for_spam_ban)
				except Throttled:
					msg = f'<b>Подождите {time_for_spam_ban} секунды. Нельзя часто использовать эту команду.</b>'
					if getUserStat(message.from_user.id)[5] == 'en':
						msg = f"<b>Wait {time_for_spam_ban} seconds. You can't use this command often.</b>"

					await message.reply(msg)
					await bot.send_message(logs_chat_id, f'<b>Пользователь {message.from_user.username} спамит!\n\n{message.text}</b>\n\n<i>Id: {message.from_user.id}</i>')
				else:
					msg = '<b>Вы перешли в раздел алгоритм!</b>'
					if getUserStat(message.from_user.id)[5] == 'en':
						msg = '<b>You have moved to the algorithm section!</b>'

					await bot.send_message(message.from_user.id, msg, reply_markup=getKeyboard(message, 'logic'))

			if msg == 'скам' or msg == 'scam':
				await getScam(message, bot, dp)

			if msg == 'портфель' or msg == 'case' or msg == 'portfolio':
				await getCase(message, bot, dp)

			if msg == 'меню' or msg == 'menu' or msg == '/меню' or msg == '/menu':
				try:
					await dp.throttle(message.text, rate=time_for_spam_ban)
				except Throttled:
					msg = f'<b>Подождите {time_for_spam_ban} секунды. Нельзя часто использовать эту команду.</b>'
					if getUserStat(message.from_user.id)[5] == 'en':
						msg = f"<b>Wait {time_for_spam_ban} seconds. You can't use this command often.</b>"

					await message.reply(msg)
					await bot.send_message(logs_chat_id, f'<b>Пользователь {message.from_user.username} спамит!\n\n{message.text}</b>\n\n<i>Id: {message.from_user.id}</i>')
				else:
					msg = '<b>Вы перешли в раздел меню!</b>'
					if getUserStat(message.from_user.id)[5] == 'en':
						msg = '<b>You have moved to the menu section!</b>'

					await bot.send_message(message.from_user.id, msg, reply_markup=getKeyboard(message, 'main'))

			if msg == 'профиль' or msg == 'profile':
				await getProfile(message, bot)

			if msg == 'волатильность' or msg == 'volatility':
				await getVol(message, bot, dp)

			if msg == 'faq':
				await bot.send_message(message.from_user.id, 'This feature is still in development.', reply_markup=getKeyboard(message, 'main'))
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
