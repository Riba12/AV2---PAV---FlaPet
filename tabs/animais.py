import os
import requests
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QHeaderView, QDialog, QVBoxLayout, QFormLayout, QLineEdit, QDialogButtonBox, QComboBox
from PyQt5.QtCore import Qt
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv('API_URL')

class PopUpAnimal(QDialog):
    def __init__(self, dados=None, parent=None):
        super().__init__(parent)

        self.dados = dados
        self.edicao = dados is not None
        titulo = "Editar Animal" if self.edicao else "Novo Animal"

        self.setWindowTitle(titulo)
        self.setFixedWidth(450)
        
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Nome
        self.inputNome = QLineEdit()
        self.inputNome.setPlaceholderText("Nome do pet")

        self.inputCliente = QComboBox()
        self.inputCliente.setPlaceholderText("Selecione o dono do pet")
        self.inputCliente.setEditable(True)
        self.inputCliente.setInsertPolicy(QComboBox.NoInsert)
        self.inputEspecie = QComboBox()
        self.inputEspecie.setPlaceholderText("Selecione a espécie")
        self.inputRaca = QComboBox()
        self.inputRaca.setPlaceholderText("Selecione a raça")
        self.inputRaca.setEnabled(False)

        self.carregar_clientes()
        self.carregar_especies()

        # Conecta mudança de espécie para carregar raças
        self.inputEspecie.currentIndexChanged.connect(self.carregar_racas)


        if self.edicao:
            self.inputNome.setText(dados['nome']) 
            cliente = self.inputCliente.findData(int(dados['cliente_id']))
            self.inputCliente.setCurrentIndex(cliente)
            especie = self.inputEspecie.findData(dados['especie_id'])
            self.inputEspecie.setCurrentIndex(especie)
            # Precisa carregar raças antes de setar
            self.carregar_racas()
            raca = self.inputRaca.findData(dados['raca_id'])
            self.inputRaca.setCurrentIndex(raca)

        form_layout.addRow("Dono do Pet:", self.inputCliente)
        form_layout.addRow("Nome:", self.inputNome)
        form_layout.addRow("Espécie:", self.inputEspecie)
        form_layout.addRow("Raça:", self.inputRaca)

        layout.addLayout(form_layout)

        self.botoes = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        self.botoes.accepted.connect(self.salvar)
        self.botoes.rejected.connect(self.reject)
        layout.addWidget(self.botoes)

        self.setLayout(layout)

    def carregar_clientes(self):
        try:
            response = requests.get(f"{API_URL}/clientes")
            if response.status_code == 200:
                dados = response.json()
                self.inputCliente.clear()
                for cliente in dados:
                    self.inputCliente.addItem(cliente['nome'], cliente['id'])
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro: {e}")

    def carregar_especies(self):
        try:
            response = requests.get(f"{API_URL}/especies")
            if response.status_code == 200:
                dados = response.json()
                self.inputEspecie.clear()
                for especie in dados:
                    self.inputEspecie.addItem(especie['nome'], especie['id'])
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro: {e}") 

    def carregar_racas(self):
        especie_id = self.inputEspecie.currentData()
        self.inputRaca.clear()
        if especie_id is None:
            self.inputRaca.setEnabled(False)
            return

        try:
            response = requests.get(f"{API_URL}/racas?especie_id={especie_id}")
            if response.status_code == 200:
                dados = response.json()
                for raca in dados:
                    self.inputRaca.addItem(raca['nome'], raca['id'])
                self.inputRaca.setEnabled(True)  
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro: {e}")

    def salvar(self):
        nome = self.inputNome.text().strip()
        cliente_id = self.inputCliente.currentData()
        especie_id = self.inputEspecie.currentData()
        raca_id = self.inputRaca.currentData()

        if not nome:
            QMessageBox.warning(self, "Erro", "Digite o nome do animal!")
            return
        if not cliente_id:
            QMessageBox.warning(self, "Erro", "Selecione um dono (cliente) da lista!")
            return
        if not especie_id or not raca_id:
            QMessageBox.warning(self, "Erro", "Selecione Espécie e Raça!")
            return
        
        payload = {
            "nome": nome,
            "cliente_id": cliente_id,
            "especie_id": especie_id,
            "raca_id": raca_id
        }

        try:
            if self.edicao:
                response = requests.put(f"{API_URL}/animais/{self.dados['id']}", data=payload)
                if response.status_code == 201: 
                    QMessageBox.information(self, "Sucesso", "Animal atualizado!")
                    self.accept()
            else:
                response = requests.post(f"{API_URL}/animais", data=payload)
                if response.status_code == 201: 
                    QMessageBox.information(self, "Sucesso", "Animal adicionado!")
                    self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha na conexão: {e}")


