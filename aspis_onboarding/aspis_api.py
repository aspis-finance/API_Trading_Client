'''aspis python api alpha'''
import requests
import json
import os 
from configparser import ConfigParser
from datetime import datetime, timedelta
import time 

class Aspis_API_client:
    def __init__(self) -> None:
        pass

    def get_balance(self):
        url = self.settings['server']['api_server'] + 'get-balance'
        params = {
        'chainId': self.chain_id,
        'vault': self.settings['server']['vault']
        }
        headers = {
        'x-api-key': self.settings['server']['api_key'],
        'Content-Type': 'application/json'
        }
        r = requests.get(url, params=params, headers=headers)
        print(type(r), r.status_code, r.headers, r.encoding, r.content)
        response = r.json()
        return response
    
    def execute(self, symbol1, symbol2, size):
        url = self.settings['server']['api_server'] + 'execute_order'
        params = {
        'chainId': self.chain_id,
        'vault': self.settings['server']['vault'],
        'srcToken': symbol1,
        'dstToken': symbol2,
        'amountIn': size, 
        'exchange': self.settings['server']['exchange'],
        'slippage': '1'
        }
        headers = {
        'x-api-key': self.settings['server']['api_key'],
        'Content-Type': 'application/json'
        }
        r = requests.post(url, json=params, headers=headers)
        print(type(r), r.status_code, r.headers, r.encoding, r.content)
        token, amount = self.parse_response(r)
        response = r.json()
        return token, amount
    
    def parse_response(self, r):
        if r.status_code == 200:
            #print('hello')
            data = r.content.decode('utf-8')
            data = json.loads(data)
            if data['status'] == 'FILLED':
                token = data['dstToken']
                amount = data['outputAmount']
                #print(f'parse: {token} {amount}')

                return token, amount

        if r.status_code == 400:
            print(f'error: {r.content}')
            return None, None
        
    def create_vault(self, config):
        chain_id = config['general']['chain_id']
        url = config['general']['api_server'] + 'create_vault' + f'?chainId={chain_id}'
        #print(f'url is : {url}')
        headers = {
        'x-api-key': config['general']['api_key'],
        'Content-Type': 'application/json'
        }
        #print('headers: ', headers)
        params = {
        'name': config['general']['name'],
        'symbol': config['general']['symbol'],
        'description': config['general']['description'],
        'maxCap': config['general']['max_cap'],
        'minDeposit': config['general']['min_deposit'],
        'maxDeposit': config['general']['max_deposit'],
        'startTime': config['general']['start_time'],
        'finishTime': config['general']['finish_time'],
        'withdrawalWindow': config['general']['withdrawal_window'],
        'freezePeriod': config['general']['freeze_period'],
        'lockLimit': config['general']['lock_limit'],
        'initialPrice': config['general']['initial_price'],
        'canChangeManager': config['general']['can_change_manager'],
        'canPerformDirectTransfer': config['general']['can_perform_direct_transfer'],
        'entranceFee': config['general']['entrance_fee'],
        'fundManagementFee': config['general']['fund_management_fee'],
        'performanceFee': config['general']['performance_fee'],
        'rageQuitFee': config['general']['rage_quit_fee'],
        'depositTokens': config['general']['deposit_tokens'],
        'tradingTokens': config['general']['trading_tokens'],
        'trustedProtocols': config['general']['trusted_protocols'],
        'quorumPercent': config['general']['quorum_percent'],
        'minApprovalPercent': config['general']['min_approval_percent'],
        'votingDuration': config['general']['voting_duration'],
        'minLpSharePercent': config['general']['min_lp_share_percent']        
        }
        #print('params: ')
        '''
        for key, value in params.items():
            print(key, '___', value)
        '''
        r = requests.post(url, json=params, headers=headers)
        print(type(r), r.status_code, r.headers, r.encoding, r.content)

        vault = self.parse_response_create_vault(r)
        return vault

    def parse_response_create_vault(self, r):
        vault = None
        if r.status_code == 200:
            data = r.content.decode('utf-8')
            data = json.loads(data)
            vault = data['vault']

        else:
            print(f'There was an error creating your vault. Message: {r.content}')

        return vault

    def read_config(self):
        config_object = ConfigParser()
        filename = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'config.ini'
        config_object.read(filename)
        settings = {sect: dict(config_object.items(sect)) for sect in config_object.sections()}
        settings['general']['deposit_tokens'] = eval(settings['general']['deposit_tokens'])
        settings['general']['trading_tokens'] = eval(settings['general']['trading_tokens'])
        settings['general']['trusted_protocols'] = eval(settings['general']['trusted_protocols'])
        return settings
    
    def run(self):
        config = self.read_config()
        config = self.convert_time(config)
        vault = self.create_vault(config)
        print('finish, vault created: ', vault.lower())

        with open('/app/config/vault.json', 'w') as f:
            f.write(vault.strip())        

    def convert_time(self, config):
        #convert time to unix format
        now = datetime.utcnow().replace(microsecond=0) 
        delta_1 = timedelta(hours=int(config['general']['start_fundraising_in']))
        delta_2 = timedelta(hours=int(config['general']['end_fundraising_in']))
        
        start = now + delta_1
        end = now + delta_2

        print(f'convert_time start: {start} end: {end}')

        start = time.mktime(start.timetuple())
        end = time.mktime(end.timetuple()) 

        print(f'convert_time start: {start} end: {end}')

        #print(now, delta_1, delta_2, start, end)

        config['general']['start_time'] = start
        config['general']['finish_time'] = end

        return config
        

    

if __name__ == '__main__':
    pass