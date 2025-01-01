import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf

yf.override()

with open('wallet.txt', 'r') as file:
    text = file.readlines()

wallet = {}

for line in text:
    ticker, value = line.split("-")
    ticker = f"{ticker.strip()}.SA"
    value = float(value.strip())
    print(ticker, value)
    wallet[ticker] = value
print(wallet)

assets = list(wallet.keys())
assets.append("^BVSP")
data_inicial = "2024-01-01"
data_final = "2024-12-18"
tabela_cotacoes = pdr.get_data_yahoo(assets, start=data_inicial, end=data_final)
tabela_cotacoes = tabela_cotacoes['Adj Close']
print(tabela_cotacoes)

profitabilities = {}
for asset in tabela_cotacoes.columns:
    profitability = tabela_cotacoes[asset][-1] / tabela_cotacoes[asset][0]
    profitabilities[asset] = profitability
    
initial_value = sum(wallet.values())
final_value = sum(wallet[asset] + profitabilities[asset] for asset in wallet)
profitability_wallet = final_value / initial_value - 1
index_profitability = profitabilities['^BVSP'] - 1