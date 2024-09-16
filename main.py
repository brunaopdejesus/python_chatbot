import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Rota para lidar com as requisições do webhook
@app.route('/', methods=['GET'])
def home():
    return "OK", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    # Verifica se há uma callback_query do Telegram
    if 'callback_query' in req:
        callback_data = req['callback_query']['data']
        
        # Processar o callback_data dos botões do Telegram
        if callback_data == 'opcao_1':
            response_text = "Você escolheu a Opção 1."
        elif callback_data == 'opcao_2':
            response_text = "Você escolheu a Opção 2."
        else:
            response_text = "Desculpe, não entendi sua escolha."

        # Enviar resposta de volta para o Telegram
        return jsonify({
            "method": "sendMessage",
            "chat_id": req['callback_query']['from']['id'],
            "text": response_text
        })
    
    # Processar intents do Dialogflow, caso não seja callback do Telegram
    intent_name = req.get('queryResult').get('intent').get('displayName')
    
    if intent_name == 'Opção 1 Intent':
        response_text = "Você escolheu a Opção 1."
    elif intent_name == 'Opção 2 Intent':
        response_text = "Você escolheu a Opção 2."
    else:
        response_text = "Desculpe, não entendi sua escolha."

    return make_webhook_response(response_text)

# Função para criar a resposta no formato aceito pelo Dialogflow
def make_webhook_response(text):
    return jsonify({
        "fulfillmentText": text,
        "source": "webhook"
    })

if __name__ == '__main__':
    # Pegar a porta da variável de ambiente ou usar 5000 como padrão
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
