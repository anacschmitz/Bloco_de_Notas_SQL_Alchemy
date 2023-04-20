
import sys
from PySide6.QtWidgets import QApplication

from Controller.Nota_Dao import DataBase
from View.Tela_bloco_notas import MainWindow

db = DataBase()
db.connect()
db.create_table_notas()
db.close_connection()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()