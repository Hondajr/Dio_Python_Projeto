menu = '''
    [D] Depositar
    [S] Sacar
    [E] Extrato
    [U] Criar Usuario
    [C] Criar Conta Corrente
    [L] Listar Contas do usuario
    [Q] Sair

'''

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUE = 3
usuarios = []
contas_correntes = []

def deposito(saldo, valor,extrato,/):
    #Deposito:
    #   Deve receber somente por posicao(positional only).
    #   Sugestao de argumentos: saldo, valor, extrato.
    #   Sugestao retorno: saldo e extrato. 
    if valor>=0:
        saldo+=valor
        extrato += f"Depósito:       R$ {valor_deposito:3.2f}\n"
        print("Valor depositado com sucesso!")
    else:
        print("Valor de Deposito invalido")
    return saldo,extrato


def saque(*,saldo,numero_saques,valor_limite,valor_saque,extrato):
    #Saque:
    #   Deve receber somente por nome(keyword only).
    #   Sugestao de argumentos: saldo, valor, extrato, limite, numero_saques,limite_saques.
    #   Sugestao retorno: saldo e extrato. 
    if (valor_saque <0):
        print("Valor digitado invalido!")
    elif (numero_saques >= LIMITE_SAQUE):
        print("Limite diario de Saques atingido, entre em contato com seu gerente!")
    elif (valor_saque>valor_limite):
        print("Valor do saque ultrapassa o limite, entre em contato com seu gerente!")
    else:
        if(valor_saque>saldo):
            print("Saldo insuficiente!")
        else:
            saldo -= valor_saque
            numero_saques += 1
            extrato += f"Saque:          R$ {valor_saque:4.2f}\n"
            print("Saque realizado com sucesso!")
    return saldo,extrato,numero_saques


def mostrar_extrato(saldo,/,*,extrato):
    #Extrato:
    #   Deve receber somente por posicao e nome.
    #   Argumentos posicionais: saldo.
    #   Argumentos nomeados: extrato. 
    print(f"{extrato}\n\nSaldo Atual:    R$ {saldo:3.2f}")

def criar_usuario(usuarios):
    #Criar Usuario:
    #   O programa deve armazenar os usuarios em uma lista
    #   Um usuario é composto por: nome, data de nascimento, cpf e endereco.
    #   Endereco é uma string formada por: 'logradouro, numero - bairro - cidade/uf'
    #   Deve ser armazenada somente numero do CPF, e nao podera haver CPFs repetidos.
    usuario = []
    usuario.append(input("Por favor digite o nome do usuario: "))
    usuario.append(input("Por favor digite a data de nascimento do usuario: "))
    cpf = input("Por favor digite o CPF do usuario, somente numeros: ")
    
    for user in usuarios:
        if cpf == user[2]:
            print("CPF já cadastrado")
            return None
        
    usuario.append(cpf)

    endereco = ""
    endereco += input("Digite o logradouro do usuario: ") + ", "
    endereco += input("Digite o numero do usuario: ") + " - "
    endereco += input("Digite o bairro do usuario: ") + " - "
    endereco += input("Digite a cidade do usuario: ") + " / "
    endereco += input("Digite o estado do usuario: ")
    usuario.append(endereco)

    return usuario

def criar_conta_corrente(contas_correntes, cpf_usuario):
    #Criar conta corrente:
    #   O programa deve armazenar contas em uma lista
    #   Uma conta é composta por: agencia, numero da conta e usuario.
    #   O numero da conta é sequencial, iniciando em 1.
    #   O numero da agencia é fixo em '0001'.
    #   O usuario pode ter mais de uma conta, mas uma conta pertence somente a um usuario.
    numero_conta = len(contas_correntes)+1
    agencia = '0001'

    nova_conta = (agencia, f'{numero_conta:06}', cpf_usuario)

    return nova_conta

def listar_contas(contas,cpf_requerido):
    contas_encontradas = []
    for conta in contas:
        if conta[2] ==cpf_requerido:
            contas_encontradas.append(conta)
    return contas_encontradas

while True:
    opcao = input(menu).lower()

    if opcao == "d":
        valor_deposito = float(input("Digite o valor a ser depositado: \n"))
        saldo, extrato = deposito(saldo,valor_deposito,extrato)

    elif opcao == "s":
        valor= float(input("Digite o valor a ser sacado: \n"))
        saldo,extrato,numero_saques = saque(saldo = saldo,numero_saques= numero_saques,valor_limite= limite,valor_saque=valor, extrato=extrato)
        
    elif opcao == "e":
        mostrar_extrato(saldo,extrato=extrato)

    elif opcao == "u":
        novo_usuario = criar_usuario(usuarios)
        if novo_usuario is not None:
            usuarios.append(novo_usuario)

    elif opcao == "c":
        cpf = input("Informe o CPF a ser vinculado: ")
        usuario_encontrado = False
        for user in usuarios:
            if cpf == user[2]:
                usuario_encontrado=True
                nova_conta = criar_conta_corrente(contas_correntes, cpf)
                if nova_conta is not None:
                    contas_correntes.append(nova_conta)
                    print("Conta criada com sucesso!")
                    break
        if not usuario_encontrado:
            print("Usuario nao encontrado")

    elif opcao == "l":
        cpf_requerido = input("Informe o CPF a ser vinculado: ")
        usuario_encontrado = False
        for user in usuarios:
            if cpf_requerido == user[2]:
                usuario_encontrado=True
                contas_usuario = listar_contas(contas_correntes,cpf_requerido)
                for conta in contas_usuario:
                    print(f"Agência: {conta[0]}")
                    print(f"Número da Conta: {conta[1]}")
                    print(f"CPF: {conta[2]}")
                    print()
                break
        if not usuario_encontrado:
            print("Usuario nao encontrado")
        
    elif opcao == "q":
        break

    else:
        print("Opção Inválida, por favor selecione novamente a opção desejada")