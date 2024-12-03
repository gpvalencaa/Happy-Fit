# from flask import Flask, redirect, request, jsonify, render_template
# from flask_cors import CORS
# import json
# import os

# app = Flask(__name__, template_folder="templates", static_folder="static")
# CORS(app)

# # Caminho para o arquivo JSON
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# ARQUIVO_JSON = os.path.join(BASE_DIR, "backend", "dados_usuarios.json")

# # Função para ler os dados do arquivo JSON
# def ler_dados():
#     if not os.path.exists(ARQUIVO_JSON):
#         return []  # Retorna lista vazia se o arquivo não existir
#     if os.path.getsize(ARQUIVO_JSON) == 0:  # Verifica se o arquivo está vazio
#         return []  # Retorna lista vazia se o arquivo estiver vazio
#     with open(ARQUIVO_JSON, 'r') as arquivo:
#         return json.load(arquivo)
    
# # Função para salvar os dados no arquivo JSON
# def salvar_dados(dados):
#     with open(ARQUIVO_JSON, 'w') as arquivo:
#         json.dump(dados, arquivo, indent=4)

# # Rota para a página inicial
# @app.route('/')
# def home():
#     return render_template('index.html')  # Página inicial

# # Rota para cadastrar usuário
# @app.route('/cadastrar', methods=['GET', 'POST'])
# def cadastrar_usuario():
#     if request.method == 'POST':
#         # Captura os dados enviados pelo formulário
#         dados_recebidos = request.form  # Captura os dados do formulário (não via JSON)
#         nome = dados_recebidos.get('nome')
#         email = dados_recebidos.get('email')
#         senha = dados_recebidos.get('senha')
#         data_nascimento = dados_recebidos.get('data_nascimento')
#         altura = dados_recebidos.get('altura')
#         sexo = dados_recebidos.get('sexo')

#         # Valida campos obrigatórios
#         campos_obrigatorios = ['nome', 'email', 'senha', 'data_nascimento', 'altura', 'sexo']
#         for campo in campos_obrigatorios:
#             if not locals().get(campo):  # Verifica se o campo foi preenchido
#                 return jsonify({"mensagem": f"Campo '{campo}' é obrigatório."}), 400

#         usuarios = ler_dados()  # Carrega usuários existentes

#         # Verifica se o email já está cadastrado
#         if any(usuario['email'] == email for usuario in usuarios):
#             return jsonify({"mensagem": "E-mail já cadastrado."}), 409

#         # Gera um ID autoincremental
#         if usuarios:
#             novo_id = max(usuario['id'] for usuario in usuarios) + 1
#         else:
#             novo_id = 1

#         novo_usuario = {
#             "id": novo_id,
#             "nome": nome,
#             "email": email,
#             "senha": senha,
#             "data_nascimento": data_nascimento,
#             "altura": altura,
#             "sexo": sexo,
#             "nivel": 1,
#             "pontos": 0,
#             "ossos": 500
#         }
#         usuarios.append(novo_usuario)  # Adiciona o novo usuário
#         salvar_dados(usuarios)  # Salva no arquivo JSON
#         return jsonify({"mensagem": "Cadastro realizado com sucesso!"}), 201

#     elif request.method == 'GET':
#         # Exibe o formulário HTML de cadastro
#         return render_template('cadastro.html')  # Página de cadastro

# # Rota para listar todos os usuários
# @app.route('/usuarios', methods=['GET'])
# def listar_usuarios():
#     usuarios = ler_dados()
#     return jsonify(usuarios)

# @app.route('/usuarios/<int:usuario_id>', methods=['GET'])
# def obter_usuario(usuario_id):
#     usuarios = ler_dados()
#     # Procure o usuário pelo ID
#     usuario = next((u for u in usuarios if u['id'] == usuario_id), None)
#     if usuario is not None:
#         return jsonify(usuario), 200  # Retorne o usuário encontrado
#     return jsonify({'erro': 'Usuário não encontrado'}), 404  # Retorne 404 se não encontrado

