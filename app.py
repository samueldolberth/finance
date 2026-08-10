from flask import Flask, jsonify

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

if __name__ == '__main__':
    app.run(debug=True)