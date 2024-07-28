'''price updates -> signals'''
from stockstats import StockDataFrame
from datetime import datetime

from events import SignalEvent

class Strategy:
    ''' mean revert strategy'''
    '''mean revert: buy rsi <20, sell rsi > 80'''
        
    def __init__(self, settings, events) -> None:
        self.settings = settings
        self.events = events

    def run(self, event):
        if self.filter_signal(event):
            signal = self.calc_rsi(event)
            if signal != 'FLAT':
                self.create_event(event, signal)

    def create_event(self, event, signal):
        timestamp = datetime.utcnow()
        self.events.put(SignalEvent(timestamp, event.symbol, signal))

    def calc_rsi(self, event):
        stock = StockDataFrame.retype(event.df)
        rsi = stock.get('rsi')
        if rsi.iloc[-1] < 30:
            signal = 'BUY'
        elif rsi.iloc[-1] > 70:
            signal = 'SELL'
        else:
            signal = 'FLAT'

        print(event.symbol, 'RSI is ', rsi.iloc[-1], 'signal is', signal)

        return signal
    
    def filter_signal(self, event):
        '''filter signal, the price must be not lower that 1% from ma, skip downtrends '''
        stock = StockDataFrame.retype(event.df)
        sma = stock.get('close_80_sma')
        last_sma = sma.iloc[-1]
        last_close = event.df['close'].iloc[-1]
        if last_close > 0.99 * last_sma:
            return True 

class Strategy2:
    '''trend following strategy
    ma10 > ma25
    this is a long-only strategy'''
    def __init__(self, settings, events) -> None:
        self.settings = settings
        self.events = events

    def run(self, event):
        signal = self.calc_ma(event)
        if signal != 'FLAT':
            self.create_event(event, signal)

    def calc_ma(self, event):
        stock = StockDataFrame.retype(event.df)
        ma_short = stock.get('close_10_sma')
        ma_long =  stock.get('close_25_sma')
        rsi = stock.get('rsi')
        
        if ma_short.iloc[-1] > ma_long.iloc[-1] and rsi.iloc[-1] < 30:
            signal = 'BUY'
        elif ma_short.iloc[-1] > ma_long.iloc[-1] and rsi.iloc[-1] > 30:
            signal = 'FLAT'
        else:
            signal = 'SELL' #short < long , sell

        print(f'STRATEGY: symbol is {event.symbol}, ma_short = {ma_short.iloc[-1]}, ma_long = {ma_long.iloc[-1]}, rsi = {rsi.iloc[-1]}, signal is {signal}')
        
        return signal
    
    def create_event(self, event, signal):
        timestamp = datetime.utcnow()
        self.events.put(SignalEvent(timestamp, event.symbol, signal))


class Strategy3:
    '''scalp / statarb
    ma30 > ma50 = uptrend, buy when price < BB
    
    vwap for trend detection, BB(14 len, 2 std), RSI for confirmation
    
    SL = 1 ATR, TP = SL * coef(1.5-2)
    '''
    def __init__(self, settings, events) -> None:
        self.settings = settings
        self.events = events

    def run(self, event):
        signal = self.calc_signal(event)
        if signal != 'FLAT':
            self.create_event(event, signal)

    def calc_signal(self, event):
        stock = StockDataFrame.retype(event.df)
        ma_short = stock.get('close_30_sma')
        ma_long =  stock.get('close_50_sma')
        stock.get('boll_20')
        #print(stock['boll_ub_20'], stock['boll_lb_20'], stock['close'].iloc[-1])
        
        if ma_short.iloc[-1] > ma_long.iloc[-1] and stock['close'].iloc[-1] < stock['boll_lb_20'].iloc[-1]:
            signal = 'BUY'
        elif ma_short.iloc[-1] > ma_long.iloc[-1]:
            signal = 'FLAT'
        else:
            signal = 'SELL' #short < long , sell

        lb = stock['boll_lb_20'].iloc[-1]
        ub = stock['boll_ub_20'].iloc[-1]

        print(f'STRATEGY: symbol is {event.symbol}, ma_short = {ma_short.iloc[-1]}, ma_long = {ma_long.iloc[-1]}, boll lb = {lb}, boll up = {ub}, signal is {signal}')
        
        return signal
    
    def create_event(self, event, signal):
        timestamp = datetime.utcnow()
        self.events.put(SignalEvent(timestamp, event.symbol, signal))