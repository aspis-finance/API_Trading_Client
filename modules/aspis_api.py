'''aspis python api alpha'''
import requests
import json

class Aspis_API_client:
    def __init__(self, settings) -> None:
        self.settings = settings
        self.chain_id = settings['server']['chain_id_default']

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
    

if __name__ == '__main__':
    pass