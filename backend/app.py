from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# Caminho para o arquivo JSON
ARQUIVO_JSON = os.path.join("backend", "dados_usuarios.json")

# Função para ler os dados do arquivo JSON
def ler_dados():
    if not os.path.exists(ARQUIVO_JSON):
        return []  # Retorna lista vazia se o arquivo não existir
    with open(ARQUIVO_JSON, 'r') as arquivo:
        return json.load(arquivo)

# Função para salvar os dados no arquivo JSON
def salvar_dados(dados):
    with open(ARQUIVO_JSON, 'w') as arquivo:
        json.dump(dados, arquivo, indent=4)

# Rota para cadastrar usuário
@app.route('/cadastrar', methods=['POST'])
def cadastrar_usuario():
    dados_recebidos = request.json  # Dados enviados do frontend
    usuarios = ler_dados()         # Carrega usuários existentes
    usuarios.append(dados_recebidos)  # Adiciona o novo usuário
    salvar_dados(usuarios)         # Salva no arquivo JSON
    return jsonify({"mensagem": "Cadastro realizado com sucesso!"}), 201

# Rota para listar todos os usuários
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = ler_dados()
    return jsonify(usuarios)



@app.route('/login', methods=['POST'])
def validar_login():
    dados_recebidos = request.json  # Dados do login enviados pelo frontend
    usuarios = ler_dados()         # Carrega usuários cadastrados

    # Busca o usuário pelo e-mail e senha
    for usuario in usuarios:
        if usuario['email'] == dados_recebidos['email'] and usuario['senha'] == dados_recebidos['senha']:
            return jsonify({"mensagem": "Login realizado com sucesso!"}), 200
    
    # Retorna erro se as credenciais não forem encontradas
    return jsonify({"mensagem": "E-mail ou senha inválidos."}), 401

if __name__ == '__main__':
    app.run(debug=True)
