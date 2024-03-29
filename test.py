from config import *
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
import pandas as pd

client = Client(binance_token, binance_secret)
tickers = client.get_ticker()
ticker_df = pd.DataFrame(tickers)
ticker_df.set_index('symbol', inplace=True)

open_price = round(float(ticker_df.loc['JASMYBUSD']['openPrice']), 4)
close_price = round(float(ticker_df.loc['JASMYBUSD']['lastPrice']), 4)

print(open_price, close_price, f'{round(((open_price - close_price) / close_price) * 100, 2)}%')






































# coins = [('SXPBUSD', -4.09), ('UNFIBUSD', -3.54), ('MKRBUSD', -3.24), ('FXSBUSD', -2.52), ('CHZBUSD', -2.36), ('OMGBUSD', -1.52), ('TRXBUSD', -1.45), ('AUDBUSD', -1.19), ('ACMBUSD', -0.78), ('BANDBUSD', -0.59), ('XMRBUSD', -0.13), ('CTKBUSD', -0.13), ('PAXGBUSD', -0.05), ('XRPBUSD', 0.0), ('ZILBUSD', 0.0), ('RSRBUSD', 0.0), ('ONEBUSD', 0.0), ('DOGEBUSD', 0.0), ('JASMYBUSD', 0.0), ('LEVERBUSD', 0.0), ('ARPABUSD', 0.0), ('REEFBUSD', 0.0), ('DGBBUSD', 0.0), ('JSTBUSD', 0.0), ('CKBBUSD', 0.0), ('IOSTBUSD', 0.0), ('XVGBUSD', 0.0), ('MAGICBUSD', 0.09), ('BCHBUSD', 0.09), ('BTSBUSD', 0.1), ('NANOBUSD', 0.1), ('STRATBUSD', 0.1), ('AIONBUSD', 0.1), ('BTTBUSD', 0.1), ('ERDBUSD', 0.1), ('BKRWBUSD', 0.1), ('VTHOBUSD', 0.1), ('DCRBUSD', 0.1), ('IRISBUSD', 0.1), ('LENDBUSD', 0.1), ('KMDBUSD', 0.1), ('WNXMBUSD', 0.1), ('BZRXBUSD', 0.1), ('YFIIBUSD', 0.1), ('SWRVBUSD', 0.1), ('FLMBUSD', 0.1), ('BOTBUSD', 0.1), ('DNTBUSD', 0.1), ('HEGICBUSD', 0.1), ('COVERBUSD', 0.1), ('BTCSTBUSD', 0.1), ('TRUBUSD', 0.1), ('PAXBUSD', 0.1), ('EPSBUSD', 0.1), ('EURBUSD', 0.18), ('SFPBUSD', 0.24), ('GBPBUSD', 0.32), ('EOSBUSD', 0.39), ('SUSHIBUSD', 0.5), ('KAVABUSD', 0.52), ('IOTABUSD', 0.52), ('LTCBUSD', 0.56), ('BALBUSD', 0.59), ('DIABUSD', 0.62), ('CHRBUSD', 0.66), ('APEBUSD', 0.81), ('AVABUSD', 0.83), ('KP3RBUSD', 0.85), ('BNTBUSD', 0.87), ('ETHBUSD', 0.92), ('LUNABUSD', 0.97), ('CFXBUSD', 0.99), ('IDEXBUSD', 1.04), ('CRVBUSD', 1.12), ('TWTBUSD', 1.14), ('UNIBUSD', 1.26), ('AAVEBUSD', 1.31), ('KNCBUSD', 1.34), ('OPBUSD', 1.38), ('NMRBUSD', 1.4), ('FTMBUSD', 1.46), ('ETCBUSD', 1.47), ('TOMOBUSD', 1.47), ('LINKBUSD', 1.54), ('ADABUSD', 1.55), ('WAVESBUSD', 1.58), ('YFIBUSD', 1.63), ('SOLBUSD', 1.65), ('TRBBUSD', 1.67), ('FILBUSD', 1.67), ('BTCBUSD', 1.69), ('ALGOBUSD', 1.7), ('LITBUSD', 1.7), ('XTZBUSD', 1.73), ('GHSTBUSD', 1.76), ('1INCHBUSD', 1.76), ('DASHBUSD', 1.79), ('MASKBUSD', 1.83), ('ZECBUSD', 1.92), ('AXSBUSD', 1.98), ('WINGBUSD', 2.07), ('STORJBUSD', 2.08), ('RUNEBUSD', 2.09), ('SANDBUSD', 2.15), ('XLMBUSD', 2.17), ('ARBUSDT', 2.21), ('APTBUSD', 2.23), ('OCEANBUSD', 2.25), ('CELOBUSD', 2.27), ('INJBUSD', 2.27), ('ENJBUSD', 2.41), ('SNXBUSD', 2.43), ('MANABUSD', 2.48), ('AERGOBUSD', 2.48), ('AUDIOBUSD', 2.48), ('HARDBUSD', 2.48), ('MATICBUSD', 2.5), ('AVAXBUSD', 2.53), ('BATBUSD', 2.56), ('ATOMBUSD', 2.58), ('WRXBUSD', 2.61), ('BNBBUSD', 2.62), ('ONTBUSD', 2.64), ('SKLBUSD', 2.7), ('LDOBUSD', 2.76), ('PROMBUSD', 2.77), ('BLZBUSD', 2.78), ('XVSBUSD', 2.87), ('SUPERBUSD', 2.9), ('DOTBUSD', 2.93), ('NEOBUSD', 2.94), ('BAKEBUSD', 2.94), ('VIDTBUSD', 3.03), ('FIOBUSD', 3.23), ('HBARBUSD', 3.39), ('LRCBUSD', 3.4), ('ROSEBUSD', 3.45), ('CVPBUSD', 3.47), ('GMTBUSD', 3.51), ('UFTBUSD', 3.54), ('PERPBUSD', 3.61), ('ICXBUSD', 3.69), ('CAKEBUSD', 3.69), ('ZRXBUSD', 3.7), ('FLOWBUSD', 3.8), ('BELBUSD', 3.88), ('DODOBUSD', 4.14), ('NEARBUSD', 4.17), ('ANTBUSD', 4.26), ('SYSBUSD', 4.26), ('RVNBUSD', 4.35), ('SRMBUSD', 4.42), ('IMXBUSD', 4.49), ('COMPBUSD', 4.61), ('QTUMBUSD', 4.62), ('GRTBUSD', 4.65), ('ALPHABUSD', 4.69), ('VETBUSD', 4.76), ('KSMBUSD', 5.36), ('CREAMBUSD', 5.37), ('DATABUSD', 6.25), ('EGLDBUSD', 6.57), ('LINABUSD', 9.09), ('RNDRBUSD', 12.29), ('CTSIBUSD', 12.62), ('AUTOBUSD', 18.09)]

