import sys, random, sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QInputDialog, QMessageBox
from PyQt5.QtWidgets import QErrorMessage, QColorDialog, QFileDialog
from PyQt5.QtCore import Qt
from CorrectDiary import CorrectDiary

# Запись в переменные параметров цветов
with open("color.txt") as f:
    mas = f.read().split('\n')
color_text = mas[0]
color_bacgr = mas[1]
color_button = mas[2]


class Diary(QMainWindow):
    def __init__(self, *args):
        print(1)
        super().__init__()
        uic.loadUi('dnevnik.ui', self)
        self.initUI(args)

    def initUI(self, args):
        self.setWindowTitle('Дневник')
        # Создание константы со всеми уроками в неделе
        self.DAYS_WEEK = [[self.monday_lesson1, self.monday_lesson2, self.monday_lesson3,
                           self.monday_lesson4, self.monday_lesson5, self.monday_lesson6,
                           self.monday_lesson7, self.monday_lesson8],
                          [self.tuesday_lesson1, self.tuesday_lesson2, self.tuesday_lesson3,
                           self.tuesday_lesson4, self.tuesday_lesson5, self.tuesday_lesson6,
                           self.tuesday_lesson7, self.tuesday_lesson8],
                          [self.wednesday_lesson1, self.wednesday_lesson2,
                           self.wednesday_lesson3, self.wednesday_lesson4,
                           self.wednesday_lesson5, self.wednesday_lesson6,
                           self.wednesday_lesson7, self.wednesday_lesson8],
                          [self.thursday_lesson1, self.thursday_lesson2, self.thursday_lesson3,
                           self.thursday_lesson4, self.thursday_lesson5, self.thursday_lesson6,
                           self.thursday_lesson7, self.thursday_lesson8],
                          [self.friday_lesson1, self.friday_lesson2, self.friday_lesson3,
                           self.friday_lesson4, self.friday_lesson5, self.friday_lesson6,
                           self.friday_lesson7, self.friday_lesson8],
                          [self.saturday_lesson1, self.saturday_lesson2, self.saturday_lesson3,
                           self.saturday_lesson4, self.saturday_lesson5, self.saturday_lesson6,
                           self.saturday_lesson7, self.saturday_lesson8]]
        # Константа со всеми днями недели
        self.DAY = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        # Константа со всем дз на неделю
        self.DAYS_DZ = [[self.monday_dz1, self.monday_dz2, self.monday_dz3,
                         self.monday_dz4, self.monday_dz5, self.monday_dz6,
                         self.monday_dz7, self.monday_dz8],
                        [self.tuesday_dz1, self.tuesday_dz2, self.tuesday_dz3,
                         self.tuesday_dz4, self.tuesday_dz5, self.tuesday_dz6,
                         self.tuesday_dz7, self.tuesday_dz8],
                        [self.wednesday_dz1, self.wednesday_dz2,
                         self.wednesday_dz3, self.wednesday_dz4,
                         self.wednesday_dz5, self.wednesday_dz6,
                         self.wednesday_dz7, self.wednesday_dz8],
                        [self.thursday_dz1, self.thursday_dz2, self.thursday_dz3,
                         self.thursday_dz4, self.thursday_dz5, self.thursday_dz6,
                         self.thursday_dz7, self.thursday_dz8],
                        [self.friday_dz1, self.friday_dz2, self.friday_dz3,
                         self.friday_dz4, self.friday_dz5, self.friday_dz6,
                         self.friday_dz7, self.friday_dz8],
                        [self.saturday_dz1, self.saturday_dz2, self.saturday_dz3,
                         self.saturday_dz4, self.saturday_dz5, self.saturday_dz6,
                         self.saturday_dz7, self.saturday_dz8]]
        # Назначение кнопок
        self.button_correct.clicked.connect(self.rasp_correct)
        self.button_delete.clicked.connect(self.delete_dz)
        self.button_save_dz.clicked.connect(self.send_dz)
        self.button_notebook.clicked.connect(self.open_notebook)
        self.button_settings.clicked.connect(self.open_settigs)
        # Установка дизайна
        self.setStyleSheet("color : {}; background-color: {}".format(color_text, color_bacgr))
        self.button_correct.setStyleSheet("background-color: {}".format(color_button))
        self.button_delete.setStyleSheet("background-color: {}".format(color_button))
        self.button_save_dz.setStyleSheet("background-color: {}".format(color_button))
        self.button_notebook.setStyleSheet("background-color: {}".format(color_button))
        self.button_diary.setStyleSheet("background-color: {}".format(color_button))
        self.button_settings.setStyleSheet("background-color: {}".format(color_button))
        # Запуск нужнвх функций
        self.timetable_insert()
        self.dz_insert()
        # Установка дизайна
        for i in range(len(self.DAYS_WEEK)):
            for j in range(len(self.DAYS_WEEK[i])):
                self.DAYS_WEEK[i][j].setStyleSheet("""background-color: {}; border: 
                1px inset grey""".format(color_bacgr))

    def keyPressEvent(self, event):
        # Сочетания клавиш для открытия двух других окон
        if int(event.modifiers()) == (Qt.AltModifier + Qt.ShiftModifier):
            print(1)
            if event.key() == Qt.Key_N:
                self.open_notebook()
            if event.key() == Qt.Key_O:
                self.open_settigs()

    def timetable_insert(self):
        # Установка расписания из базы данных в окно
        con = sqlite3.connect("расписание.db")
        cur = con.cursor()
        for i in range(len(self.DAYS_WEEK)):
            if i == 0:
                timetable = cur.execute("""SELECT Monday FROM timetable""").fetchall()
            elif i == 1:
                timetable = cur.execute("""SELECT Tuesday FROM timetable""").fetchall()
            elif i == 2:
                timetable = cur.execute("""SELECT Wednesday FROM timetable""").fetchall()
            elif i == 3:
                timetable = cur.execute("""SELECT Thursday FROM timetable""").fetchall()
            elif i == 4:
                timetable = cur.execute("""SELECT Friday FROM timetable""").fetchall()
            elif i == 5:
                timetable = cur.execute("""SELECT Saturday FROM timetable""").fetchall()
            for j in range(len(self.DAYS_WEEK[i])):
                self.DAYS_WEEK[i][j].setText(timetable[j][0])
        con.close()

    def dz_insert(self):
        # Установка дз из базы данных в окно
        con = sqlite3.connect("расписание.db")
        cur = con.cursor()
        for i in range(len(self.DAYS_DZ)):
            if i == 0:
                timetable = cur.execute("""SELECT Monday FROM dz""").fetchall()
            elif i == 1:
                timetable = cur.execute("""SELECT Tuesday FROM dz""").fetchall()
            elif i == 2:
                timetable = cur.execute("""SELECT Wednesday FROM dz""").fetchall()
            elif i == 3:
                timetable = cur.execute("""SELECT Thursday FROM dz""").fetchall()
            elif i == 4:
                timetable = cur.execute("""SELECT Friday FROM dz""").fetchall()
            elif i == 5:
                timetable = cur.execute("""SELECT Saturday FROM dz""").fetchall()
            for j in range(len(self.DAYS_WEEK[i])):
                self.DAYS_DZ[i][j].setText(timetable[j][0])
        timetable = cur.execute("""SELECT Tuesday FROM timetable""").fetchall()
        self.tuesday_lesson2.setText(timetable[1][0])
        con.close()

    def delete_dz(self):
        # удаление всего дз из окна и базы данных
        con = sqlite3.connect("расписание.db")
        cur = con.cursor()
        cur.execute("""UPDATE dz SET Monday = ''""")
        cur.execute("""UPDATE dz SET Tuesday = ''""")
        cur.execute("""UPDATE dz SET Wednesday = ''""")
        cur.execute("""UPDATE dz SET Thursday = ''""")
        cur.execute("""UPDATE dz SET Friday = ''""")
        cur.execute("""UPDATE dz SET Saturday = ''""")
        con.commit()
        con.close()
        self.dz_insert()

    def send_dz(self):
        # Вставка нового дз в базу данных(после нажатия "сохранить")
        dop = [[], [], [], [], [], []]
        for i in range(len(self.DAYS_DZ)):
            for j in range(len(self.DAYS_DZ[i])):
                dop[i].append(self.DAYS_DZ[i][j].text())
        con = sqlite3.connect("расписание.db")
        cur = con.cursor()
        for i in range(len(dop[0])):
            cur.execute("""UPDATE dz SET Monday = ? WHERE id = ?""", (dop[0][i], i + 1))
            cur.execute("""UPDATE dz SET Tuesday = ? WHERE id = ?""", (dop[1][i], i + 1))
            cur.execute("""UPDATE dz SET Wednesday = ? WHERE id = ?""", (dop[2][i], i + 1))
            cur.execute("""UPDATE dz SET Thursday = ? WHERE id = ?""", (dop[3][i], i + 1))
            cur.execute("""UPDATE dz SET Friday = ? WHERE id = ?""", (dop[4][i], i + 1))
            cur.execute("""UPDATE dz SET Saturday = ? WHERE id = ?""", (dop[5][i], i + 1))
        con.commit()
        con.close()

    def rasp_correct(self):
        # Открытие окна для редактирования расписания с передачей переменной, содержащей
        # текущее расписание, взятое из базы данных
        self.indi = True
        dop = []
        con = sqlite3.connect("расписание.db")
        cur = con.cursor()
        dop.append(cur.execute("""SELECT Monday FROM timetable""").fetchall())
        dop.append(cur.execute("""SELECT Tuesday FROM timetable""").fetchall())
        dop.append(cur.execute("""SELECT Wednesday FROM timetable""").fetchall())
        dop.append(cur.execute("""SELECT Thursday FROM timetable""").fetchall())
        dop.append(cur.execute("""SELECT Friday FROM timetable""").fetchall())
        dop.append(cur.execute("""SELECT Saturday FROM timetable""").fetchall())
        con.close()
        self.second_form = CorrectDiary(self, dop)
        self.second_form.show()

    def open_notebook(self):
        # открытие блокнота
        self.second_form = Notebook(self)
        self.second_form.show()
        self.close()

    def open_settigs(self):
        # открытие настроек
        self.second_form = Settings(self)
        self.second_form.show()
        self.close()


