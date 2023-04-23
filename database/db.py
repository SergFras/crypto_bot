import sqlite3 as sl
import datetime
import os.path

path = 'database/users.db'


def createDB():
	if not(os.path.exists(path)):
		con = sl.connect(path)

		with con:
			con.execute("""
				CREATE TABLE USERS (
					uid INTEGER,
					uname TEXT,
					uregdate TEXT,
					udefwork INTEGER,
					uadmin INTEGER,
					uthread TEXT,
					uprocent REAL,
					uinterval REAL,
					upid INTEGER,
					u1m INTEGER,
					u5m INTEGER,
					u15m INTEGER,
					u30m INTEGER
				);
			""")
		con.commit()
		con.close()


def delUser(uid):
	uid = int(uid)
	con = sl.connect(path)
	cur = con.cursor()
	cur.execute(f'DELETE from USERS where uid = {uid}')
	con.commit()
	con.close()


def regUser(uid, uname):
	uregdate = str(datetime.date.today())
	con = sl.connect(path)
	cur = con.cursor()
	cur.execute('INSERT INTO USERS (uid, uname, uregdate, udefwork, uadmin, ulang, uprocent, uinterval, upid, u1m, u5m, u15m, u30m) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', (int(uid), str(uname), f'{uregdate}', 0, 0, 'en', 0.5, 1, 0, 0, 0, 0, 0))
	con.commit()
	con.close()


def getAllStat():
	con = sl.connect(path)
	users = con.execute(f'SELECT * FROM USERS').fetchall()

	return users


def getAllAdmins():
	con = sl.connect(path)
	users = con.execute(f'SELECT * FROM USERS WHERE uadmin = 1').fetchall()

	return users


def getAllGuests():
	con = sl.connect(path)
	users = con.execute(f'SELECT * FROM USERS WHERE uadmin = 0').fetchall()

	return users


def getUserStat(uid):
	uid = int(uid)
	con = sl.connect(path)
	user = con.execute(f'SELECT * FROM USERS WHERE uid = {uid}').fetchone()

	if user is None:
		con.close()
		return None
	else:
		con.close()

		uid = user[0]
		uname = user[1]
		uregdate = user[2]
		udefwork = user[3]
		uadmin = user[4]
		ulang = user[5]
		uprocent = user[6]
		uinterval = user[7]
		upid = user[8]
		u1m = user[9]
		u5m = user[10]
		u15m = user[11]
		u30m = user[12]

		return (uid, uname, uregdate, udefwork, uadmin, ulang, uprocent, uinterval, upid, u1m, u5m, u15m, u30m)


def getTfPidsStat():
	con = sl.connect('database/tf_pids.db')
	user = con.execute(f'SELECT * FROM USERS').fetchone()

	if user is None:
		con.close()
		return None
	else:
		con.close()

		u1m = user[0]
		u5m = user[1]
		u15m = user[2]
		u30m = user[3]

		return (u1m, u5m, u15m, u30m)


def updateTfPid(utf, tfpid):
	con = sl.connect('database/tf_pids.db')
	user = con.execute(f'SELECT * FROM USERS').fetchone()

	if user is None:
		con.close()
		return None
	else:
		con.execute(f"UPDATE USERS SET {utf} = {tfpid}")
		con.commit()
		con.close()


def updateUpid(uid, upid):
	uid = int(uid)
	con = sl.connect(path)
	user = con.execute(f'SELECT * FROM USERS WHERE uid = {uid}').fetchone()

	if user is None:
		con.close()
		return None
	else:
		con.execute(f"UPDATE USERS SET upid = {upid} WHERE uid = {uid}")
		con.commit()
		con.close()


def updateUnick(uid, unick):
	con = sl.connect(path)
	user = con.execute(f'SELECT * FROM USERS WHERE uid = {uid}').fetchone()

	if user is None:
		con.close()
		return None
	else:
		con.execute(f"UPDATE USERS SET uname = ? WHERE uid = ?", (unick, uid))
		con.commit()
		con.close()


def updateLogicTF(uid, utf, umin):
	uid = int(uid)
	con = sl.connect(path)
	user = con.execute(f'SELECT * FROM USERS WHERE uid = {uid}').fetchone()

	if user is None:
		con.close()
		return None
	else:
		con.execute(f"UPDATE USERS SET {utf} = {umin} WHERE uid = {uid}")
		con.commit()
		con.close()


def updateUprocent(uid, uprocent):
	con = sl.connect(path)
	user = con.execute(f'SELECT * FROM USERS WHERE uid = {uid}').fetchone()

	if user is None:
		con.close()
		return None
	else:
		con.execute(f"UPDATE USERS SET uprocent = {uprocent} WHERE uid = {uid}")
		con.commit()
		con.close()


def updateUinterval(uid, uinterval):
	con = sl.connect(path)
	user = con.execute(f'SELECT * FROM USERS WHERE uid = {uid}').fetchone()

	if user is None:
		con.close()
		return None
	else:
		con.execute(f"UPDATE USERS SET uinterval = {uinterval} WHERE uid = {uid}")
		con.commit()
		con.close()


def updateUser(uid, udefwork):
	con = sl.connect(path)
	user = con.execute(f'SELECT * FROM USERS WHERE uid = {uid}').fetchone()

	if user is None:
		con.close()
		return None
	else:
		con.execute(f"UPDATE USERS SET udefwork = {udefwork} WHERE uid = {uid}")
		con.commit()
		con.close()


def setAdmin(uid, uadmin):
	uadmin = int(uadmin)
	con = sl.connect(path)
	user = con.execute(f'SELECT * FROM USERS WHERE uid = {uid}').fetchone()

	if user is None:
		con.close()
		return None
	else:
		con.execute(f"UPDATE USERS SET uadmin = {uadmin} WHERE uid = {uid}")
		con.commit()
		con.close()
