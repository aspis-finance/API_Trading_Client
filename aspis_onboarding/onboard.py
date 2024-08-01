from aspis_api import Aspis_API_client
print('-1')
client = Aspis_API_client()
print('0')
config = client.read_config()
print('1')
config = client.convert_time(config)
print('2')
vault = client.create_vault(config)
print('3')

if vault:
    print('Finish, vault created: ', vault)
    print('\nCopy your vault name from the terminal or check vault.txt for your vault name')
    with open('/app/config/vault.txt', 'w') as f:
        f.write(vault.strip())
else:
    print('Something went wrong. Try to change vault name and other parameters in config.ini')



