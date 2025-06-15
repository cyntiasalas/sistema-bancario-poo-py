import datetime


class Transacao:
    """Interface para transações bancárias."""
    def __init__(self, valor):
        self._valor = valor
        self._data = datetime.datetime.now()

    @property
    def valor(self):
        return self._valor

    @property
    def data(self):
        return self._data

    def registrar(self, conta):
        """Método abstrato para registrar a transação na conta."""
        raise NotImplementedError("Método registrar deve ser implementado pela subclasse.")

class Deposito(Transacao):
    """Representa uma transação de depósito."""
    def __init__(self, valor):
        super().__init__(valor)

    def registrar(self, conta):
        """Registra o depósito na conta."""
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)
            return True
        return False

class Saque(Transacao):
    """Representa uma transação de saque."""
    def __init__(self, valor):
        super().__init__(valor)

    def registrar(self, conta):
        """Registra o saque na conta."""
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)
            return True
        return False

# ==================== Classe Historico ====================
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": transacao.data.strftime("%d-%m-%Y %H:%M:%S"),
        })

# ==================== Classe Conta ====================
class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = "0001" # Agência fixa conforme padrão comum
        self._cliente = cliente
        self._historico = Historico()

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
        if valor <= 0:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False
        if valor > self._saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
            return False

        self._saldo -= valor
        print("\n=== Saque realizado com sucesso! ===")
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        self._saldo += valor
        print("\n=== Depósito realizado com sucesso! ===")
        return True

# ==================== Classe ContaCorrente ====================
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500.0, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques
        self._numero_saques = 0

    @property
    def limite(self):
        return self._limite

    @property
    def limite_saques(self):
        return self._limite_saques

    def sacar(self, valor):
        excedeu_limite = valor > self._limite
        excedeu_saques = self._numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
            return False
        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
            return False
        else:
            if super().sacar(valor): # Chama o sacar da classe base
                self._numero_saques += 1
                return True
            return False # Saque falhou na classe base

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

# ==================== Classe Cliente ====================
class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    @property
    def endereco(self):
        return self._endereco

    @property
    def contas(self):
        return self._contas

    def realizar_transacao(self, conta, transacao):
        """
        Realiza uma transação (Depósito ou Saque) na conta do cliente.
        """
        if isinstance(transacao, Transacao):
            if transacao.registrar(conta):
                print(f"\nOperação de {transacao.__class__.__name__} realizada com sucesso!")
            else:
                print(f"\nFalha ao realizar a operação de {transacao.__class__.__name__}.")
        else:
            print("\nTransação inválida. Deve ser uma instância de Deposito ou Saque.")

    def adicionar_conta(self, conta):
        """Adiciona uma conta à lista de contas do cliente."""
        self._contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self._nome = nome
        self._data_nascimento = data_nascimento
        self._cpf = cpf 

    @property
    def nome(self):
        return self._nome

    @property
    def data_nascimento(self):
        return self._data_nascimento

    @property
    def cpf(self):
        return self._cpf

    def __str__(self):
        return f"""\
            Nome:\t\t{self.nome}
            CPF:\t\t{self.cpf}
            Endereço:\t{self.endereco}
        """

# ==================== Funções de Menu Adaptadas para Classes ====================

def menu():
    menu_str = """\n
    =========== MENU ===========
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nu]\tNova conta
    [nc]\tNovo usuário
    [lc]\tListar contas
    [q]\tSair
    => """
    return input(menu_str)

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta. @@@")
        return None

    # Implementação simplificada: escolhe a primeira conta.
    # Em um sistema real, haveria uma seleção de contas se o cliente tiver múltiplas.
    return cliente.contas[0]

def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    if not transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in transacoes:
            print(f"{transacao['tipo']}:\tR$ {transacao['valor']:.2f} ({transacao['data']})")

    print(f"\nSaldo:\t\tR$ {conta.saldo:.2f}")
    print("==========================================")


def criar_usuario(clientes):
    cpf = input("Informe o CPF (somente números): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente com este CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    try:
        # Tenta converter a data para um objeto datetime para validação básica
        datetime.datetime.strptime(data_nascimento, "%d-%m-%Y")
    except ValueError:
        print("\n@@@ Formato de data inválido. Use dd-mm-aaaa. @@@")
        return

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")


def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)

    print("\n=== Conta criada com sucesso! ===")


def listar_contas(contas):
    if not contas:
        print("\n@@@ Nenhuma conta cadastrada. @@@")
        return

    for conta in contas:
        print("=" * 100)
        print(str(conta)) # Chama o método __str__ da ContaCorrente
    print("=" * 100)


# ==================== Função Principal ====================
def main():
    clientes = []
    contas = []
    numero_conta = 1

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nc":
            criar_usuario(clientes)

        elif opcao == "nu":
            criar_conta(numero_conta, clientes, contas)
            numero_conta += 1

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")

if __name__ == "__main__":
    main()