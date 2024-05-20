import stock_data_fetcher
from stock_data_fetcher import StockService
import json
from groq import Groq
from get_hist_stock_data import fetch_stock_data
import config
stock_service= StockService(config.BASE_URL)


client = Groq(api_key='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')
MODEL = 'llama3-8b-8192'
#Login to obtain access token
def get_hausses_baisses(message):
    token = stock_service.login("22015595", "1")

    Hausses=stock_service.get_palmares_hausse(token)
    Baisses=stock_service.get_palmares_baisse(token)
    Hausses=Hausses['content']
    client = Groq(
        api_key='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',
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"answer these question {message} based on this contexts: {Hausses}(represent the highest stock ),and {Baisses}(represent the lowest stock )i a simple way without indicating too much deatil (reformualte)",
            }
        ],
        model="llama3-8b-8192",
    )

    response=(chat_completion.choices[0].message.content)
    return response


