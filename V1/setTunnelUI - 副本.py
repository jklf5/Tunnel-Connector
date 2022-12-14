# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'setTunnelUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWin(object):
    def setupUi(self, MainWin):
        MainWin.setObjectName("MainWin")
        MainWin.resize(764, 547)
        self.centralwidget = QtWidgets.QWidget(MainWin)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        self.txtBrowerStatus = QtWidgets.QTextBrowser(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtBrowerStatus.sizePolicy().hasHeightForWidth())
        self.txtBrowerStatus.setSizePolicy(sizePolicy)
        self.txtBrowerStatus.setObjectName("txtBrowerStatus")
        self.gridLayout.addWidget(self.txtBrowerStatus, 5, 0, 1, 3)
        self.proxyListBox = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.proxyListBox.sizePolicy().hasHeightForWidth())
        self.proxyListBox.setSizePolicy(sizePolicy)
        self.proxyListBox.setObjectName("proxyListBox")
        self.gridLayout.addWidget(self.proxyListBox, 1, 1, 1, 1)
        self.serverListBox = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.serverListBox.sizePolicy().hasHeightForWidth())
        self.serverListBox.setSizePolicy(sizePolicy)
        self.serverListBox.setObjectName("serverListBox")
        self.gridLayout.addWidget(self.serverListBox, 1, 0, 1, 1)
        self.btnStart = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnStart.sizePolicy().hasHeightForWidth())
        self.btnStart.setSizePolicy(sizePolicy)
        self.btnStart.setObjectName("btnStart")
        self.gridLayout.addWidget(self.btnStart, 2, 0, 1, 1)
        self.txtBrowerLog = QtWidgets.QTextBrowser(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtBrowerLog.sizePolicy().hasHeightForWidth())
        self.txtBrowerLog.setSizePolicy(sizePolicy)
        self.txtBrowerLog.setObjectName("txtBrowerLog")
        self.gridLayout.addWidget(self.txtBrowerLog, 1, 2, 3, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.btnAllStart = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnAllStart.sizePolicy().hasHeightForWidth())
        self.btnAllStart.setSizePolicy(sizePolicy)
        self.btnAllStart.setObjectName("btnAllStart")
        self.gridLayout.addWidget(self.btnAllStart, 2, 1, 1, 1)
        self.btnAllStop = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnAllStop.sizePolicy().hasHeightForWidth())
        self.btnAllStop.setSizePolicy(sizePolicy)
        self.btnAllStop.setObjectName("btnAllStop")
        self.gridLayout.addWidget(self.btnAllStop, 3, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 2, 1, 1)
        self.btnStop = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnStop.sizePolicy().hasHeightForWidth())
        self.btnStop.setSizePolicy(sizePolicy)
        self.btnStop.setObjectName("btnStop")
        self.gridLayout.addWidget(self.btnStop, 3, 0, 1, 1)
        MainWin.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWin)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 764, 23))
        self.menubar.setObjectName("menubar")
        self.menuConnect = QtWidgets.QMenu(self.menubar)
        self.menuConnect.setObjectName("menuConnect")
        self.menuEncode = QtWidgets.QMenu(self.menubar)
        self.menuEncode.setEnabled(True)
        self.menuEncode.setObjectName("menuEncode")
        MainWin.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWin)
        self.statusbar.setObjectName("statusbar")
        MainWin.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuConnect.menuAction())
        self.menubar.addAction(self.menuEncode.menuAction())

        self.retranslateUi(MainWin)
        QtCore.QMetaObject.connectSlotsByName(MainWin)

    def retranslateUi(self, MainWin):
        _translate = QtCore.QCoreApplication.translate
        MainWin.setWindowTitle(_translate("MainWin", "Establish Tunnel to Server"))
        self.label_4.setText(_translate("MainWin", "Status"))
        self.btnStart.setText(_translate("MainWin", "??????"))
        self.label_2.setText(_translate("MainWin", "Target"))
        self.btnAllStart.setText(_translate("MainWin", "????????????"))
        self.btnAllStop.setText(_translate("MainWin", "????????????"))
        self.label_3.setText(_translate("MainWin", "Proxy"))
        self.label.setText(_translate("MainWin", "Log"))
        self.btnStop.setText(_translate("MainWin", "??????"))
        self.menuConnect.setTitle(_translate("MainWin", "????????????"))
        self.menuEncode.setTitle(_translate("MainWin", "??????"))