# # Rota para login
# @app.route('/login', methods=['GET', 'POST'])
# def validar_login():
#     if request.method == 'POST':
#         # Lógica de login com POST (dados enviados pelo formulário)
#         dados_recebidos = request.json  # Dados enviados do frontend
#         if not dados_recebidos:
#             return jsonify({"mensagem": "Dados não fornecidos."}), 400

#         email = dados_recebidos.get('email')
#         senha = dados_recebidos.get('senha')

#         if not email or not senha:
#             return jsonify({"mensagem": "E-mail e senha são obrigatórios."}), 400

#         usuarios = ler_dados()  # Carrega usuários cadastrados

#         # Busca o usuário pelo e-mail e senha
#         for usuario in usuarios:
#             if usuario.get('email') == email and usuario.get('senha') == senha:
#                 redirect(f"/home/{usuario['id']}")
#                 return jsonify({"mensagem": "Login bem-sucedido!", "id": usuario['id']}), 200

#         return jsonify({"mensagem": "E-mail ou senha inválidos."}), 401

#     elif request.method == 'GET':
#         # Aqui você pode renderizar a página de login com o formulário HTML
#         return render_template('login.html')  # Retorna a página de login

# @app.route('/home/<int:userId>')
# def home(userId):
#     return render_template('home.html', userId=userId)


# @app.route('/home', methods=['GET'])
# def tela_inicial():
#     return render_template('home.html')

# @app.route('/metas', methods=['GET'])
# def tela_metas():
#     return render_template('metas.html')

# @app.route('/progresso', methods=['GET'])
# def tela_progresso():
#     return render_template('progresso.html')

# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, redirect, request, jsonify, render_template, url_for
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
        return []
    if os.path.getsize(ARQUIVO_JSON) == 0:
        return []
    with open(ARQUIVO_JSON, 'r') as arquivo:
        return json.load(arquivo)

# Função para salvar os dados no arquivo JSON
def salvar_dados(dados):
    with open(ARQUIVO_JSON, 'w') as arquivo:
        json.dump(dados, arquivo, indent=4)

# Rota para a página inicial
@app.route('/')
def home():
    return render_template('index.html')

# Rota para cadastrar usuário
@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar_usuario():
    if request.method == 'POST':
        dados_recebidos = request.form
        nome = dados_recebidos.get('nome')
        email = dados_recebidos.get('email')
        senha = dados_recebidos.get('senha')
        data_nascimento = dados_recebidos.get('data_nascimento')
        altura = dados_recebidos.get('altura')
        sexo = dados_recebidos.get('sexo')
        etnia = dados_recebidos.get('sexo')
        peso = dados_recebidos.get('peso')

        campos_obrigatorios = ['nome', 'email', 'senha', 'data_nascimento', 'altura', 'sexo', 'peso']
        for campo in campos_obrigatorios:
            if not locals().get(campo):
                return jsonify({"mensagem": f"Campo '{campo}' é obrigatório."}), 400

        usuarios = ler_dados()

        if any(usuario['email'] == email for usuario in usuarios):
            return jsonify({"mensagem": "E-mail já cadastrado."}), 409

        novo_id = max(usuario['id'] for usuario in usuarios) + 1 if usuarios else 1

        novo_usuario = {
            "id": novo_id,
            "nome": nome,
            "email": email,
            "senha": senha,
            "data_nascimento": data_nascimento,
            "altura": altura,
            "sexo": sexo,
            "nivel": 1,
            "pontos": 0,
            'etnia': etnia,
            'peso': int(peso),
            'missao1': False,
            'missao2': False,
            'missao3': False,
            'missao4': False,
            'missao5': False,
            
        }
        usuarios.append(novo_usuario)
        salvar_dados(usuarios)
        return render_template('index.html')

    return render_template('cadastro.html')

# Rota para listar todos os usuários
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = ler_dados()
    return jsonify(usuarios)