class Animal:
    def __init__(self, janela):
        self.janela = janela
        self.configurar_tabela()
        self.carregar_animais()
        self.conectar_botoes()

    def configurar_tabela(self):
        colunas = ["ID", "Nome", "Cliente", "Espécie", "Raça"]
        self.janela.tabelaAnimais.setColumnCount(len(colunas))
        self.janela.tabelaAnimais.setHorizontalHeaderLabels(colunas)

        header = self.janela.tabelaAnimais.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents) 
        header.setSectionResizeMode(1, QHeaderView.Stretch)           
        header.setSectionResizeMode(2, QHeaderView.Stretch)           
        header.setSectionResizeMode(3, QHeaderView.Stretch)    
        header.setSectionResizeMode(4, QHeaderView.Stretch)     

    def conectar_botoes(self):
        self.janela.AtualizaAniBT.clicked.connect(self.atualizar)
        self.janela.AdicionarAniBT.clicked.connect(self.adicionar)
        self.janela.EditarAniBT.clicked.connect(self.editar)
        self.janela.ExcluirAniBT.clicked.connect(self.excluir)      

    def atualizar(self):
        self.carregar_animais()
    
    def adicionar(self):
        dialog = PopUpAnimal(parent=self.janela)
        dialog.carregar_clientes()
        dialog.carregar_especies()
        dialog.inputEspecie.currentIndexChanged.connect(dialog.carregar_racas)
        if dialog.exec_() == QDialog.Accepted:
            self.carregar_animais()
       
    def editar(self):
        linha_selecionada = self.janela.tabelaAnimais.currentRow()
        if linha_selecionada < 0:
            QMessageBox.warning(self.janela, "Aviso", "Selecione um animal para editar.")
            return

        animal_id = self.janela.tabelaAnimais.item(linha_selecionada, 0).text()

        try:
            response = requests.get(f"{API_URL}/animais/{animal_id}")
            if response.status_code == 200:
                dados = response.json()
                dialog = PopUpAnimal(dados=dados, parent=self.janela)
                dialog.carregar_clientes()
                dialog.carregar_especies()
                dialog.inputEspecie.currentIndexChanged.connect(dialog.carregar_racas)
                if dialog.exec_() == QDialog.Accepted:
                    self.carregar_animais()
            else:
                QMessageBox.critical(self.janela, "Erro", "Falha ao buscar dados do animal na API.")
        except Exception as e:
            QMessageBox.critical(self.janela, "Erro", f"Ocorreu um erro: {e}")

    def excluir(self):
        linha_selecionada = self.janela.tabelaAnimais.currentRow()
        if linha_selecionada < 0:
            QMessageBox.warning(self.janela, "Aviso", "Selecione um animal para excluir.")
            return

        animal_id = self.janela.tabelaAnimais.item(linha_selecionada, 0).text()

        try:
            response = requests.delete(f"{API_URL}/animais/{animal_id}")
            if response.status_code == 204:
                QMessageBox.information(self.janela, "Sucesso", "Animal excluído com sucesso.")
                self.carregar_animais()
            else:
                QMessageBox.critical(self.janela, "Erro", "Falha ao excluir o animal na API.")
        except Exception as e:
            QMessageBox.critical(self.janela, "Erro", f"Ocorreu um erro: {e}")

    def criar_item_centralizado(self, texto):
        item = QTableWidgetItem(str(texto))
        item.setTextAlignment(Qt.AlignCenter)
        return item

    def carregar_animais(self):
        try:
            response = requests.get(f"{API_URL}/animais")

            if response.status_code == 200:
                dados = response.json()
                self.janela.tabelaAnimais.setRowCount(0)

                for linha_idx, animal in enumerate(dados):
                    self.janela.tabelaAnimais.insertRow(linha_idx)

                    self.janela.tabelaAnimais.setItem(linha_idx, 0, self.criar_item_centralizado(animal['id']))
                    self.janela.tabelaAnimais.setItem(linha_idx, 1, self.criar_item_centralizado(animal['nome']))
                    self.janela.tabelaAnimais.setItem(linha_idx, 2, self.criar_item_centralizado(animal['cliente_nome']))
                    self.janela.tabelaAnimais.setItem(linha_idx, 3, self.criar_item_centralizado(animal['especie_nome']))
                    self.janela.tabelaAnimais.setItem(linha_idx, 4, self.criar_item_centralizado(animal['raca_nome']))

            else:
                QMessageBox.critical(self.janela, "Erro", "Falha ao buscar animais da API.")
        except Exception as e:
            QMessageBox.critical(self.janela, "Erro", f"Ocorreu um erro: {e}")