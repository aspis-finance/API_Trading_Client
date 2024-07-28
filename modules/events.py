class Event(object):
    """
    Event is base class providing an interface for all subsequent
    (inherited) events, that will trigger further events in the
    trading infrastructure.
    """
    pass

class OHLCVUpdate(Event):
    def __init__(self, timestamp, symbol:str, timeframe:str, df):
        self.type = 'OHLCVUPDATE'
        self.timestamp = timestamp
        self.symbol = symbol
        self.timeframe = timeframe
        self.df = df

class BalanceUpdate(Event):
    def __init__(self, timestamp, symbol, amount) -> None:
        self.type = 'BALANCEUPDATE'
        self.timestamp = timestamp
        self.symbol = symbol
        self.amount = float(amount)

class SignalEvent(Event):
    def __init__(self, timestamp, symbol, signal) -> None:
        self.type = 'SIGNALEVENT'
        self.timestamp = timestamp
        self.symbol = symbol 
        self.signal = signal 

class OrderEvent(Event):
    def __init__(self, timestamp, token1, token2, amount, entry_price, initial_value, status, stop_loss, take_profit) -> None:
        self.type = 'ORDEREVENT'
        self.timestamp = timestamp
        self.token1 = token1 
        self.token2 = token2
        self.amount = amount 

        self.entry_price = entry_price
        self.initial_value = initial_value
        self.status = status #OPEN or PENDING
        self.stop_loss = stop_loss
        self.take_profit = take_profit 

class PositionEvent(Event):
    def __init__(self, timestamp, token, amount, entry_price, initial_value, status, stop_loss, take_profit) -> None:
        self.type = 'POSITIONEVENT'
        self.timestamp = timestamp
        self.token = token
        self.amount = amount
        self.entry_price = entry_price
        self.initial_value = initial_value
        self.status = status #OPEN or PENDING
        self.stop_loss = stop_loss
        self.take_profit = take_profit 
