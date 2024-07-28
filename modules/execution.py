from datetime import datetime

from aspis_api import Aspis_API_client
from events import PositionEvent

class Execution:
    '''add additional logic here
    filter size = 0
    
    round to .0000000001'''
    def __init__(self, settings, events) -> None:
        self.api = Aspis_API_client(settings)
        self.events = events

    def execute(self, event):
        if event.amount:
            token, amount = self.api.execute(event.token1, event.token2, event.amount)

            if token and amount:
                if token not in ['USDT', 'USDC', 'DAI']:
                    #create position event
                    self.create_position_event(event, token, amount)


    def create_position_event(self, event, token, amount):
        #timestamp, token, entry_price, initial_value, status, stop_loss, take_profit
        timestamp = datetime.utcnow()
        status = 'OPEN'
        self.events.put(PositionEvent(timestamp, token, amount, event.entry_price, event.initial_value, status, event.stop_loss, event.take_profit))
        