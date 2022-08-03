from PyQt5.Qt import *
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from demo import Ui_Dialog

class demoRealization(QWidget, Ui_Dialog):

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setWindowTitle("test")
        self.resize(600, 500)
        self.setupUi(self)
        # self.pushButton()
        self.btn.pressed.connect(self.pushButton)


    def pushButton(self):
        text = self.lineEdit.text()
        self.txtEdit.setText(text)
        # self.txtBrow.append("324")
        self.txtBrow.setText(text + " 123")

    def closeEvent(self, QCloseEvent):
        reply = QtWidgets.QMessageBox.question(self, '警告', "确定关闭当前窗口?",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = demoRealization()

    window.show()
    sys.exit(app.exec_())


