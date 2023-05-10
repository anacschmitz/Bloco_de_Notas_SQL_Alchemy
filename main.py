
import sys
from PySide6.QtWidgets import QApplication

from View.Tela_bloco_notas import MainWindow


app = QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()