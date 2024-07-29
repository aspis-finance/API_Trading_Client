from aspis_api import Aspis_API_client

client = Aspis_API_client()

config = client.read_config()
config = client.convert_time(config)
vault = client.create_vault(config)

if vault:
    print('Finish, vault created: ', vault)
    print('\nCopy your vault name from the terminal or check vault.txt for your vault name')
else:
    print('Something went wrong. Try to change vault name and other parameters in config.ini')

with open('/app/config/vault.txt', 'w') as f:
    f.write(vault.strip())

