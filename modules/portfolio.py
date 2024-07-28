'''gathers all balances data, generates orders'''
from datetime import datetime
import math

from events import OrderEvent

def convert_to_binance_format(symbol):
    #self.settings['trade']['default_usd']
    if symbol in ['WBTC']:
        return 'BTC/USDT'   
    if symbol in ['WETH']:
        return 'ETH/USDT'
    else:
        return symbol 

def convert_from_binance_format(symbol):
    if symbol in ['BTC/USDT', 'BTC/USDC']:
        return 'WBTC'
    if symbol in ['ETH/USDT', 'ETH/USDC']:
        return 'WETH'
    else:
        return symbol[:-5]

def parse_symbol(symbol, side):
    elems = symbol.split('/')
    if side == 'BUY':
        token1 = elems[1]
        token2 = elems[0] 
         
    if side == 'SELL':
        token1 = elems[0]
        token2 = elems[1] 

    return token1, token2

def filter_symbol_names(symbol):
    '''ETH -> WETH
    BTC -> WBTC'''
    if symbol == 'BTC':
        return 'WBTC'
    elif symbol == 'ETH':
        return 'WETH'
    else:
        return symbol

class Portfolio:
    '''total assets to be traded: 5
    if BUY: use 10% of all cash to buy them
    if SELL: sell all available
    target
    '''

    def __init__(self, settings, events, data_storage) -> None:
        self.settings = settings
        self.events = events
        self.data_storage = data_storage

    def read_price(self, symbol):
        symbol = convert_to_binance_format(symbol)
        df = self.data_storage.ohlcv.data[symbol]
        price = df['close'].iloc[-1]
        return price

    def run(self, event):
        #calc usd values
        #calc targets
        #check targets
        #generate orders
        target, target_usd = self.calc_targets(event)
        self.check_targets(event, target, target_usd)
        pass

    def calc_targets(self, event):
        if event.signal == 'SELL':
            target = 0
            target_usd = 0

        if event.signal == 'BUY':
            price = self.read_price(event.symbol)
            target = 0.1 * self.data_storage.balances.total / price
            target_usd = 0.1 * self.data_storage.balances.total

        #print(f'Portfolio: symbol is {event.symbol}, target is {target}') 
        return target, target_usd

    def check_targets(self, event, target, target_usd):
        min_trade_size = int(self.settings['trade']['min_trade_size'])
        '''if difference between target and available amount > min_size, create orders'''
        #print(self.data_storage.balances.usd_values)
        available_balance = self.data_storage.balances.usd_values[convert_from_binance_format(event.symbol)]
        #print(f'SIGNAL IS {event.signal}, SYMBOL is {event.symbol}, available balance in USD is {available_balance}, target in USD is {target_usd}')
        
        amount = 0

        token1, token2 = parse_symbol(event.symbol, event.signal)

        token1 = filter_symbol_names(token1)
        token2 = filter_symbol_names(token2)

        #BTC/USDT buy: execute USDT 2 BTC
        #BTC/USDT sell: execute BTC 0.0001 USDT
        
        #refactor: make a separate func calc_amount()
        if event.signal == 'BUY':
            #buy if available amount < target - min trade
            if available_balance < target_usd - min_trade_size:
                amount = target_usd - available_balance
                             
        if event.signal == 'SELL':
            #sell all available balance 
            amount = self.data_storage.balances.data[convert_from_binance_format(event.symbol)]
            if available_balance < min_trade_size:
                amount = 0
        #amount = round(amount, 8)
        amount = math.floor(amount * 100000000) / 100000000

        entry_price, initial_value, status, stop_loss, take_profit = self.calc_stops(event, amount)
        self.generate_order(token1, token2, amount, entry_price, initial_value, status, stop_loss, take_profit)

    def generate_order(self, token1, token2, amount, entry_price, initial_value, status, stop_loss, take_profit):
        timestamp = datetime.utcnow()
        self.events.put(OrderEvent(timestamp, token1, token2, amount, entry_price, initial_value, status, stop_loss, take_profit))
        #print(f'-_____________________order created: execute {token1} {token2} {amount}')

    #entry_price, initial_value, status, stop_loss, take_profit
    def calc_stops(self, event, amount):
        entry_price = self.read_price(event.symbol)
        initial_value = amount
        status = 'PENDING'
        stop_loss = entry_price - entry_price * float(self.settings['trade']['stop_loss']) / len(self.settings['trade']['markets'])
        take_profit = entry_price + entry_price * float(self.settings['trade']['take_profit']) / len(self.settings['trade']['markets'])
        return entry_price, initial_value, status, stop_loss, take_profit