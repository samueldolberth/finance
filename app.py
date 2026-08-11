from flask import Flask, jsonify, request

app = Flask(__name__)

receitas = [
    {
        "id": 1,
        "descricao": "Salario",
        "valor": 2500.00
    },
    {
        "id": 2,
        "descricao": "Freelance",
        "valor": 500.00
    }
]

@app.route('/receitas', methods=['GET'])
def get_receitas():
    return jsonify(receitas)

@app.route('/receitas', methods=['POST'])
def adicionar_receita():
    dados = request.get_json()

    nova_receita = {
        "id": len(receitas) + 1,
        "descricao": dados["descricao"],
        "valor": dados["valor"]
    }

    receitas.append(nova_receita)

    return jsonify(nova_receita), 201

if __name__ == '__main__':
    app.run(debug=True)