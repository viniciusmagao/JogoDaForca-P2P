from peer import conectar_peer, falar_hello, enviar_mensagem, receber_mensagem


def main():

    conexao = conectar_peer("127.0.0.1", 5001)
    print("Conexão estabelecida com sucesso!")

    try:
        hello = falar_hello("bob@CIC")

        enviar_mensagem(conexao, hello)
        print("HELLO enviado!")

        resposta = receber_mensagem(conexao)
        print("Resposta recebida: ")
        print(resposta)

    finally:
        conexao.close()


if __name__ == "__main__":
    main()