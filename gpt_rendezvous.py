import socket
import json


# Configuração do servidor Rendezvous
RDV_HOST = "pyp2p.mfcaetano.cc"
RDV_PORT = 8080

# Tamanho máximo de uma mensagem, conforme a especificação
MAX_LINE_SIZE = 32768


def comunicar_com_rendezvous(mensagem):
    """
    Envia uma mensagem JSON ao servidor Rendezvous
    e retorna a resposta recebida.
    """

    # Converte o dicionário Python para JSON e adiciona \n
    dados = json.dumps(mensagem) + "\n"

    # Converte o texto para bytes UTF-8
    dados_bytes = dados.encode("utf-8")

    # Verifica o tamanho da mensagem
    if len(dados_bytes) > MAX_LINE_SIZE:
        raise ValueError("Mensagem maior que 32 KiB.")

    # Abre uma conexão TCP com timeout de 5 segundos
    with socket.create_connection(
        (RDV_HOST, RDV_PORT),
        timeout=5
    ) as conexao:

        # Define um timeout para as operações de leitura
        conexao.settimeout(5)

        # Envia a mensagem
        conexao.sendall(dados_bytes)

        # Recebe a resposta até a quebra de linha
        with conexao.makefile("rb") as arquivo:
            resposta_bytes = arquivo.readline(MAX_LINE_SIZE + 1)

        # Verifica se a resposta respeita o limite
        if len(resposta_bytes) > MAX_LINE_SIZE:
            raise ValueError("Resposta maior que 32 KiB.")

        # Verifica se o servidor enviou uma resposta
        if not resposta_bytes:
            raise ConnectionError("O servidor fechou a conexão sem responder.")

        # Converte os bytes recebidos para texto
        resposta_texto = resposta_bytes.decode("utf-8").strip()

        # Converte o JSON recebido para um dicionário Python
        resposta = json.loads(resposta_texto)

        return resposta


def main():
    # Mensagem de teste: registro temporário
    mensagem = {
        "type": "REGISTER",
        "namespace": "CIC",
        "name": "teste_python_123",
        "port": 4000,
        "ttl": 60
    }

    try:
        resposta = comunicar_com_rendezvous(mensagem)

        print("Resposta do Rendezvous:")
        print(resposta)

    except (OSError, ValueError, json.JSONDecodeError,
            ConnectionError) as erro:
        print(f"Erro na comunicação: {erro}")


if __name__ == "__main__":
    main()