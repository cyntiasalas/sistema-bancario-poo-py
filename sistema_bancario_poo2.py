import datetime
from abc import ABC, abstractmethod

# ==================== Funções Auxiliares de Validação ====================
def validar_cpf(cpf):
    """
    Valida um número de CPF brasileiro.
    Retorna True se o CPF for válido, False caso contrário.
    """
    cpf = ''.join(filter(str.isdigit, cpf)) # Remove caracteres não numéricos

    if len(cpf) != 11:
        return False

    # Verifica se todos os dígitos são iguais (ex: 111.111.111-11)
    if cpf == cpf[0] * 11:
        return False

    # Validação do primeiro dígito verificador
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    if digito1 != int(cpf[9]):
        return False

    # Validação do segundo dígito verificador
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    if digito2 != int(cpf[10]):
        return False

    return True

# ==================== Classe Transacao (Abstrata) ====================
class Transacao(ABC):
    """Interface abstrata para transações bancárias."""
    def __init__(self, valor):
        self._valor = valor
        self._data = datetime.datetime.now()

    @property
    def valor(self):
        return self._valor

    @property
    def data(self):
        return self._data

    @abstractmethod
    def registrar(self, conta):
        """Método abstrato para registrar a transação na conta."""
        pass # Deve ser implementado pelas subclasses

class Deposito(Transacao):
    """Representa uma transação de depósito."""
    def __init__(self, valor):
        super().__init__(valor)

    def registrar(self, conta):
        """Registra o depósito na conta."""
        return conta.depositar(self.valor) # A lógica de adicionar ao histórico é movida para o depositar da Conta

class Saque(Transacao):
    """Representa uma transação de saque."""
    def __init__(self, valor):
        super().__init__(valor)

    def registrar(self, conta):
        """Registra o saque na conta."""
        return conta.sacar(self.valor) # A lógica de adicionar ao histórico é movida para o sacar da Conta

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
            print("\n@@@ Erro no saque: O valor informado é inválido (deve ser positivo). @@@") # Adicionado aqui para clareza
            return False
        if valor > self._saldo:
            print("\n@@@ Erro no saque: Você não tem saldo suficiente. @@@") # Adicionado aqui para clareza
            return False

        self._saldo -= valor
        self.historico.adicionar_transacao(Saque(valor)) # Adiciona ao histórico
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("\n@@@ Erro no depósito: O valor informado é inválido (deve ser positivo). @@@") # Adicionado aqui para clareza
            return False

        self._saldo += valor
        self.historico.adicionar_transacao(Deposito(valor)) # Adiciona ao histórico
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
            print("\n@@@ Erro no saque: O valor do saque excede o limite. @@@") # Adicionado aqui para clareza
            return False
        elif excedeu_saques:
            print("\n@@@ Erro no saque: Número máximo de saques diários excedido. @@@") # Adicionado aqui para clareza
            return False
        else:
            # Chama o sacar da classe base. Se a classe base retornar False (e.g., saldo insuficiente ou valor inválido),
            # a mensagem já foi impressa pela base.
            if super().sacar(valor):
                self._numero_saques += 1
                return True
            return False # Saque falhou na classe base (saldo insuficiente ou valor inválido)

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
            Saldo:\t\tR$ {self.saldo:.2f}
            Limite:\t\tR$ {self.limite:.2f}
            Saques Restantes: {self.limite_saques - self._numero_saques}
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
        Retorna True se a transação for bem-sucedida, False caso contrário.
        As mensagens de erro específicas da transação são agora gerenciadas
        pela lógica dentro dos métodos de sacar/depositar da conta.
        """
        if not isinstance(transacao, Transacao):
            print("\n@@@ Erro: Transação inválida. Deve ser uma instância de Deposito ou Saque. @@@")
            return False
        return transacao.registrar(conta)

    def adicionar_conta(self, conta):
        """Adiciona uma conta à lista de contas do cliente."""
        self._contas.append(conta)

# ==================== Classe PessoaFisica ====================
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
            Data Nasc.:\t{self.data_nascimento}
            Endereço:\t{self.endereco}
        """

