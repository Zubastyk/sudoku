from PyQt6 import QtGui, QtWidgets
import sys
from modules.mainwindow import MainWindow


app = QtWidgets.QApplication(sys.argv)
app.setWindowIcon(QtGui.QIcon(r"images/svd.png"))
window = MainWindow()
window.show()
sys.exit(app.exec())

"""
    Известные ошибки
    
    не работает красный свет при блокировке
    не работают кнопки от 2 до 9
    нет сетки (границ ячеек)
"""