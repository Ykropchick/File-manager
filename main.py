import sys
import os
from PyQt6.QtCore import Qt
from queue import Queue
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
    QToolBar,
    QWidgetAction,
    QLineEdit,
    QToolButton,
    QLayout,
    QScrollArea,
)
from PyQt6.QtGui import QPalette, QColor, QAction, QIcon
from PyQt6.QtCore import Qt, QSize
import designed


class MainWindow(QMainWindow, designed.Ui_MainWindow):
    def __init__(self):
        # setup PyQt
        super().__init__()
        self.setupUi(self)

        # icon initialization
        self.file_icon = QIcon('file_icon.png')
        self.folder_icon = QIcon('folder_icon.png')
        self.left_arrow = QIcon('left_arrow.png')
        self.right_arrow = QIcon('right_arrow.png')

        # the history of user
        self.history = [os.getcwd()]
        self.cur_index = 0

        # search setup
        self.SearchLine.setText(os.getcwd())
        self.SearchLine.textChanged.connect(self.text_changed)
        self.SearchLine.returnPressed.connect(self.return_pressed)

        # text that in search line
        self.text = os.getcwd()

        # setup previous and next folder
        self.PreviousFolder.setIcon(self.left_arrow)
        self.NextFolder.setIcon(self.right_arrow)
        self.PreviousFolder.released.connect(self.previous_folder)
        self.NextFolder.released.connect(self.next_folder)

        self.draw_scrollbar()

    def previous_folder(self):
        if self.cur_index > 0:
            self.cur_index -= 1
            path = self.history[self.cur_index]
            print(f'previous = {self.cur_index}')
            self.SearchLine.setText(path)
            os.chdir(path)

            self.draw_scrollbar()

    def next_folder(self):
        if self.cur_index < len(self.history) - 1:
            self.cur_index += 1
            path = self.history[self.cur_index]
            print(f'next = {self.cur_index}')

            self.SearchLine.setText(path)
            os.chdir(path)

            self.draw_scrollbar()

    def change_directory(self, dir):
        try:
            new_path = os.getcwd() + os.sep + dir
            os.chdir(new_path)

            self.text = os.getcwd()
            self.SearchLine.setText(new_path)

            self.history = self.history[:self.cur_index + 1]
            self.history.append(new_path)
            self.cur_index = len(self.history) - 1
            print(self.history, self.cur_index)

            self.draw_scrollbar()
        except:
            pass

    def text_changed(self, s):
        self.text = s

    def return_pressed(self):
        try:
            os.chdir(self.text)

            self.history.append(self.text)
            self.cur_index = len(self.history) - 1

            self.draw_scrollbar()
        except:
            pass

    def draw_scrollbar(self):
        # the widget that will go to scrollbar
        self.widget = QWidget()
        # the layer of folder and their names
        self.vbox = QVBoxLayout()

        for i in os.listdir():

            # the name of file or folder
            text = QLabel(i)
            # the icon of folder and file that clickable
            button = QToolButton()

            if '.' in i:
                button.setIcon(self.file_icon)
            else:
                button.setIcon(self.folder_icon)

            button.setIconSize(QSize(50, 50))
            button.released.connect(lambda x=i: self.change_directory(x))

            self.vbox.addWidget(button)
            self.vbox.addWidget(text)

        # reduce distance between icon and names
        self.vbox.addStretch(1)
        self.widget.setLayout(self.vbox)

        self.FoldersMenu.setWidget(self.widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
