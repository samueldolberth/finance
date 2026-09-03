# Controle Financeiro

Aplicação web desenvolvida em **Python com Flask** para auxiliar no controle de receitas e despesas pessoais. O sistema permite cadastrar, visualizar, editar e remover receitas e despesas, além de apresentar um dashboard com totais, saldo e despesas agrupadas por categoria.

## Funcionalidades

* Cadastro, edição, visualização e remoção de receitas.
* Cadastro, edição, visualização e remoção de despesas.
* Dashboard com receitas, despesas, saldo e informações resumidas.
* Agrupamento das despesas por categoria.
* Mensagens de feedback utilizando `flash()`.
* Utilização de **Session** para armazenar informações durante a navegação.
* Utilização de **Cookie** para salvar a preferência de tema claro ou escuro.
* Persistência dos dados utilizando **MySQL** com SQLAlchemy.

## Tecnologias

* Python
* Flask
* Flask-SQLAlchemy
* MySQL
* HTML
* CSS

## Como executar

1. Clone ou baixe o projeto.
2. Instale as dependências:

```bash
pip install flask flask-sqlalchemy pymysql
```

3. Crie o banco de dados `finance` no MySQL.
4. Confira a configuração da conexão com o banco no arquivo `app.py`.
5. Execute a aplicação:

```bash
python app.py
```

6. Acesse no navegador:

```text
http://127.0.0.1:5000/
```

## Rotas da Aplicação

### Dashboard e páginas gerais

* `GET /` — Exibe o dashboard principal com receitas, despesas, saldo e informações financeiras.
* `GET /sobre` — Exibe a página com informações sobre o projeto.
* `GET /tema/<tema>` — Altera o tema da aplicação entre claro e escuro utilizando Cookie.

### Despesas

* `GET /despesas` — Lista todas as despesas cadastradas.
* `GET /despesas/nova` — Exibe o formulário para cadastro de uma nova despesa.
* `POST /despesas/nova` — Cadastra uma nova despesa no banco de dados.
* `GET /despesa/<id>` — Exibe os detalhes de uma despesa específica.
* `GET /despesa/<id>/editar` — Exibe o formulário para edição de uma despesa.
* `POST /despesa/<id>/editar` — Atualiza os dados de uma despesa.
* `POST /despesa/<id>/remover` — Remove uma despesa do banco de dados.

### Receitas

* `GET /receitas` — Lista todas as receitas cadastradas.
* `GET /receitas/nova` — Exibe o formulário para cadastro de uma nova receita.
* `POST /receitas/nova` — Cadastra uma nova receita no banco de dados.
* `GET /receita/<id>` — Exibe os detalhes de uma receita específica.
* `GET /receita/<id>/editar` — Exibe o formulário para edição de uma receita.
* `POST /receita/<id>/editar` — Atualiza os dados de uma receita.
* `POST /receita/<id>/remover` — Remove uma receita do banco de dados.
