import sys
from PyQt6.QtWidgets import QApplication, QDialog, QLineEdit
from PyQt6 import QtCore, QtWidgets
import math
import sqlite3

boglanish = sqlite3.connect("shakllar_bazasi.db")
cursor = boglanish.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS shakllar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    shakl TEXT(50),
    hajm INTEGER,
    yuza INTEGER
)
""")




class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(260, 450)
        self.graphicsView = QtWidgets.QGraphicsView(parent=Dialog)
        self.graphicsView.setGeometry(QtCore.QRect(0, -10, 791, 621))
        self.graphicsView.setStyleSheet("background-color:rgb(172, 200, 166)")
        self.graphicsView.setObjectName("graphicsView")
#        self.graphicsView_2 = QtWidgets.QGraphicsView(parent=Dialog)
 #       self.graphicsView_2.setGeometry(QtCore.QRect(260, 1, 531, 611))
 #       self.graphicsView_2.setObjectName("graphicsView_2")
        self.textBrowser = QtWidgets.QTextBrowser(parent=Dialog)
        self.textBrowser.setGeometry(QtCore.QRect(10, 200, 241, 192))
        self.pushButton = QtWidgets.QPushButton(parent=Dialog)
        self.pushButton.setGeometry(QtCore.QRect(10, 400, 91, 31))
        self.pushButton.setStyleSheet("background-color:red; color:white;")
        self.pushButton.setText("Bazani Tozalash")
        self.pushButton_2 = QtWidgets.QPushButton(parent=Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(131, 400, 120, 31))
        self.pushButton_2.setStyleSheet("background-color:green; color:white;")
        self.pushButton_2.setText("Hisoblash va Saqlash")
        self.label = QtWidgets.QLabel(parent=Dialog)
        self.label.setGeometry(QtCore.QRect(20, 0, 71, 81))
        self.label.setStyleSheet("color:white; font-size: 50px; font-weight: bold;")
        self.label.setText("3D")
        self.label_2 = QtWidgets.QLabel(parent=Dialog)
        self.label_2.setGeometry(QtCore.QRect(90, 10, 161, 61))
        self.label_2.setStyleSheet("color:white; font-size: 50px; font-weight: bold;")
        self.label_2.setText("Forms")
        self.comboBox = QtWidgets.QComboBox(parent=Dialog)
        self.comboBox.setGeometry(QtCore.QRect(40, 70, 171, 22))
        self.comboBox.addItem("kub")
        self.comboBox.addItem("paralelopiped")
        self.comboBox.addItem("piramida")
        self.comboBox.addItem("shar")
        self.input_fields = []
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle("3D Shakl Tanlash")
class Interfeys(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.clear_database)
        self.ui.comboBox.currentIndexChanged.connect(self.on_shape_selected)  
        self.ui.pushButton_2.clicked.connect(self.kalkulyator)
    def clear_database(self):
        self.ui.textBrowser.clear()
        self.ui.textBrowser.append("Baza tozalandi.")
    def on_shape_selected(self):
        tanlangan_shakl = self.ui.comboBox.currentText()
        for field in self.ui.input_fields:
            field.deleteLater()
        self.ui.input_fields.clear()
        if tanlangan_shakl == "kub":
            input_count = 1
        elif tanlangan_shakl == "paralelopiped":
            input_count = 3  
        elif tanlangan_shakl == "piramida":
            input_count = 3  
        elif tanlangan_shakl == "shar":
            input_count = 1  
        else:
            input_count = 1  
        for i in range(input_count):
            new_input = QLineEdit(self)
            new_input.setGeometry(QtCore.QRect(40, 100 + (i * 30), 171, 22))
            new_input.setPlaceholderText(f"{tanlangan_shakl} parametri {i+1}...")
            self.ui.input_fields.append(new_input)
            new_input.setParent(self)
            new_input.show()
    
    def kalkulyator(self):
        tanlangan_shakl = self.ui.comboBox.currentText()
        try:
            values = [float(field.text()) for field in self.ui.input_fields]
        except ValueError:
            self.ui.textBrowser.append("Xato: Iltimos, faqat son kiriting!")
            return
        hajm = 0
        yuza = 0
        if tanlangan_shakl == "kub":
            if len(values) == 1:
                a = values[0]
                hajm = a ** 3
                yuza = 6 * (a ** 2)
        elif tanlangan_shakl == "paralelopiped":
            if len(values) == 3:
                a, b, c = values
                hajm = a * b * c
                yuza = 2 * (a * b + a * c + b * c)
        elif tanlangan_shakl == "piramida":
            if len(values) == 3:
                a, b, h = values
                hajm = (1/3) * (a * b) * h
                yuza = (a ** 2) + 2 * a * math.sqrt((a/2) ** 2 + h ** 2)
        elif tanlangan_shakl == "shar":
            if len(values) == 1:
                r = values[0]
                hajm = (4/3) * math.pi * (r ** 3)
                yuza = 4 * math.pi * (r ** 2)
        else:
            self.ui.textBrowser.append("Shakl tanlanmadi yoki noto‘g‘ri parametr kiritildi.")
            return
        self.ui.textBrowser.append(f"Tanlangan shakl: {tanlangan_shakl}\nHajmi: {round(hajm, 2)}\nYuzasi: {round(yuza, 2)}")  
        cursor.execute("insert into shakllar (shakl,hajm,yuza) values (?,?,?)",(tanlangan_shakl,int(hajm),int(yuza)))
    def get_selected_shape(self):
        tanlangan_shakl = self.ui.comboBox.currentText()
        input_field = self.ui.input_fields.get(tanlangan_shakl)
        if input_field:
            qiymat = input_field.text()
            self.ui.textBrowser.append(f"Tanlangan: {tanlangan_shakl}, Kiritilgan qiymat: {qiymat}")
        else:
            self.ui.textBrowser.append(f"Tanlangan: {tanlangan_shakl}, Kiritish maydoni yo'q")
          
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Interfeys()
    window.show()
    sys.exit(app.exec())
    
boglanish.commit()
boglanish.close() 
    