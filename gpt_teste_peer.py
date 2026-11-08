import socket
from peer import enviar_mensagem, receber_mensagem

def main():
    # Cria dois sockets conectados entre si
    peer_a, peer_b = socket.socketpair()

    try:
        # Peer A envia uma mensagem para o Peer B
        mensagem = {
            "type": "HELLO",
            "peer_id": "alice@CIC",
            "ttl": 1
        }

        enviar_mensagem(peer_a, mensagem)

        # Peer B recebe a mensagem
        recebida = receber_mensagem(peer_b)

        print("Peer B recebeu: ")
        print(recebida)

        # Peer B responde para o Peer A
        resposta = {
            "type": "HELLO_OK",
            "peer_id": "bob@CIC",
            "ttl": 1
        }

        enviar_mensagem(peer_b, resposta)

        # Peer A recebe a resposta
        recebida = receber_mensagem(peer_a)

        print("\nPeer A recebeu: ")
        print(recebida)

    finally:
        peer_a.close()
        peer_b.close()

if __name__ == "__main__":
    main()