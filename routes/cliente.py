from flask import Blueprint

cliente_route = Blueprint('cliente', __name__)

@cliente_route.route('/')
def lista_cliente():
    pass

@cliente_route.route('/')
def obter_cliente():
    pass