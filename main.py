# comentário para uma única linha aff...
"""
Por enquanto, não precisamos instalar bibliotecas externas: 
o Python já possui os módulos socket e json necessários para essa parte.
"""
# import json # para usar o json.JSONDecodeError
from util import linha
from menu import menu_principal
from peer import falar_hello, responder_hello_ok
from servidor_rdv import registrar_peer, descobrir_peers, cancelar_registro

def main():
    print("PyP2P-Forca")
    print("Projeto iniciado com sucesso!")

    #menu_principal()
    
    # identifica o peer
    namespace = "CIC"
    name = "viniciusG15"
    port = 4000
    ttl = 60
    
    
    hello = falar_hello("alice@CIC")

    print("\nMensagem HELLO:")
    print(hello)

    hello_ok = responder_hello_ok(
        hello["msg_id"],
        "bob@CIC"
    )

    print("\nMensagem HELLO_OK:")
    print(hello_ok)


    """
    try:
        resposta_register = registrar_peer(namespace, name, port, ttl)
        print(f"{resposta_register}")

    except (OSError, ValueError, KeyError) as erro:
        print(f"\nErro: {erro}")
    

    linha()
    print("REGISTER do rendezvous:")
    resposta_register = registrar_peer(namespace, name, port, ttl)
    print(f"{resposta_register}")
   
    linha()
    print("DISCOVER do rendezvous:")
    resposta_discover = descobrir_peers()
    for peer in resposta_discover.get("peers",[]):
        print(f"{peer}")
    # imprimir_respostas(resposta_discover)
    # E possivel especificar o namespace da descoberta

    linha()
    print("UNREGISTER do rendezvous")
    resposta_unregister = cancelar_registro(namespace)
    print(f"{resposta_unregister}")
    """
    
    
if __name__ == "__main__":
    main()