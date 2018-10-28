# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Qt\TST\BatchNueBee\BatchNueBee.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MW_BatchNueBee(object):
    def setupUi(self, MW_BatchNueBee):
        MW_BatchNueBee.setObjectName("MW_BatchNueBee")
        MW_BatchNueBee.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MW_BatchNueBee)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_test_temp2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_test_temp2.setObjectName("pushButton_test_temp2")
        self.gridLayout.addWidget(self.pushButton_test_temp2, 2, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 0, 1, 1)
        self.pushButton_test_temp1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_test_temp1.setObjectName("pushButton_test_temp1")
        self.gridLayout.addWidget(self.pushButton_test_temp1, 1, 0, 1, 1)
        self.pushButton_test_temp3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_test_temp3.setObjectName("pushButton_test_temp3")
        self.gridLayout.addWidget(self.pushButton_test_temp3, 3, 0, 1, 1)
        self.pushButton_test_temp4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_test_temp4.setObjectName("pushButton_test_temp4")
        self.gridLayout.addWidget(self.pushButton_test_temp4, 4, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setObjectName("tableView")
        self.verticalLayout.addWidget(self.tableView)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout.setStretch(0, 3)
        self.horizontalLayout.setStretch(1, 7)
        MW_BatchNueBee.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MW_BatchNueBee)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MW_BatchNueBee.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MW_BatchNueBee)
        self.statusbar.setObjectName("statusbar")
        MW_BatchNueBee.setStatusBar(self.statusbar)

        self.retranslateUi(MW_BatchNueBee)
        QtCore.QMetaObject.connectSlotsByName(MW_BatchNueBee)

    def retranslateUi(self, MW_BatchNueBee):
        _translate = QtCore.QCoreApplication.translate
        MW_BatchNueBee.setWindowTitle(_translate("MW_BatchNueBee", "BatchNueBee"))
        self.pushButton_test_temp2.setText(_translate("MW_BatchNueBee", "Test_temp2"))
        self.pushButton.setText(_translate("MW_BatchNueBee", "TEST"))
        self.pushButton_test_temp1.setText(_translate("MW_BatchNueBee", "Test_temp1"))
        self.pushButton_test_temp3.setText(_translate("MW_BatchNueBee", "Test_temp3"))
        self.pushButton_test_temp4.setText(_translate("MW_BatchNueBee", "Test_temp4"))

