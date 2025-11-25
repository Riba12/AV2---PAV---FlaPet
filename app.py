import sys
from PyQt5 import QtWidgets, uic
import os
from dotenv import load_dotenv
from tabs.clientes import Cliente
from tabs.servicos import Servicos
from tabs.animais import Animal
from tabs.agendamentos import Agendamento

load_dotenv()

class SistemaPetShop(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        uic.loadUi('interface.ui', self)

        self.clientes_tab = Cliente(self)
        self.servicos_tab = Servicos(self)
        self.animais_tab = Animal(self)
        self.agendamentos_tab = Agendamento(self)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    janela = SistemaPetShop()
    janela.show()
    sys.exit(app.exec_())