# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Qt\TST\BatchNueBee\AddTrendGroup.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog_Add_Trend_Group(object):
    def setupUi(self, Dialog_Add_Trend_Group):
        Dialog_Add_Trend_Group.setObjectName("Dialog_Add_Trend_Group")
        Dialog_Add_Trend_Group.resize(400, 300)
        Dialog_Add_Trend_Group.setModal(False)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog_Add_Trend_Group)
        self.buttonBox.setGeometry(QtCore.QRect(30, 260, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(Dialog_Add_Trend_Group)
        self.label.setGeometry(QtCore.QRect(20, 18, 171, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(Dialog_Add_Trend_Group)
        self.lineEdit.setGeometry(QtCore.QRect(20, 50, 361, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit.setFont(font)
        self.lineEdit.setText("")
        self.lineEdit.setMaxLength(32)
        self.lineEdit.setObjectName("lineEdit")
        self.label_2 = QtWidgets.QLabel(Dialog_Add_Trend_Group)
        self.label_2.setGeometry(QtCore.QRect(20, 109, 171, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.textEdit = QtWidgets.QTextEdit(Dialog_Add_Trend_Group)
        self.textEdit.setGeometry(QtCore.QRect(20, 150, 361, 101))
        self.textEdit.setObjectName("textEdit")

        self.retranslateUi(Dialog_Add_Trend_Group)
        self.buttonBox.accepted.connect(Dialog_Add_Trend_Group.accept)
        self.buttonBox.rejected.connect(Dialog_Add_Trend_Group.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog_Add_Trend_Group)

    def retranslateUi(self, Dialog_Add_Trend_Group):
        _translate = QtCore.QCoreApplication.translate
        Dialog_Add_Trend_Group.setWindowTitle(_translate("Dialog_Add_Trend_Group", "Add New Trend Group"))
        self.label.setText(_translate("Dialog_Add_Trend_Group", "Group Name:"))
        self.label_2.setText(_translate("Dialog_Add_Trend_Group", "Description:"))

