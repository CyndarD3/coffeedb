import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem, QSpinBox





class main_window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.pushButton_2.clicked.connect(self.show_redact)
        self.con = sqlite3.connect("coffee.sqlite")
        self.renew()

    def renew(self):
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
        self.con = sqlite3.connect("coffee.sqlite")
        self.pushButton.clicked.connect(self.redaction)
        self.tableWidget.itemChanged.connect(self.item_changed)
        self.pushButton_2.clicked.connect(self.saving)

        self.pushButton_3.clicked.connect(self.creation)
        self.modified = {}
        self.titles = None

    def creation(self):
        cur = self.con.cursor()
        item_id = self.spinBox.text()
        result = cur.execute(f"insert into coffee values({item_id}, '', 0, 0, '', 0, 0)")

        self.con.commit()
        main_window.renew(ex)
        self.redaction()

    def redaction(self):
        cur = self.con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        item_id = self.spinBox.text()
        result = cur.execute("SELECT * FROM coffee WHERE id=?",
                             (item_id,)).fetchall()
        # Заполнили размеры таблицы
        self.tableWidget.setRowCount(len(result))
        # Если запись не нашлась, то не будем ничего делать
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}

    def item_changed(self, item):
        self.modified[self.titles[item.column()]] = item.text()

    def saving(self):
        if self.modified:
            cur = self.con.cursor()
            que = "UPDATE coffee SET\n"
            for key in self.modified.keys():
                que += "{}='{}'\n".format(key, self.modified.get(key))
            que += "WHERE id = ?"
            cur.execute(que, (self.spinBox.text(),))
            self.con.commit()
            self.modified.clear()
            main_window.renew(ex)



if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        ex = main_window()
        ex.show()
        sys.exit(app.exec_())
    except:
        print('Неверное значение ID')