from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

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
    date = db.Column(db.date, nullable=False)

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
        valor = float(request.form.get("valor"))
        data = request.form.get("data")
        novo_id = len(lista_receitas) + 1

        lista_receitas.append({"id": novo_id, "descricao": descricao, "valor": valor,"data": data})

        return redirect(url_for("dashboard"))

    return render_template("nova_receita.html")

def popular_banco():
    if Receita.query.count() == 0:
        db.session.add(Receita(
            descricao = "Salário",
            valor = "1990",
            data = "05/08/2026",
        ))
        db.session.add(Receita(
            descricao = "Vale Refeição",
            valor = "200",
            data = "08/08/2026"
        ))
        db.session.add(Receita(
            descricao = "Freelance"
            valor = "450"
            data = "10/08/2026"
        ))

with app.app_context():
    db.create_all()

    nova = Receita(titulo="Teste DB")
    db.session.add(nova)
    db.session.commit()

    todas = Receita.query.all()
    for receita in todas:
        print(receita.id, receita.titulo)

# Executa o servidor
if __name__ == "__main__":
    app.run(debug=True)

