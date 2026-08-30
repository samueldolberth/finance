
from flask import Flask, request, render_template

# Inicialização
app = Flask(__name__)

# Lista temporária de receitas
lista_receitas = [
    {
        "id": 1,
        "descricao": "Salário",
        "valor": 1990,
        "data": "05/08/2026"
    },
    {
        "id": 2,
        "descricao": "Vale Refeição",
        "valor": 200,
        "data": "08/08/2026"
    },
    {
        "id": 3,
        "descricao": "Freelance",
        "valor": 450,
        "data": "10/08/2026"
    },
    {
        "id": 4,
        "descricao": "Venda de produto",
        "valor": 180,
        "data": "12/08/2026"
    },
    {
        "id": 5,
        "descricao": "Bônus",
        "valor": 300,
        "data": "15/08/2026"
    },
    {
        "id": 6,
        "descricao": "Hora extra",
        "valor": 250,
        "data": "18/08/2026"
    },
    {
        "id": 7,
        "descricao": "Rendimento",
        "valor": 120,
        "data": "20/08/2026"
    },
    {
        "id": 8,
        "descricao": "Comissão",
        "valor": 350,
        "data": "25/08/2026"
    }
]



# Página inicial
@app.route("/")
def dashboard():
    return render_template("dashboard.html", receitas=lista_receitas)


# Página sobre
@app.route("/sobre")
def sobre():
    return render_template("sobre.html")


# Cadastro de receitas
@app.route("/receitas", methods=["GET", "POST"])
def cadastro_receitas():

    if request.method == "POST":
        descricao = request.form.get("descricao")
        valor = request.form.get("valor")
        data = request.form.get("data")

        return f"Receita recebida: {descricao} - R$ {valor} - {data}"

    return render_template("receitas.html")


# Executa o servidor
if __name__ == "__main__":
    app.run(debug=True)