from datetime import datetime, date

from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QComboBox, QWidget, QPushButton, QMessageBox, QSizePolicy, \
    QLabel, QLineEdit, QTableWidget, QAbstractItemView, QTableWidgetItem, QTextEdit, QHeaderView

from Model.Nota import Nota
from Controller.Nota_Dao import DataBase

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(500, 700)

        self.setWindowTitle('Bloco de Notas')

        self.lbl_id = QLabel('ID')
        self.txt_id = QLineEdit()

        self.txt_id.setVisible(False)
        self.lbl_id.setVisible(False)
        self.txt_id.setReadOnly(False)


        self.lbl_titulo_nota = QLabel('Título da Nota')
        self.txt_titulo_nota = QLineEdit()

        self.lbl_texto = QLabel('Conteúdo')
        self.txt_texto = QTextEdit()

        self.lbl_data = QLabel('Data de Criação da Nota')

        self.btn_salvar = QPushButton('Salvar')
        self.btn_limpar = QPushButton('Limpar')
        self.btn_remover = QPushButton('Remover')
        self.btn_atualizar = QPushButton('Atualizar')

        self.bloco_de_notas = QTableWidget()

        self.bloco_de_notas.setColumnCount(4)
        self.bloco_de_notas.setHorizontalHeaderLabels(['ID', 'Título da Nota', 'Conteúdo', 'Data'])

        header = self.bloco_de_notas.horizontalHeader()
        for i in range(self.bloco_de_notas.columnCount()):
            if i != 2:
                header.setSectionResizeMode(i, QHeaderView.ResizeToContents)


        self.bloco_de_notas.setSelectionMode(QAbstractItemView.NoSelection)
        self.bloco_de_notas.setEditTriggers(QAbstractItemView.NoEditTriggers)

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_id)
        layout.addWidget(self.txt_id)

        layout.addWidget(self.lbl_titulo_nota)
        layout.addWidget(self.txt_titulo_nota)
        layout.addWidget(self.lbl_texto)
        layout.addWidget(self.txt_texto)
        layout.addWidget(self.bloco_de_notas)
        layout.addWidget(self.btn_salvar)
        layout.addWidget(self.btn_limpar)
        layout.addWidget(self.btn_remover)

        self.container = QWidget()
        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setCentralWidget(self.container)
        self.container.setLayout(layout)

        # self.consulta_bloco_notas()
        self.bloco_de_notas.cellDoubleClicked.connect(self.carregar_notas)

        self.btn_remover.setVisible(True)
        self.btn_salvar.clicked.connect(self.salvar_nota)
        self.popula_bloco_de_notas()
        self.btn_remover.clicked.connect(self.remover_nota)

        self.btn_limpar.clicked.connect(self.limpar_campos)
        # self.btn_atualizar.clicked.connect(self.salvar_nota)
        self.popula_bloco_de_notas()

    def remover_nota(self):
        msg = QMessageBox()
        msg.setWindowTitle('Remover Nota')
        msg.setText('Esta nota será removida :)')
        msg.setInformativeText(f'Você deseja remover a nota de ID n° {self.txt_id.text()} ?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.button(QMessageBox.Yes).setText('Sim')
        msg.button(QMessageBox.No).setText('Não')
        resposta = msg.exec()

        if resposta == QMessageBox.Yes:
            db = DataBase()
            retorno = db.deletar_nota(self.txt_id.text())

            if retorno == 'ok':
                new_msg = QMessageBox()
                new_msg.setWindowTitle('Remover Nota')
                new_msg.setText('Nota Removida com sucesso!')
                new_msg.exec()
                self.limpar_campos()

            else:
                new_msg = QMessageBox()
                new_msg.setWindowTitle('Remover nota')
                new_msg.setText('Erro ao remover nota')
                new_msg.exec()

        self.txt_id.setReadOnly(False)
        self.popula_bloco_de_notas()

    def salvar_nota(self):
        db = DataBase()

        id = self.txt_id.text()
        titulo_nota = self.txt_titulo_nota.text()
        data = date.today()
        texto = str(self.txt_texto.toPlainText())

        nota = Nota(id, titulo_nota, texto, data)

        if self.btn_salvar.text() == 'Salvar':
            retorno = db.salvar_nota(nota)

            if retorno == 'ok':
                msg = QMessageBox()
                msg.setWindowTitle('Salvar Nota')
                msg.setText('Nota Salva com sucesso!')
                msg.exec()
                self.limpar_campos()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle('Erro!!!')
                msg.setText(f'Erro ao cadastrar a nota!')
                msg.exec()

        elif self.btn_salvar.text() == 'Atualizar':

            retorno = db.atualizar_nota(nota)
            if retorno == 'ok':
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle('Atualizações')
                msg.setText('Nota Atualizada com Sucesso!')
                msg.exec()
                self.limpar_campos()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle('Erro ao Atualizar!')
                msg.setText('Erro ao Atualizar, verifique os dados!')
                msg.exec()

        self.popula_bloco_de_notas()
        self.txt_id.setReadOnly(True)

    def limpar_campos(self):
        for widget in self.container.children():
            if isinstance(widget, QTextEdit):
                widget.clear()
            elif isinstance(widget, QLineEdit):
                widget.clear()
            elif isinstance(widget, QComboBox):
                widget.setCurrentIndex(0)

            self.btn_remover.setVisible(False)
            self.btn_salvar.setText('Salvar')
            self.txt_id.setReadOnly(True)

            self.txt_id.setVisible(False)
            self.lbl_id.setVisible(False)

    def popula_bloco_de_notas(self):
        self.bloco_de_notas.setRowCount(0)
        db = DataBase()
        lista_notas = db.consultar_bloco()
        self.bloco_de_notas.setRowCount(len(lista_notas))

        for linha, nota in enumerate(lista_notas):
            for coluna, valor in enumerate(nota):
                self.bloco_de_notas.setItem(linha, coluna, QTableWidgetItem(str(valor)))

    def carregar_notas(self, row, column):
        self.txt_id.setText(self.bloco_de_notas.item(row, 0).text())
        self.txt_titulo_nota.setText(self.bloco_de_notas.item(row, 1).text())
        self.txt_texto.setText(self.bloco_de_notas.item(row, 2).text())
        self.btn_salvar.setText('Atualizar')
        self.btn_remover.setVisible(True)

        self.txt_id.setVisible(True)
        self.lbl_id.setVisible(True)
        self.txt_id.setReadOnly(True)

