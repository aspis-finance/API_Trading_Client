### Basic Trading Algo for Aspis

1. General
2. File Structure
3. Aspis API
4. Config
5. Events
6. Data Storage
7. Main Loop
8. Data Manager
9. Strategy
10. Portfolio
11. Execution
12. Risk Manager

**1. General**
This guide will enable users to develop their own software to trade on aspis.finance. It presents a framework to handle various investment strategies, including trend-following and mean-reversion strategies.

The code snippets will be in Python, but you can use the same architecture in any language. All code is open source and available on GitHub - link.

**2. File Structure**
We will use about 10 files for different purposes. You can modify this structure according to your needs or use it as is. There are several categories of files: config, structural, and strategy.

- Config: `config.ini`
- Structural: `main_loop`, `events`, `data_manager`, `data_storage`, `aspis_api`
- Strategy: `strategy`, `portfolio`, `risk_manager`, `execution`

We will dive deeper and describe each file a bit later.

**3. Aspis API**
This file contains 2 core methods that are absolutely required for algo trading: `get_balance` and `execute`.

- `get_balance` allows you to get all available balances of the vault (your trading account in Aspis).
- `execute` allows you to send trades to DEXes.

Our simple API connector also contains the method `parse_response`, which returns the result of an executed trade, e.g., if the trade was successful and the amount of tokens received.

**4. Config**
Config has 3 main sections: general, server, and trade.

- The general section handles your account data like a username to manage several trading algos.
- The trade section is responsible for the trading settings. The most important settings are:
  - `markets`: a list of markets you want to trade
  - `timeframe`: OHLCV timeframe to get the price data from Binance
  - `ohlcv_sleep` & `balance_sleep`: the amount of time to sleep between API calls, in seconds
  - `min_trade_size`: the minimum amount to trade, in USD (default: $1)
  - `stop_loss`: the amount of loss that will trigger the risk manager to sell all positions (default: 0.05, equivalent to 5%)
  - `take_profit`: the amount of profit that will trigger sell orders

- The server section is responsible for connection settings, vault, and exchange settings. The most important settings are:
  - `api_server`: Aspis API server IP
  - `chain_id_default`: chain ID settings to send trades to (options: Arbitrum (42161) and Polygon (137))
  - `vault`: your vault address
  - `api_key`: your Aspis API key
  - `exchange`: DEX to execute trades (options: 1inch, Uniswap, Odos)

**5. Events**
Using events is a good practice to separate your trading logic, create custom handlers for each event, write logs, etc. The most important events are:
- `OHLCVUpdate`: price updates from Binance exchange
- `BalanceUpdate`: vault balances update from Aspis API
- `SignalEvent`: emitted when the price or any custom indicator triggers a certain level; contains data about the market and the desired trade direction (buy or sell)
- `OrderEvent`: emitted after performing checks on a signal event; contains the amount of units to trade and info to control the open position (entry_price, stop_loss, take_profit)
- `PositionEvent`: indicates an open position after an order is executed; used to control stop losses and take profit thresholds

**6. Data Storage**
This is a simple in-memory data storage used to store all the info that our algo needs. More professional systems can consider using Redis as an in-memory data storage or other alternatives. You can also use traditional databases like PostgreSQL to store balances, trades, logs, etc.

In our implementation, we use 3 data structures:
- `OHLCV`: responsible for price data
- `Balances`: contains current vault balances
- `Positions`: contains info about open positions, if any

**7. Main Loop**
This is the entry point to our application. It gathers all the modules and settings. 
- The `event_loop` function handles all possible events. You can add custom events or handlers.
- The `run` function uses an asyncio infinite loop to perform tasks: handle the event loop, update prices, and balances.

**8. Data Manager**
The data manager contains 2 asyncio coroutines that run price updates and balance updates.

- `OHLCV` class: connects to Binance API without authentication, takes raw data, creates a pandas dataframe, and puts it into an `OHLCVUpdate` event using the ccxt library.
- `Balances` class: connects to Aspis API, gets balance updates, and produces `BalanceUpdate` events using a simple non-official Aspis API connector.

If your trading algo requires more data, you can add more data handlers to the data manager, such as news updates or websocket data.

**9. Strategy**
This module is responsible for any trading logic. In our example, the strategy module gets price updates as `OHLCVUpdate` events, calculates simple indicators like MAs, RSI, Bollinger Bands, etc., and produces signal events if conditions are met.

This code is mostly for educational purposes, and you should not expect such a simple strategy to help you beat the markets. NFA.

**10. Portfolio**
This module receives signals from the strategy module and checks our balances. If we have a BUY signal, the portfolio assumes that we need to have a certain position. It checks the available balances and produces buy orders if needed. If the signal is sell and we have non-zero balances, sell orders are created.

**11. Execution**
This class handles order events, uses our simple Aspis API connector to execute our orders, parses API responses, and creates a position if needed.

**12. Risk Manager**
This class reads our position data and price updates from data storage. If the current price is lower than stop loss or higher than take profit, it generates orders to close our open positions.
