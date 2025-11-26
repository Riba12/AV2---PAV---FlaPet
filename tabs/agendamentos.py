import os
import requests
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QHeaderView, QDialog, QVBoxLayout, QFormLayout, QComboBox, QDateTimeEdit, QDialogButtonBox
from PyQt5.QtCore import Qt, QDateTime
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv('API_URL')

class PopUpAgendamento(QDialog):
    def __init__(self, dados=None, parent=None):
        super().__init__(parent)
        
        self.dados = dados
        self.edicao = dados is not None
        titulo = "Editar Agendamento" if self.edicao else "Novo Agendamento"

        self.setWindowTitle(titulo)
        self.setFixedWidth(450)

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.inputAnimal = QComboBox()
        self.inputAnimal.setPlaceholderText("Selecione o animal")
        self.inputAnimal.setEditable(True)
        self.inputAnimal.setInsertPolicy(QComboBox.NoInsert)

        self.inputServico = QComboBox()
        self.inputServico.setPlaceholderText("Selecione o serviço")

        self.inputData = QDateTimeEdit(QDateTime.currentDateTime())
        self.inputData.setCalendarPopup(True)

        self.carregar_animais()
        self.carregar_servicos()

        if self.edicao:
            animal_id = self.inputAnimal.findData(int(dados['animal_id']))
            self.inputAnimal.setCurrentIndex(animal_id)
            servico_id = self.inputServico.findData(int(dados['servico_id']))
            self.inputServico.setCurrentIndex(servico_id)
            self.inputData.setDateTime(QDateTime.fromString(dados['data_hora'], Qt.ISODate))

        form_layout.addRow("Animal:", self.inputAnimal)
        form_layout.addRow("Serviço:", self.inputServico)
        form_layout.addRow("Data e Hora:", self.inputData)

        layout.addLayout(form_layout)

        self.botoes = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        self.botoes.accepted.connect(self.salvar)
        self.botoes.rejected.connect(self.reject)
        layout.addWidget(self.botoes)

        self.setLayout(layout)

    def carregar_animais(self):
        try:           
            response = requests.get(f"{API_URL}/animais")
            if response.status_code == 200:
                dados = response.json()
                self.inputAnimal.clear()
                for animal in dados:
                    self.inputAnimal.addItem(animal['nome'], animal['id'])
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao carregar animais: {e}")

    def carregar_servicos(self):
        try:           
            response = requests.get(f"{API_URL}/servicos")
            if response.status_code == 200:
                dados = response.json()
                self.inputServico.clear()
                for servico in dados:
                    self.inputServico.addItem(servico['nome'], servico['id'])
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao carregar serviços: {e}")

    def salvar(self):
        payload = {
            "animal_id": self.inputAnimal.currentData(),
            "servico_id": self.inputServico.currentData(),
            "data_hora": self.inputData.dateTime().toString(Qt.ISODate)
        }

        try:
            if self.edicao:
                response = requests.put(f"{API_URL}/agendamentos/{self.dados['id']}", data=payload)
                if response.status_code == 200: 
                    QMessageBox.information(self, "Sucesso", "Agendamento atualizado!")
                    self.accept()
            else:
                response = requests.post(f"{API_URL}/agendamentos", data=payload)
                if response.status_code == 201: 
                    QMessageBox.information(self, "Sucesso", "Agendamento adicionado!")
                    self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha na conexão: {e}")


