from datetime import datetime

menu = """

[d] Depositar Dinheiro
[s] Sacar Dinheiro
[e] Extrato Bancário
-----------------------------
[u] Cadastrar Usuário
[l] Listar Usuários
-----------------------------
[c] Cadastrar Conta Corrente
[r] Listar Conta Corrente
-----------------------------
[q] Sair do Sitema

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
usuarios = []
contas = []
LIMITE_SAQUES = 3

def saque(*, saldo, extrato, limite, numero_saques, limite_saques):
    if numero_saques >= limite_saques:
        print("Operação falhou! Número máximo de saques diários atingido.")
    elif saldo == 0:
        print("Operação falhou! Saldo insuficiente.")
    else:
        print("Informe o valor de Saque:")
        valor = float(input())

        if valor > limite:
            print("Operação falhou! O valor do saque excede o limite.")
        elif valor > saldo:
            print("Operação falhou! Saldo insuficiente.")
        elif valor <= 0:
            print("Operação falhou! O valor informado é inválido.")
        else:
            saldo -= valor
            extrato += "Saque: R$ " + f"{valor:.2f} - \n".rjust(23)
            print(f"Saque Efetuado com Sucesso!\nSeu saldo é de: R$ {saldo:.2f}")
            numero_saques += 1
    return saldo, extrato, numero_saques

def depositar(saldo, extrato, /):
    print("Informe o valor de Depósito:")
    valor = float(input())
    if valor <= 0:
        print("Operação falhou! O valor informado é inválido.")
    else:
        saldo += valor
        extrato += "Depósito: R$ " + f"{valor:.2f} + \n".rjust(20)
        print(f"Depósito Efetuado com Sucesso!\nSeu saldo é de: R$ {saldo:.2f}")    
    return saldo, extrato

def listar_extrato(saldo, /, *, extrato):
    if extrato == "":
        print("Não foram realizadas movimentações.")
    else:
        print("*******[EXTRATO BANCÁRIO]******")
        print(extrato[:-1])
        print("-------------------------------")
        print("Saldo: R$ " + f"{abs(saldo):.2f} {'+' if saldo >= 0 else '-'} \n".rjust(23))

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return False if usuarios_filtrados == [] else True

def valiar_cpf(cpf):
    if len(cpf) == 11 and cpf.isdigit():
       return True
    else:
        return False

def sim(mensagem):
    while True:
        print(f"{mensagem} [S/N]")
        if input().lower() == "s":
            return True
        else:
            return False

def validar_data_nascimento(data_string, formato="%d/%m/%Y"):
    try:
        data = datetime.strptime(data_string, formato)
        # Verificar se a data é realista (por exemplo, não aceitar 31/02)
        if data.strftime(formato) != data_string:
            return False
        return True
    except ValueError:
        return False

def cadastrar_usuario(usuarios):
    # Loop Validar CPF
    while True:
        cpf = input("Informe o CPF (somente número): ")
        if valiar_cpf(cpf):
            break
        else: 
            if sim("CPF inválido! Abortar cadastro?"):
                return None
    
    if filtrar_usuario(cpf, usuarios):
        print("Já existe usuário com esse CPF!")
        return None 
    else:
        nome = input("Informe o nome completo: ")

        while True:
            data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
            if validar_data_nascimento(data_nascimento):
                break
            if sim("Data de nascimento inválida! Abortar cadastro?"):
                return None
            # Se o usuário não quiser abortar, o loop continuará pedindo a data
        
        endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado: ")
        
        if sim("Confirma os dados informados?"):
            usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})   
            print("Usuário cadastrado com sucesso!")    

        return None
                         
def listar_usuarios(usuarios):
    if usuarios == []:
        print("Não há usuários cadastrados!")
    else:   
        for usuario in usuarios:
            print("-" * 100)
            print(f"Nome: {usuario['nome']} - CPF: {usuario['cpf']} - Data de Nascimento: {usuario['data_nascimento']}\nEndereço: {usuario['endereco']}")
    return None

def cadastrar_conta(contas):
    agencia = "0001"
    conta = len(contas) + 1
    cpf = input("Informe o CPF do usuário: ")
    if filtrar_usuario(cpf, usuarios):
        contas.append({"agencia": agencia, "conta": conta, "cpf": cpf})
        print(f"""
Conta cadastrada com sucesso!
Agência: {agencia}
Conta Corrente: {conta}
CPF: {cpf}""")
    else:
        print("Usuário não encontrado!")
    return None

def listar_contas(contas):
    if contas == []:
        print("Não há contas cadastradas!")
    else:
        for conta in contas:
            print("-" * 100)
            print(f"Agência: {conta['agencia']} - Conta: {conta['conta']} - CPF: {conta['cpf']}")
    return None

while True:
    opcao = input(menu).lower()

    if opcao == "d":
        saldo, extrato = depositar(saldo, extrato)
    elif opcao == "s":
        saldo, extrato, numero_saques = saque(saldo=saldo, extrato=extrato, limite=limite, numero_saques=numero_saques, limite_saques=LIMITE_SAQUES)
            
    elif opcao == "e":
        listar_extrato(saldo, extrato=extrato)

    elif opcao == "u":
        cadastrar_usuario(usuarios)

    elif opcao == "l":
        listar_usuarios(usuarios)

    elif opcao == "c":
        cadastrar_conta(contas)

    elif opcao == "r":
        listar_contas(contas)

    elif opcao == "q":
        break
    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")