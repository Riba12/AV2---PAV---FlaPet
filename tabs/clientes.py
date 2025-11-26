import os
import requests
from PyQt5.QtWidgets import  QVBoxLayout, QFormLayout, QDialogButtonBox, QLineEdit, QSpinBox, QDoubleSpinBox, QMessageBox, QHeaderView, QTableWidgetItem, QDialog
from PyQt5.QtCore import Qt
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv('API_URL')

class EditCliente(QDialog):
    def __init__(self, dados, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Editar Cliente")
        self.setFixedWidth(350)
        
        # ID para usar no PUT depois
        self.id_cliente = dados['id']

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # 1. Nome
        self.inputNome = QLineEdit()
        self.inputNome.setText(dados['nome']) 
        form_layout.addRow("Nome:", self.inputNome)

        # 2. CPF
        self.inputCpf = QLineEdit()
        self.inputCpf.setText(dados['cpf']) 
        form_layout.addRow("Cpf:", self.inputCpf)

        # 3. Telefone
        self.inputTelefone = QLineEdit()
        self.inputTelefone.setText(dados['telefone']) 
        form_layout.addRow("Telefone:", self.inputTelefone)

        layout.addLayout(form_layout)

        self.botoes = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        self.botoes.accepted.connect(self.salvar)
        self.botoes.rejected.connect(self.reject)
        layout.addWidget(self.botoes)

        self.setLayout(layout)

    def salvar(self):
        payload = {
            "nome": self.inputNome.text().strip(),
            "cpf": self.inputCpf.text().strip(),
            "telefone": self.inputTelefone.text().strip()
        }

        try:
            response = requests.put(f"{API_URL}/clientes/{self.id_cliente}", data=payload)
            if response.status_code == 201: 
                QMessageBox.information(self, "Sucesso", "Cliente atualizado!")
                self.accept()
            else:
                try:
                    erro_json = response.json()
                    msg = erro_json.get('message', str(erro_json))
                except ValueError:
                    msg = response.text
                QMessageBox.warning(self, "Erro API", f"{msg}")
                
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha na conexão: {e}")

class AddCliente(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Novo Cliente")
        self.setFixedWidth(350)

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # 1. Nome
        self.inputNome = QLineEdit()
        self.inputNome.setPlaceholderText("Ex: Fulano de tal")
        form_layout.addRow("Nome:", self.inputNome)

        # 2. CPF
        self.inputCpf = QLineEdit()
        self.inputCpf.setPlaceholderText("Ex: xxx.xxx.xxx-xx")
        form_layout.addRow("CPF:", self.inputCpf)

        # 3. Telefone 
        self.inputTelefone = QLineEdit()
        self.inputTelefone.setPlaceholderText("Ex: (xx) xxxx-xxxx")
        form_layout.addRow("Telefone:", self.inputTelefone)

        layout.addLayout(form_layout)

        # Botões
        self.botoes = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        self.botoes.accepted.connect(self.salvar)
        self.botoes.rejected.connect(self.reject)
        layout.addWidget(self.botoes)

        self.setLayout(layout)

    def salvar(self):
        nome = self.inputNome.text().strip()
        cpf = self.inputCpf.text().strip()
        telefone = self.inputTelefone.text().strip()

        if not nome:
            QMessageBox.warning(self, "Erro", "O nome do serviço é obrigatório!")
            return

        payload = {
            "nome": nome,
            "cpf": cpf,
            "telefone": telefone
        }

        try:
            response = requests.post(f"{API_URL}/clientes", data=payload)
            
            if response.status_code == 201:
                QMessageBox.information(self, "Sucesso", "Cliente cadastrado!")
                self.accept()
            else:
                msg = response.json().get('message', response.text)
                QMessageBox.warning(self, "Erro API", f"{msg}")
                
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha na conexão: {e}")


class Cliente:
    def __init__(self, janela):
        self.janela = janela
        self.configurar_tabela()
        self.carregar_clientes()
        self.conectar_botoes()

    def configurar_tabela(self):
        colunas = ["ID", "Nome", "Cpf", "Telefone"]
        self.janela.tabelaClientes.setColumnCount(len(colunas))
        self.janela.tabelaClientes.setHorizontalHeaderLabels(colunas)

        header = self.janela.tabelaClientes.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents) 
        header.setSectionResizeMode(1, QHeaderView.Stretch)           
        header.setSectionResizeMode(2, QHeaderView.Stretch)           
        header.setSectionResizeMode(3, QHeaderView.Stretch)       

    def conectar_botoes(self):
        self.janela.AtualizaCliBT.clicked.connect(self.atualizar)
        self.janela.AdicionarCliBT.clicked.connect(self.adicionar)
        self.janela.EditarCliBT.clicked.connect(self.editar)
        self.janela.ExcluirCliBT.clicked.connect(self.excluir)

    def atualizar(self):
        self.carregar_clientes()

    def adicionar(self):
        dialog = AddCliente(self.janela)
        if dialog.exec_() == QDialog.Accepted:
            self.carregar_clientes()

    def editar(self):
        linha_selecionada = self.janela.tabelaClientes.currentRow()
        if linha_selecionada < 0:
            QMessageBox.warning(self.janela, "Aviso", "Selecione um cliente para editar.")
            return

        cliente_id = self.janela.tabelaClientes.item(linha_selecionada, 0).text()

        try:
            response = requests.get(f"{API_URL}/clientes/{cliente_id}")
            if response.status_code == 200:
                dados = response.json()
                dialog = EditCliente(dados, self.janela)
                if dialog.exec_() == QDialog.Accepted:
                    self.carregar_clientes()
            else:
                QMessageBox.critical(self.janela, "Erro", "Falha ao buscar dados do cliente.")
        except Exception as e:
            QMessageBox.critical(self.janela, "Erro", f"Ocorreu um erro: {e}")    

    def excluir(self):
        linha_selecionada = self.janela.tabelaClientes.currentRow()
        if linha_selecionada < 0:
            QMessageBox.warning(self.janela, "Aviso", "Selecione um cliente para excluir.")
            return

        cliente_id = self.janela.tabelaClientes.item(linha_selecionada, 0).text()

        confirm = QMessageBox.question(
            self.janela,
            "Confirmação",
            "Tem certeza que deseja excluir este cliente?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            try:
                response = requests.delete(f"{API_URL}/clientes/{cliente_id}")
                if response.status_code == 204:
                    QMessageBox.information(self.janela, "Sucesso", "Cliente excluído com sucesso.")
                    self.carregar_clientes()
                else:
                    QMessageBox.critical(self.janela, "Erro", "Falha ao excluir o cliente.")
            except Exception as e:
                QMessageBox.critical(self.janela, "Erro", f"Ocorreu um erro: {e}")

    def criar_item_centralizado(self, texto):
        item = QTableWidgetItem(str(texto))
        item.setTextAlignment(Qt.AlignCenter)
        return item

    def carregar_clientes(self):
        try:
            response = requests.get(f"{API_URL}/clientes")

            if response.status_code == 200:
                dados = response.json()
                self.janela.tabelaClientes.setRowCount(0)

                for linha_idx, cliente in enumerate(dados):
                    self.janela.tabelaClientes.insertRow(linha_idx)

                    self.janela.tabelaClientes.setItem(linha_idx, 0, self.criar_item_centralizado(cliente['id']))
                    self.janela.tabelaClientes.setItem(linha_idx, 1, self.criar_item_centralizado(cliente['nome']))
                    self.janela.tabelaClientes.setItem(linha_idx, 2, self.criar_item_centralizado(cliente['cpf']))
                    self.janela.tabelaClientes.setItem(linha_idx, 3, self.criar_item_centralizado(cliente['telefone']))
            else:
                QMessageBox.critical(self.janela, "Erro", "Falha ao buscar clientes da API.")
        except Exception as e:
            QMessageBox.critical(self.janela, "Erro", f"Ocorreu um erro: {e}")