import os
import requests
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QHeaderView
from PyQt5.QtCore import Qt
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv('API_URL')

class Cliente:
    def __init__(self, janela):
        self.janela = janela
        self.configurar_tabela()
        self.carregar_clientes()

    def configurar_tabela(self):
        colunas = ["ID", "Nome", "Cpf", "Telefone"]
        self.janela.tabelaClientes.setColumnCount(len(colunas))
        self.janela.tabelaClientes.setHorizontalHeaderLabels(colunas)

        header = self.janela.tabelaClientes.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents) 
        header.setSectionResizeMode(1, QHeaderView.Stretch)           
        header.setSectionResizeMode(2, QHeaderView.Stretch)           
        header.setSectionResizeMode(3, QHeaderView.Stretch)           

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