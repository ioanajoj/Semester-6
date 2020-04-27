import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QGridLayout, QTableWidget, QTableWidgetItem, \
    QHeaderView, QPushButton, QVBoxLayout, QHBoxLayout

from brute_force.domain import Playground


class MainWindow(QMainWindow):

    def __init__(self, *args, playground=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Stratec Path (Almost) Finder")
        self.resize(playground.board.shape[0] * 45, playground.board.shape[1] * 30)

        # main layout
        self.layout = QVBoxLayout()

        # details layout
        details_layout = QHBoxLayout()
        self.selection_label = QLabel(text='No selected pair of points')
        details_layout.addWidget(self.selection_label)

        self.layout.addLayout(details_layout)

        # buttons layout
        # next path button
        horizontal_layout = QHBoxLayout()
        self.complete_path_button = QPushButton(text='Next path')
        self.complete_path_button.clicked.connect(self.complete_path_button_clicked)
        horizontal_layout.addWidget(self.complete_path_button)
        # next step for current path
        self.next_step_button = QPushButton(text='Next step on current path')
        self.next_step_button.clicked.connect(self.next_step_button_clicked)
        horizontal_layout.addWidget(self.next_step_button)

        self.layout.addLayout(horizontal_layout)

        # table widget for playground
        if playground:
            self.table_widget = TableWidget(playground)
            self.layout.addWidget(self.table_widget)
        else:
            label = QLabel("Could not display table widget :(")
            label.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(label)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

    def complete_path_button_clicked(self):
        print('complete_path_button_clicked')
        if not self.table_widget.playground.set_pp():
            self.selection_label.setText('Finished routing')
        else:
            self.selection_label.setText(f'Current pair of points {self.table_widget.playground.current_pp.value}')
            self.table_widget.complete_path()

    def next_step_button_clicked(self):
        print('next_step_button_clicked')
        if not self.table_widget.playground.set_pp():
            self.selection_label.setText('Finished routing')
        else:
            self.selection_label.setText(f'Current pair of points {self.table_widget.playground.current_pp.value}')
            self.table_widget.next_step()


class TableWidget(QWidget):

    def __init__(self, playground):
        super(TableWidget, self).__init__()
        self.playground = playground
        self.green_value = 80
        self.table = None
        self.initUI()
        self.show_numbered_pins()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        self.table = QTableWidget(self)
        self.table.setRowCount(self.playground.board.shape[0])
        self.table.setColumnCount(self.playground.board.shape[1])

        labels = [str(i) for i in range(self.playground.board.shape[0])]
        self.table.setHorizontalHeaderLabels(labels)
        self.table.setVerticalHeaderLabels(labels)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        grid.addWidget(self.table, 0, 0)
        self.show()

    def show_numbered_pins(self):
        for pin_pair in self.playground.points_pq:
            item_x = QTableWidgetItem(str(pin_pair.value))
            item_x.setBackground(QBrush(QColor(137, 84, 222)))
            item_y = QTableWidgetItem(str(pin_pair.value))
            item_y.setBackground(QBrush(QColor(137, 84, 222)))
            self.table.setItem(pin_pair.x[0], pin_pair.x[1], item_x)
            self.table.setItem(pin_pair.y[0], pin_pair.y[1], item_y)

    def complete_path(self):
        if not self.playground.current_pp.completed:
            self.clean_path(self.playground.current_pp.path[0])
            self.clean_path(self.playground.current_pp.path[1])
        self.playground.a_star()
        self.draw_path(self.playground.current_pp.final_path)

    def next_step(self):
        self.clean_path(self.playground.current_pp.path[0])
        self.clean_path(self.playground.current_pp.path[1])
        self.playground.go_one_step()
        if self.playground.current_pp.completed:
            self.draw_path(self.playground.current_pp.final_path)
        else:
            self.draw_path(self.playground.current_pp.path[0])
            self.draw_path(self.playground.current_pp.path[1])

    def draw_path(self, path):
        if not path:
            return
        value = str(self.playground.board[path[0]])
        for coords in path:
            item = QTableWidgetItem(str(value))
            item.setBackground(QBrush(QColor(235, self.green_value, 52)))
            self.table.setItem(coords[0], coords[1], item)
        self.green_value += 50
        self.green_value = self.green_value % 255

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def clean_path(self, path):
        for coords in path:
            if self.table.item(coords[0], coords[1]):
                self.table.item(coords[0], coords[1]).setText('')
                self.table.item(coords[0], coords[1]).setBackground(QBrush(QColor(255, 255, 255)))
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()


if __name__ == '__main__':
    filepath = '..\\2020_Internship_Challenge_Software\\Step_Two-Z.csv'

    playground = Playground(filepath)
    print('Starting GUI..')

    app = QApplication(sys.argv)
    window = MainWindow(playground=playground)
    window.show()
    app.exec_()
