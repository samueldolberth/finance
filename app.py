from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

# Inicialização
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://root:@localhost/finance"
)
db = SQLAlchemy(app)

class Receita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)

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
        valor_texto = request.form.get("valor")
        data = datetime.strptime(
            request.form.get("data"),
            "%Y-%m-%d"
        )

        erros = []
        if not descricao:
            erros.append("A descrição é obrigatoria.")

        valor = None
        try:
            valor = float(valor_texto)
            if valor <= 0:
                erros.append("O valor tem que ser maior que zero.")
        except ValueError:
            erros.append("Valor inválido.")

        if erros:
            for erro in erros:
                flash(erro, "Erro")
            return render_template("nova_receita.html")

        nova_receita = Receita(
            descricao = descricao,
            valor = valor,
            data = data
        )
        db.session.add(nova_receita)
        db.session.commit()
        flash("Receita cadastrada com sucesso!", "sucesso")
        return redirect(url_for("dashboard"))
    return render_template("nova_receita.html")

def popular_banco():
    if Receita.query.count() == 0:
        db.session.add(Receita(
            descricao = "Salário",
            valor = 1990,
            data = date(2026, 8, 5)
        ))
        db.session.add(Receita(
            descricao = "Vale Refeição",
            valor = 200,
            data = date=(2026, 8, 8)
        ))
        db.session.add(Receita(
            descricao = "Freelance",
            valor = 450,
            data = date(2026, 8, 10)
        ))


# Executa o servidor
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        popular_banco()
    app.run(debug=True)

