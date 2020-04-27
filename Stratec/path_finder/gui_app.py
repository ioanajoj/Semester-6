import sys
import numpy as np

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QTableWidget, QTableWidgetItem, \
    QHeaderView, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QSpinBox, QMessageBox

from path_finder.domain import Playground


class StartWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super(StartWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Stratec")

        self.selected_file = None

        self.layout = QVBoxLayout()

        height_layout = QHBoxLayout()
        height_layout.addWidget(QLabel('Height: '))
        self.height_spin = QSpinBox()
        height_layout.addWidget(self.height_spin)
        self.layout.addLayout(height_layout)

        width_layout = QHBoxLayout()
        width_layout.addWidget(QLabel('Width: '))
        self.width_spin = QSpinBox()
        width_layout.addWidget(self.width_spin)
        self.layout.addLayout(width_layout)

        # open empty playground button
        self.open_empty_playground_button = QPushButton('Open empty playground')
        self.open_empty_playground_button.clicked.connect(self.open_empty_playground_button_clicked)
        self.layout.addWidget(self.open_empty_playground_button)

        # load playground from csv file
        self.open_file_dialog_button = QPushButton('Load playground from csv file')
        self.open_file_dialog_button.clicked.connect(self.open_file_dialog_button_clicked)
        self.layout.addWidget(self.open_file_dialog_button)

        self.setLayout(self.layout)
        self.game_windows = []

        self.open_selected_file_button = QPushButton('Open')
        self.open_selected_file_button.clicked.connect(self.load_playground_from_selected_file)

    def open_empty_playground_button_clicked(self):
        print('open_empty_playground_button_clicked')
        if self.height_spin.value() < 5 or self.width_spin.value() < 5:
            QMessageBox.about(self,
                              ':(',
                              'Please change height and width to values higher or equal to 5')
        else:
            playground = Playground(shape=np.array([self.height_spin.value(), self.width_spin.value()]))
            new_game = MainWindow(playground=playground)
            self.game_windows.append(new_game)
            new_game.show()

    def open_file_dialog_button_clicked(self):
        print('open_csv_file_button_clicked')
        select_file_widget = FileDialog()
        select_file_widget.open_file_name_dialog()
        select_file_widget.show()

        if select_file_widget.selected_filename:
            h_layout = QHBoxLayout()
            self.selected_file = select_file_widget.selected_filename
            h_layout.addWidget(QLabel(select_file_widget.selected_filename))
            open_selected_file_button = QPushButton('Open')
            open_selected_file_button.clicked.connect(
                lambda: self.load_playground_from_selected_file(select_file_widget.selected_filename)
            )
            h_layout.addWidget(open_selected_file_button)
            self.layout.addLayout(h_layout)
        select_file_widget.close()

    def load_playground_from_selected_file(self, file):
        playground = Playground(filepath=file)
        new_game = MainWindow(playground=playground)
        self.game_windows.append(new_game)
        new_game.show()


class MainWindow(QWidget):

    def __init__(self, *args, playground=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Stratec (Almost) Path Finder")
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
        if not playground:
            self.complete_path_button.setDisabled(True)
            self.next_step_button.setDisabled(True)

        configure_board_layout = QHBoxLayout()
        self.add_pins_button = QPushButton(text='Add pair of pins')
        self.add_pins_button.clicked.connect(self.add_pins_button_clicked)
        configure_board_layout.addWidget(self.add_pins_button)
        self.layout.addLayout(configure_board_layout)

        # table widget for playground
        if playground:
            self.table_widget = TableWidget(playground)
            self.layout.addWidget(self.table_widget)
        else:
            label = QLabel("Could not display table widget :(")
            label.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(label)

        # save button
        self.save_configuration_button = QPushButton(text='Save configuration as csv')
        self.save_configuration_button.clicked.connect(self.save_configuration_button_clicked)
        self.layout.addWidget(self.save_configuration_button)

        self.setLayout(self.layout)

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
        # self.table_widget.next_step_parallel()

    def add_pins_button_clicked(self):
        print('add_pins_button_clicked')
        self.table_widget.add_pins()

    def save_configuration_button_clicked(self):
        select_file_widget = FileDialog()
        select_file_widget.save_file_dialog()
        select_file_widget.show()
        if select_file_widget.selected_filename:
            self.table_widget.playground.save_to_csv(select_file_widget.selected_filename)


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

    def next_step_parallel(self):
        for pp in self.playground.points_pq:
            self.clean_path(pp.path[0])
            self.clean_path(pp.path[1])
        self.playground.a_star_steps()
        for pp in self.playground.points_pq:
            if pp.completed:
                self.draw_path(pp.final_path)
            else:
                self.draw_path(pp.path[0])
                self.draw_path(pp.path[1])

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

    def add_pins(self):
        selected = self.table.selectedIndexes()
        if len(selected) != 2:
            QMessageBox.about(self,
                              ':(',
                              'Please select two points in the table')
        else:
            for index in self.table.selectedIndexes():
                print(f'{index.row()} {index.column()}')
            self.playground.add_points(
                (selected[0].row(), selected[0].column()),
                (selected[1].row(), selected[1].column())
            )
            self.show_numbered_pins()


class FileDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Dialog'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.selected_filename = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

    def open_file_name_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                   "All Files (*);;CSV Files (*.csv)", options=options)
        print(file_name)
        self.selected_filename = file_name

    def save_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                   "All Files (*);;CSV Files (*.csv)", options=options)
        print(file_name)
        self.selected_filename = file_name


if __name__ == '__main__':
    filepath = '..\\2020_Internship_Challenge_Software\\Step_Two-Z.csv'
    app = QApplication(sys.argv)

    startWindow = StartWindow()
    startWindow.show()

    app.exec_()
