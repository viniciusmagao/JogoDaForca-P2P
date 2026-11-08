import os
import time

#------------------------------------------------------------
# IMPRIMIR
def imprimir(resposta, tipo):

    match tipo:
        # REGISTER
        case "r":
            print("\nreposta: ")
            print(resposta)
        # DISCOVER
        case "d":
            print("\nreposta: ")
            for peer in resposta.get("peers",[]):
                print(peer)
        # UNREGISTER
        case "u":
            print("\nreposta: ")
            print(resposta)

    """
    #----------------------------
    # DISCOVER
    if resposta.get("status") != "OK":
        print(f"Erro do servidor: {resposta.get('message','Erro desconhecido')}")
        return

    peers = resposta.get("peers", [])

    if not peers:
        print("Nenhum peer encontrado.")
        return

    versao mais simples:
    for peer in 'peers':
            print(f"{peer}")

    for i, peer in enumerate(peers, start=1):
        print(f"\nPeer {i}")
        print(f"  Nome: {peer['name']}")
        print(f"  Namespace: {peer['namespace']}")
        print(f"  IP: {peer['ip']}")
        print(f"  Porta: {peer['port']}")
        print(f"  TTL: {peer['ttl']}")
        print(f"  Expira em: {peer['expires_in']} segundos")
    """

#------------------------------------------------------------
# LINHA
def linha(tipo):
    match tipo:
        case 0:
            limpa_tela()
            print("\n==================================================")
            print("> JOGO DA FORCA [byG14]")
        case 1:
            print("\n--------------------------------------------------")
        case 2:
            print("\n==================================================")

#------------------------------------------------------------
# LIMPA
def limpa_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

#------------------------------------------------------------
# CONGELA
def congela_tela(duracao):
    time.sleep(duracao)

#------------------------------------------------------------
# ERRORs
def error_msg(tipo):

    match tipo:
        case "error_namespace":
            #raise ValueError("Namespace deve ter entre 1 e 64 caracteres.")
            print("Namespace deve ter entre 1 e 64 caracteres.")
        case "error_name":
            #raise ValueError("Nome deve ter entre 1 e 64 caracteres.")
            print("Nome deve ter entre 1 e 64 caracteres.")
        case "error_port":
            #raise ValueError("A porta deve ser um inteiro entre 1 e 65535.")
            print("A porta deve ser um inteiro entre 1 e 65535.")
        case "error_ttl":
            #raise ValueError("O TTL deve ser um número inteiro.") 
            print("O TTL deve ser um número inteiro.") 
        case "opcao_invalida":
            limpa_tela()
            linha(0)
            print("\nOpcao invalida!")
            congela_tela(2)
        case "erro_tam_msg":
            # Utilizada para msg recebida e msg enviada
            print("Mensagem excede o limite de 32 KiB.")
        case "erro_conexao":
            print("Conexao encerrada pelo outro peer.")
            raise ConnectionError("Conexao encerrada pelo outro peer.")
        case "erro_dict":
            print("A mensagem recebida deve ser um objeto JSON.")
        case "hello_invalido":
            print("Mensagem HELLO inválida!")

def valida_campo(campo, tipo):

    match tipo:
        case "namespace":
            # Valida namespace
            if not isinstance(campo, str) or not 1 <= len(campo) <= 64:
                error_msg("error_namespace")
                return False
            else:
                return True
        case "name":
            # Valida name
                if not isinstance(campo, str) or not 1 <= len(campo) <= 64:
                    error_msg("error_name")
                    return False
                else:
                    return True
        case "port":
            # Valida porta
            if isinstance(campo, bool) or not isinstance(campo, int) or not 1 <= campo <= 65535:
                error_msg("error_port")
                return False
            else:
                return True
        case "ttl":
             # Valida TTL
            if isinstance(campo, bool) or not isinstance(campo, int):
                error_msg("error_ttl")
                return False
            else:
                return True