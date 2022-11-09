import nest_asyncio
nest_asyncio.apply()
import numpy as np
import pandas as pd

pip install python-binance

import asyncio
from binance import BinanceSocketManager
from binance.client import Client

api_key = ""
api_secret = ""

client = Client(api_key, api_secret)

ST = 7
LT = 25

def gethistoricals (symbol, LT):
  df = pd.DataFrame(client.get_historical_klines(symbol, '1d',
                                                 str(LT) + 'days ago UTC',
                                                 '1 day ago UTC'))
  closes = pd.DataFrame(df[4])
  closes.columns = ['Close']
  closes['ST'] = closes.Close.rolling(ST-1).sum()
  closes['LT'] = closes.Close.rolling(LT-1).sum()
  closes.dropna(inplace=True)
  return closes

	def liveSMA(hist, live):
  liveST = (hist['ST'].values + live.Price.values) / ST
  liveLT = (hist['LT'].values + live.Price.values) / LT
  return liveST, liveLT

	def createframe(msg):
  df = pd.DataFrame([msg])
  df = df.loc[:,['s', 'E', 'p']]
  df.columns = ['symbol', 'Time', 'Price']
  df.Price = df.Price.astype(float)
  df.Time = pd.to_datetime(df.Time, unit='ms')
  return df

	async def main(coin, qty, SL_limit, open_position = False):
  bm = BinanceSocketManager(client)
  ts = bm.trade_socket(coin)
  async with ts as tscm:
    res = await tscm.recv()
    if res:
      frame = createframe(res)
      print(frame)
      livest, livelt = liveSMA(historycals, frame)
      if livest > livelt and not open_position:
        order = client.create_order(symbol=coin, syde='BUY', type='MARKET', quantity=qty)
        print(order)
        buyprice = float(order['fills'][0]['price'])
        open_position = True

      if open_position:
        if frame.Price[0] < buyprice * SL_limit or frame.Price[0] > 1.02 * buyprice:
          order = client.create_order(symbol=coin, syde='SELL', type='MARKET', quantity=qty)
          print(order)
          loop.stop()

if __name__ == '__main__':
  loop = asyncio.get_event_loop()
  loop.run_until_complete(main('BTCBUSD', 0.11057293, 0.999))
