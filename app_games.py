# app_games.py

# INSTALANDO A APLICAÇÃO:
# python3 -m venv venv
# source venv/bin/activate
# pip install flask flask-cors

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

# Garante que o JSON não use ASCII, permitindo acentos
app.config["JSON_AS_ASCII"] = False

# Habilita o CORS para que nosso frontend possa se comunicar com a API
CORS(app)

# Nosso "Banco de Dados" em memória para a coleção de jogos
jogos = [
    {
        "id": 1,
        "titulo": "Chrono Trigger",
        "console": "SNES",
        "ano_lancamento": 1995,
        "genero": "RPG"
    },
    {
        "id": 2,
        "titulo": "Sonic the Hedgehog 2",
        "console": "Mega Drive",
        "ano_lancamento": 1992,
        "genero": "Plataforma"
    },
    {
        "id": 3,
        "titulo": "Street Fighter II",
        "console": "Arcade",
        "ano_lancamento": 1991,
        "genero": "Luta"
    }
]

# --- ROTAS DA API ---

# GET - Listar todos os jogos
@app.route("/jogos", methods=["GET"])
def get_jogos():
    return jsonify(jogos)

# GET - Buscar um jogo pelo ID
@app.route("/jogos/<int:jogo_id>", methods=["GET"])
def get_jogo_por_id(jogo_id):
    # Usando a mesma lógica eficiente do seu exemplo para encontrar o item
    jogo = next((j for j in jogos if j["id"] == jogo_id), None)
    if jogo:
        return jsonify(jogo)
    return jsonify({"error": "Jogo não encontrado"}), 404

# POST - Criar um novo jogo
@app.route("/jogos", methods=["POST"])
def create_jogo():
    data = request.get_json()

    # Lógica simples para gerar um novo ID
    novo_id = max([j['id'] for j in jogos]) + 1 if jogos else 1
    
    novo_jogo = {
        "id": novo_id,
        "titulo": data['titulo'],
        "console": data['console'],
        "ano_lancamento": data['ano_lancamento'],
        "genero": data['genero']
    }
    
    jogos.append(novo_jogo)
    return jsonify(novo_jogo), 201  # 201 Created

# PUT - Atualizar um jogo existente
@app.route("/jogos/<int:jogo_id>", methods=["PUT"])
def update_jogo(jogo_id):
    data = request.get_json()
    for jogo in jogos:
        if jogo["id"] == jogo_id:
            jogo.update(data)
            return jsonify(jogo)
    return jsonify({"error": "Jogo não encontrado"}), 404

# DELETE - Remover um jogo
@app.route("/jogos/<int:jogo_id>", methods=["DELETE"])
def delete_jogo(jogo_id):
    global jogos
    tamanho_antes = len(jogos)
    # Recria a lista sem o jogo a ser deletado
    jogos = [j for j in jogos if j["id"] != jogo_id]
    
    if len(jogos) == tamanho_antes:
        return jsonify({"error": "Jogo não encontrado"}), 404
        
    return jsonify({"msg": f"Jogo {jogo_id} removido com sucesso"})

# Inicia o servidor
if __name__ == "__main__":
    app.run(debug=True, port=3344)