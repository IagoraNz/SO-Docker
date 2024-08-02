import couchdb
import os

def main():
    couchdb_url = os.getenv('COUCHDB_URL', 'http://admin:adminpassword@localhost:5984')
    server = couchdb.Server(couchdb_url)
    
    # Crie ou abra um banco de dados
    db_name = 'mydatabase'
    if db_name in server:
        db = server[db_name]
    else:
        db = server.create(db_name)
    
    # Exemplo de inserção de um documento
    doc_id, doc_rev = db.save({'type': 'example', 'message': 'Hello, CouchDB!'})
    print(f'Document saved with ID: {doc_id}')

if __name__ == '__main__':
    main()