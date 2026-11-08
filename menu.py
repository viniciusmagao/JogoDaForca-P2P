from servidor_rdv import (
    registrar_peer,
    descobrir_peers,
    cancelar_registro
)
from util import linha, error_msg, limpa_tela, imprimir

def menu_principal():

    while True:
        linha(0)
        print("\n")
        print("1. Registrar peer")
        print("2. Descobrir peers")
        print("3. Cancelar registro")
        print("0. Sair")
        linha(1)

        opcao = input("Escolha uma opção: ")

        match opcao:
            case "1":
                linha(0)
                print("1. REGISTRAR PEER\n")
                resposta = registrar_peer()
                imprimir(resposta,"r")
                input("\nPressione ENTER para voltar ao menu...")
            case "2":
                linha(0)
                print("1. DESCOBRIR PEER\n")
                resposta = descobrir_peers()
                imprimir(resposta,"d")
                input("\nPressione ENTER para voltar ao menu...")
            case "3":
                linha(0)
                print("3. CANCELAR REGISTRO\n")
                resposta = cancelar_registro()
                imprimir(resposta, "u")
                input("\nPressione ENTER para voltar ao menu...")
            case "0":
                linha(1)
                print("Saindo...")
                break
            case _:
                error_msg("opcao_invalida")