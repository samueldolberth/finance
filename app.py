from flask import Flask
from routes.home import home_route

# inicializaçãp
app = Flask(__name__)

receitas = [
    {"id": 1, "nome": ""}
]

app.register_blueprint(home_route)

app.run(debug=True)