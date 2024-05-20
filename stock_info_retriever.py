import csv
import config
# Load stock data from CSV into a dictionary
stock_data = {}
with open(config.STOCK_DATA_FILE, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        stock_name = row['name'].lower()
        stock_data[stock_name] = {
            'ticker': row['ticker'],
            'group': row['group'] if 'group' in row else None
        }

# Function to extract stock names, tickers, and groups from user question
def extract_stock_info(question):
    question = question.lower()  # Convert question to lowercase for case-insensitive matching
    stock_names = []
    stock_tickers = []
    stock_groups = []
    words = question.split()
    i = 0
    while i < len(words):
        for j in range(i + 1, min(i + 4, len(words)) + 1):
            phrase = ' '.join(words[i:j])
            if phrase in stock_data:  # Check if the phrase is a stock name
                stock_names.append(phrase)
                stock_tickers.append(stock_data[phrase]['ticker'])
                stock_groups.append(stock_data[phrase]['group'])
                i = j - 1  # Move i to the end of the found stock name
                break
            elif phrase.upper() in [data['ticker'] for data in stock_data.values()]:  # Check if the phrase is a ticker
                for name, data in stock_data.items():
                    if data['ticker'] == phrase.upper():
                        stock_names.append(name)
                        stock_tickers.append(phrase.upper())
                        stock_groups.append(data['group'])
                        i = j - 1  # Move i to the end of the found ticker
                        break
        i += 1

    tab=[stock_names, stock_tickers, stock_groups]
    return tab
