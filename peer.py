import uuid
import json
import socket
from util import error_msg

VERSAO_PROTOCOLO = "1.0"
FEATURES = ["hangman"]
TTL = 1
TAMANHO_MAXIMO_MENSAGEM = 32 * 1024

#------------------------------------------------------------
# MSG_ID
def gerar_msg_id():
    """
    Gera um identificador único UUID v4.
    """

    return str(uuid.uuid4())

#============================================================
#------------------------------------------------------------
# HELLO: MSG
def falar_hello(peer_id):
    """
    Fala HELLO iniciando a conexao TCP
    """

    mensagem = {
        "type": "HELLO",
        "msg_id": gerar_msg_id(),
        "peer_id": peer_id,
        "version": VERSAO_PROTOCOLO,
        "features": FEATURES,
        "ttl": TTL
    }

    return mensagem

#------------------------------------------------------------
# HELLO: VALIDACAO
def validar_hello(mensagem):
    # Verifica se todos os campos obrigatórios existem

    campos_obrigatorios = [
        "type",
        "msg_id",
        "peer_id",
        "version",
        "features",
        "ttl"
    ]

    # Se tiver algum campo faltando já retorna false
    for campo in campos_obrigatorios:
        if campo not in mensagem:
            return False

    # Verifica os tipos dos campos
    if not isinstance(mensagem["msg_id"], str):
        return False

    if not isinstance(mensagem["peer_id"], str):
        return False

    if not isinstance(mensagem["version"], str):
        return False

    # Verifica se é uma lista
    if not isinstance(mensagem["features"], list):
        return False

    # Verifica cada elemento da lista
    if not all(isinstance(feature, str) for feature in mensagem["features"]):
        return False

    if not isinstance(mensagem["ttl"], int) or isinstance(mensagem["ttl"], bool):
        return False

    # Verifica os valores exigidos pelo protocolo
    if mensagem["version"] != VERSAO_PROTOCOLO:
        return False

    if "hangman" not in mensagem["features"]:
        return False

    if mensagem["ttl"] != TTL:
        return False

    return True

#------------------------------------------------------------
# HELLO: RESPONDENDO
def responder_hello(conexao):
    mensagem = receber_mensagem(conexao)

    if not validar_hello(mensagem):
        error_msg("hello_invalido")
        return False

    print(f"HELLO recebido de {mensagem["peer_id"]}")

    resposta = falar_hello_ok(
        mensagem["msg_id"],
        "alice@CIC"
    )

    enviar_mensagem(conexao, resposta)

    print("HELLO_OK enviado!")

    return True
    
#------------------------------------------------------------
# HELLO_OK: MSG
def falar_hello_ok(msg_id, peer_id):
    """
    Enviar um HELLO_OK, em resposta ao HELLO
    O msg_id deve ser o mesmo recebido no HELLO
    """

    mensagem = {
        "type": "HELLO_OK",
        "msg_id": msg_id,
        "peer_id": peer_id,
        "version": VERSAO_PROTOCOLO,
        "features": FEATURES,
        "ttl": TTL
    }

    return mensagem

#============================================================
#------------------------------------------------------------
# ENVIAR MENSAGEM
def enviar_mensagem(conexao, mensagem):
    # O parâmetro conexao será o socket TCP já conectado ao outro peer

    # sockets TCP trabalham com bytes
    dados = json.dumps(mensagem).encode("utf-8") + b"\n"

    if len(dados) > TAMANHO_MAXIMO_MENSAGEM:
        error_msg("erro_tam_msg")

    # Envia todos os bytes mesmo que sejam várias operações internas de envio
    conexao.sendall(dados)

#------------------------------------------------------------
# RECEBER MENSAGEM
def receber_mensagem(conexao):
    dados = bytearray()

    while True:
        """
        O TCP não garante que uma mensagem inteira chegada de uma só
        vez, pode chegar dividida em vários pedaços. Por isso vamos
        lendo os bytes até encontrar \n. Encontrando o \n, consideramos
        que recebemos uma mensagem completa. Por isso usamos o while aqui
        """
        byte = conexao.recv(1)

        if not byte:
            error_msg("erro_conexao")

        # Mensagem vazia
        if byte == b"\n":
            break

        dados.extend(byte)

        if len(dados) > TAMANHO_MAXIMO_MENSAGEM:
            error_msg("erro_tam_msg")

    try:
        # Decodificacao da mensagem, se estiver tudo certo
        mensagem = json.loads(dados.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as erro:
        # ATENCAO!! Ver como passar esse erro pra função de erros
        raise ValueError("Mensagem recebida não contém um JSON válido") from erro

    if not isinstance(mensagem, dict):
        error_msg("erro_dict")

    return mensagem

#============================================================
#------------------------------------------------------------
# INICIAR SERVIDOR
def iniciar_servidor(porta, host="127.0.0.1"):
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    servidor.bind((host, porta))
    servidor.listen()

    print(f"Servidor aguardando conexões em {host}:{porta}")

    return servidor

#------------------------------------------------------------
# ACEITAR CONEXAO
def aceitar_conexao(servidor):
    # O método accept retorna 2 valores
    conexao, endereco = servidor.accept()

    print(f"Conexão recebida de {endereco}")

    return conexao

#------------------------------------------------------------
# CONECTAR PEER
def conectar_peer(host, porta):
    # AF_INET diz pra usar IPv4
    conexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        conexao.connect((host, porta))
        print(f"Conectado ao peer {host}:{porta}")

        return conexao
    
    except Exception:
        conexao.close()
        raise