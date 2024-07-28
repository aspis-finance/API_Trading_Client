
class Balances:
    def __init__(self):
        self.data = {}
        self.total = 0
        self.usd_values = {}

    def update(self, event):
        self.data[event.symbol] = event.amount
        
    def read(self):
        return self.data

class OHLCV:
    def __init__(self):
        self.data = {}

    def update(self, event):
        self.data[event.symbol] = event.df        

    def read(self):
        return self.data

class Positions:
    def __init__(self):
        self.data = {}

    def update(self, event):
        self.data[event.token] = event
        
    def read(self):
        return self.data 

class DataStorage:
    def __init__(self, settings):
        self.settings = settings
        self.balances = Balances()
        self.ohlcv = OHLCV()
        self.positions = Positions()

    def calc_usd_value(self):
        total = 0
        for key, value in self.balances.data.items():
            if key in ['USDT', 'USDC', 'DAI']:
                usd_value = value
                
            elif key in ['WBTC']:
                symbol = 'BTC/' + self.settings['trade']['default_usd']
                df = self.ohlcv.data[symbol]
                price = df['close'].iloc[-1]
                usd_value = value * price
                
            elif key in ['WETH']:
                symbol = 'ETH/' + self.settings['trade']['default_usd']
                df = self.ohlcv.data[symbol]
                price = df['close'].iloc[-1]
                usd_value = value * price
                
            else:
                symbol = key + self.settings['trade']['default_usd']
                try:
                    df = self.ohlcv.data[symbol]
                    price = df['close'].iloc[-1]
                    usd_value = value * price
                except Exception as e:
                    usd_value = 0
                    continue 
                
            self.balances.usd_values[key] = usd_value

            total += usd_value
        self.balances.total = total

