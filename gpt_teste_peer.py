import socket
from peer import enviar_mensagem, receber_mensagem
from peer import falar_hello, validar_hello, falar_hello_ok

"""
Teste pra verifiacar a validação da mensagem HELLO

def main():
    mensagem = falar_hello("bob@CIC")

    if validar_hello(mensagem):
        print("Mensagem HELLO válida!")
    else:
        print("Mensagem HELLO inválida!")

    # Testando uma mensagem com TTL incorreto
    mensagem["ttl"] = 2

    if validar_hello(mensagem):
        print("Mensagem HELLO válida!")
    else:
        print("Mensagem HELLO inválida!")


if __name__ == "__main__":
    main()
"""
"""
Teste pra validar comunicação entre dois peers: 
    envio e recebimento de mensagens

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
"""