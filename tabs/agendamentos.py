import os
import requests
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QHeaderView
from PyQt5.QtCore import Qt
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv('API_URL')

class Agendamento:
    def __init__(self, janela):
        self.janela = janela
        self.configurar_tabela()
        self.carregar_agendamentos()
        

    def configurar_tabela(self):
        colunas = ["ID", "Data", "Status", "Agendamento", "Animal"]
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
        self.janela.AdicionaAgeBT.clicked.connect(self.adicionar)

    def atualizar(self):
        self.carregar_agendamentos()   

    # def adicionar(self):


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