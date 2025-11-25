import os
import requests
from PyQt5.QtWidgets import  QVBoxLayout, QFormLayout, QDialogButtonBox, QLineEdit, QSpinBox, QDoubleSpinBox, QMessageBox, QHeaderView, QTableWidgetItem, QDialog
from PyQt5.QtCore import Qt
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv('API_URL')

class EditServico(QDialog):
    def __init__(self, dados, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Editar Serviço")
        self.setFixedWidth(350)
        
        # ID para usar no PUT depois
        self.id_servico = dados['id']

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # 1. Nome
        self.inputNome = QLineEdit()
        self.inputNome.setText(dados['nome']) 
        form_layout.addRow("Nome:", self.inputNome)

        # 2. Descrição
        self.inputDescricao = QLineEdit()
        self.inputDescricao.setText(dados['descricao']) 
        form_layout.addRow("Descrição:", self.inputDescricao)

        # 3. Valor
        self.inputValor = QDoubleSpinBox()
        self.inputValor.setRange(0, 20000)
        self.inputValor.setPrefix("R$ ")
        self.inputValor.setDecimals(2)
        self.inputValor.setValue(float(dados['valor'])) 
        form_layout.addRow("Valor:", self.inputValor)

        # 4. Tempo
        self.inputTempo = QSpinBox()
        self.inputTempo.setRange(1, 600)
        self.inputTempo.setSuffix(" min")
        self.inputTempo.setValue(int(dados['tempo_minutos'])) 
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
            response = requests.put(f"{API_URL}/servicos/{self.id_servico}", data=payload)
            if response.status_code == 201: 
                QMessageBox.information(self, "Sucesso", "Serviço atualizado!")
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

class AddServico(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Novo Serviço")
        self.setFixedWidth(350)

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # 1. Nome
        self.inputNome = QLineEdit()
        self.inputNome.setPlaceholderText("Ex: Banho e Tosa")
        form_layout.addRow("Nome:", self.inputNome)

        # 2. Descrição
        self.inputDescricao = QLineEdit()
        self.inputDescricao.setPlaceholderText("Ex: Completo com hidratação")
        form_layout.addRow("Descrição:", self.inputDescricao)

        # 3. Valor 
        self.inputValor = QDoubleSpinBox()
        self.inputValor.setRange(0, 20000) 
        self.inputValor.setPrefix("R$ ")
        self.inputValor.setDecimals(2)
        form_layout.addRow("Valor:", self.inputValor)

        # 4. Tempo em Minutos 
        self.inputTempo = QSpinBox()
        self.inputTempo.setRange(1, 600) 
        self.inputTempo.setSuffix(" min")
        self.inputTempo.setValue(30) 
        form_layout.addRow("Duração:", self.inputTempo)

        layout.addLayout(form_layout)

        # Botões
        self.botoes = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        self.botoes.accepted.connect(self.salvar)
        self.botoes.rejected.connect(self.reject)
        layout.addWidget(self.botoes)

        self.setLayout(layout)

    def salvar(self):
        nome = self.inputNome.text().strip()
        descricao = self.inputDescricao.text().strip()
        valor = self.inputValor.value() 
        tempo = self.inputTempo.value() 

        if not nome:
            QMessageBox.warning(self, "Erro", "O nome do serviço é obrigatório!")
            return

        payload = {
            "nome": nome,
            "descricao": descricao,
            "valor": valor,
            "tempo_minutos": tempo
        }

        try:
            response = requests.post(f"{API_URL}/servicos", data=payload)
            
            if response.status_code == 201:
                QMessageBox.information(self, "Sucesso", "Serviço cadastrado!")
                self.accept()
            else:
                msg = response.json().get('message', response.text)
                QMessageBox.warning(self, "Erro API", f"{msg}")
                
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
        dialog = AddServico(self.janela)
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
                dialog = EditServico(dados, self.janela)
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