class Notebook(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('notebook.ui', self)
        self.initUI(args)

    def initUI(self, args):
        self.setWindowTitle('Блокнот')
        # из текстового файла достается количество страниц
        with open("page.txt") as f:
            self.maxcount = int(f.read())
            self.count = 1
            f.close()
        # вывод в LCDNumber значений
        self.count_page_max.display(self.maxcount)
        self.count_page.display(self.count)
        # вывод содержания первой страницы
        with open("1.txt") as f:
            dop = f.read().split('\n')
            dop = '\n'.join(dop)
            self.note.setText(dop)
            f.close()
        # установка активности кнопок, чтобы не было ошибок
        if self.maxcount == 1:
            self.button_right_page.setEnabled(False)
        self.button_left_page.setEnabled(False)
        # установка функций кнопок
        self.button_add_page.clicked.connect(self.add_page)
        self.button_save_page.clicked.connect(self.save_page)
        self.button_left_page.clicked.connect(self.left_page)
        self.button_right_page.clicked.connect(self.right_page)
        self.button_clear_page.clicked.connect(self.clear_page)
        self.button_delete_page.clicked.connect(self.delete_page)
        self.button_enter_page.clicked.connect(self.enter_page)
        self.button_diary.clicked.connect(self.open_diary)
        self.button_settings.clicked.connect(self.open_settings)
        # установка дизайна
        self.setStyleSheet("color : {}; background-color: {}".format(color_text, color_bacgr))
        self.button_add_page.setStyleSheet("background-color: {}".format(color_button))
        self.button_save_page.setStyleSheet("background-color: {}".format(color_button))
        self.button_left_page.setStyleSheet("background-color: {}".format(color_button))
        self.button_right_page.setStyleSheet("background-color: {}".format(color_button))
        self.button_clear_page.setStyleSheet("background-color: {}".format(color_button))
        self.button_delete_page.setStyleSheet("background-color: {}".format(color_button))
        self.button_enter_page.setStyleSheet("background-color: {}".format(color_button))
        self.button_diary.setStyleSheet("background-color: {}".format(color_button))
        self.button_settings.setStyleSheet("background-color: {}".format(color_button))
        self.button_notebook.setStyleSheet("background-color: {}".format(color_button))

    def keyPressEvent(self, event):
        # клавиши для открытия двух других окон
        if int(event.modifiers()) == (Qt.AltModifier + Qt.ShiftModifier):
            print(1)
            if event.key() == Qt.Key_O:
                self.open_settings()
            if event.key() == Qt.Key_D:
                self.open_diary()

    def add_page(self):
        # создание новой страницы и переход на нее
        self.maxcount += 1
        self.count = self.maxcount
        # обновление LCDNumber
        self.count_page.display(self.count)
        self.count_page_max.display(self.count)
        # обновление количества страниц в файле
        with open("page.txt", 'w') as f:
            f.write(str(self.maxcount))
        # создание нового файла под эту страницу
        with open("{}.txt".format(str(self.maxcount)), 'w') as f:
            f.write('')
        # подготовка кнопок и вывода
        self.note.clear()
        self.button_left_page.setEnabled(True)

    def save_page(self):
        # сохранить изменения на текущей странице
        with open("{}.txt".format(self.count), 'w') as f:
            f.write(self.note.toPlainText())

    def left_page(self):
        # кнопка для листания страниц влево
        self.count -= 1
        self.note.clear()
        # загрузка содержания другой страницы
        with open("{}.txt".format(self.count)) as f:
            self.note.setText(f.read())
        # установка активности кнопок
        if self.count == 1:
            self.button_left_page.setEnabled(False)
        self.button_right_page.setEnabled(True)
        # обновление LCDNumber
        self.count_page.display(self.count)

    def right_page(self):
        # кнопка для листания страниц вправо
        self.count += 1
        self.note.clear()
        with open("{}.txt".format(self.count)) as f:
            self.note.setText(f.read())
        if self.count == self.maxcount:
            self.button_right_page.setEnabled(False)
        self.button_left_page.setEnabled(True)
        self.count_page.display(self.count)

    def clear_page(self):
        # очистка текущей страницы от всего содержимого
        with open("{}.txt".format(self.count), 'w') as f:
            f.write('')
        self.note.clear()

    def delete_page(self):
        # предупреждение о тонкостях удаления страниц
        if self.count != self.maxcount:
            dop = 'Удалится не текущая страница, а последняя. \n \t           Продолжить?'
        else:
            dop = 'Удалить страницу?'
        reply = QMessageBox.question(self, 'Удаление страницы', dop, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        # в случае положительного ответа
        if reply == QMessageBox.Yes:
            # проверка, что не удаляется единственная страница, а если удаляется, выводится ошибка
            if self.maxcount == 1:
                error = QErrorMessage(self)
                error.showMessage('Ошибка. Осталась всего одна страница. Ее нельзя удалять')
                return
            # в файле последней страницы удаляется все содержимое
            with open("{}.txt".format(self.maxcount), 'w') as f:
                f.write('')
            # если пользователь находился на последней странице, а ее удаляют, он переместится на
            # предыдущую, а если нет, то останется на прежней
            if self.count == self.maxcount:
                self.count -= 1
                self.maxcount -= 1
                with open("{}.txt".format(self.maxcount)) as f:
                    self.note.setText(f.read())
                self.count_page.display(self.count)
                self.count_page_max.display(self.count)
            else:
                self.maxcount -= 1
                self.count_page.display(self.count)
                self.count_page_max.display(self.maxcount)
            with open("page.txt", 'w') as f:
                f.write(str(self.maxcount))
        # установка активности кнопок
        if self.maxcount == 1:
            self.button_left_page.setEnabled(False)
            self.button_right_page.setEnabled(False)
        elif self.count == 1:
            self.button_left_page.setEnabled(False)
            self.button_right_page.setEnabled(True)
        elif self.count == self.maxcount:
            self.button_left_page.setEnabled(True)
            self.button_right_page.setEnabled(False)
        else:
            self.button_left_page.setEnabled(True)
            self.button_right_page.setEnabled(True)

    def enter_page(self):
        # получение номера страницы, к которой нужно перейти
        dop = self.edit_page.text()
        # проверка на корректность введенных данных, иначе ошибка
        if not dop.isdigit():
            error = QErrorMessage(self)
            error.showMessage('Ошибка. Некорректный ввод данных')
        elif int(dop) > self.maxcount or dop == '0':
            error = QErrorMessage(self)
            error.showMessage('Ошибка. Страницы с таким номером не существует')
        else:
            # переход к нужной странице
            with open("{}.txt".format(dop)) as f:
                self.note.setText(f.read())
            self.count = int(dop)
            self.count_page.display(int(dop))
        self.edit_page.setText('')
        # установка активности кнопок
        if self.maxcount == 1:
            self.button_left_page.setEnabled(False)
            self.button_right_page.setEnabled(False)
        elif self.count == 1:
            self.button_left_page.setEnabled(False)
            self.button_right_page.setEnabled(True)
        elif self.count == self.maxcount:
            self.button_left_page.setEnabled(True)
            self.button_right_page.setEnabled(False)
        else:
            self.button_left_page.setEnabled(True)
            self.button_right_page.setEnabled(True)

    def open_diary(self):
        # открытие дневника
        self.second_form = Diary(self)
        self.second_form.show()
        self.close()

    def open_settings(self):
        # открытие настроек
        self.second_form = Settings(self)
        self.second_form.show()
        self.close()


class Settings(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('settings.ui', self)
        self.initUI(args)

    def initUI(self, args):
        self.setWindowTitle('Настройки')
        self.button_layout()
        # установка функций кнопок
        self.button_enter_settings.clicked.connect(self.enter_settings)
        self.button_enter_author.clicked.connect(self.enter_author)
        self.button_diary.clicked.connect(self.open_diary)
        self.button_notebook.clicked.connect(self.open_notebook)
        self.button_enter_color.clicked.connect(self.enter_color)
        self.button_enter_text.clicked.connect(self.enter_text)
        self.button_enter_button.clicked.connect(self.enter_button)
        self.color_layout()

    def keyPressEvent(self, event):
        # клавиши для открытия двух других окон
        if int(event.modifiers()) == (Qt.AltModifier + Qt.ShiftModifier):
            print(1)
            if event.key() == Qt.Key_N:
                self.open_notebook()
            if event.key() == Qt.Key_D:
                self.open_diary()

    def color_layout(self):
        # установка дизайна
        self.setStyleSheet("color : {}; background-color: {}".format(color_text, color_bacgr))
        self.button_enter_settings.setStyleSheet("background-color: {}".format(color_button))
        self.button_enter_author.setStyleSheet("background-color: {}".format(color_button))
        self.button_diary.setStyleSheet("background-color: {}".format(color_button))
        self.button_notebook.setStyleSheet("background-color: {}".format(color_button))
        self.button_enter_color.setStyleSheet("background-color: {}".format(color_button))
        self.button_enter_text.setStyleSheet("background-color: {}".format(color_button))
        self.button_enter_button.setStyleSheet("background-color: {}".format(color_button))
        self.button_settings.setStyleSheet("background-color: {}".format(color_button))
        self.label_settings.setStyleSheet("background-color: {}".format(color_bacgr))
        self.label_author.setStyleSheet("background-color: {}".format(color_bacgr))
        self.label_exper.setStyleSheet("background-color: {}".format(color_bacgr))
        self.label_color.setStyleSheet("background-color: {}".format(color_bacgr))
        self.label_text.setStyleSheet("background-color: {}".format(color_bacgr))
        self.label_button.setStyleSheet("background-color: {}".format(color_bacgr))
        self.label_menu.setStyleSheet("background-color: {}".format(color_bacgr))
        self.label_theme.setStyleSheet("background-color: {}".format(color_bacgr))
        self.radio_author_settings.setStyleSheet("background-color: {}".format(color_bacgr))
        self.radio_exper_settings.setStyleSheet("background-color: {}".format(color_bacgr))
        self.radio_ligth.setStyleSheet("background-color: {}".format(color_bacgr))
        self.radio_dark.setStyleSheet("background-color: {}".format(color_bacgr))

    def button_layout(self):
        # получение из файла информации о состоянии RadioButton
        with open("radiobutton.txt") as f:
            dop = f.read().split('\n')
        # перевод из текста в логику
        if dop[0] == 'True':
            dop[0] = True
        else:
            dop[0] = False
        if dop[1] == 'True':
            dop[1] = True
        elif dop[1] == 'False':
            dop[1] = False
        # установка значений RadioButton и PuchButton
        if dop[0]:
            self.radio_author_settings.setChecked(True)
            self.button_enter_color.setEnabled(False)
            self.button_enter_text.setEnabled(False)
            self.button_enter_button.setEnabled(False)
            self.button_enter_author.setEnabled(True)
            if dop[1]:
                self.radio_ligth.setChecked(True)
            else:
                self.radio_dark.setChecked(True)
        else:
            self.radio_exper_settings.setChecked(True)
            self.button_enter_color.setEnabled(True)
            self.button_enter_text.setEnabled(True)
            self.button_enter_button.setEnabled(True)
            self.button_enter_author.setEnabled(False)

    def enter_settings(self):
        dop = []
        # запись в файл информации о настройках, полученной из RadioButton
        if self.radio_author_settings.isChecked():
            dop.append('True')
            if self.radio_ligth.isChecked():
                dop.append('True')
            else:
                dop.append('False')
        else:
            dop.append('False')
            dop.append('True')
        with open("radiobutton.txt", 'w') as f:
            f.write('\n'.join(dop))
        self.button_layout()

    def enter_author(self):
        # если выбраны авторские настройки, установка светлой или темной темы
        global color_button, color_bacgr, color_text
        if self.radio_ligth.isChecked():
            color_text = 'black'
            color_bacgr = '#f1f1f1'
            color_button = '#e3e3e3'
            dop = '\n'.join([color_text, color_bacgr, color_button])
            with open("color.txt", 'w') as f:
                f.write(dop)
            dop = ['True', 'True']
        else:
            color_text = 'white'
            color_bacgr = '#343434'
            color_button = '#636363'
            dop = '\n'.join([color_text, color_bacgr, color_button])
            with open("color.txt", 'w') as f:
                f.write(dop)
            dop = ['True', 'False']
        with open("radiobutton.txt", 'w') as f:
            f.write('\n'.join(dop))
        self.color_layout()

    def enter_color(self):
        global color_bacgr
        # установка фона в экспериментальных настройках
        dop = QColorDialog.getColor()
        color, press_indi = dop.name(), dop.isValid()
        if press_indi:
            color_bacgr = color
            with open("color.txt", 'w') as f:
                f.write('\n'.join([color_text, color_bacgr, color_button]))
        self.color_layout()

    def enter_text(self):
        global color_text
        # установка текста в экспериментальных настройках
        dop = QColorDialog.getColor()
        color, press_indi = dop.name(), dop.isValid()
        if press_indi:
            color_text = color
            with open("color.txt", 'w') as f:
                f.write('\n'.join([color_text, color_bacgr, color_button]))
        self.color_layout()

    def enter_button(self):
        global color_button
        # установка цыета кнопок в экспериментальных настройках
        dop = QColorDialog.getColor()
        color, press_indi = dop.name(), dop.isValid()
        if press_indi:
            color_button = color
            with open("color.txt", 'w') as f:
                f.write('\n'.join([color_text, color_bacgr, color_button]))
        self.color_layout()

    def open_diary(self):
        # открытие дневника
        self.second_form = Diary(self)
        self.second_form.show()
        self.close()

    def open_notebook(self):
        # открытие блокнота
        self.second_form = Notebook(self)
        self.second_form.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Diary()
    ex.show()
    sys.exit(app.
    exec ())
print()
