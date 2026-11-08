def iniciar_servidor(porta, host="127.0.0.1"):
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    servidor.bind((host, porta))
    servidor.listen()

    print(f"Servidor aguardando conexões em {host}:{porta}")

    return servidor


def aceitar_conexao(servidor):
    conexao, endereco = servidor.accept()

    print(f"Conexão recebida de {endereco}")

    return conexao


def conectar_peer(host, porta):
    conexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        conexao.connect((host, porta))
        print(f"Conectado ao peer {host}:{porta}")

        return conexao

    except Exception:
        conexao.close()
        raise