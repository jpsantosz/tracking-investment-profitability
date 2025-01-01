import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf

# Substitui o padrão de acesso para o Yahoo Finance, que é necessário para o funcionamento da biblioteca
yf.override()

# Lê o arquivo "wallet.txt" que contém a carteira de ativos e seus valores iniciais
with open('wallet.txt', 'r') as file:
    text = file.readlines()

# Inicializa um dicionário para armazenar os ativos e seus valores
wallet = {}

# Processa cada linha do arquivo da carteira
for line in text:
    # Divide a linha no formato "ticker - valor" e extrai os dados
    ticker, value = line.split("-")
    ticker = f"{ticker.strip()}.SA" # Adiciona o sufixo ".SA" para identificar ativos na bolsa brasileira
    value = float(value.strip())
    print(ticker, value)
    wallet[ticker] = value
print(wallet)

# Lista de ativos da carteira, incluindo o índice IBOVESPA (^BVSP) para comparação
assets = list(wallet.keys())
assets.append("^BVSP")

data_inicial = "2024-01-01"
data_final = "2024-12-18"
# Obtém as cotações ajustadas dos ativos no período definido
tabela_cotacoes = pdr.get_data_yahoo(assets, start=data_inicial, end=data_final)
tabela_cotacoes = tabela_cotacoes['Adj Close']
print(tabela_cotacoes)

# Calcula a rentabilidade de cada ativo
profitabilities = {}
for asset in tabela_cotacoes.columns:
    profitability = tabela_cotacoes[asset][-1] / tabela_cotacoes[asset][0]
    profitabilities[asset] = profitability

# Calcula o valor inicial da carteira (soma dos valores iniciais de cada ativo)
initial_value = sum(wallet.values())
# Calcula o valor final da carteira considerando as rentabilidades de cada ativo
final_value = sum(wallet[asset] + profitabilities[asset] for asset in wallet)
# Calcula a rentabilidade da carteira
profitability_wallet = final_value / initial_value - 1
# Calcula a rentabilidade do índice IBOVESPA
index_profitability = profitabilities['^BVSP'] - 1