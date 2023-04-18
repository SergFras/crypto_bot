import re
import requests
from bs4 import BeautifulSoup

header = {
	'user_agent': 'Mozilla/5.0'
}

def resClear(s, val):
	words_clear = []
	if val == 'wtf':
		words_clear = ['<', '>', '"', 'span', 'class', '=', '_ngcontent-sc172', '/']
	elif val == 'new':
		words_clear = ['<', '>', '"', 'span', 'class', '=', '.', '-', 'input', '/', 'i-price-buy', 'b', 'price', 'no', 'data', 'wrap', 'coin',
		 'id', 'sym', 'ol', 'tc', 'target', "'", '{', '}']
	elif val == 'sec_ob':
		words_clear = ['json', 'aed', 'del', 'ars']
	elif val == 'adv':
		words_clear = ['span', '<', '>', '/', '[', ']', '900', '#', '&', ';', ':', '.', 'tw', 'text', 'gray', 'dark', 'white', 'font', 'class', '_', '"', '-', '=', 'data', 'no', 'target', 'decimal',
		 'wrap', 'medium', 'price', 'button', 'bg', 'transparent', 'focus', 'outline', 'ne', 'pl', 'pr', 'action', 'click', 'gt', 'coins', 'information',
		 'toggleMarketCapFdvRatio', 'i', 'fas', 'fa', 'chevron', 'down', 'marketCapFdvToggle', 'opac', 'ty', 'lse']

	s = str(s)
	for i in range(len(words_clear)):
		if words_clear[i] in s:
			s = s.replace(words_clear[i], ' ')
			s = re.sub(r'\s+', ' ', s)
	return s.strip()

# WhatToFarm
def getPrice(url):
	temp = []

	response = requests.get(url)
	soup = BeautifulSoup(response.text, 'lxml')
	divs = soup.find_all('div', class_='row')

	for div in divs:
		spans = div.find_all('span')
		for span in spans:
			temp.append(resClear(span, 'wtf'))
	return temp[0][1:]

def getResponse():
	url = 'https://www.coingecko.com/ru/Криптовалюты'
	return int(str(requests.get(url, headers=header))[11:-2])

# CoinGeko Объем
def getAdvInfo(url):
	temp = ''

	response = requests.get(url, headers=header)
	resp = int(str(response)[11:-2]) # Ответ от Сервера

	if resp == 200:
		soup = BeautifulSoup(response.text, 'lxml')
		divs = soup.find_all('div', class_='tw-flex')

		for tr in divs:
			trs = tr.find_all('span', class_='tw-text-gray-900 dark:tw-text-white tw-font-medium')
			temp += resClear(trs, 'adv')
		temp = temp[50:100]
		temp = temp.split(' ')
		for i in range(len(temp)):
			temp[i] = str(temp[i])
			if '$' not in temp[i]:
				temp[i] = ''
			else: break

		temp = str(''.join(temp)[1:])

		value = ''
		for i in temp:
			if not(i.isalpha()):
				value += i
			else: break
		return value
	else:
		return f'--\nОшибка!\nКод ошибки: {resp}'


# CoinGeko prices
def getnewPrices(url):
	temp = ''

	response = requests.get(url, headers=header)
	resp = int(str(response)[11:-2]) # Ответ от Сервера

	if resp == 200:
		soup = BeautifulSoup(response.text, 'lxml')
		divs = soup.find_all('span', class_='no-wrap')

		for i in divs:
			temp += resClear(i, 'new')

		temp = temp[:70]
		temp = resClear(temp, 'sec_ob')
		temp = temp.split(' ')
		for i in range(len(temp)):
			temp[i] = str(temp[i])
			if '$' not in temp[i]:
				temp[i] = ''
			else: break

		temp = str(''.join(temp)[1:])
		temp = re.match(r'^.*?\:', temp).group(0)[:-1]

		return temp
	else:
		return f'--\nОшибка!\nКод ошибки: {resp}'


def checkCoinScam(token):
	response = requests.get(f'https://sapi.honeypot.is/v1/GetContractVerification?address={token}')
	if int(str(response)[11:-2]) == 200:
		req = response.text[-7:]

		return req.replace(':', '').replace('}', '')
	else:
		return 'Ошибка соединения!'
