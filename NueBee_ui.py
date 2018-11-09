# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '\\192.168.3.33\Backup\Qt\TST\BatchNueBee\NueBee.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(872, 677)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tableView_batches = QtWidgets.QTableView(self.centralwidget)
        self.tableView_batches.setObjectName("tableView_batches")
        self.horizontalLayout_2.addWidget(self.tableView_batches)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_tst2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_tst2.setObjectName("pushButton_tst2")
        self.gridLayout.addWidget(self.pushButton_tst2, 1, 0, 1, 1)
        self.pushButton_tst5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_tst5.setObjectName("pushButton_tst5")
        self.gridLayout.addWidget(self.pushButton_tst5, 4, 0, 1, 1)
        self.pushButton_tst4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_tst4.setObjectName("pushButton_tst4")
        self.gridLayout.addWidget(self.pushButton_tst4, 3, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 6, 0, 1, 1)
        self.pushButton_tst3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_tst3.setObjectName("pushButton_tst3")
        self.gridLayout.addWidget(self.pushButton_tst3, 2, 0, 1, 1)
        self.pushButton_tst1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_tst1.setObjectName("pushButton_tst1")
        self.gridLayout.addWidget(self.pushButton_tst1, 0, 0, 1, 1)
        self.pushButton_tst6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_tst6.setObjectName("pushButton_tst6")
        self.gridLayout.addWidget(self.pushButton_tst6, 5, 0, 1, 1)
        self.horizontalLayout_2.addLayout(self.gridLayout)
        self.horizontalLayout_2.setStretch(0, 8)
        self.horizontalLayout_2.setStretch(1, 2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(0, 7)
        self.verticalLayout.setStretch(1, 3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 872, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "NueBee"))
        self.pushButton_tst2.setText(_translate("MainWindow", "Test2"))
        self.pushButton_tst5.setText(_translate("MainWindow", "Test5"))
        self.pushButton_tst4.setText(_translate("MainWindow", "Test4"))
        self.pushButton_tst3.setText(_translate("MainWindow", "Test3"))
        self.pushButton_tst1.setText(_translate("MainWindow", "Test1"))
        self.pushButton_tst6.setText(_translate("MainWindow", "Test6"))

