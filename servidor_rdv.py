import socket
import json

from util import linha, error_msg, valida_campo

# Configuração do servidor Rendezvous
RDV_HOST = "pyp2p.mfcaetano.cc"
RDV_PORT = 8080

# Tamanho máximo de linha 32 KiB (32768 bytes)
MAX_LINE_SIZE = 32768

#------------------------------------------------------------
# REGISTER
def registrar_peer():
    """
    Registra um peer no servidor rendezvous
    """
    
    namespace = input("namespace: ")
    v_namespace = valida_campo(namespace, "namespace")

    name = input("name: ")
    v_name = valida_campo(name, "name")
    
    port = int(input("port: "))
    v_port = valida_campo(int(port),"port")
    
    ttl_input = input("ttl (ENTER para usar 7200): ")
    if ttl_input == "":
            ttl = 7200
    else:
        ttl = int(ttl_input)
        v_ttl = valida_campo(ttl, "ttl")
   
    if (v_namespace and v_name and v_port and v_ttl):
        
        # Monta mensagem de registro
        mensagem = {
            "type": "REGISTER",
            "namespace": namespace,
            "name": name,
            "port": port,
            "ttl": ttl
        }

        # Envia a mensagem
        resposta = comunicar_com_rendezvous(mensagem)
        return resposta

#------------------------------------------------------------
# DISCOVER
def descobrir_peers(namespace=None):
    """
    Solicita ao rendezvous a lista de peers registrados.
    Se o namespace não é informado, retorna todos os peers
    """
    """
    Explicando o None:
    Em Python, o None significa a ausência de um valor. Ele
    é um objeto especial pertencente ao próprio tipo NoneType
    e é usado para indicar que uma variável, parâmetro ou 
    função não possui nenhum dado atribuído ou retorno 
    significativo.
    """

    namespace = input("namespace (ENTER para descobrir todos os peers): ")
    if namespace == "":
        mensagem = { "type": "DISCOVER" }
    else:
        v_namespace = valida_campo(namespace, "namespace")
        if v_namespace:
            mensagem["namespace"] = namespace
    
    resposta = comunicar_com_rendezvous(mensagem)
    return resposta

#------------------------------------------------------------
# UNREGISTER
def cancelar_registro():

    namespace = input("namespace: ")
    name = input("name (ENTER para vazio): ")
    port = input("port (ENTER para vazio): ")

    mensagem = { "type": "UNREGISTER" }
                
    if(valida_campo(namespace, "namespace")):
        mensagem["namespace"] = namespace
    else:
        error_msg("error_namespace")
        return

    if name != "":
        if (valida_campo(name, "name")):
            mensagem["name"] = name
        else:
            error_msg("error_name")
            return

    if port != "":
        if (valida_campo(port, "port")):
            mensagem["port"] = port
        else:
            error_msg("error_port")
            return

    resposta = comunicar_com_rendezvous(mensagem)
    return resposta

#------------------------------------------------------------
# TCP
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

    #------------------------------------------------------------
    # Abre uma conexão TCP com timeout de 5 seguntos
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

        # Verifica se a resposta respeita o limite de 32 KiB
        # A resposta precisa respeitar o limide de 32 KiB???
        if len(resposta_bytes) > MAX_LINE_SIZE:
            raise ValueError("Resposta maior que 32 KiB.")

        # Verifica se o servidor enviou uma resposta
        if not resposta_bytes:
            raise ValueError("O servidor fechou a conexão sem responder.")

        # Converte os bytes recebidos para texto (JSON?)
        resposta_texto = resposta_bytes.decode("utf-8").strip()

        # Converto o JSON recebido para um dicionário Python
        resposta = json.loads(resposta_texto)

        return resposta