# for i in range(len(coins)):
#     print(i, coins[i])

# msg = f'<b>Всего монет:</b> <i>{len(cmd_coins)}</i>\n<b>Биржа:</b> <i>binance</i>\n\n'
# if getUserStat(message.from_user.id)[5] == 'en':
# 	msg = f'<b>Total coins:</b> <i>{len(cmd_coins)}</i>\n<b>Stock Market:</b> <i>binance</i>\n\n'
# for i in range(len(cmd_coins) // 2):
#     temp.append(f'<code>{cmd_coins[i][:-4]}: {vols[i]}%</code>')
#
# for i in range(len(cmd_coins) // 2, len(cmd_coins)):
#     temp2.append(f'<code>{cmd_coins[i][:-4]}: {vols[i]}%</code>')
#
# for i in range(len(temp)):
#     msg += f'<code>{spaces(temp, temp[i])} {temp2[i]}</code>\n'







# with open('test.txt') as f:
#     coins = f.readlines()
#
#     for i in range(len(coins)):
#         coins[i] = coins[i].replace('https://www.binance.com/en/trade/', '')
#         coins[i] = coins[i].replace('\n', '')
#         coins[i] = coins[i].replace('/', '')
#         coins[i] = coins[i].replace('_', '')
#     print(coins)
#     print(len(coins))
#
# binance_coins = ['BTCBUSD', 'APTBUSD', 'XRPBUSD', 'SOLBUSD', 'ZILBUSD', 'RSRBUSD', 'TRBBUSD', 'CRVBUSD', 'SXPBUSD',
# 'UNIBUSD', 'BNBBUSD', 'ETHBUSD', 'RVNBUSD', 'XLMBUSD', 'ADABUSD', 'LTCBUSD', 'CHZBUSD', 'FTMBUSD', 'ONEBUSD', 'DOTBUSD',
# 'ZECBUSD', 'GMTBUSD', 'ATOMBUSD', 'KAVABUSD', 'FLOWBUSD', 'CELOBUSD', 'DOGEBUSD', 'MASKBUSD', 'DASHBUSD', 'BANDBUSD',
# 'ALGOBUSD', 'MATICBUSD', 'WAVESBUSD', 'SUSHIBUSD', 'IOTABUSD', 'JASMYBUSD', 'LEVERBUSD',
# 'GRTBUSD', 'INJBUSD', 'IMXBUSD', 'MAGICBUSD', 'RNDRBUSD', 'CHRBUSD', 'ARPABUSD', 'UNFIBUSD', 'EOSBUSD', 'HBARBUSD', 'REEFBUSD',
# 'BCHABCBUSD', 'LINKBUSD', 'ETCBUSD', 'TRXBUSD', 'BCHBUSD', 'QTUMBUSD', 'VETBUSD', 'EURBUSD', 'BULLBUSD', 'BEARBUSD', 'ETHBULLBUSD',
# 'ETHBEARBUSD', 'ICXBUSD', 'BTSBUSD', 'BNTBUSD', 'NEOBUSD', 'XTZBUSD', 'EOSBULLBUSD', 'EOSBEARBUSD', 'XRPBULLBUSD', 'XRPBEARBUSD',
# 'BATBUSD', 'ENJBUSD', 'NANOBUSD', 'ONTBUSD', 'STRATBUSD', 'AIONBUSD', 'BTTBUSD', 'TOMOBUSD', 'XMRBUSD', 'BNBBULLBUSD', 'BNBBEARBUSD',
# 'DATABUSD', 'CTSIBUSD', 'ERDBUSD', 'WRXBUSD', 'KNCBUSD', 'REPBUSD', 'LRCBUSD', 'IQBUSD', 'GBPBUSD', 'DGBBUSD', 'COMPBUSD', 'BKRWBUSD',
# 'SNXBUSD', 'VTHOBUSD', 'DCRBUSD', 'STORJBUSD', 'IRISBUSD', 'MKRBUSD', 'DAIBUSD', 'RUNEBUSD', 'MANABUSD', 'LENDBUSD', 'ZRXBUSD', 'AUDBUSD',
# 'FIOBUSD', 'AVABUSD', 'BALBUSD', 'YFIBUSD', 'BLZBUSD', 'KMDBUSD', 'JSTBUSD', 'SRMBUSD', 'ANTBUSD', 'SANDBUSD', 'OCEANBUSD', 'NMRBUSD',
# 'LUNABUSD', 'IDEXBUSD', 'PAXGBUSD', 'WNXMBUSD', 'BZRXBUSD', 'YFIIBUSD', 'KSMBUSD', 'EGLDBUSD', 'DIABUSD', 'BELBUSD', 'SWRVBUSD', 'WINGBUSD',
# 'CREAMBUSD', 'AVAXBUSD', 'FLMBUSD', 'CAKEBUSD', 'XVSBUSD', 'ALPHABUSD', 'VIDTBUSD', 'AAVEBUSD', 'NEARBUSD', 'FILBUSD', 'AERGOBUSD', 'AUDIOBUSD',
# 'CTKBUSD', 'BOTBUSD', 'KP3RBUSD', 'AXSBUSD', 'HARDBUSD', 'DNTBUSD', 'CVPBUSD', 'STRAXBUSD', 'FORBUSD', 'FRONTBUSD', 'BCHABUSD', 'ROSEBUSD',
# 'SYSBUSD', 'HEGICBUSD', 'PROMBUSD', 'SKLBUSD', 'COVERBUSD', 'GHSTBUSD', 'DFBUSD', 'JUVBUSD', 'PSGBUSD', 'BTCSTBUSD', 'TRUBUSD', 'DEXEBUSD',
# 'USDCBUSD', 'TUSDBUSD', 'PAXBUSD', 'CKBBUSD', 'TWTBUSD', 'LITBUSD', 'SFPBUSD', 'FXSBUSD', 'DODOBUSD', 'BAKEBUSD', 'UFTBUSD', '1INCHBUSD',
# 'IOSTBUSD', 'OMGBUSD', 'ACMBUSD', 'AUCTIONBUSD', 'PHABUSD', 'TVKBUSD', 'BADGERBUSD', 'FISBUSD', 'OMBUSD', 'PONDBUSD', 'DEGOBUSD', 'ALICEBUSD',
# 'BIFIBUSD', 'LINABUSD', 'PERPBUSD', 'RAMPBUSD', 'SUPERBUSD', 'CFXBUSD', 'XVGBUSD', 'EPSBUSD', 'AUTOBUSD', 'TKOBUSD', 'TLMBUSD', 'BTGBUSD',
# 'ARBUSDT', 'LDOBUSD', 'APEBUSD', 'OPBUSD']
#
# binance_coins = ['BTCBUSD', 'APTBUSD', 'XRPBUSD', 'SOLBUSD', 'ZILBUSD', 'RSRBUSD', 'TRBBUSD', 'CRVBUSD', 'SXPBUSD',
# 'UNIBUSD', 'BNBBUSD', 'ETHBUSD', 'RVNBUSD', 'XLMBUSD', 'ADABUSD', 'LTCBUSD', 'CHZBUSD', 'FTMBUSD', 'ONEBUSD', 'DOTBUSD',
# 'ZECBUSD', 'GMTBUSD', 'ATOMBUSD', 'KAVABUSD', 'FLOWBUSD', 'CELOBUSD', 'DOGEBUSD', 'MASKBUSD', 'DASHBUSD', 'BANDBUSD',
# 'ALGOBUSD', 'MATICBUSD', 'WAVESBUSD', 'SUSHIBUSD', 'IOTABUSD', 'JASMYBUSD', 'LEVERBUSD',
# 'GRTBUSD', 'INJBUSD', 'IMXBUSD', 'MAGICBUSD', 'RNDRBUSD', 'CHRBUSD', 'ARPABUSD', 'UNFIBUSD', 'EOSBUSD', 'HBARBUSD', 'REEFBUSD']














