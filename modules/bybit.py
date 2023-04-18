import requests
from config import *


def getPrice(lst):
	tmp = []

	for i in lst:
		price = requests.get(f'https://api.bybit.com/spot/v3/public/quote/ticker/price?symbol={i}').json()

		if price['retMsg'] == 'OK':
			tmp.append(price['result']['price'])
		else:
			tmp.append('None')
	return tmp