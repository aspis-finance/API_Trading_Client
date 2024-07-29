## Welcome to Aspis.finance
This guide will help you to onboard and use Aspis API.

## 1. API key
First of all, get your API key from Aspis team. Then, go to config.ini in this folder and paste your API key to line 3: api_key = your_key_12345

## 2. Configure your vault
Go to config.ini and set all parameters for your vault. 

This short description can help you: https://lush-gymnast-e1e.notion.site/create_vault-44b6361fa42f4341a8dca1f5357bd992

Check Aspis knowledge base to learn more about Aspis vaults: https://info.aspis.finance/for-vault-creators/create-on-chain-vault/before-creating-the-vault

## 3. Run the onboarding script
When config.ini is ready, run the script to create your vault. Use the following steps:

# create a docker container
```
docker build -t onboarding .
```

# run docker container
```
docker run -v $(pwd):/app/config onboarding
```

If everything is ok, then your new vault is created and you will see the address both in your terminal and in vault.txt file. Copy this address to set up your trading algo. Onboarding is completed! 

If something went wrong and the vault was not created, try to change parameters in config.ini. Maybe vault name is already in use, try to change it and run the script again. 