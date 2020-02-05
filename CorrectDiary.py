import sys, random, sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QInputDialog, QMessageBox
from PyQt5.QtWidgets import QErrorMessage, QColorDialog, QFileDialog
from PyQt5.QtCore import Qt


class CorrectDiary(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('correct.ui', self)
        self.initUI(args)

    def initUI(self, args):
        self.setWindowTitle('Редактировать расписание')
        # объект класса Diary
        self.dnev = args[0]
        # расписание, полученное из Diary
        self.rasp = args[1][:]
        # константа со всем расписанием
        self.DAYS_CORRECT = [[self.monday_correct1, self.monday_correct2, self.monday_correct3,
                              self.monday_correct4, self.monday_correct5, self.monday_correct6,
                              self.monday_correct7, self.monday_correct8],
                             [self.tuesday_correct1, self.tuesday_correct2, self.tuesday_correct3,
                              self.tuesday_correct4, self.tuesday_correct5, self.tuesday_correct6,
                              self.tuesday_correct7, self.tuesday_correct8],
                             [self.wednesday_correct1, self.wednesday_correct2,
                              self.wednesday_correct3, self.wednesday_correct4,
                              self.wednesday_correct5, self.wednesday_correct6,
                              self.wednesday_correct7, self.wednesday_correct8],
                             [self.thursday_correct1, self.thursday_correct2, self.thursday_correct3,
                              self.thursday_correct4, self.thursday_correct5, self.thursday_correct6,
                              self.thursday_correct7, self.thursday_correct8],
                             [self.friday_correct1, self.friday_correct2, self.friday_correct3,
                              self.friday_correct4, self.friday_correct5, self.friday_correct6,
                              self.friday_correct7, self.friday_correct8],
                             [self.saturday_correct1, self.saturday_correct2, self.saturday_correct3,
                              self.saturday_correct4, self.saturday_correct5, self.saturday_correct6,
                              self.saturday_correct7, self.saturday_correct8]]
        self.timetable_insert()
        self.button_save_correct.clicked.connect(self.save_correct)
        # установка дизайна
        with open("color.txt") as f:
            mas = f.read().split('\n')
        color_text = mas[0]
        color_bacgr = mas[1]
        color_button = mas[2]
        self.setStyleSheet("color : {}; background-color: {}".format(color_text, color_bacgr))
        self.button_save_correct.setStyleSheet("background-color: {}".format(color_button))

    def timetable_insert(self):
        # вставка текущего расписания из БД
        for i in range(len(self.DAYS_CORRECT)):
            for j in range(len(self.DAYS_CORRECT[i])):
                self.DAYS_CORRECT[i][j].setText(self.rasp[i][j][0])

    def save_correct(self):
        # сохранение измененного расписания в БД
        dop = [[], [], [], [], [], []]
        for i in range(len(self.DAYS_CORRECT)):
            for j in range(len(self.DAYS_CORRECT[i])):
                dop[i].append(self.DAYS_CORRECT[i][j].text())
        con = sqlite3.connect("расписание.db")
        cur = con.cursor()
        for i in range(len(dop[0])):
            cur.execute("""UPDATE timetable SET Monday = ? WHERE id = ?""", (dop[0][i], i + 1))
            cur.execute("""UPDATE timetable SET Tuesday = ? WHERE id = ?""", (dop[1][i], i + 1))
            cur.execute("""UPDATE timetable SET Wednesday = ? WHERE id = ?""", (dop[2][i], i + 1))
            cur.execute("""UPDATE timetable SET Thursday = ? WHERE id = ?""", (dop[3][i], i + 1))
            cur.execute("""UPDATE timetable SET Friday = ? WHERE id = ?""", (dop[4][i], i + 1))
            cur.execute("""UPDATE timetable SET Saturday = ? WHERE id = ?""", (dop[5][i], i + 1))
        con.commit()
        con.close()
        self.dnev.timetable_insert()