@app.route('/usuarios/<int:usuario_id>', methods=['GET'])
def obter_usuario(usuario_id):
    usuarios = ler_dados()
    usuario = next((u for u in usuarios if u['id'] == usuario_id), None)
    if usuario:
        return jsonify(usuario), 200
    return jsonify({'erro': 'Usuário não encontrado'}), 404

@app.route('/login', methods=['GET', 'POST'])
def validar_login():
    if request.method == 'POST':
        # Lógica de login com POST
        dados_recebidos = request.json
        if not dados_recebidos:
            return jsonify({"mensagem": "Dados não fornecidos."}), 400

        email = dados_recebidos.get('email')
        senha = dados_recebidos.get('senha')

        if not email or not senha:
            return jsonify({"mensagem": "E-mail e senha são obrigatórios."}), 400

        usuarios = ler_dados()

        # Busca o usuário pelo e-mail e senha
        for usuario in usuarios:
            if usuario.get('email') == email and usuario.get('senha') == senha:
                return jsonify({"mensagem": "Login bem-sucedido!", "id": usuario['id']}), 200

        return jsonify({"mensagem": "E-mail ou senha inválidos."}), 401

    elif request.method == 'GET':
        # Exibe a página de login
        return render_template('login.html')

# Carrega os dados dos usuários a partir de um arquivo JSON
def carregar_usuarios():
    with open(ARQUIVO_JSON, 'r') as f:
        return json.load(f)

# Atualiza o arquivo JSON com os dados modificados
def salvar_usuarios(usuarios):
    with open(ARQUIVO_JSON, 'w') as f:
        json.dump(usuarios, f, indent=4)

@app.route('/usuarios/<int:usuario_id>', methods=['PUT'])
def atualizar_usuario(usuario_id):
    usuarios = carregar_usuarios()  # Carrega a lista de usuários do arquivo JSON
    usuario = next((u for u in usuarios if u['id'] == usuario_id), None)
    
    if not usuario:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    dados = request.get_json()

    # Atualiza os campos do usuário com os dados recebidos
    usuario.update(dados)

    # Salva os dados atualizados no arquivo JSON
    salvar_usuarios(usuarios)

    return jsonify(usuario), 200


# # Rota para login
# @app.route('/login', methods=['POST'])
# def validar_login():
#     dados_recebidos = request.json
#     if not dados_recebidos:
#         return jsonify({"mensagem": "Dados não fornecidos."}), 400

#     email = dados_recebidos.get('email')
#     senha = dados_recebidos.get('senha')

#     if not email or not senha:
#         return jsonify({"mensagem": "E-mail e senha são obrigatórios."}), 400

#     usuarios = ler_dados()

#     for usuario in usuarios:
#         if usuario.get('email') == email and usuario.get('senha') == senha:
#             return jsonify({"mensagem": "Login bem-sucedido!", "id": usuario['id']}), 200

#     return jsonify({"mensagem": "E-mail ou senha inválidos."}), 401

@app.route('/usuarios/<int:user_id>/missao', methods=['POST'])
def concluir_missao(user_id):
    usuarios = carregar_usuarios()  # Carrega a lista de usuários do arquivo JSON
    data = request.json
    missao = data.get("missao")
    
    # Encontra o usuário com o ID fornecido
    user = next((u for u in usuarios if u["id"] == user_id), None)
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    # Verifica se a missão foi fornecida e se ela é válida
    if missao and missao in user:
        user[missao] = True 
        # Exemplo: Adiciona pontos ao concluir a missão (se necessário)
        # user["pontos"] += 300 
        
        # Salva os dados atualizados no arquivo JSON
        salvar_usuarios(usuarios)

        return jsonify(user), 200
    
    return jsonify({"error": "Missão inválida"}), 400


# Rota para a home do usuário
@app.route('/home/<int:user_id>')
def home_usuario(user_id):
    return render_template('home.html', userId=user_id)

# Rotas adicionais
@app.route('/metas', methods=['GET'])
def tela_metas():
    return render_template('metas.html')

@app.route('/progresso', methods=['GET'])
def tela_progresso():
    return render_template('progresso.html')

if __name__ == '__main__':
    app.run(debug=True)
