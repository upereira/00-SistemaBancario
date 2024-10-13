from abc import ABC, abstractmethod
from datetime import datetime

# Função auxiliar para confirmar ação com [S/N]
def sim(mensagem):
    while True:
        resposta = input(f"{mensagem} [S/N]: ").lower()
        if resposta == "s":
            return True
        elif resposta == "n":
            return False
        else:
            print("Resposta inválida! Por favor, responda com 'S' ou 'N'.")

# Classe Banco para gerenciar clientes e contas
class Banco:
    def __init__(self):
        self.clientes = []
        self.contas = []

    def cadastrar_usuario(self):
        while True:
            cpf = input("Informe o CPF (somente números): ")
            if not validar_cpf(cpf):
                if sim("CPF inválido! Deseja tentar novamente?"):
                    continue
                else:
                    return

            if any(cliente.cpf == cpf for cliente in self.clientes):
                print("Já existe um usuário com esse CPF!")
                return

            nome = input("Informe o nome completo: ")

            while True:
                data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
                if not validar_data_nascimento(data_nascimento):
                    if sim("Data de nascimento inválida! Deseja tentar novamente?"):
                        continue
                    else:
                        return
                break

            endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

            cliente = PessoaFisica(nome, cpf, data_nascimento, endereco)
            self.clientes.append(cliente)
            print("Usuário cadastrado com sucesso!")
            break

    def listar_usuarios(self):
        if not self.clientes:
            print("Não há usuários cadastrados!")
        else:
            for cliente in self.clientes:
                print("-" * 100)
                print(f"Nome: {cliente.nome} - CPF: {cliente.cpf} - Data de Nascimento: {cliente.data_nascimento}")
                print(f"Endereço: {cliente.endereco}")
                print("-" * 100)

    def cadastrar_conta(self):
        cpf = input("Informe o CPF do usuário: ")  # Solicita o CPF do usuário
        cliente = next((cliente for cliente in self.clientes if cliente.cpf == cpf), None)
        if not cliente:
            print("Usuário não encontrado!")
            return

        numero_conta = len(self.contas) + 1  # Gera automaticamente o número da conta
        conta = ContaCorrente(cliente, numero_conta, limite=500, limite_saques=3)
        cliente.adicionar_conta(conta)
        self.contas.append(conta)
        print(f"Conta {numero_conta} cadastrada com sucesso para o cliente {cliente.nome}.")

    def listar_contas(self):
        if not self.contas:
            print("Não há contas cadastradas!")
        else:
            for conta in self.contas:
                print("-" * 100)
                print(f"Agência: {conta.agencia} - Conta: {conta.numero} - CPF: {conta.cliente.cpf}")
                print("-" * 100)

    def realizar_deposito(self):
        while True:
            try:
                numero = int(input("Informe o número da conta: "))
                conta = next((conta for conta in self.contas if conta.numero == numero), None)
                if not conta:
                    if sim("Conta não encontrada! Deseja tentar novamente?"):
                        continue
                    else:
                        return  # Aborta e volta ao menu principal
                valor = float(input("Informe o valor do depósito: "))
                if valor <= 0:
                    if sim("O valor do depósito deve ser positivo! Deseja tentar novamente?"):
                        continue
                    else:
                        return  # Aborta e volta ao menu principal
                deposito = Deposito(valor)
                conta.cliente.realizar_transacao(conta, deposito)
                break
            except ValueError:
                if sim("Entrada inválida! Deseja tentar novamente?"):
                    continue
                else:
                    return  # Aborta e volta ao menu principal

    def realizar_saque(self):
        while True:
            try:
                numero = int(input("Informe o número da conta: "))
                conta = next((conta for conta in self.contas if conta.numero == numero), None)
                if not conta:
                    if sim("Conta não encontrada! Deseja tentar novamente?"):
                        continue
                    else:
                        return  # Aborta e volta ao menu principal
                valor = float(input("Informe o valor do saque: "))
                saque = Saque(valor, conta.limite, conta.numero_saques, conta.limite_saques)
                conta.cliente.realizar_transacao(conta, saque)
                conta.numero_saques += 1
                break
            except ValueError:
                if sim("Entrada inválida! Deseja tentar novamente?"):
                    continue
                else:
                    return  # Aborta e volta ao menu principal

    def exibir_extrato(self):
        while True:
            try:
                numero = int(input("Informe o número da conta: "))
                conta = next((conta for conta in self.contas if conta.numero == numero), None)
                if not conta:
                    if sim("Conta não encontrada! Deseja tentar novamente?"):
                        continue
                    else:
                        return  # Aborta e volta ao menu principal
                conta.historico.exibir_extrato()
                break
            except ValueError:
                if sim("Entrada inválida! Deseja tentar novamente?"):
                    continue
                else:
                    return  # Aborta e volta ao menu principal

