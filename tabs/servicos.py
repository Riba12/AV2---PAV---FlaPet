import os
import requests
from PyQt5.QtWidgets import  QVBoxLayout, QFormLayout, QDialogButtonBox, QLineEdit, QSpinBox, QDoubleSpinBox, QMessageBox, QHeaderView, QTableWidgetItem, QDialog
from PyQt5.QtCore import Qt
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv('API_URL')

class PopUpServico(QDialog):
    def __init__(self, dados=None, parent=None):
        super().__init__(parent)

        self.dados = dados
        self.edicao = dados is not None
        titulo = "Editar Serviço" if self.edicao else "Novo Serviço"

        self.setWindowTitle(titulo)
        self.setFixedWidth(450)

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.inputNome = QLineEdit()
        self.inputNome.setPlaceholderText("Nome do serviço")
        self.inputDescricao = QLineEdit()
        self.inputDescricao.setPlaceholderText("Descrição do serviço")
        self.inputValor = QDoubleSpinBox()
        self.inputValor.setRange(0, 20000)
        self.inputValor.setPrefix("R$ ")
        self.inputValor.setDecimals(2)
        self.inputTempo = QSpinBox()
        self.inputTempo.setRange(1, 600)
        self.inputTempo.setSuffix(" min")

        if self.edicao:
            self.inputNome.setText(dados['nome']) 
            self.inputDescricao.setText(dados['descricao']) 
            self.inputValor.setValue(float(dados['valor'])) 
            self.inputTempo.setValue(int(dados['tempo_minutos'])) 

        form_layout.addRow("Nome:", self.inputNome)
        form_layout.addRow("Descrição:", self.inputDescricao)
        form_layout.addRow("Valor:", self.inputValor)
        form_layout.addRow("Duração:", self.inputTempo)

        layout.addLayout(form_layout)

        self.botoes = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        self.botoes.accepted.connect(self.salvar)
        self.botoes.rejected.connect(self.reject)
        layout.addWidget(self.botoes)

        self.setLayout(layout)

    def salvar(self):
        payload = {
            "nome": self.inputNome.text().strip(),
            "descricao": self.inputDescricao.text().strip(),
            "valor": self.inputValor.value(),
            "tempo_minutos": self.inputTempo.value()
        }

        try:
            if self.edicao:
                response = requests.put(f"{API_URL}/servicos/{self.dados['id']}", data=payload)
                if response.status_code == 201: 
                    QMessageBox.information(self, "Sucesso", "Serviço atualizado!")
                    self.accept()
            else:
                response = requests.post(f"{API_URL}/servicos", data=payload)
                if response.status_code == 201: 
                    QMessageBox.information(self, "Sucesso", "Serviço adicionado!")
                    self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha na conexão: {e}")


class Servicos:
    def __init__(self, janela):
        self.janela = janela
        self.configurar_tabela()
        self.carregar_servicos()
        self.conectar_botoes()

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
    
    def conectar_botoes(self):
        self.janela.AtualizaSerBT.clicked.connect(self.atualizar)
        self.janela.AdicionarSerBT.clicked.connect(self.adicionar)
        self.janela.EditarSerBT.clicked.connect(self.editar)
        self.janela.ExcluirSerBT.clicked.connect(self.excluir)
    
    def atualizar(self):
        self.carregar_servicos()
    
    def adicionar(self):
        dialog = PopUpServico(parent=self.janela)
        if dialog.exec_() == QDialog.Accepted:
            self.carregar_servicos()

    def editar(self):
        linha_selecionada = self.janela.tabelaServicos.currentRow()
        if linha_selecionada < 0:
            QMessageBox.warning(self.janela, "Erro", "Selecione um serviço para editar.")
            return

        id_servico = self.janela.tabelaServicos.item(linha_selecionada, 0).text()

        try:
            response = requests.get(f"{API_URL}/servicos/{id_servico}")
            if response.status_code == 200:
                dados = response.json()
                dialog = PopUpServico(dados=dados, parent=self.janela)
                if dialog.exec_() == QDialog.Accepted:
                    self.carregar_servicos()
            else:
                QMessageBox.warning(self.janela, "Erro", "Falha ao buscar dados do serviço.")
        except Exception as e:
            QMessageBox.critical(self.janela, "Erro", f"Falha na conexão: {e}")

    def excluir(self):
        linha_selecionada = self.janela.tabelaServicos.currentRow()
        if linha_selecionada < 0:
            QMessageBox.warning(self.janela, "Erro", "Selecione um serviço para excluir.")
            return

        id_servico = self.janela.tabelaServicos.item(linha_selecionada, 0).text()

        confirm = QMessageBox.question(self.janela, "Confirmar Exclusão", "Tem certeza que deseja excluir este serviço?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            try:
                response = requests.delete(f"{API_URL}/servicos/{id_servico}")
                if response.status_code == 204:
                    QMessageBox.information(self.janela, "Sucesso", "Serviço excluído com sucesso.")
                    self.carregar_servicos()
                else:
                    QMessageBox.warning(self.janela, "Erro", "Falha ao excluir o serviço.")
            except Exception as e:
                QMessageBox.critical(self.janela, "Erro", f"Falha na conexão: {e}")

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