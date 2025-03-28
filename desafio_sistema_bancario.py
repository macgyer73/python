import textwrap
from datetime import datetime

class SistemaBancario:
    def __init__(self):
        self.contas = {}  # Dicionário para armazenar as contas (CPF como chave)
        self.LIMITE_SAQUES = 3 #definido limete de 3 saques por dia 
        self.LIMITE_VALOR_SAQUE = 500.00 #definido valor maximo para saque 
        self.conta_selecionada = None  # Armazena a conta atualmente selecionada

    def menu_principal(self): # menu principal, para cadastrar uma conta nova, listar contas e selecionar a conta para operações 
        menu = """\n
        ================ Menu Principal ================
        [1]\tNova conta
        [2]\tListar contas
        [3]\tSelecionar conta 
        [q]\tSair do Sistema
        
        => """
        return input(textwrap.dedent(menu))

    def menu_conta(self): # menu da conta para manipular a conta selecionada, aqui pode fazer deposito, saque ver extrato , dados da conta e trocar a senha 
        menu = """\n
        ================ Sua Conta ================
        [1]\tSaque
        [2]\tDepósito
        [3]\tExtrato 
        [4]\tTrocar a Senha
        [5]\tMeus Dados
        [q]\tVoltar ao Menu Principal

        => """
        return input(textwrap.dedent(menu))

    def criar_conta(self):
        """Cria uma nova conta bancária com informações completas do cliente"""
        print("\n--- Nova Conta ---")
        cpf = input("Informe o CPF (somente números): ")
        
        if cpf in self.contas:
            print("\nCPF já cadastrado!")
            return False
        
        senha = input("Crie uma senha de 4 digitos: ")
        nome = input("Nome completo: ")
        telefone = input("Telefone no formato xx-xxxx-xxxx: ")
        endereco = input("Endereço: no formato Rua, numero, Bairro, Cidade/Estado:  ")
        
        # Validação simples dos campos obrigatórios
        if not cpf or not senha or not nome:
            print("\nCPF, senha e nome são obrigatórios!")
            return False
        
        # Gera um número de conta aleatório (simplificado)
        numero_conta = str(len(self.contas) + 1000)
        
        # Armazena os dados da conta
        self.contas[cpf] = {
            'senha': senha,
            'conta': numero_conta,
            'saldo': 0.0,
            'extrato': [],
            'dados_cliente': {
                'nome': nome,
                'telefone': telefone,
                'endereco': endereco
            },
            'saques_hoje': 0,
            'ultimo_dia_saque': None
        }
        
        print(f"\nConta criada com sucesso para {nome}!")
        print(f"Número da conta: {numero_conta}")
        return True
    
    def listar_contas(self):
        """Lista todas as contas cadastradas"""
        print("\n--- Contas Cadastradas ---")
        if not self.contas:
            print("Nenhuma conta cadastrada.")
            return
        
        for cpf, conta in self.contas.items():
            print(f"CPF: {cpf} | Conta: {conta['conta']} | Nome: {conta['dados_cliente']['nome']}")
    
    def selecionar_conta(self):
        """Seleciona uma conta para operações"""
        print("\n--- Acessar Conta ---")
        cpf = input("Informe o CPF: ")
        senha = input("Informe a senha: ")
        
        conta = self.acessar_conta(cpf, senha)
        if conta:
            self.conta_selecionada = cpf
            print(f"\nBem-vindo(a), {conta['dados_cliente']['nome']}!")
            return True
        return False
    
    def resetar_contador_saques(self, conta):
        """Reseta o contador de saques se for um novo dia"""
        hoje = datetime.now().day
        if conta['ultimo_dia_saque'] != hoje:
            conta['saques_hoje'] = 0
            conta['ultimo_dia_saque'] = hoje
    
    def acessar_conta(self, cpf, senha):
        """Acessa uma conta existente"""
        if cpf not in self.contas:
            print("\nCPF não cadastrado!")
            return None
        
        if self.contas[cpf]['senha'] != senha:
            print("\nSenha incorreta!")
            return None
        
        return self.contas[cpf]
    
    def trocar_senha(self):
        """Altera a senha da conta"""
        if not self.conta_selecionada:
            print("\nNenhuma conta selecionada!")
            return False
        
        senha_atual = input("Informe a senha atual: ")
        nova_senha = input("Crie uma nova senha: ")
        
        conta = self.acessar_conta(self.conta_selecionada, senha_atual)
        if conta:
            if senha_atual == nova_senha:
                print("\nA nova senha não pode ser igual à senha atual!")
                return False
            
            conta['senha'] = nova_senha
            print("\nSenha alterada com sucesso!")
            return True
        return False
    
    def consultar_saldo(self):
        """Consulta o saldo da conta"""
        if not self.conta_selecionada:
            print("\nNenhuma conta selecionada!")
            return None
        
        conta = self.contas[self.conta_selecionada]
        print(f"\nSaldo atual: R$ {conta['saldo']:.2f}")
        return conta['saldo']
    
    def consultar_extrato(self):
        """Mostra o extrato da conta"""
        if not self.conta_selecionada:
            print("\nNenhuma conta selecionada!")
            return None
        
        conta = self.contas[self.conta_selecionada]
        print("\n--- Extrato Bancário ---")
        print(f"Conta: {conta['conta']}")
        print(f"Cliente: {conta['dados_cliente']['nome']}")
        print("\nÚltimas movimentações:")
        
        if not conta['extrato']:
            print("Nenhuma movimentação registrada.")
        else:
            for mov in conta['extrato']:
                print(f"{mov['data']} - {mov['tipo']}: R$ {mov['valor']:.2f}")
        
        print(f"\nSaldo atual: R$ {conta['saldo']:.2f}")
        return conta['extrato']
    
    def consultar_dados_cliente(self):
        """Consulta os dados cadastrais do cliente"""
        if not self.conta_selecionada:
            print("\nNenhuma conta selecionada!")
            return None
        
        conta = self.contas[self.conta_selecionada]
        dados = conta['dados_cliente']
        print("\n--- Meus Dados ---")
        print(f"Nome: {dados['nome']}")
        print(f"CPF: {self.conta_selecionada}")
        print(f"Telefone: {dados['telefone']}")
        print(f"Endereço: {dados['endereco']}")
        print(f"Número da conta: {conta['conta']}")
        return dados
    
    def depositar(self):
        """Realiza um depósito"""
        if not self.conta_selecionada:
            print("\nNenhuma conta selecionada!")
            return False
        
        try:
            valor = float(input("Informe o valor do depósito: "))
        except ValueError:
            print("\nValor inválido!")
            return False
            
        if valor <= 0:
            print("\nO valor do depósito deve ser positivo!")
            return False
            
        conta = self.contas[self.conta_selecionada]
        conta['saldo'] += valor
        conta['extrato'].append({
            'data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            'tipo': 'Depósito',
            'valor': valor
        })
        print(f"\nDepósito de R$ {valor:.2f} realizado com sucesso!")
        return True
    
    def sacar(self):
        """Realiza um saque com as novas regras"""
        if not self.conta_selecionada:
            print("\nNenhuma conta selecionada!")
            return False
            
        try:
            valor = float(input("Informe o valor do saque: "))
        except ValueError:
            print("\nValor inválido!")
            return False
        
        conta = self.contas[self.conta_selecionada]
        
        # Verifica se é um novo dia para resetar o contador
        self.resetar_contador_saques(conta)
        
        # Verifica as regras de saque
        if valor <= 0:
            print("\nO valor do saque deve ser positivo!") # impedir inserção valores negativos 
            return False
            
        if valor > self.LIMITE_VALOR_SAQUE:
            print(f"\nValor máximo por saque é R$ {self.LIMITE_VALOR_SAQUE:.2f}!") #checa valor definido pelo banco de valor maximo de saque
            return False
            
        if conta['saques_hoje'] >= self.LIMITE_SAQUES: # verifica limite de saques diarios estabelecidos
            print(f"\nLimite de {self.LIMITE_SAQUES} saques diários atingido!")
            return False
            
        if conta['saldo'] < valor:
            print("\nSaldo insuficiente!")
            return False
            
        # Efetua o saque
        conta['saldo'] -= valor
        conta['saques_hoje'] += 1
        conta['extrato'].append({
            'data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), #data e hora  no saque
            'tipo': 'Saque',
            'valor': -valor
        })
        print(f"\nSaque de R$ {valor:.2f} realizado com sucesso!")
        print(f"Saques realizados hoje: {conta['saques_hoje']}/{self.LIMITE_SAQUES}")
        return True

    def executar(self):
        """Método principal que executa o sistema bancário"""
        while True:
            opcao = self.menu_principal().lower()
            
            if opcao == "1":
                self.criar_conta()
            elif opcao == "2":
                self.listar_contas()
            elif opcao == "3":
                if self.selecionar_conta():
                    self.operacoes_conta()
            elif opcao == "q":
                print("\nSistema encerrado. Até logo!")
                break
            else:
                print("\nOpção inválida! Por favor, selecione novamente.")
    
    def operacoes_conta(self):
        """Menu de operações da conta selecionada"""
        while True:
            opcao = self.menu_conta().lower()
            
            if opcao == "1":
                self.sacar()
            elif opcao == "2":
                self.depositar()
            elif opcao == "3":
                self.consultar_extrato()
            elif opcao == "4":
                self.trocar_senha()
            elif opcao == "5":
                self.consultar_dados_cliente()
            elif opcao == "q":
                self.conta_selecionada = None
                print("\nVoltando ao menu principal...")
                break
            else:
                print("\nOpção inválida! Por favor, selecione novamente.")


# Execução do sistema
if __name__ == "__main__":
    sistema = SistemaBancario()
    sistema.executar()