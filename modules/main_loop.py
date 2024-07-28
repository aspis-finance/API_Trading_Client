from queue import Queue
import asyncio
from configparser import ConfigParser
import os

from data_storage import DataStorage
from data_manager import DataManager
from strategy import Strategy, Strategy2, Strategy3
from portfolio import Portfolio
from execution import Execution
from risk_manager import RiskManager

class MainLoop:
    def __init__(self):
        settings = self.read_config()
        
        self.events = Queue()
        self.data_storage = DataStorage(settings=settings)
        self.data_manager = DataManager(settings=settings, events=self.events)
        self.strategy = Strategy(settings=settings, events=self.events)
        self.portfolio = Portfolio(settings=settings, events=self.events, data_storage=self.data_storage)
        self.execution = Execution(settings=settings, events=self.events)
        self.risk_manager = RiskManager(settings=settings, events=self.events, data_storage=self.data_storage)

    def read_config(self):
        config_object = ConfigParser()
        filename = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'config.ini'
        config_object.read(filename)
        settings = {sect: dict(config_object.items(sect)) for sect in config_object.sections()}
        settings['trade']['markets'] = eval(settings['trade']['markets']) #string to dict
        return settings

    async def event_loop(self):
        #all bot trading events
        while True:
            await asyncio.sleep(0.1)

            try:
                event = self.events.get(False)

            except Exception as e:
                await asyncio.sleep(0)

            else:
                try:
                    if event is not None:

                        if event.type == 'OHLCVUPDATE':
                            #print(f'OHLCV UPDATE EVENT: timestamp: {event.timestamp}, symbol {event.symbol}, timeframe {event.timeframe}')
                            self.data_storage.ohlcv.update(event)
                            self.strategy.run(event)

                            self.risk_manager.check_prices(event)

                        if event.type == 'BALANCEUPDATE':
                            print(f'BALANCE UPDATE EVENT: timestamp: {event.timestamp}, symbol {event.symbol}, amount {event.amount}')
                            self.data_storage.balances.update(event)
                            self.data_storage.calc_usd_value()

                        if event.type == 'SIGNALEVENT':
                            print(f'NEW SIGNAL EVENT: timestamp: {event.timestamp}, symbol {event.symbol}, signal {event.signal}')
                            #self.data_storage.balances.update(event)
                            self.portfolio.run(event)

                        if event.type == 'ORDEREVENT':
                            print(f'NEW ORDER EVENT: timestamp: {event.timestamp}, amount {event.amount} from {event.token1} to {event.token2} ')
                            self.execution.execute(event)

                        if event.type == 'POSITIONEVENT':
                            print(f'NEW POSITION EVENT: token: {event.token} amount: {event.amount} initial_value($) {event.initial_value} stop: {event.stop_loss}, take profit: {event.take_profit}')
                            self.data_storage.positions.update(event)

                        #parse api answers
                        #200 -> save positions data
                        #400 -> log errors 
                        #if loss 2% per position -> fix loss by risk manager
                        #max loss in settings 10% -> sell all -> pause for 1 day?

                        #calc everything in portfolio 
                        #send it to order event
                        #if it's FILLED
                        #create position event
                        
                except Exception as e:
                    print('event_loop error:', e)

    def run(self):
        #run bot here
        self.ioloop = asyncio.get_event_loop()
        #add more tasks here
        tasks = [self.ioloop.create_task(self.event_loop()), \
                 self.ioloop.create_task(self.data_manager.task_ohlcv()), \
                 self.ioloop.create_task(self.data_manager.task_balances())
                 ]
        wait_tasks = asyncio.wait(tasks)
        self.ioloop.run_until_complete(wait_tasks)
        self.ioloop.close()
    
if __name__ == '__main__':
    bot = MainLoop()
    bot.run()
