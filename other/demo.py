# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'demo.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(679, 493)
        self.btn = QtWidgets.QPushButton(Dialog)
        self.btn.setGeometry(QtCore.QRect(450, 230, 92, 28))
        self.btn.setObjectName("btn")
        self.txtBrow = QtWidgets.QTextBrowser(Dialog)
        self.txtBrow.setGeometry(QtCore.QRect(120, 140, 256, 192))
        self.txtBrow.setOpenExternalLinks(True)
        self.txtBrow.setObjectName("txtBrow")
        self.txtEdit = QtWidgets.QTextEdit(Dialog)
        self.txtEdit.setGeometry(QtCore.QRect(180, 30, 104, 71))
        self.txtEdit.setObjectName("txtEdit")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(430, 50, 113, 26))
        self.lineEdit.setObjectName("lineEdit")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.btn.setText(_translate("Dialog", "Connect 96"))
        self.txtBrow.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Microsoft YaHei UI\'; font-size:11.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">默认</p></body></html>"))
