from flask import Flask, request

# inicializaçãp
app = Flask(__name__)

receitas = [
    {"id": 1, "nome": ""}
]

@app.route("/")
def index():
    return "Bem vindo ao FINANCE"

@app.route("/sobre")
def sobre():
    return "Página Sobre"

@app.route("/novo", methods=["GET", "POST"])
def novo():
    if request.method == "POST":
        return "Dados recebidos (em construção)"
    return "Formunlário de cadastro (em construção)"

if __name__ == "__main__":
    app.run(debug=True)