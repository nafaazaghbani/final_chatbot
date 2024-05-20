import csv
from datetime import datetime
import investpy
import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG
import ChoiceSelector
# Establish a connection to the MySQL database
try:
    db_connection = mysql.connector.connect(**DB_CONFIG)
    cursor = db_connection.cursor()
    print("Connected to the database")
except Error as e:
    print("Error connecting to MySQL database:", e)
    exit(1)

# Create the stock_data table with indexes
create_table_query = """
CREATE TABLE IF NOT EXISTS stock_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    symbol VARCHAR(10),
    date DATE,
    open FLOAT,
    high FLOAT,
    low FLOAT,
    close FLOAT,
    volume INT,
    currency VARCHAR(10),
    INDEX symbol_index (symbol),
    INDEX date_index (date)
)
"""
try:
    cursor.execute(create_table_query)
    print("Table 'stock_data' created successfully")
except Error as e:
    print("Error creating table:", e)
    exit(1)

# Function to fetch historical stock data for a symbol and save it to the database
def fetch_and_save_stock_data(symbol):
    try:
        df = investpy.get_stock_historical_data(stock=symbol,
                                                country='Tunisia',
                                                from_date=config.date1,
                                                to_date=config.date2)
        print(f"Fetched data for {symbol}")

        # Save data to the MySQL database
        for index, row in df.iterrows():
            sql = "INSERT INTO stock_data (symbol, date, open, high, low, close, volume, currency) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            values = (symbol, index.strftime('%Y-%m-%d'), row['Open'], row['High'], row['Low'], row['Close'], row['Volume'], row['Currency'])
            cursor.execute(sql, values)

        db_connection.commit()
        print(f"Data for {symbol} saved to the database")

    except investpy.utils.exceptions.SymbolError:
        print(f"Symbol '{symbol}' not found or unavailable.")
    except investpy.utils.exceptions.ParseException:
        print(f"Failed to parse data for symbol '{symbol}'.")
    except Error as e:
        print(f"Failed to save data for {symbol}: {e}")

# List to store symbols
symbols = []

# Open the CSV file and extract symbols
with open(config.HISTORY_STOCK_DATA_FILE, newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip header row
    for row in reader:
        symbol = row[1]
        symbols.append(symbol)

# Fetch historical stock data for each symbol and save it to the database
for symbol in symbols:
    fetch_and_save_stock_data(symbol)

# Close the database connection
try:
    cursor.close()
    db_connection.close()
    print("Database connection closed")
except Error as e:
    print("Error closing database connection:", e)