class Agendamento:
    def __init__(self, janela):
        self.janela = janela
        self.configurar_tabela()
        self.carregar_agendamentos()
        self.conectar_botoes()
        

    def configurar_tabela(self):
        colunas = ["ID", "Data", "Animal", "Servico", "Status"]
        self.janela.tabelaAgendamentos.setColumnCount(len(colunas))
        self.janela.tabelaAgendamentos.setHorizontalHeaderLabels(colunas)

        header = self.janela.tabelaAgendamentos.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents) 
        header.setSectionResizeMode(1, QHeaderView.Stretch)           
        header.setSectionResizeMode(2, QHeaderView.Stretch)           
        header.setSectionResizeMode(3, QHeaderView.Stretch)    
        header.setSectionResizeMode(4, QHeaderView.Stretch)           

    def conectar_botoes(self):
        self.janela.AtualizaAgeBT.clicked.connect(self.atualizar)
        self.janela.AdicionarAgeBT.clicked.connect(self.adicionar)
        self.janela.EditarAgeBT.clicked.connect(self.editar)
        self.janela.ExcluirAgeBT.clicked.connect(self.cancelar)
        self.janela.FinalizarAgeBT.clicked.connect(self.finalizar)

    def atualizar(self):
        self.carregar_agendamentos()   

    def adicionar(self):
        popup = PopUpAgendamento(parent=self.janela)
        if popup.exec_() == QDialog.Accepted:
            self.carregar_agendamentos()

    def editar(self):
        linha_selecionada = self.janela.tabelaAgendamentos.currentRow()
        if linha_selecionada < 0:
            QMessageBox.warning(self.janela, "Aviso", "Selecione um agendamento para editar.")
            return
        id_agendamento = self.janela.tabelaAgendamentos.item(linha_selecionada, 0).text()
        try:
            response = requests.get(f"{API_URL}/agendamentos/{id_agendamento}")
            if response.status_code == 200:
                dados = response.json()
                dialog = PopUpAgendamento(dados=dados, parent=self.janela)
                if dialog.exec_() == QDialog.Accepted:
                    self.carregar_agendamentos()
            else:
                QMessageBox.critical(self.janela, "Erro", "Falha ao buscar dados do agendamento.")
        except Exception as e:
            QMessageBox.critical(self.janela, "Erro", f"Ocorreu um erro: {e}")

    def mudar_status(self, novo_status):
        linha_selecionada = self.janela.tabelaAgendamentos.currentRow()
        if linha_selecionada < 0:
            QMessageBox.warning(self.janela, "Aviso", "Selecione um agendamento.")
            return
        id_agendamento = self.janela.tabelaAgendamentos.item(linha_selecionada, 0).text()
        try:
            response = requests.patch(f"{API_URL}/agendamentos/{id_agendamento}", data={'status': novo_status})
            if response.status_code == 200:
                self.carregar_agendamentos()
            else:
                QMessageBox.critical(self.janela, "Erro", f"Falha ao atualizar status do agendamento. {response.text}")
        except Exception as e:
            QMessageBox.critical(self.janela, "Erro", f"Ocorreu um erro: {e}")

    def cancelar(self):
        resp = QMessageBox.question(self.janela, "Cancelar", "Deseja cancelar este agendamento?", QMessageBox.Yes | QMessageBox.No)
        if resp == QMessageBox.Yes:
            self.mudar_status("CANCELADO")

    def finalizar(self):
        resp = QMessageBox.question(self.janela, "Finalizar", "Deseja finalizar este agendamento?", QMessageBox.Yes | QMessageBox.No)
        if resp == QMessageBox.Yes:
            self.mudar_status("CONCLUIDO")

    def criar_item_centralizado(self, texto):
        item = QTableWidgetItem(str(texto))
        item.setTextAlignment(Qt.AlignCenter)
        return item

    def carregar_agendamentos(self):
        try:
            response = requests.get(f"{API_URL}/agendamentos")

            if response.status_code == 200:
                dados = response.json()
                self.janela.tabelaAgendamentos.setRowCount(0)

                for linha_idx, agendamento in enumerate(dados):
                    self.janela.tabelaAgendamentos.insertRow(linha_idx)

                    self.janela.tabelaAgendamentos.setItem(linha_idx, 0, self.criar_item_centralizado(agendamento['id']))
                    self.janela.tabelaAgendamentos.setItem(linha_idx, 1, self.criar_item_centralizado(agendamento['data_hora']))
                    self.janela.tabelaAgendamentos.setItem(linha_idx, 2, self.criar_item_centralizado(agendamento['animal_nome']))
                    self.janela.tabelaAgendamentos.setItem(linha_idx, 3, self.criar_item_centralizado(agendamento['servico_nome']))
                    self.janela.tabelaAgendamentos.setItem(linha_idx, 4, self.criar_item_centralizado(agendamento['status']))

            else:
                QMessageBox.critical(self.janela, "Erro", "Falha ao buscar agendamentos da API.")
        except Exception as e:
            QMessageBox.critical(self.janela, "Erro", f"Ocorreu um erro: {e}")