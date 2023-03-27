from PyQt6 import QtCore, QtGui, QtWidgets, QtPrintSupport
import re
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
        
        action = myMenuFile.addAction(QtGui.QIcon(r"images/Open.png"),
                                      "&Открыть...", QtGui.QKeySequence("Ctrl+O"), 
                                      self.onOpenFile)
        toolBar.addAction(action)
        action.setStatusTip("Загрузка головоломки из файла")
        
        action = myMenuFile.addAction(QtGui.QIcon(r"images/Save.png"),
                                      "Со&хранить...", QtGui.QKeySequence("Ctrl+S"), 
                                      self.onSave)
        toolBar.addAction(action)
        action.setStatusTip("Сохранение головоломки в файле")
        
        action = myMenuFile.addAction("&Сохранить кмпактно...", QtGui.QKeySequence("Ctrl+O"), 
                                      self.onSaveMini)
        action.setStatusTip("Сохранение головоломки в компактномформате")
        
        myMenuFile.addSeparator()
        toolBar.addSeparator()
        
        action = myMenuFile.addAction("&Выход",
                            QtGui.QKeySequence("Ctrl+Q"),
                            QtWidgets.QApplication.instance().quit)
        action.setStatusTip("Завершение работы программы")
        
        myMenuEdit = menuBar.addMenu("&Правка")
        
        action = myMenuEdit.addAction(QtGui.QIcon(r"images/Copy.png"),
                            "К&опировать", QtGui.QKeySequence("Ctrl+C"),
                            self.onCopyData)
        toolBar.addAction(action)
        action.setStatusTip("Кoпиpoвание гоnоволомки в буфер обмена")

        action = myMenuEdit.addAction("&Кoпиpoвaть компактно",
                                        self.onCopyDataMini)
        action.setStatusTip ("Копирование в компактном формате")
        
        action = myMenuEdit.addAction("Koпиpoвaть &для Excel",
                                        self.onCopyDataExcel)
        action.setStatusTip("Кoпиpoвaниe в формате МS Excel")

        action = myMenuEdit.addAction(QtGui.QIcon(r"images/Paste.png"),
                            "&Вставить", 
                            QtGui.QKeySequence("Ctrl+V"),
                            self.onPasteData)
        toolBar.addAction(action)
        action.setStatusTip("Вставка гоnоволомки из буфера обмена")

        action = myMenuEdit.addAction("Вcтaвить &из Excel",
                            self.onPasteDataExcel)
        action.setStatusTip("Вставка гоnоволомки из МS Excel")
        
        myMenuEdit.addSeparator()
        toolBar.addSeparator()
              
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
            
    def onCopyData(self):
        QtWidgets.QApplication.clipboard().setText(
            self.sudoku.getDataAllCells())
    
    def onCopyDataMini(self):
        QtWidgets.QApplication.clipboard().setText(
            self.sudoku.getDataAllCellsMini())
        
    def onCopyDataExcel(self):
        QtWidgets.QApplication.clipboard().setText(
            self.sudoku.getDataAllCellsExcel())
        
    def onPasteData(self):
        data = QtWidgets.QApplication.clipboard().text()
        if data:
            if len(data) == 81 or len(data) == 162:
                r = re.compile(r"[^0-9]")
                if not r.match(data):
                    self.sudoku.setDataAllCells(data)
                    return
        self.dataErrorMsg()
    
    def onPasteDataExcel(self):
        data = QtWidgets.QApplication.clipboard().text()
        if data:
            data = data.replace("\r", "") 
            r = re.compile(r"([0-9]?[\t\n]){81}")
            if r.match(data):
                result = []
                if data[-1] == "\n":
                   data = data[:-1]
                dl = data.split("\n")
                for sl in dl:
                    dli = sl.split("\t")
                    for sli in dli:
                        if len(sli) == 0:
                            result.append("00")
                        else:
                            result.append("0" + sli[0])
                data = "".join(result)
                self.sudoku.setDataAllCells(data)
                return
        self.dataErrorMsg() 
    
    def onOpenFile(self):
        fileName = QtWidgets.QFileDialog.getOpenFileName(self,
                    "Выберите файл", QtCore.QDir.homePath(),
                    "Судоку(*.svd)")[0]
        if fileName:
            data = ""
            try:
                with open(fileName, newline="") as f:
                    data = f.read()
            except:
                QtWidgets.QMessageBox.information(self, "Судоку",
                          "Не удалось открыть файл")
                return
            if len(data) > 2:
                if data[-1] == "\n":
                    data = data[:-1]
                if len(data) == 81 or len(data) == 162:
                    r = re.compile(r"[^0-9]")
                    if not r.match(data):
                        self.sudoku.setDataAllCells(data)
                        return
            self.dataErrorMsg()
            
    def onSave(self):
        self.saveSVDFile(self.sudoku.getDataAllCells())        
        
    def onSaveMini(self):
        self.saveSVDFile(self.sudoku.getDataAllCellsMini())
        
    def saveSVDFile(self, data):
        fileName = QtWidgets.QFileDialog.getSaveFileName(self,
                    "Выберите файл", QtCore.QDir.homePath(),
                    "Судоку(*.svd)")[0]
        if fileName:
            try:
                with open(fileName, mode="w", newline="") as f:
                    f.write(data)
                self.statusBar().showMessage("Файл сохранен", 10000)
            except:
                QtWidgets.QMessageBox.information(self, "Судоку",
                            "Не удалось сохранить файл")
                
                
            
    
    def dataErrorMsg(self):
        QtWidgets.QMessageBox.information(self, "Судоку",
                "Данные имеют неправильный формат")
    
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