# CASE

# data, msg = [], '<b>📕Ваш портфель:</b>\n\n'
#
# if getUserStat(message.from_user.id)[5] == 'en':
#     msg = '<b>📕Status of your portfolio:</b>\n\n'
#
# for path in filenames:
#     with open(f'allcases/{message.from_user.id}/{path}') as f:
#         tmp = [path[:-4], f.readlines()]
#         data.append(tmp)
#
# for info in data:
#     values = []
#     msg += f'<b>{info[0]}:</b>\n'
#
#     for i in info[1]:
#         i = i.replace('\n', '')
#         values.append(list(i.split(' ')))
#     for i in values:
#         price = checkPrice(i[0])
#
#         if price != 'Error':
#             msg += f'<i>{i[0]}</i>\n<b>📊Price:</b> ${price}\n<b>📉24h:</b> {None}%\n<b>💳Hold:</b> {i[2]} (${round(float(i[2]) * price, 3)})\n<b>⚖️AvgBuy:</b> ${i[1]}\n<b>📈P&L:</b> ${round(price - float(i[1]), 3)} ({None}%)\n\n'
#         else:
#             if getUserStat(message.from_user.id)[5] == 'en':
#                 msg += f'<i>{i[0]}</i>\n<b>This coin is not found on binance!</b>\n\n'
#             else:
#                 msg += f'<i>{i[0]}</i>\n<b>Такого койна нет на бинансе!</b>\n\n'
#     msg += '\n'
# msg += '\n<code>/case help</code>'
#
# await bot.send_message(message.from_user.id, msg)
