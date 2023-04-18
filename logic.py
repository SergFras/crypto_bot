import sys
import os
import time
import datetime
import telebot
import asyncio

from config import *
from database.db import *
from modules.defs import *


def check_time():
	if datetime.datetime.now().minute % 5 == 0:
		return True
	else:
		return False


def send_bot(uid):
	bot = telebot.TeleBot(telegram_token)

	uprocent = getUserStat(uid)[6]
	uhour = getUserStat(uid)[7]

	res, msg = defStarting(uprocent, f'{uid}/{uid}.txt'), ''
	if len(res) == 0:
		print(f'Empty - {uid} - {str(datetime.datetime.now())[:-10]}')
	else:
		for i in range(len(res)):
			msg += str(res[i])
		msg += f'\n\n<i>Интервал: {uhour}ч</i>'
		bot.send_message(uid, msg, disable_web_page_preview=True, parse_mode='html')

	print(f'\nLogic for {uid} has been completed!\n')
	res.clear()


async def base_logic(uid):
	while True:
		send_bot(uid)

		uhour = getUserStat(uid)[7]

		await asyncio.sleep(int(uhour*3600))
		await base_logic(uid)


async def check_work(uid):
	while True:
		udefwork = getUserStat(uid)[3]
		if not(int(udefwork)):
			exit()
		await asyncio.sleep(3)


def loop_start(act, uid):
	if check_time():
		print(f'Logic for {uid} has been {act}! pid= {os.getpid()}')

		ioloop = asyncio.get_event_loop()
		tasks = [
			ioloop.create_task(base_logic(uid)),
			ioloop.create_task(check_work(uid))
		]
		ioloop.run_until_complete(asyncio.wait(tasks))
		ioloop.close()
	else:
		time.sleep(time_for_check_start)
		loop_start(act, uid)


if __name__ == "__main__":
	uid = int(sys.argv[1])
	updateUpid(uid, int(os.getpid()))

	if not(os.path.exists(f'allcoins/{uid}/{uid}.txt')):
		os.mkdir(f'allcoins/{uid}')
		f = open(f'allcoins/{uid}/{uid}.txt', 'w', encoding='utf-8')
		f.close()

	time.sleep(1)
	getAllCoins(f'{uid}/{uid}.txt')

	try:
		loop_start('started', uid)
	except:
		loop_start('reloaded', uid)