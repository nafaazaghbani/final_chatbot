import json
from groq import Groq
from get_hist_stock_data import fetch_stock_data
from datetime import date

client = Groq(api_key='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')
MODEL = 'llama3-70b-8192'
today = date.today()


# dd/mm/YY
def run_conversation(user_prompt):
    messages = [
        {
            "role": "system",
            "content": f"You are an assistant in exchange website that do a function calling LLM that uses the data extracted from the get_stock_data function to answer questions around stock data withthout saying that you use a function."
        },
        {
            "role": "user",
            "content": user_prompt,
        }
    ]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "fetch_stock_data",
                "description": "Get the data about a symbol",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "description": "data about symbol  ",
                        },
                        "date1": {
                            "type": "string",
                            "description": "The start date for the historical data and can be none "
                        },
                        "date2": {
                            "type": "string",
                            "description": "The end date for the historical data in and can be none "
                        }
                    },
                    "required": ["symbol"],
                },
            },
        }
    ]
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        max_tokens=4096
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    if tool_calls:
        available_functions = {
            "fetch_stock_data": fetch_stock_data,
        }
        messages.append(response_message)
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)

            function_response = function_to_call(
                symbol=function_args.get("symbol"),
                date1=function_args.get("date1"),
                date2=function_args.get("date2")

            )

            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )
        second_response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )
        return second_response.choices[0].message.content