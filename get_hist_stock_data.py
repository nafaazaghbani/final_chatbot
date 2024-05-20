import json
import mysql.connector
from datetime import date

from dateutil.parser import parse as parse_date
from mysql.connector import Error
from config import DB_CONFIG
import stock_info_retriever
import config
from stock_data_fetcher import StockService



def connect_to_database():
    """Establishes a connection to the MySQL database."""
    try:
        db_connection = mysql.connector.connect(**DB_CONFIG)
        #print("Connected to the database")
        return db_connection
    except Error as e:
        #print("Error connecting to MySQL database:", e)
        return None

def fetch_stock_data(symbol, date1=None, date2=None):
    """
    Retrieve historical stock data from the MySQL database for a specific stock symbol and date range.

    Args:
    - symbol (str): The stock symbol.
    - date1 (str): The start date for the historical data.
    - date2 (str): The end date for the historical data.

    Returns:
    - dict: Historical stock data.
    """
    today = date.today()

    # dd/mm/YY
    current = today.strftime("%d/%m/%Y")
    db_connection = connect_to_database()
    if db_connection is None:
        return None

    cursor = db_connection.cursor(dictionary=True)

    try:
        if date2 == None:
            date2 = date1

        # Parse dates if provided
        if date1:
            date1 = parse_date(date1).date()
        if date2:
            date2 = parse_date(date2).date()

        # Query the database for historical stock data for the specified symbol and date range
        select_query = """
        SELECT date, open, high, low, close, volume
        FROM stock_data
        WHERE symbol = %s 
            AND (date >= %s OR %s IS NULL) 
            AND (date <= %s OR %s IS NULL)
        """
        cursor.execute(select_query, (symbol, date1, date1, date2, date2))
        rows = cursor.fetchall()

        if not rows:
            return(f"No data found for symbol '{symbol}' ")

        # Convert retrieved data to dictionary
        stock_data = {}
        for row in rows:
            date_str = row['date'].strftime('%Y-%m-%d')
            stock_data[date_str] = {
                'Open': row['open'],
                'High': row['high'],
                'Low': row['low'],
                'Close': row['close'],
                'Volume': row['volume'],
                'Currency': 'TND'  # Assuming currency is always Tunisian Dinar
            }
        json_string = json.dumps(stock_data)
        return json_string

    except Error as e:
        print(f"Error retrieving data: {e}")
        return None

    finally:
        cursor.close()
        db_connection.close()


