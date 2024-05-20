from flask import Flask, request, jsonify
from flask_cors import CORS
import config
from stock_data_fetcher import StockService
from ChoiceSelector import choice
from model_fn_call_stock_data import run_conversation
from message_trait import message_traitement
from model_fn_call_fortes import get_hausses_baisses
import stock_info_retriever

app = Flask(__name__)
CORS(app)

# Simulated database for storing messages
messages = []

def message_traitement(message):
    stock_service = StockService(config.BASE_URL)
    token = stock_service.login("22015595", "1")
    stock_check = stock_info_retriever.extract_stock_info(message)

    if stock_check[0]:
        message = message.replace(" ", "")
        if (message.lower() == (stock_check[0][0]).lower() and len(message.lower()) == len((stock_check[0][0]).lower())) or (message.lower() == (stock_check[0][0]).lower() and len(message.lower()) == len((stock_check[1][0]).lower())):
            response = stock_service.get_stock_by_symbol(token, int(stock_check[2][0]), str(stock_check[1][0]))
            return response
        else:
            response = run_conversation(message)
            return str(response)
    else:
        choice_selected = choice(message)
        if choice_selected == "general finance question":
            return "q/a"  # yassine code
        elif choice_selected == "FORTES":
            response = get_hausses_baisses(message)
            return response
    

@app.route('/messages', methods=['GET', 'POST'])
def handle_messages():
    if request.method == 'POST':
        data = request.get_json()
        message_text = data.get('message')

        if message_text:
            processed_message = message_traitement(message_text)
            # Append the processed message to the messages list
            messages.append({'text': processed_message, 'type': 'received'})
            return jsonify({'processed_message': processed_message})
        else:
            return jsonify({'error': 'No message provided'}), 400

    elif request.method == 'GET':
        # Fetch messages
        return jsonify({'processed_messages': messages})

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
