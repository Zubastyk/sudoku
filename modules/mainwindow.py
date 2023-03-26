from PyQt6 import QtCore, QtGui, QtWidgets, QtPrintSupport
from modules.widget import Widget


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent, 
                                       flags=QtCore.Qt.WindowType.Window |
                                       QtCore.Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.setWindowTitle("Судоку 2.0.0")
        self.setStyleSheet(
            "QFrame Qpushutton {font-size:10pt; font-family:Veranda;"
            "color:black;font-weight:bold;}"
            "MyLabel {font-size:14pt;font-family:Veranda;"
            "border:2px solid #000000;}")
        self.settings = QtCore.QSettings("Прохоренок и Дронов", "Судоку")
        self.printer = QtPrintSupport.QPrinter()
        self.sudoku = Widget()
        self.setCentralWidget(self.sudoku)
        menuBar = self.menuBar()
        toolBar = QtWidgets.QToolBar()
        
        myMenuFile = menuBar.addMenu("&Файл")
        
        action = myMenuFile.addAction(QtGui.QIcon(r"images/New.png"),
                                      "&Новый", QtGui.QKeySequence("Ctrl+N"), 
                                      self.sudoku.onClearAllCells)
        toolBar.addAction(action)
        action.setStatusTip("Создание новой, пустой головоломки")
        myMenuFile.addSeparator()
        toolBar.addSeparator()
        
        action = myMenuFile.addAction("&Выход",
                            QtGui.QKeySequence("Ctrl+Q"),
                            QtWidgets.QApplication.instance().quit)
        action.setStatusTip("Завершение работы программы")
        
        myMenuEdit = menuBar.addMenu("&Правка")
        
        action = myMenuEdit.addAction("&Блокировать", 
                            QtCore.Qt.Key.Key_F2, self.sudoku.onBlocKCell)
        action.setStatusTip("Блокирование активной ячейки")
        
        action = myMenuEdit.addAction(QtGui.QIcon(r"images/Lock.png"),
                                      "Б&локировать все",
                                      QtCore.Qt.Key.Key_F3,
                                      self.sudoku.onBlockCells)
        toolBar.addAction(action)
        action.setStatusTip("Блокирование всех ячеек")
        
        action = myMenuEdit.addAction("&Разблокировать",
                            QtCore.Qt.Key.Key_F4, self.sudoku.onClearBlockCell)
        action.setStatusTip("Разблокирование активной ячейки")
        
        action = myMenuEdit.addAction(QtGui.QIcon(r"images/Unlock.png"),
                                      "Р&азблокировать все",
                                      QtCore.Qt.Key.Key_F5, 
                                      self.sudoku.onClearBlockCells)
        toolBar.addAction(action)
        action.setStatusTip("Разблокирование всех ячеек")
        
        myMenuAbout = menuBar.addMenu("&Справка")
        
        action = myMenuAbout.addAction("О &программе...", self.aboutProgramm)
        action.setStatusTip("Получение сведений о программе")
        
        action = myMenuAbout.addAction("О &Qt...", self.aboutQt)
        action.setStatusTip("Получение сведений о фреймворке Qt")
        toolBar.setMovable(False)
        toolBar.setFloatable(False)
        self.addToolBar(toolBar)
        statusBar = self.statusBar()
        statusBar.setSizeGripEnabled(False)
        statusBar.showMessage("\"Судоку\" приветствует вас", 20000)
        if self.settings.contains("X") and self.settings.contains("Y"):
            self.move(int(self.settings.value("X")), int(self.settings.value("Y")))
            
    def closeEvent(self, evt):
        g = self.geometry()
        self.settings.setValue("X", g.left())
        self.settings.setValue("Y", g.top())
        
    def aboutProgramm(self):
        QtWidgets.QMessageBox.about(self, "О программе",
                                    "<center>\"Судоку\" v2.0.0<br><br>"
                                    "Программа для просмотра и редактирования судоку<br><br>"
                                    "(c) Прохоренок Н.А., Дронов В.А. 2011-2022 гг.")
        
    def aboutQt(self):
        QtWidgets.QMessageBox.aboutQt(self, title="О фреймфорке Qt")