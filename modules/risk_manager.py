from datetime import datetime
import math

from events import OrderEvent

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
    
def convert_from_binance_format(symbol):
    if symbol in ['BTC/USDT', 'BTC/USDC']:
        return 'WBTC'
    if symbol in ['ETH/USDT', 'ETH/USDC']:
        return 'WETH'
    else:
        return symbol[:-5]

class RiskManager:
    '''reads positions data from data_storage
    sells position if stop reached
    sell position if take profit reached'''
    
    def __init__(self, settings, events, data_storage) -> None:
        self.settings = settings
        self.events = events
        self.data_storage = data_storage

    def check_prices(self, event):
        last_close = event.df['close'].iloc[-1]
        token = convert_from_binance_format(event.symbol)
        try:

            positions = self.data_storage.positions.read()
            position = positions[token]
            entry_price = position.entry_price
            stop_loss = position.stop_loss
            take_profit = position.take_profit
            print(f'Risk Manager: symbol {event.symbol} token {token} price {last_close} entry: {entry_price} stop: {stop_loss} take: {take_profit}')
            #if price > take or price < stop: generate orders
            if last_close < stop_loss or last_close > take_profit:
                #generate stop loss / take profit order
                token1, token2 = parse_symbol(event.symbol, side = 'SELL')

                token1 = filter_symbol_names(token1)
                token2 = filter_symbol_names(token2)

                min_trade_size = int(self.settings['trade']['min_trade_size'])
                available_balance = self.data_storage.balances.usd_values[convert_from_binance_format(event.symbol)]
        

                amount = self.data_storage.balances.data[convert_from_binance_format(event.symbol)]
                amount = math.floor(amount * 100000000) / 100000000
                if available_balance < min_trade_size:
                    amount = 0

                entry_price = 0
                initial_value = 0
                status = 'PENDING'
                stop_loss = 0
                take_profit = 0 

                self.generate_order(token1, token2, amount, entry_price, initial_value, status, stop_loss, take_profit)

            

        except Exception as e:
            print(f'RiskManager. Probably no position found. Error: {e}')

    
    def generate_order(self, token1, token2, amount, entry_price, initial_value, status, stop_loss, take_profit):
        timestamp = datetime.utcnow()
        self.events.put(OrderEvent(timestamp, token1, token2, amount, entry_price, initial_value, status, stop_loss, take_profit))
        