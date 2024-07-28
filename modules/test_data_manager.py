import os 

from data_manager import DataManager
from configparser import ConfigParser
from aspis_api import Aspis_API_client

def read_config():
        config_object = ConfigParser()
        filename = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'config.ini'
        config_object.read(filename )
        settings = {sect: dict(config_object.items(sect)) for sect in config_object.sections()}
        settings['trade']['markets'] = eval(settings['trade']['markets']) #string to dict
        return settings

settings = read_config()
dm = DataManager(settings, 'events')
api = Aspis_API_client(settings=settings)

def test_get():
    data = dm.get(symbol='BTC/USDT', timeframe='15m', limit=100)
    print(data)

def test_create_df():
    data = dm.get(symbol='BTC/USDT', timeframe='1h', limit=100)
    df = dm.create_df(data)
    print(df)

def test_get_balance():
     data = dm.balances.get()
     print(data)

def test_balances_event():
     dm.balances.run_all()

def test_execute():
     #resp = api.execute('USDT', 'WETH', '2')
     resp = api.execute('WETH', 'USDT', '0.0001')
     print(resp)



if __name__ == '__main__':
    #test_get()
    #test_create_df()  
    test_get_balance()  
    #test_balances_event()
    test_execute()
    #test_get_balance()
    pass