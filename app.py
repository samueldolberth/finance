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

    total_receitas = db.session.query(
        db.func.sum(Receita.valor)
    ).scalar() or 0

    total_despesas = db.session.query(
        db.func.sum(Despesa.valor)
    ).scalar() or 0

    saldo = total_receitas - total_despesas

    quantidade_receitas = Receita.query.count()
    quantidade_despesas = Despesa.query.count()

    ultimas_receitas = Receita.query.order_by(
        Receita.data.desc()
    ).limit(5).all()

    ultimas_despesas = Despesa.query.order_by(
        Despesa.data.desc()
    ).limit(5).all()

    # Despesas agrupadas por categoria
    despesas_categoria = db.session.query(
        Despesa.categoria,
        db.func.sum(Despesa.valor)
    ).group_by(
        Despesa.categoria
    ).all()

    categorias = [
        item[0] for item in despesas_categoria
    ]

    valores_categorias = [
        float(item[1]) for item in despesas_categoria
    ]

    return render_template(
        "dashboard.html",
        total_receitas=total_receitas,
        total_despesas=total_despesas,
        saldo=saldo,
        quantidade_receitas=quantidade_receitas,
        quantidade_despesas=quantidade_despesas,
        ultimas_receitas=ultimas_receitas,
        ultimas_despesas=ultimas_despesas,
        categorias=categorias,
        valores_categorias=valores_categorias
    )


@app.route("/despesas")
def despesas():
    despesas = Despesa.query.all()
    return render_template("despesas.html", despesas=despesas)

@app.route("/despesas/nova", methods=["GET", "POST"])
def cadastro_despesas():
    if request.method == "POST":
        descricao = request.form.get("descricao", "").strip()
        valor_texto = request.form.get("valor")
        data_texto = request.form.get("data")
        categoria = request.form.get("categoria", "").strip()

        erros = []

        if not descricao:
            erros.append("A descrição é obrigatória.")

        valor = None
        try:
            valor = float(valor_texto)
            if valor <= 0:
                erros.append("O valor deve ser maior que zero.")
        except (ValueError, TypeError):
            erros.append("Valor inválido.")

        data = None
        try:
            data = datetime.strptime(data_texto, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            erros.append("Data inválida.")

        if not categoria:
            erros.append("A categoria é obrigatória.")

        if erros:
            for erro in erros:
                flash(erro, "erro")

            return render_template("nova_despesa.html")

        nova_despesa = Despesa(
            descricao=descricao,
            valor=valor,
            data=data,
            categoria=categoria
        )

        db.session.add(nova_despesa)
        db.session.commit()

        flash("Despesa cadastrada com sucesso!", "sucesso")

        return redirect(url_for("despesas"))
    
    return render_template("nova_despesa.html")

@app.route("/despesa/<int:despesa_id>")
def detalhe_despesa(despesa_id):
    despesa = db.get_or_404(Despesa, despesa_id)
    return render_template("detalhe_despesa.html", despesa=despesa)



@app.route("/despesa/<int:despesa_id>/remover", methods=["POST"])
def remover_despesa(despesa_id):

    despesa = db.get_or_404(Despesa, despesa_id)

    db.session.delete(despesa)
    db.session.commit()

    flash("Despesa removida.", "sucesso")

    return redirect(url_for("despesas"))

@app.route("/receitas")
def receitas():
   receitas = Receita.query.all()
   return render_template("receitas.html", receitas=receitas)

@app.route("/despesa/<int:despesa_id>/editar", methods=["GET", "POST"])
def editar_despesa(despesa_id):

    despesa = db.get_or_404(Despesa, despesa_id)

    if request.method == "POST":

        despesa.descricao = request.form.get(
            "descricao", ""
        ).strip()

        despesa.valor = float(
            request.form.get("valor", 0)
        )

        despesa.data = datetime.strptime(
            request.form.get("data"),
            "%Y-%m-%d"
        ).date()

        despesa.categoria = request.form.get(
            "categoria", ""
        ).strip()

        db.session.commit()

        flash(
            "Despesa atualizada com sucesso!",
            "sucesso"
        )

        return redirect(url_for("despesas"))

    return render_template(
        "editar_despesa.html",
        despesa=despesa
    )

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

    # Receitas
    if Receita.query.count() == 0:

        db.session.add(Receita(
            descricao="Salário",
            valor=1990,
            data=date(2026, 8, 5)
        ))

        db.session.add(Receita(
            descricao="Vale Refeição",
            valor=200,
            data=date(2026, 8, 8)
        ))

        db.session.add(Receita(
            descricao="Freelance",
            valor=450,
            data=date(2026, 8, 10)
        ))

        db.session.commit()


    # Despesas
    if Despesa.query.count() == 0:

        db.session.add(Despesa(
            descricao="Aluguel",
            valor=800,
            data=date(2026, 8, 5),
            categoria="Moradia"
        ))

        db.session.add(Despesa(
            descricao="Supermercado",
            valor=350,
            data=date(2026, 8, 7),
            categoria="Alimentação"
        ))

        db.session.add(Despesa(
            descricao="Conta de luz",
            valor=120,
            data=date(2026, 8, 10),
            categoria="Contas"
        ))

        db.session.add(Despesa(
            descricao="Combustível",
            valor=200,
            data=date(2026, 8, 12),
            categoria="Transporte"
        ))

        db.session.add(Despesa(
            descricao="Academia",
            valor=80,
            data=date(2026, 8, 15),
            categoria="Saúde"
        ))

        db.session.add(Despesa(
            descricao="Cinema",
            valor=60,
            data=date(2026, 8, 20),
            categoria="Lazer"
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

