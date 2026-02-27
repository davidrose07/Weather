#!/usr/bin/env python3

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

class Ui_MainWindow(object):
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(502, 315)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setStyleSheet("background-color: rgba(36, 31, 49, 120);\n"
"color: rgb(246, 245, 244);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_icon = QtWidgets.QLabel(self.centralwidget)
        self.label_icon.setGeometry(QtCore.QRect(410, 0, 91, 51))
        self.label_icon.setStyleSheet("background-color: rgba(36, 31, 49, 120);\n"
"color: rgb(222, 221, 218);")
        self.label_icon.setText("")
        self.label_icon.setObjectName("label_icon")
        self.listView = QtWidgets.QListView(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(10, 50, 491, 261))
        self.listView.setStyleSheet("background-color: rgba(36, 31, 49, 120);\n"
"color: rgb(246, 245, 244);")
        self.listView.setObjectName("listView")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(10, 10, 401, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("background-color: rgba(36, 31, 49, 120);\n"
"color: rgb(246, 245, 244);")
        self.lineEdit.setObjectName("lineEdit")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 502, 22))
        self.menubar.setObjectName("menubar")
        self.menuGeo = QtWidgets.QMenu(self.menubar)
        self.menuGeo.setObjectName("menuGeo")
        self.menuTheme = QtWidgets.QMenu(self.menubar)
        self.menuTheme.setObjectName("menuTheme")
        self.menuTranslucent = QtWidgets.QMenu(self.menuTheme)
        self.menuTranslucent.setObjectName("menuTranslucent")
        MainWindow.setMenuBar(self.menubar)

        # Add corner widget (time label) to the top-right corner of the menu bar
        self.time_label = QtWidgets.QLabel("Loading...")
        self.time_label.setStyleSheet("color: rgb(246, 245, 244); font-weight: bold;")
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setFixedWidth(120)  # Adjust width as necessary
        self.menubar.setCornerWidget(self.time_label, Qt.TopRightCorner)
        
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionChange_Location = QtWidgets.QAction(MainWindow)
        self.actionChange_Location.setObjectName("actionChange_Location")
        self.actionChange_Default = QtWidgets.QAction(MainWindow)
        self.actionChange_Default.setObjectName("actionChange_Default")
        self.actionDark = QtWidgets.QAction(MainWindow)
        self.actionDark.setObjectName("actionDark")
        self.actionLight = QtWidgets.QAction(MainWindow)
        self.actionLight.setObjectName("actionLight")
        self.actionHeavyTranslucency = QtWidgets.QAction(MainWindow)
        self.actionHeavyTranslucency.setObjectName("actionHeavyTranslucency")
        self.actionLightTranslucency = QtWidgets.QAction(MainWindow)
        self.actionLightTranslucency.setObjectName("actionLightTranslucency")
        self.menuGeo.addAction(self.actionChange_Location)
        self.menuGeo.addAction(self.actionChange_Default)
        self.menuTranslucent.addAction(self.actionHeavyTranslucency)
        self.menuTranslucent.addAction(self.actionLightTranslucency)
        self.menuTheme.addAction(self.menuTranslucent.menuAction())
        self.menuTheme.addSeparator()
        self.menuTheme.addAction(self.actionDark)
        self.menuTheme.addAction(self.actionLight)
        self.menubar.addAction(self.menuGeo.menuAction())
        self.menubar.addAction(self.menuTheme.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)   

        # Application only works in translucent mode with this code.  ???
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.listView.setAttribute(Qt.WA_TranslucentBackground)
        self.lineEdit.setAttribute(Qt.WA_TranslucentBackground)
        self.menubar.setAttribute(Qt.WA_TranslucentBackground)
        self.label_icon.setAttribute(Qt.WA_TranslucentBackground)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Weather"))
        self.menuGeo.setTitle(_translate("MainWindow", "Geo"))
        self.menuTheme.setTitle(_translate("MainWindow", "Theme"))
        self.menuTranslucent.setTitle(_translate("MainWindow", "Translucent"))
        self.actionChange_Location.setText(_translate("MainWindow", "Change Location"))
        self.actionChange_Default.setText(_translate("MainWindow", "Change Default Location"))
        self.actionDark.setText(_translate("MainWindow", "Dark"))
        self.actionLight.setText(_translate("MainWindow", "Light"))
        self.actionHeavyTranslucency.setText(_translate("MainWindow", "Heavy"))
        self.actionLightTranslucency.setText(_translate("MainWindow", "Light"))


    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
