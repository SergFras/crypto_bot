import sys
import os
import time
import datetime
import telebot

from config import *
from database.db import *
from modules.defs import *


def send_bot(utf, uhour, uprocent):
	bot = telebot.TeleBot(telegram_token)

	res, msg = defStarting(uprocent, f'{utf}.txt'), ''
	if len(res) == 0:
		print(f'Empty - {utf} - {str(datetime.datetime.now())[:-10]}')
	else:
		for i in range(len(res)):
			msg += str(res[i])
		msg += f'\n\n<i>Интервал: {uhour} мин</i>'
		for j in getAllStat():
			if j[9] and (utf == 'u1m'):
				bot.send_message(j[0], msg, disable_web_page_preview=True, parse_mode='html')
			if j[10] and (utf == 'u5m'):
				bot.send_message(j[0], msg, disable_web_page_preview=True, parse_mode='html')
			if j[11] and (utf == 'u15m'):
				bot.send_message(j[0], msg, disable_web_page_preview=True, parse_mode='html')
			if j[12] and (utf == 'u30m'):
				bot.send_message(j[0], msg, disable_web_page_preview=True, parse_mode='html')
		if utf == 'u5m':
			bot.send_message(notifications_chat_id, msg, disable_web_page_preview=True, parse_mode='html')

	print(f'\nLogic for {utf} has been completed!\n')
	res.clear()


def check_time():
	if datetime.datetime.now().minute % 5 == 0:
		return True
	else:
		return False


def base_logic(utf, uhour, uprocent):
	send_bot(utf, uhour, uprocent)

	time.sleep(int(uhour)*60)
	base_logic(utf, uhour, uprocent)


def start(act, utf, uhour, uprocent):
	if check_time():
		print(f'Logic for {utf} has been {act}! pid= {os.getpid()}')

		base_logic(utf, uhour, uprocent)
	else:
		time.sleep(time_for_check_start)
		start(act, utf, uhour, uprocent)


if __name__ == "__main__":
	utf = str(sys.argv[1])
	uhour = int(sys.argv[2])
	uprocent = float(sys.argv[3])

	if utf == 'u1m':
		updateTfPid('u1m', int(os.getpid()))
	if utf == 'u5m':
		updateTfPid('u5m', int(os.getpid()))
	if utf == 'u15m':
		updateTfPid('u15m', int(os.getpid()))
	if utf == 'u30m':
		updateTfPid('u30m', int(os.getpid()))

	if not(os.path.exists(f'allcoins/{utf}.txt')):
		f = open(f'allcoins/{utf}.txt', 'w', encoding='utf-8')
		f.close()

	time.sleep(1)
	getAllCoins(f'{utf}.txt')

	try:
		start('started', utf, uhour, uprocent)
	except:
		start('reloaded', utf, uhour, uprocent)