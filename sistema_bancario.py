menu = """

[d] Depositar Dinheiro
[s] Sacar Dinheiro
[e] Extrato Bancário
[q] Sair do Sitema

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:
    opcao = input(menu).lower()

    if opcao == "d":
        print("Informe o valor de Depósito:")
        valor = float(input())
        if valor <= 0:
            print("Operação falhou! O valor informado é inválido.")
        else:
            saldo += valor
            extrato += "Depósito: R$ " + f"{valor:.2f} + \n".rjust(20)
            print(f"Depósito Efetuado com Sucesso!\nSeu saldo é de: R$ {saldo:.2f}")
    elif opcao == "s":
        if numero_saques >= LIMITE_SAQUES:
            print("Operação falhou! Número máximo de saques diários atingido.")
            continue

        if saldo == 0:
            print("Operação falhou! Saldo insuficiente.")
            continue

        print("Informe o valor de Saque:")
        valor = float(input())

        if valor > limite:
            print("Operação falhou! O valor do saque excede o limite.")
            continue

        if valor > saldo:
            print("Operação falhou! Saldo insuficiente.")
            continue

        if valor <= 0:
            print("Operação falhou! O valor informado é inválido.")
        else:
            saldo -= valor
            extrato += "Saque: R$ " + f"{valor:.2f} - \n".rjust(23)
            print(f"Saque Efetuado com Sucesso!\nSeu saldo é de: R$ {saldo:.2f}")
            numero_saques += 1
            
    elif opcao == "e":
        if extrato == "":
            print("Não foram realizadas movimentações.")
        else:
            print("*******[EXTRATO BANCÁRIO]******")
            print(extrato[:-1])
            print("-------------------------------")
            print("Saldo: R$ " + f"{abs(saldo):.2f} {'+' if saldo >= 0 else '-'} \n".rjust(23))

    elif opcao == "q":
        break
    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")