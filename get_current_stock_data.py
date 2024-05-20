from stock_data_fetcher import StockService
from stock_info_retriever import extract_stock_info
import csv
import config
import json
stock_service= StockService(config.BASE_URL)
token = stock_service.login("22015595", "1")
stock_data = {}
with open(config.STOCK_DATA_FILE, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        stock_name = row['name'].lower()
        stock_data[stock_name] = {
            'ticker': row['ticker'],
            'group': row['group'] if 'group' in row else None
        }

# Function to retrieve stock info by symbol or name
def get_stock_info(input_value):
    tab=[]
    input_value = input_value.lower()  # Convert input to lowercase for case-insensitive matching
    if input_value in stock_data:  # Check if input is a stock name
        name = input_value
        ticker = stock_data[name]['ticker']
        group = stock_data[name]['group']
    else:
        ticker = input_value.upper()
        name = None
        group = None
        for stock_name, data in stock_data.items():
            if data['ticker'] == ticker:  # Check if input is a ticker
                name = stock_name
                group = data['group']
                break

    if name:
        tab=[name,ticker,group]
        return tab
    else:
        return {
             'Stock not found'
        }



def get_current_data(symbol):

    data=get_stock_info(symbol)

    flux_data =stock_service.get_stock_by_symbol(token,int(data[2]),str(data[1]))
    return flux_data
#k=get_current_data('ATL')
#print(k)
