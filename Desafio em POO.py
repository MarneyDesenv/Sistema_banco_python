from abc import ABC,    abstractclassmethod, abstractproperty
from datetime import datetime
import textwrap

class cliente:
    def _init_(self, endereco):
        self.endereco = endereco
        self.contas = []
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    def adicionar_conta(self,conta):
        self.contas.append(conta)        


class pessoafisica(cliente):
    def _init_(self,nome, data_nascimento, cpf, endereco):
        super()._init_(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class conta:
    def _init_(self, numero , cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = historico()
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
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

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo


        if excedeu_saldo:
            print("\n@@@ operação falhou! você não tem saldo suficiente. @@@")

        elif valor > 0:
            self._saldo -= valor
            print ("\n saque realizado com sucesso!") 
            return True

        else:
            print ("\n operação falhou! o valor informado é invalido")

        return False

    def depositar(self, valor):
        if valor > 0 :
            self._saldo += valor       
            print("\n deposito realizado com sucesso!")

        else:
            print ("\n operação falhou! o valor informado é invalido")
            return False

        return True                

class contacorrente(conta):
    def _init_ (self, numero , cliente, limite = 500, limite_saque = 3):
        super()._init_(numero , cliente)
        self.limite = limite
        self.limite_saque = limite_saque

    def sacar(self, valor):
        numero_saque = len(
            [
            transacao for transacao in self.historico.
            transacoes if transacao ["tipo"] ==saque.
            __name__]
        )
       

        excedeu_limite = valor > self.limite
        excedeu_saque = numero_saque >= self.limite_saque


        if excedeu_limite:
            print("\n operação falhou! o vlaor do saque excede o limite.")

        elif excedeu_saque:
            print("\n operação falhou! numero máximo de saques excedido") 

        else:
            return super(). sacar(valor)

        return False   
        
    def _str_(self):
        return f"""\
             agencia:\t{self.agencia}
             c/c:\t\t{self.numero}
             titular:\t{self.cliente.nome}
        """     
        
               

class historico:
    def _init_ (self):
        self.transacoes = []

    @property
    def transacoes(self):
        return self._transacoes 

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao._class_._name_,
                "valor": transacao.valor,
                "data": datetime.now().strftime
                ("%d-%m-%y %H:%M:%s"),
            }
        )   

class transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass


class saque(transacao):
    def _init_(self, valor):
        self._valor = valor

    @property
    def valor (self):
        return self._valor

    def registrar(self , cconta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)    

class deposito(transacao):
    def _init_ (self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

    
def menu():
    menu = """\n
    ========menu=======
    [D] \t depositar 
    [S] \t sacar
    [E] \t extrato
    [NC]\t nova conta
    [LC]\t listar contas
    [NU]\t novo usuario
    [Q]\t sair
    """
    return input(textwrap.dedent(menu))

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n cliente não possui conta!")
        return
    
    # fixme: não permite cliente escolher conta
    return cliente.contas[0]



def depositar(clientes):
    cpf = input ("informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not clientes:
        print("\n  cliente não encontrado!")
        return
    
    Valor = float(input("informe o valor do deposito: "))
    transacao = deposito(Valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf , clientes)

    if not cliente:
        print ("\n cliente não encontrado!")
        return

    valor = float(input("informe o valor do saque:"))
    transacao = saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cpf = input ("informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf , clientes)

    if not cliente:
        print("\n cliente não encontrado!")
        return

    conta = recuperar_conta_cliente(clientes)
    if not conta:
        return

    print ("\n ============extrato===========")  
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "não foram realizadas movimentações."

    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\ R$
            {transacao['valor']:.2f}"

    print (extrato)
    print(f"\n saldo:\n\tR$ {conta.saldo:.2f}")
    print("===================================")


def criar_cliente(clientes):
    cpf = input("informe o CPF (somente numero):")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n já existe cliente com esse CPF")
        return

    nome = input("informe o nome completo:")
    data_nascimento = input("informe a data de nascimento (dd - mm - aaaa):") 
    endereco = input ("informe o endereço (logradouro, nro - bairro - cidade\sigla estado):") 

    cliente = pessoafisica(nome = nome,
    data_nascimento = data_nascimento, cpf =  cpf,
    endereco = endereco)

    clientes.append(cliente)

    print("\n ==== cliente criado com successo ==== ")


def criar_conta(numero_conta, clientes, contas):
    cpf = input("informe o CPF do cliente:")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print ("\n cliente não encontrado, fluxo de criação de conta encerrado")
        return

    conta =  contacorrente.nova_conta(cliente = cliente,
    numero = numero_conta) 
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n =====conta criada com sucesso!======")

def listar_contas(contas):
    for conta in contas:
        print ("=" * 100)
        print (textwrap.dedent(str(conta)))

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu

        if opcao == "D":
            depositar(clientes)

        elif opcao == "S":
            sacar(clientes)
        elif opcao == "E":
            exibir_extrato(clientes)
        elif opcao == "NU":
            criar_cliente(clientes)
        elif opcao == "NC":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        elif opcao == "LC":
            listar_contas(contas)
        elif opcao =="Q":
            break
        else:
            print("\n operação invalida, por favor selecione novamente a operação desejada.")      

main()              