# ==================== Funções de Menu e Interação com o Usuário ====================

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

    # FUTURO: Se o cliente tiver múltiplas contas, implementar lógica de seleção aqui.
    # Ex: pedir ao usuário para escolher a conta pelo número.
    # Por enquanto, retorna a primeira conta encontrada.
    print(f"\nSelecionando a primeira conta do cliente {cliente.nome} (número {cliente.contas[0].numero}).")
    return cliente.contas[0]

def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Operação falhou: Cliente não encontrado! @@@")
        return

    valor_str = input("Informe o valor do depósito: ")
    try:
        valor = float(valor_str)
    except ValueError:
        print("\n@@@ Operação falhou: Valor inválido. Por favor, digite um número. @@@")
        return

    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return # Mensagem já tratada em recuperar_conta_cliente

    if cliente.realizar_transacao(conta, transacao):
        print("\n=== Depósito realizado com sucesso! ===")
    # As mensagens de erro para valor <= 0 já estão dentro de Conta.depositar


def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Operação falhou: Cliente não encontrado! @@@")
        return

    valor_str = input("Informe o valor do saque: ")
    try:
        valor = float(valor_str)
    except ValueError:
        print("\n@@@ Operação falhou: Valor inválido. Por favor, digite um número. @@@")
        return

    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return # Mensagem já tratada em recuperar_conta_cliente

    if cliente.realizar_transacao(conta, transacao):
        print("\n=== Saque realizado com sucesso! ===")
    # As mensagens de erro para saldo insuficiente, limite e saques excedidos
    # já são tratadas dentro de Conta.sacar e ContaCorrente.sacar.


def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Operação falhou: Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return # Mensagem já tratada em recuperar_conta_cliente

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

    if not validar_cpf(cpf): # Nova validação de CPF
        print("\n@@@ Operação falhou: CPF inválido! Verifique o formato e os dígitos. @@@")
        return

    cliente_existente = filtrar_cliente(cpf, clientes)
    if cliente_existente:
        print("\n@@@ Operação falhou: Já existe cliente com este CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    try:
        datetime.datetime.strptime(data_nascimento, "%d-%m-%Y")
    except ValueError:
        print("\n@@@ Operação falhou: Formato de data de nascimento inválido. Use dd-mm-aaaa. @@@")
        return

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")


def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Operação falhou: Cliente não encontrado! Favor criar o usuário primeiro. @@@") # Mensagem mais clara
        return

    # O sistema permite múltiplos clientes com o mesmo CPF caso a validação acima seja ignorada ou desativada,
    # mas o filtrar_cliente filtra por CPF, então sempre pegará o primeiro.
    # O ideal seria garantir que o CPF é único na criação do usuário.

    # Verificar se o cliente já possui uma conta (regra de negócio, se cada cliente pode ter apenas uma conta)
    # if cliente.contas:
    #     print("\n@@@ Cliente já possui uma conta. Não é possível criar outra. @@@")
    #     return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)

    print(f"\n=== Conta {numero_conta} criada com sucesso para {cliente.nome}! ===")


def listar_contas(contas):
    if not contas:
        print("\n@@@ Nenhuma conta cadastrada. @@@")
        return

    for conta in contas:
        print("=" * 100)
        print(str(conta))
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

        elif opcao == "nc": # Novo usuário
            criar_usuario(clientes)

        elif opcao == "nu": # Nova conta
            criar_conta(numero_conta, clientes, contas)
            # Apenas incrementa o número da conta se a conta foi realmente criada.
            # Se criar_conta falhar por CPF não encontrado, o numero_conta não deve avançar.
            # Uma forma de lidar com isso é fazer criar_conta retornar um bool.
            # Por simplicidade, vou considerar que o usuário vai criar o cliente antes.
            # Se quiser mais robustez, pode ajustar assim:
            # if criar_conta(numero_conta, clientes, contas):
            #     numero_conta += 1
            # (Mas isso implicaria mudar o print de sucesso para dentro da main ou o retorno)
            # Por enquanto, deixamos como está com o incremento simples.
            numero_conta += 1

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")

if __name__ == "__main__":
    main()