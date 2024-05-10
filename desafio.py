from abc import ABC, abstractmethod
from datetime import datetime
import textwrap

class Conta:
    def __init__(self,numero,cliente) :
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero,cliente)
    
    def sacar(self,valor):
        if valor < 0:
            print("Valor de Saque Inválido")
        elif self._saldo < valor:
            print("Saldo Insuficiente!")
        else:
            self._saldo -= valor
            print("Saque realizado com sucesso!")
            return True
        
        return False

    def depositar(self,valor):
        if valor<0:
            print("Valor de Depósito inválido!")
        else:
            self._saldo += valor
            print("Valor depositado com sucesso!")
            return True
    
        return False

class ContaCorrente(Conta):
    def __init__(self,numero , cliente, limite = 500, limite_saques=3):
        super().__init__(numero,cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saque = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])
        if (numero_saque>=self._limite_saques):
            print("Limite diario de Saques atingido, entre em contato com seu gerente!")
        elif (valor>self._limite):
            print("Valor do saque ultrapassa o limite, entre em contato com seu gerente!")
        else:
            return super().sacar(valor)
        return False

    def depositar(self,valor):
        if valor<0:
            print("Valor de Depósito inválido!")
        else:
            return super().depositar(valor)
        return False
    
    def __str__(self):
        return f""" Agência: \t {self.agencia}\nConta Corrente \t {self.numero}\nTitular \t {self.cliente.nome}"""

class Cliente:
    def __init__(self, logradouro,numero,bairro,cidade,estado):
        self._endereco = logradouro + ", " + numero + " - " + bairro + " - " +cidade + " / " + estado
        self._contas = []

    @property
    def contas(self):
        return self._contas

    @property
    def endereco(self):
        return self._endereco
    
    def adicionar_conta(self, conta):
        self._contas.append(conta)

    def realizar_transacao(self,conta,transacao):
        transacao.registrar(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf,nome,dia,mes,ano,**kwargs):
        super().__init__(**kwargs)
        self._cpf = cpf
        self._nome = nome
        self._dia = dia
        self._mes = mes
        self._ano = ano
    
    @property
    def nome(self):
        return self._nome
    
    @property
    def cpf(self):
        return self._cpf

    def __str__(self):
        return f"Nome: {self._nome}, CPF: {self._cpf}, Data de Nascimento: {self._dia}/{str(self._mes).zfill(2)}/{self._ano}, Endereço: {self._endereco}"
        
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self,transacao):
        self._transacoes.append({"tipo": transacao.__class__.__name__, "valor": transacao.valor,"data": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),})

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self,conta):
        pass

class Deposito(Transacao):
    def __init__(self,valor):
        self._valor=valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self,conta):
        transacao = conta.depositar(self.valor)
        if transacao:
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self,valor):
        self._valor=valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self,conta):
        transacao = conta.sacar(self.valor)
        if transacao:
            conta.historico.adicionar_transacao(self)

def menu():
    menu = '''
        [D] Depositar
        [S] Sacar
        [E] Extrato
        [U] Criar Usuario
        [C] Criar Conta Corrente
        [L] Listar Contas do usuario
        [Q] Sair
    '''
    return input(menu).lower()

def filtrar_cliente(cpf,clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf ==cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Conta nao encontrada!")
        return
    return cliente.contas[0]

def depositar(clientes):
    cpf = input("Digite o CPF do cliente: ")
    cliente = filtrar_cliente(cpf,clientes)

    if not cliente:
        print("CPF não cadastrado!")
        return
    
    valor = float (input("Digite o valor a ser depositado: "))
    transacao = Deposito(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta,transacao)

def sacar(clientes):
    cpf = input("Digite o CPF do cliente: ")
    cliente = filtrar_cliente(cpf,clientes)

    if not cliente:
        print("CPF não cadastrado!")
        return
    
    valor = float (input("Digite o valor a ser sacado: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return
    
    cliente.realizar_transacao(conta,transacao)
            
def exibir_extrato(clientes):
    cpf = input("Digite o CPF do cliente: ")
    cliente = filtrar_cliente(cpf,clientes)

    if not cliente:
        print("CPF não cadastrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("\n ==============================================================")
    transacoes = conta.historico.transacoes
    extrato = ""

    if not transacoes:
        extrato = "Não há informações a serem exibidas"
    else:
        for trans in transacoes:
            extrato += f"{trans['tipo']}:\tR$ {trans['valor']:4.2f}\n"

    print(extrato)
    print(f"\nSaldo Atual:\tR${conta.saldo:4.2f}")
    print("==============================================================")

def criar_cliente(clientes):
    cpf = input("Digite o CPF do cliente: ")
    cliente = filtrar_cliente(cpf,clientes)

    if cliente:
        print("CPF já cadastrado cadastrado!")
        return
    
    nome = input("Informe o nome do novo cliente: ")

    dia = input("Dia de Nascimento(DD): ")
    mes = input("Mês do Nascimento(MM): ")
    ano = input("Ano do Nascimento(AAAA): ")

    logradouro = input("Digite o logradouro do usuario: ")
    numero = input("Digite o numero do usuario: ")
    bairro = input("Digite o bairro do usuario: ")
    cidade = input("Digite a cidade do usuario: ")
    estado = input("Digite o estado do usuario: ")

    cliente = PessoaFisica(cpf,nome,dia,mes,ano,logradouro=logradouro,numero = numero,bairro=bairro,cidade = cidade,estado = estado)

    clientes.append(cliente)

    print("Cliente cadastrado com sucesso!")

def criar_conta(numero_conta,clientes,contas):
    cpf = input("Digite o CPF do cliente: ")
    cliente = filtrar_cliente(cpf,clientes)

    if not cliente:
        print("CPF não cadastrado!")
        return
    
    conta = ContaCorrente.nova_conta(cliente = cliente, numero = numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("C/C criada com sucesso!")

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)
            
        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "u":
            criar_cliente(clientes)

        elif opcao == "c":
            numero_conta = len(contas) - 1
            criar_conta(numero_conta,clientes,contas)

        elif opcao == "l":
            listar_contas(contas)
            
        elif opcao == "q":
            break

        else:
            print("Opção Inválida, por favor selecione novamente a opção desejada")

main()