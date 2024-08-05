from flask import Flask, request, redirect, url_for, render_template_string, jsonify
import couchdb
import os

app = Flask(__name__)

# Conectar ao CouchDB
couchdb_url = os.getenv('COUCHDB_URL', 'http://admin:adminpassword@localhost:5984')
server = couchdb.Server(couchdb_url)

@app.route('/')
def index():
    print("Acessou a rota /")
    return render_template_string('''
        <h1>Docker e CouchDB</h1>
        <ul>
            <li><a href="{{ url_for('create_db') }}">Criar banco de dados</a></li>
            <li><a href="{{ url_for('insert_doc') }}">Inserir documento</a></li>
            <li><a href="{{ url_for('query_docs') }}">Consultas</a></li>
            <li><a href="{{ url_for('delete_doc') }}">Remover documento</a></li>
            <li><a href="{{ url_for('delete_db') }}">Remover banco de dados</a></li>
        </ul>
    ''')

@app.route('/create_db', methods=['GET', 'POST'])
def create_db():
    if request.method == 'POST':
        db_name = request.form.get('db_name')
        if db_name in server:
            return "Banco de dados já existe"
        else:
            server.create(db_name)
            return f'Banco de dados {db_name} criado com sucesso'
    return '''
        <h1>Criar Banco de Dados</h1>
        <form method="post">
            Nome do banco de dados: <input type="text" name="db_name">
            <input type="submit" value="Criar">
        </form>
    '''

@app.route('/insert_doc', methods=['GET', 'POST'])
def insert_doc():
    if request.method == 'POST':
        db_name = request.form.get('db_name')
        if db_name not in server:
            return "Banco de dados não encontrado"
        doc_id = request.form.get('doc_id')
        tipo = request.form.get('tipo')
        mensagem = request.form.get('mensagem')
        doc = {
            '_id': doc_id,
            'tipo': tipo,
            'message': mensagem
        }
        db = server[db_name]
        try:
            db.save(doc)
            return f'Documento salvo com ID: {doc_id}'
        except couchdb.http.ResourceConflict:
            return f'Erro: Documento com ID "{doc_id}" já existe.'
    return '''
        <h1>Inserir Documento</h1>
        <form method="post">
            Nome do banco de dados: <input type="text" name="db_name"><br>
            ID do documento: <input type="text" name="doc_id"><br>
            Tipo: <input type="text" name="tipo"><br>
            Mensagem: <input type="text" name="mensagem"><br>
            <input type="submit" value="Inserir">
        </form>
    '''

@app.route('/query_docs', methods=['GET', 'POST'])
def query_docs():
    if request.method == 'POST':
        db_name = request.form.get('db_name')
        if db_name not in server:
            return "Banco de dados não encontrado"
        consulta = request.form.get('consulta')
        db = server[db_name]
        result = []

        if consulta == '1':
            doc_id = request.form.get('doc_id')
            if doc_id:
                try:
                    doc = db[doc_id]
                    result.append(doc)
                except couchdb.http.ResourceNotFound:
                    result.append(f'Erro: Documento com ID "{doc_id}" não encontrado.')
            else:
                return 'Erro: ID do documento não fornecido.'

        elif consulta == '2':
            tipo = request.form.get('tipo')
            tipo_value = request.form.get('tipo_value')
            if tipo and tipo_value:
                for doc_id in db:
                    doc = db[doc_id]
                    if doc.get('tipo') == tipo_value:
                        result.append(doc)
            else:
                return 'Erro: Tipo ou valor do tipo não fornecidos.'

        elif consulta == '3':
            mensagem = request.form.get('mensagem')
            mensagem_value = request.form.get('mensagem_value')
            if mensagem and mensagem_value:
                for doc_id in db:
                    doc = db[doc_id]
                    if doc.get('message') == mensagem_value:
                        result.append(doc)
            else:
                return 'Erro: Mensagem ou valor da mensagem não fornecidos.'

        elif consulta == '4':
            for doc_id in db:
                doc = db[doc_id]
                result.append(doc)

        return jsonify(result)

    return '''
        <h1>Consultar Documentos</h1>
        <form method="post">
            Nome do banco de dados: <input type="text" name="db_name"><br>
            Consultar por: <br>
            <input type="radio" name="consulta" value="1"> ID
            <input type="text" name="doc_id"><br>
            <input type="radio" name="consulta" value="2"> Tipo
            <input type="text" name="tipo_value"><br>
            <input type="radio" name="consulta" value="3"> Mensagem
            <input type="text" name="mensagem_value"><br>
            <input type="radio" name="consulta" value="4"> Todos<br>
            <input type="submit" value="Consultar">
        </form>
    '''

@app.route('/delete_doc', methods=['GET', 'POST'])
def delete_doc():
    if request.method == 'POST':
        db_name = request.form.get('db_name')
        if db_name not in server:
            return "Banco de dados não encontrado"
        doc_id = request.form.get('doc_id')
        db = server[db_name]
        try:
            doc = db[doc_id]
            db.delete(doc)
            return f'Documento com ID "{doc_id}" removido com sucesso.'
        except couchdb.http.ResourceNotFound:
            return f'Erro: Documento com ID "{doc_id}" não encontrado.'
    return '''
        <h1>Remover Documento</h1>
        <form method="post">
            Nome do banco de dados: <input type="text" name="db_name"><br>
            ID do documento: <input type="text" name="doc_id"><br>
            <input type="submit" value="Remover">
        </form>
    '''

@app.route('/delete_db', methods=['GET', 'POST'])
def delete_db():
    if request.method == 'POST':
        db_name = request.form.get('db_name')
        if db_name not in server:
            return "Banco de dados não encontrado"
        try:
            server.delete(db_name)
            return f'Banco de dados "{db_name}" removido com sucesso.'
        except couchdb.http.ResourceNotFound:
            return f'Erro: Banco de dados "{db_name}" não encontrado.'
    return '''
        <h1>Remover Banco de Dados</h1>
        <form method="post">
            Nome do banco de dados: <input type="text" name="db_name"><br>
            <input type="submit" value="Remover">
        </form>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
