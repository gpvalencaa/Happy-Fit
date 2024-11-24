from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import os

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# Caminho para o arquivo JSON
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_JSON = os.path.join(BASE_DIR, "backend", "dados_usuarios.json")

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

# Rota para a página inicial
@app.route('/')
def home():
    return render_template('index.html')  # Página inicial

# Rota para cadastrar usuário
@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar_usuario():
    if request.method == 'POST':
        # Captura os dados enviados pelo formulário
        dados_recebidos = request.form  # Captura os dados do formulário (não via JSON)
        nome = dados_recebidos.get('nome')
        email = dados_recebidos.get('email')
        senha = dados_recebidos.get('senha')
        data_nascimento = dados_recebidos.get('data_nascimento')
        altura = dados_recebidos.get('altura')
        sexo = dados_recebidos.get('sexo')

        # Valida campos obrigatórios
        campos_obrigatorios = ['nome', 'email', 'senha', 'data_nascimento', 'altura', 'sexo']
        for campo in campos_obrigatorios:
            if not locals().get(campo):  # Verifica se o campo foi preenchido
                return jsonify({"mensagem": f"Campo '{campo}' é obrigatório."}), 400

        usuarios = ler_dados()  # Carrega usuários existentes

        # Verifica se o email já está cadastrado
        if any(usuario['email'] == email for usuario in usuarios):
            return jsonify({"mensagem": "E-mail já cadastrado."}), 409

        novo_usuario = {
            "nome": nome,
            "email": email,
            "senha": senha,
            "data_nascimento": data_nascimento,
            "altura": altura,
            "sexo": sexo,
        }
        usuarios.append(novo_usuario)  # Adiciona o novo usuário
        salvar_dados(usuarios)  # Salva no arquivo JSON
        return jsonify({"mensagem": "Cadastro realizado com sucesso!"}), 201

    elif request.method == 'GET':
        # Exibe o formulário HTML de cadastro
        return render_template('cadastro.html')  # Página de cadastro

# Rota para listar todos os usuários
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = ler_dados()
    return jsonify(usuarios)

# Rota para login
@app.route('/login', methods=['GET', 'POST'])
def validar_login():
    if request.method == 'POST':
        # Lógica de login com POST (dados enviados pelo formulário)
        dados_recebidos = request.json  # Dados enviados do frontend
        if not dados_recebidos:
            return jsonify({"mensagem": "Dados não fornecidos."}), 400

        email = dados_recebidos.get('email')
        senha = dados_recebidos.get('senha')

        if not email or not senha:
            return jsonify({"mensagem": "E-mail e senha são obrigatórios."}), 400

        usuarios = ler_dados()  # Carrega usuários cadastrados

        # Busca o usuário pelo e-mail e senha
        for usuario in usuarios:
            if usuario.get('email') == email and usuario.get('senha') == senha:
                return jsonify({"mensagem": "Login realizado com sucesso!"}), 200

        return jsonify({"mensagem": "E-mail ou senha inválidos."}), 401

    elif request.method == 'GET':
        # Aqui você pode renderizar a página de login com o formulário HTML
        return render_template('login.html')  # Retorna a página de login

@app.route('/home', methods=['GET'])
def tela_inicial():
    return render_template('home.html')  # Página de cadastro

if __name__ == '__main__':
    app.run(debug=True)
