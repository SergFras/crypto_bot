import time
from config import *
from database.db import *

def restart():
	time_frades_pids = getTfPidsStat()
	for i in time_frades_pids:
		os.system(f'start Taskkill /PID {i} /F')

	tfs = time_frades
	minutes = time_frades_minutes
	precents = time_frades_precents

	for i in range(len(tfs)):
		os.system(f'start python logic_times.py {tfs[i]} {minutes[i]} {precents[i]}')

while True:
	now = time.localtime()

	if now.tm_hour == 7 and now.tm_min == 58:
		restart()
	if now.tm_hour == 13 and now.tm_min == 58:
		restart()
	if now.tm_hour == 17 and now.tm_min == 58:
		restart()
	if now.tm_hour == 23 and now.tm_min == 58:
		restart()

	time.sleep(40)
