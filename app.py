from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

# Inicialização
app = Flask(__name__)

app.config["SECRET_KEY"] = "chave-teste"

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://root:@localhost/finance"
)
db = SQLAlchemy(app)

class Receita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.Date, nullable=False)

class Despesa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.Date, nullable=False)
    categoria = db.Column(db.String(50))

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/despesas")
def despesas():
    despesas = Despesa.query.all()
    return render_template("despesas.html", despesas=despesas)


def cadastro_despesas():
    pass

@app.route("/receitas")
def receitas():
   receitas = Receita.query.all()
   return render_template("receitas.html", receitas=receitas)


# Página sobre
@app.route("/sobre")
def sobre():
    return render_template("sobre.html")


# Cadastro de receitas
@app.route("/receitas/nova", methods=["GET", "POST"])
def cadastro_receitas():

    if request.method == "POST":
        descricao = request.form.get("descricao")
        valor_texto = request.form.get("valor")
        data = datetime.strptime(
            request.form.get("data"),
            "%Y-%m-%d"
        ).date()

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
        return redirect(url_for('receitas'))
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
            data = date(2026, 8, 8)
        ))
        db.session.add(Receita(
            descricao = "Freelance",
            valor = 450,
            data = date(2026, 8, 10)
        ))
        db.session.commit()

@app.route("/receita/<int:receita_id>")
def detalhe_receita(receita_id):
    receita = db.get_or_404(Receita, receita_id)
    return render_template("detalhe.html", receita=receita)

@app.route("/receita/<int:receita_id>/editar", methods=["GET", "POST"])
def editar_receita(receita_id):
    receita = db.get_or_404(Receita, receita_id)
    if request.method == "POST":
        receita.descricao = request.form.get("descricao", "").strip()
        receita.valor = float(request.form.get("valor", 0))
        receita.data = datetime.strptime(request.form.get("data"),"%Y-%m-%d").date()
        db.session.commit()
        flash("Receita atualizada com sucesso!", "sucesso")
        return redirect(url_for("receitas"))
    return render_template("editar.html", receita=receita)

@app.route("/receita/<int:receita_id>/remover", methods=["POST"])
def remover_receita(receita_id):
    receita = db.get_or_404(Receita, receita_id)
    db.session.delete(receita)
    db.session.commit()
    flash("Receita removida.", "sucesso")
    return redirect(url_for("receitas"))

# Executa o servidor
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        popular_banco()
    app.run(debug=True)

