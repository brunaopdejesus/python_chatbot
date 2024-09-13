from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "OK", 200

# Rota para lidar com as requisições do webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    
    # Processar a intent recebida
    intent_name = req.get('queryResult').get('intent').get('displayName')
    
    # Tratamento baseado no nome da intent
    if intent_name == 'Opção 1 Intent':
        response_text = "Você escolheu a Opção 1."
    elif intent_name == 'Opção 2 Intent':
        response_text = "Você escolheu a Opção 2."
    else:
        response_text = "Desculpe, não entendi sua escolha."

    # Montar a resposta para o Dialogflow
    return make_webhook_response(response_text)

# Função para criar a resposta no formato aceito pelo Dialogflow
def make_webhook_response(text):
    return jsonify({
        "fulfillmentText": text,
        "source": "webhook"
    })

if __name__ == '__main__':
    # Iniciar o servidor Flask
    app.run(port=5000, debug=True)
