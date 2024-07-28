import ccxt
import pandas as pd
from datetime import datetime
import asyncio

from events import OHLCVUpdate, BalanceUpdate
from aspis_api import Aspis_API_client

class OHLCV:
    def __init__(self, settings, events):
        self.settings = settings
        self.events = events

        self.api_noauth = {
            'apiKey': '',
            'secret': ''}
        self.api = ccxt.binance(self.api_noauth)

        self.timeframes = ['5m', '15m', '1h']

    def get(self, symbol, timeframe, limit):
        try:

            ohlcv = self.api.fetch_ohlcv(symbol, timeframe=timeframe, since=None, limit=limit)
        except Exception as e:
            print('OHLCV.get() error: ', e)
        return ohlcv
    
    def create_df(self, ohlcv):
        df = pd.DataFrame(data = ohlcv, columns = ['timestamp',
                                                   'open',
                                                   'high',
                                                   'low',
                                                   'close',
                                                   'volume'])
        return df
    
    def create_event(self, symbol, timeframe, df):
        timestamp = datetime.utcnow()
        self.events.put(OHLCVUpdate(timestamp, symbol, timeframe, df))

    def run_all(self):
        for symbol in self.settings['trade']['markets']:
            timeframe = self.settings['trade']['timeframe']
            limit = int(self.settings['trade']['limit'])
            data = self.get(symbol, timeframe, limit)
            df = self.create_df(data)
            self.create_event(symbol, timeframe, df)

class Balances:
    def __init__(self, settings, events):
        self.settings = settings
        self.events = events
        self.api = Aspis_API_client(settings=settings)

    def get(self):
        data = self.api.get_balance()
        return data

    def create_event(self, data):
        timestamp = datetime.utcnow()
        for key, value in data.items():
            symbol = key
            amount = value['non_scaled']
            self.events.put(BalanceUpdate(timestamp, symbol, amount))

    def run_all(self):
        data = self.get()
        self.create_event(data)

class DataManager:
    def __init__(self, settings, events):
        self.settings = settings
        self.events = events
        self.ohlcv = OHLCV(settings, events)
        self.balances = Balances(settings, events)

    @asyncio.coroutine
    def task_ohlcv(self):
        while True:
            try:
                self.ohlcv.run_all()
            except Exception as e:
                print('DataManager.task_ohlcv() error: ', e) 
            yield from asyncio.sleep(int(self.settings['trade']['ohlcv_sleep']))

    @asyncio.coroutine
    def task_balances(self):
        while True:
            try:
                self.balances.run_all()
            except Exception as e:
                print('DataManager.task_balances() error: ', e)
            yield from asyncio.sleep(int(self.settings['trade']['balance_sleep']))

if __name__ == '__main__':
    pass       


