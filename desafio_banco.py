menu = '''
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair

'''

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUE = 3

while True:
    opcao = input(menu).lower()

    if opcao == "d":
        valor_deposito = float(input("Digite o valor a ser depositado: \n"))
        if(valor_deposito>0):
            saldo += valor_deposito
            extrato += f"Depósito:       R$ {valor_deposito:3.2f}\n"
            print("Valor depositado com sucesso!")
        else:
            print("Valor de Deposito invalido")

    elif opcao == "s":
        valor_saque= float(input("Digite o valor a ser sacado: \n"))
        if (valor_saque <0):
            print("Valor digitado invalido!")
        elif (numero_saques >= LIMITE_SAQUE):
            print("Limite diario de Saques atingido, entre em contato com seu gerente!")
        elif (valor_saque>500):
            print("Valor do saque ultrapassa o limite, entre em contato com seu gerente!")
        else:
            if(valor_saque>saldo):
                print("Saldo insuficiente!")
            else:
                saldo -= valor_saque
                numero_saques += 1
                extrato += f"Saque:          R$ {valor_saque:4.2f}\n"
                print("Saque realizado com sucesso!")

    elif opcao == "e":
        print(f"{extrato}\n\nSaldo Atual:    R$ {saldo:3.2f}")

    elif opcao == "q":
        break
    
    else:
        print("Opção Inválida, por favor selecione novamente a opção desejada")