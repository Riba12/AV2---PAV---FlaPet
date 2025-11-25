import os
import requests
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QHeaderView
from PyQt5.QtCore import Qt
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv('API_URL')

class Servicos:
    def __init__(self, janela):
        self.janela = janela
        self.configurar_tabela()
        self.carregar_servicos()

    def configurar_tabela(self):
        colunas = ["ID", "Nome", "Descrição", "Valor", "Tempo"]
        self.janela.tabelaServicos.setColumnCount(len(colunas))
        self.janela.tabelaServicos.setHorizontalHeaderLabels(colunas)

        header = self.janela.tabelaServicos.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents) 
        header.setSectionResizeMode(1, QHeaderView.Stretch)           
        header.setSectionResizeMode(2, QHeaderView.Stretch)           
        header.setSectionResizeMode(3, QHeaderView.Stretch)    
        header.setSectionResizeMode(4, QHeaderView.Stretch)           
       

    def criar_item_centralizado(self, texto):
        item = QTableWidgetItem(str(texto))
        item.setTextAlignment(Qt.AlignCenter)
        return item

    def carregar_servicos(self):
        try:
            response = requests.get(f"{API_URL}/servicos")

            if response.status_code == 200:
                dados = response.json()
                self.janela.tabelaServicos.setRowCount(0)

                for linha_idx, servico in enumerate(dados):
                    self.janela.tabelaServicos.insertRow(linha_idx)

                    self.janela.tabelaServicos.setItem(linha_idx, 0, self.criar_item_centralizado(servico['id']))
                    self.janela.tabelaServicos.setItem(linha_idx, 1, self.criar_item_centralizado(servico['nome']))
                    self.janela.tabelaServicos.setItem(linha_idx, 2, self.criar_item_centralizado(servico['descricao']))
                    self.janela.tabelaServicos.setItem(linha_idx, 3, self.criar_item_centralizado(f"R$ {servico['valor']}"))
                    self.janela.tabelaServicos.setItem(linha_idx, 4, self.criar_item_centralizado(f"{servico['tempo_minutos']} min"))

            else:
                QMessageBox.critical(self.janela, "Erro", "Falha ao buscar servicos da API.")
        except Exception as e:
            QMessageBox.critical(self.janela, "Erro", f"Ocorreu um erro: {e}")