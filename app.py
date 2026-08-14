from flask import Flask, jsonify, request, url_for, render_template, redirect

# inicializaçãp
app = Flask(__name__)

receitas = [ # lista de receitas em JSON

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

# inicio aulas

def pagina(titulo, conteudo):
    return f"""

    <!DOCTYPE html>
    <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <title>{titulo}</title>
        </head>
        <body>
            <nav>
                <a href="{url_for('index')}">Inicio</a> |
                <a href="{url_for('sobre')}">Sobre</a> |
                <a href="{url_for('contato')}">Contato</a>
            </nav>
            <hr>
            {conteudo}
        </body>
    </html>
"""

@app.route('/home')
def home():
    return redirect(url_for('index'))

@app.route('/')
def index():
    return pagina("Primeira Página", "<h1>Primeira Página</h1>")

@app.route('/sobre')
def sobre():
    return pagina("Sobre", "<h1>Sobre</h1><p>Esta é a página sobre.</p>")

@app.route('/contato')
def contato():
    return pagina("Contato", "<h1>Contato</h1><p>Esta é a página de contato.</p>")

@app.route('/produto/<int:id>')
def detalhe_produto(id):
    return pagina(f"Produto {id}", f"<h1>Produto {id}</h1><p>Detalhes do produto {id}.</p>")

# fora da aula
@app.route('/primeiratela')
def ola_mundo():
    return render_template('index.html')

# execução
if __name__ == '__main__':
    app.run(debug=True)