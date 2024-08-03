import couchdb
import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    couchdb_url = os.getenv('COUCHDB_URL', 'http://admin:adminpassword@localhost:5984')
    server = couchdb.Server(couchdb_url)

    while True:
        clear()
        print("Docker e CouchDB")
        print("1. Criar banco de dados")
        print("2. Inserir documento")
        print("3. Consultas")
        print("4. Remover documento")
        print("5. Remover banco de dados")
        print("0. Sair")
        try:
            opcao = int(input("Escolha uma opção: "))
        except ValueError:
            print("Opção inválida, tente novamente.")
            continue

        if opcao == 1:
            db_name = input("Digite o nome do banco de dados: ")
            if db_name in server:
                print("Banco de dados já existe")
            else:
                db = server.create(db_name)
                print(f'Banco de dados {db_name} criado com sucesso')
        elif opcao == 2:
            if len(server) == 0:
                print("Não existe nenhum banco de dados")
                continue
            db_name = input("Digite o nome do banco de dados: ")
            if db_name not in server:
                print("Banco de dados não encontrado")
                continue

            doc_id = input("Digite o ID do documento: ")
            tipo = input("Digite o tipo do documento: ")
            mensagem = input("Digite a mensagem do documento: ")

            doc = {
                '_id': doc_id,
                'tipo': tipo,
                'message': mensagem
            }
            db = server[db_name]
            
            try:
                doc_id, doc_rev = db.save(doc)
                print(f'Documento salvo com ID: {doc_id}')
            except couchdb.http.ResourceConflict:
                print(f'Erro: Documento com ID "{doc_id}" já existe.')
        elif opcao == 3:
            if len(server) == 0:
                print("Não existe nenhum banco de dados")
                continue
            db_name = input("Digite o nome do banco de dados: ")
            if db_name not in server:
                print("Banco de dados não encontrado")
                continue

            print("\nConsultar por: ")
            print("1. ID")
            print("2. Tipo")
            print("3. Mensagem")
            print("4. Todos")
            try:
                consulta = int(input("Escolha uma opção: "))
            except ValueError:
                print("Opção inválida, tente novamente.")
                continue

            db = server[db_name]
            if consulta == 1:
                doc_id = input("Digite o ID do documento: ")
                try:
                    doc = db[doc_id]
                    print(f'Documento encontrado: {doc}')
                except couchdb.http.ResourceNotFound:
                    print(f'Erro: Documento com ID "{doc_id}" não encontrado.')
            elif consulta == 2:
                tipo = input("Digite o tipo do documento: ")
                for doc_id in db:
                    doc = db[doc_id]
                    if doc['tipo'] == tipo:
                        print(f'Documento encontrado: {doc}')
            elif consulta == 3:
                mensagem = input("Digite a mensagem do documento: ")
                for doc_id in db:
                    doc = db[doc_id]
                    if doc['message'] == mensagem:
                        print(f'Documento encontrado: {doc}')
            elif consulta == 4:
                for doc_id in db:
                    doc = db[doc_id]
                    print(f'Documento encontrado: {doc}')
        elif opcao == 4:
            if len(server) == 0:
                print("Não existe nenhum banco de dados")
                continue
            db_name = input("Digite o nome do banco de dados: ")
            if db_name not in server:
                print("Banco de dados não encontrado")
                continue

            doc_id = input("Digite o ID do documento: ")
            db = server[db_name]
            try:
                doc = db[doc_id]
                db.delete(doc)
                print(f'Documento com ID "{doc_id}" removido com sucesso.')
            except couchdb.http.ResourceNotFound:
                print(f'Erro: Documento com ID "{doc_id}" não encontrado.')
        elif opcao == 5:
            if len(server) == 0:
                print("Não existe nenhum banco de dados")
                continue
            db_name = input("Digite o nome do banco de dados: ")
            if db_name not in server:
                print("Banco de dados não encontrado")
                continue  
            try:
                server.delete(db_name)
                print(f'Banco de dados "{db_name}" removido com sucesso.')
            except couchdb.http.ResourceNotFound:
                print(f'Erro: Banco de dados "{db_name}" não encontrado.')
        elif opcao == 0:
            print("Saindo...")
            break
        else:
            print("Opção inválida, tente novamente.")
        input("Pressione Enter para continuar...")

if __name__ == '__main__':
    main()