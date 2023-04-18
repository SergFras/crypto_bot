import database.db as dbb
import modules.defs as mod
from config import *

import telebot
#import asyncio
import time

def get_ucoins(uid):
	uid = int(uid)
	mod.getAllCoins(f'{uid}.txt')
	time.sleep(7)

def analize(uid, udefwork, bot):
	if udefwork:
		uprocent = dbb.getUserStat(uid)[6]
		res = mod.defStarting(uprocent, f'{uid}.txt')
		if len(res) == 0:
			print(f'{uid} Empty')
		for i in range(len(res)):
			bot.send_message(uid, res[i], parse_mode='html')
		res.clear()
		uhour = dbb.getUserStat(uid)[7]
		time.sleep(int(uhour*3600))
		analize(uid, udefwork, bot)

def start_thread(uid):
	uid = int(uid)
	mod.createFile(f'{uid}.txt')
	get_ucoins(uid)
	print(f'Thread for user {uid} has been started')
	bot = telebot.TeleBot(token)

	udefwork = dbb.getUserStat(uid)[3]
	analize(uid, udefwork, bot)

def go(uid):
	uid = int(uid)
	start_thread(uid)
	#loop = asyncio.new_event_loop()
	#loop.run_until_complete(start_thread(uid))