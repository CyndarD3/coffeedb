import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem





class main_window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.pushButton_2.clicked.connect(self.show_redact)

        self.con = sqlite3.connect("coffee.sqlite")
        cur = self.con.cursor()
        output = cur.execute('''SELECT * FROM coffee''').fetchall()
        self.tableWidget.setRowCount(len(output))
        self.tableWidget.setColumnCount(len(output[0]))
        for i, elem in enumerate(output):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def show_redact(self):
        self.w1 = redact()
        self.w1.show()


class redact(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = main_window()
    ex.show()
    sys.exit(app.exec_())