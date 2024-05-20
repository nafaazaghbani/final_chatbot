import ChoiceSelector
import config
import stock_data_fetcher
from stock_data_fetcher import StockService
import stock_info_retriever
from ChoiceSelector import choice
from model_fn_call_stock_data import run_conversation
from model_fn_call_fortes import get_hausses_baisses
#Login to obtain access token

def message_traitement(message):
    stock_service = StockService(config.BASE_URL)

    token = stock_service.login("22015595", "1")

    stock_check=stock_info_retriever.extract_stock_info(message)

    if stock_check[0] :
        message=message.replace(" ","")
        if (message.lower() == (stock_check[0][0]).lower()and len(message.lower()) == len((stock_check[0][0]).lower())) or ( message.lower() == (stock_check[0][0]).lower()and len(message.lower()) == len((stock_check[1][0]).lower())):

            response=stock_service.get_stock_by_symbol(token,int(stock_check[2][0]),str(stock_check[1][0]))

            return (str(response) + '  TND')

        else :
            response=run_conversation(message)
            return response
    else :
          choice_selected=choice(message)
          if choice_selected=="general finance question":
              return ("q/a")#yassine code
          elif choice_selected=="FORTES":
              response=get_hausses_baisses(message)

