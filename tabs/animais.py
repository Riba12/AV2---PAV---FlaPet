import os
import requests
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QHeaderView
from PyQt5.QtCore import Qt
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv('API_URL')

class Animal:
    def __init__(self, janela):
        self.janela = janela
        self.configurar_tabela()
        self.carregar_animais()

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