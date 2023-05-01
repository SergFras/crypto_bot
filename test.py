Топ 10 самых волатильных монет:
... % 24h vol
... % 24h vol
... % 24h vol
... % 24h vol
... % 24h vol
Топ 10 самых неволатильных монет:
... % 24h vol
... % 24h vol
... % 24h vol
... % 24h vol
... % 24h vol


:45.981033





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
