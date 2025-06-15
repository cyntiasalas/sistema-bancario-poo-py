# sistema-bancario-poo-py

Sistema Bancário Orientado a Objetos em Python
Este projeto implementa um sistema bancário básico em Python, utilizando os princípios da Programação Orientada a Objetos (POO) conforme um diagrama UML fornecido. O sistema permite a criação de usuários (Pessoas Físicas), contas correntes, e a realização de operações bancárias como depósito, saque e consulta de extrato.

🚀 Funcionalidades
Criação de Usuários: Cadastro de novos clientes como Pessoas Físicas, com informações como nome, CPF, data de nascimento e endereço.
Criação de Contas Correntes: Associação de contas correntes a clientes existentes, com controle de número da conta, agência, limite de saque e número de saques diários.
Depósito: Realização de depósitos em contas, com validação de valores.
Saque: Realização de saques em contas, com validação de saldo, limite por saque e limite diário de saques.
Extrato: Consulta do histórico de transações e saldo atual da conta.
Listagem de Contas: Exibição de todas as contas cadastradas no sistema.
Menu Interativo: Interface de linha de comando para interação com o usuário.

⚙️ Estrutura do Projeto (Classes e Relacionamentos)
O projeto é construído com base nos seguintes conceitos de POO e classes:

Classes Principais:

Cliente: Representa um cliente do banco. Possui um endereço e uma lista de contas associadas. Pode realizar transações em suas contas.

PessoaFisica: Herda de Cliente e adiciona atributos específicos de pessoa física, como nome, data de nascimento e CPF.

Conta: Classe base que representa uma conta bancária. Contém saldo, número da conta, agência, cliente associado e um histórico de transações.

ContaCorrente: Herda de Conta e adiciona funcionalidades específicas de uma conta corrente, como limite de saque por operação e limite de saques diários.

Historico: Responsável por armazenar e gerenciar o registro de todas as transações de uma conta.
Transacao (Classe Abstrata - ABC): Define uma interface para as operações de transação. Possui um valor e um método abstrato registrar().

Deposito: Herda de Transacao e implementa a lógica específica para registrar um depósito.

Saque: Herda de Transacao e implementa a lógica específica para registrar um saque.

Relacionamentos (Conforme Diagrama UML):
Um Cliente pode ter várias Contas (relação 1 para N).
Uma Conta pertence a um Cliente (relação 1 para 1).
Uma Conta possui um Historico (relação 1 para 1).
Um Historico registra várias Transacaos (relação 1 para N).
Deposito e Saque são tipos específicos de Transacao (relação de herança/generalização).


🛠️ Tecnologias Utilizadas
Python 3.x
Módulos padrão: datetime, abc (para classes abstratas)


▶️ Como Executar
Clone o repositório (se estiver em um repositório Git) ou salve o código em um arquivo .py (ex: banco_poo.py).

Execute o arquivo Python a partir do seu terminal:

Bash

python banco_poo.py
Siga as instruções do menu interativo para criar usuários, contas e realizar operações.

