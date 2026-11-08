from peer import iniciar_servidor, aceitar_conexao, responder_hello


def main():
    servidor = iniciar_servidor(5001)

    try:
        conexao = aceitar_conexao(servidor)
        print("Conexão estabelecida com sucesso!")
        
        try:
            """
            O servidor está esperando uma conexão, quando isso
            acontecer ele vai responder com o responder_hello(),
            ou seja, vai mandar um HELLO_OK
            """
            responder_hello(conexao)
        finally:
            conexao.close()

    finally:
        servidor.close()


if __name__ == "__main__":
    main()