# Cliente e PessoaFisica
class Cliente:
    def __init__(self, nome, cpf, data_nascimento, endereco):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

class PessoaFisica(Cliente):
    pass

# Conta e ContaCorrente
class Conta:
    def __init__(self, cliente, numero, agencia="0001"):
        self.saldo = 0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.historico.adicionar_transacao(f"Depósito", valor)
            print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")
            return True
        else:
            print("Operação falhou! O valor informado é inválido.")
            return False

    def sacar(self, valor, limite, numero_saques, limite_saques):
        if numero_saques >= limite_saques:
            print("Operação falhou! Número máximo de saques diários atingido.")
            return False
        elif valor > limite:
            print("Operação falhou! O valor do saque excede o limite.")
            return False
        elif valor > self.saldo:
            print("Operação falhou! Saldo insuficiente.")
            return False
        else:
            self.saldo -= valor
            self.historico.adicionar_transacao(f"Saque", valor)
            print(f"Saque de R$ {valor:.2f} realizado com sucesso.")
            return True

    def exibir_saldo(self):
        print(f"Saldo atual: R$ {self.saldo:.2f}")

class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite, limite_saques):
        super().__init__(cliente, numero)
        self.limite = limite
        self.limite_saques = limite_saques
        self.numero_saques = 0

# Historico
class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, tipo, valor):
        self.transacoes.append((tipo, valor))

    def exibir_extrato(self):
        print("*******[EXTRATO BANCÁRIO]******")
        saldo = 0.0
        for tipo, valor in self.transacoes:
            if tipo == "Depósito":
                print(f"Depósito: R$ {valor:>15.2f} +")
                saldo += valor
            elif tipo == "Saque":
                print(f"Saque: R$ {valor:>18.2f} -")
                saldo -= valor
        print("-------------------------------")
        print(f"Saldo: R$ {saldo:>18.2f} +")

# Interface de Transação e as classes Deposito e Saque
class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        conta.depositar(self.valor)

class Saque(Transacao):
    def __init__(self, valor, limite, numero_saques, limite_saques):
        self.valor = valor
        self.limite = limite
        self.numero_saques = numero_saques
        self.limite_saques = limite_saques

    def registrar(self, conta):
        conta.sacar(self.valor, self.limite, self.numero_saques, self.limite_saques)

# Funções auxiliares para CPF e data de nascimento
def validar_cpf(cpf):
    return len(cpf) == 11 and cpf.isdigit()

def validar_data_nascimento(data_string, formato="%d/%m/%Y"):
    try:
        data = datetime.strptime(data_string, formato)
        return data.strftime(formato) == data_string
    except ValueError:
        return False

# Classe Menu para interagir com o sistema bancário
class Menu:
    def __init__(self, banco):
        self.banco = banco

    def exibir(self):
        menu_text = """
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
        [q] Sair do Sistema

        => """
        while True:
            opcao = input(menu_text).lower()

            if opcao == "d":
                self.banco.realizar_deposito()
            elif opcao == "s":
                self.banco.realizar_saque()
            elif opcao == "e":
                self.banco.exibir_extrato()
            elif opcao == "u":
                self.banco.cadastrar_usuario()
            elif opcao == "l":
                self.banco.listar_usuarios()
            elif opcao == "c":
                self.banco.cadastrar_conta()
            elif opcao == "r":
                self.banco.listar_contas()
            elif opcao == "q":
                print("Saindo do sistema...")
                break
            else:
                print("Operação inválida!")

# Instanciando Banco e Menu
banco = Banco()
menu = Menu(banco)

# Iniciar o sistema
menu.exibir()
