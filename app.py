from flask import Flask, jsonify
import requests
import os


app = Flask(__name__)

# SEU ACCESS TOKEN AQUI
ACCESS_TOKEN = os.getenv('CONTA_AZUL_TOKEN')

HEADERS = {
    'Authorization': f'Bearer {ACCESS_TOKEN}'
}

# === FUNÇÃO ÚNICA PARA CONSULTAR ENDPOINTS ===
def consultar_api_contaazul(endpoint, params=None):
    base_url = 'https://api.contaazul.com/v1/'
    url = base_url + endpoint
    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({
            'erro': f'Erro ao acessar {endpoint}',
            'status': response.status_code,
            'detalhes': response.text
        }), 500

# === ROTAS FINANCEIRAS ===

@app.route('/lancamentos', methods=['GET'])
def lancamentos():
    return consultar_api_contaazul('financial_transactions', {'page': 1, 'size': 100})

@app.route('/receber', methods=['GET'])
def receber():
    return consultar_api_contaazul('receivables')

@app.route('/pagar', methods=['GET'])
def pagar():
    return consultar_api_contaazul('payables')

@app.route('/bancos', methods=['GET'])
def bancos():
    return consultar_api_contaazul('bank_accounts')

@app.route('/extrato', methods=['GET'])
def extrato():
    return consultar_api_contaazul('bank_transactions')

@app.route('/centros_custo', methods=['GET'])
def centros_custo():
    return consultar_api_contaazul('cost_centers')


if __name__ == '__main__':
    app.run(debug=True)
