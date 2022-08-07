import sys
import os
from PyQt6.QtCore import Qt
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

        # the history of user, updated if
        self.history = [os.getcwd()]

        # search setup
        self.SearchLine.setText(os.getcwd())
        self.SearchLine.textChanged.connect(self.text_changed)
        self.SearchLine.returnPressed.connect(self.return_pressed)

        # text that in search line
        self.text = os.getcwd()

        # setup previous and next folder
        self.PreviousFolder.setIcon(self.left_arrow)
        self.NextFolder.setIcon(self.right_arrow)
        # self.PreviousFolder.released().connect
        # self.NextFolder.released().connect

        self.draw_scrollbar()

    # def next_folder(self):
    #     if


    def change_directory(self, dir):
        try:
            new_path = os.getcwd() + os.sep + dir
            os.chdir(new_path)

            self.history.append(new_path)
            self.text = os.getcwd()
            self.SearchLine.setText(new_path)

            self.draw_scrollbar()
        except:
            pass

    def text_changed(self, s):
        self.text = s

    def return_pressed(self):
        try:
            os.chdir(self.text)
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
