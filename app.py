from flask import Flask, request, jsonify
from flask_cors import CORS
from message_trait import message_traitement
app = Flask(__name__)

# Enable CORS for all origins (adjust for production)
CORS(app)  # Consider using specific origins for production

# Simulated database for storing messages
messages = []

@app.route('/messages', methods=['GET', 'POST'])
def handle_messages():
    if request.method == 'POST':
        # Process message (send message)
        data = request.get_json()
        message_text = data.get('message')

        if message_text:
            # Simulate message processing (replace with your logic)
            processed_message =message_traitement(message_text)

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
