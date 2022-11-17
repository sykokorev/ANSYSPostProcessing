from PySide6.QtWidgets import (
    QMainWindow, QGridLayout,
    QWidget, QTabWidget, QLabel,
    QLineEdit, QComboBox, QListWidget,
    QListWidgetItem, QTabWidget,
    QLayout, QVBoxLayout, QHBoxLayout,
    QButtonGroup, QPushButton, QFileDialog
)
from PySide6.QtCore import Qt, QRect, QSize, QPoint
from PySide6.QtGui import QFont


from utils.consts import FONT
from utils.parse_out import *



def clicked(btn, func):
    btn.clicked.connect(func)


def pressed(btn, func):
    btn.pressed.connect(func)


def released(btn, func):
    btn.released.connect(func)


def toggled(btn, func):
    btn.toggled.connect(func)


class Label(QLabel):
    def __init__(self, text: str, geometry: list, alignment: 
                        Qt.AlignmentFlag=[Qt.AlignHCenter, Qt.AlignVCenter], **kwargs):
        super(Label, self).__init__()

        font = kwargs.get('font', FONT)
        qfont = QFont(*font)

        self.setText(text)
        rect = QRect(*geometry)
        self.setGeometry(rect)
        self.setAlignment(alignment[0])
        self.setAlignment(alignment[1])
        self.setFont(qfont)


class ComboBox(QComboBox):
    def __init__(self, items: list, geometry: list, alignment: Qt.AlignmentFlag=Qt.AlignCenter, **kwargs):
        super(ComboBox, self).__init__()

        font = kwargs.get('font', FONT)
        qfont = QFont(*font)

        self.addItems(items)
        size = QSize(*geometry)
        self.setFixedSize(size)
        self.setFont(qfont)


class ListWidget(QListWidget):
    def __init__(self, items: list, geometry: list, alignment: Qt.AlignmentFlag=Qt.AlignLeft, **kwargs):
        super(ListWidget, self).__init__()

        font = kwargs.get('font', FONT)
        qfont = QFont(*font)

        self.setItemAlignment(alignment)
        for i, item in enumerate(items):
            qitem = QListWidgetItem(item)
            self.insertItem(i, qitem)
            

        size = QSize(*geometry)
        self.setFixedSize(size)
        self.setFont(qfont)


class TabWidget(QTabWidget):
    def __init__(self, tabs: dict, **kwargs):
        super(TabWidget, self).__init__()

        font = kwargs.get('font', FONT)
        tab_position = kwargs.get('TabPosition', QTabWidget.West)

        self.setFont(QFont(*font))
        self.setTabPosition(tab_position)
        for tab, widget in tabs.items():
            if isinstance(widget, QWidget):
                self.addTab(widget, tab)
            elif isinstance(widget, (QGridLayout, QLayout, QVBoxLayout, QHBoxLayout)):
                w = QWidget()
                w.setLayout(widget)
                self.addTab(w, tab)


class GridLayout(QGridLayout):
    def __init__(self, widgets: list, **settings):
        super(GridLayout, self).__init__()

        hspace = settings.get('hspace', 30)
        vspace = settings.get('vspace', 30)
        rect = settings.get('rect', [0, 0, 200, 200])
        col_stretch = settings.get('col_stretch', [])
        row_stretch = settings.get('row_stretch', [])
        col_min_size = settings.get('col_min_size', None)
        row_min_size = settings.get('row_min_size', None)

        self.setHorizontalSpacing(hspace)
        self.setVerticalSpacing(vspace)
        self.setGeometry(QRect(*rect))

        if col_min_size:
            self.setColumnMinimumWidth(*col_min_size)
        if row_min_size:
            self.setRowMinimumHeight(*row_min_size)

        for item in widgets:
            wl = item[0]
            widget = item[1]
            position = item[2]
            if wl == 'layout':
                self.addLayout(widget, *position)
            elif wl == 'widget':
                self.addWidget(widget, *position)
        
        for col in col_stretch:
            self.setColumnStretch(*col)
        for row in row_stretch:
            self.setRowStretch(*row)


class ButtonGroup(QButtonGroup):
    def __init__(self, buttons: list):
        super(ButtonGroup, self).__init__()
        
        for btn in buttons:
            self.addButton(btn)


class PushButton(QPushButton):
    def __init__(self, **settings):
        super(PushButton, self).__init__()

        signal_map = {
            'clicked': clicked,
            'pressed': pressed,
            'released': released,
            'toggled': toggled
        }

        text = settings.get('text', 'Push Me!')
        checkable = settings.get('checkable', True)
        shortcut = settings.get('shortcut', None)
        signals = settings.get('signals', None)
        font = settings.get('font', FONT)

        self.setText(text)
        self.setCheckable(checkable)
        self.setFont(QFont(*font))
        
        if shortcut:
            self.setShortcut(shortcut)

        if signals:
            for signal in signals:
                signal_map[signal[0]].__call__(self, signal[1])


class FileDialog(QFileDialog):
    def __init__(self, **settings):
        super(FileDialog, self).__init__()

        signal_map = {
            'directoryEntered': self.dire
        }

        self.filters = settings.get('filter', None)

    def open_directory(self):
        self.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        self.setOption(QFileDialog.Option.ShowDirsOnly)
        return self.getExistingDirectory()
    

class MainWindow(QMainWindow):

    def __init__(self, **kwargs):
        
        super().__init__()

        empty = QWidget()

        size = kwargs.get('size', [1280, 720])
        title = kwargs.get('Title', '')
        self.setWindowTitle(title)
        self.resize(*size)
        self.domains = kwargs.get('domains')
        self.domain_layout = self.domainsUI()

        self.turbosurface_layout = self.turbosurfaceUI()
        self.main_layout = QGridLayout()

        self.buttons = self.controlButtonUI()
        self.buttons_layout = GridLayout(
            widgets=[
                *[['widget', btn, [row, 0]] for row, btn in enumerate(self.buttons.buttons())],
                ['widget', empty, [len(self.buttons.buttons()), 0]]
            ]
        )
        self.res_file_directory = None

        tabs = {
            'Settings': self.domain_layout,
            'Turbo Surfaces': self.turbosurface_layout,
            'Planes': QWidget(),
            'Images': QWidget(),
            'Report': QWidget(),
            'Presentation': QWidget()
        }
        self.tab_widget = TabWidget(tabs=tabs)

        self.main_layout.addWidget(self.tab_widget, 0, 0)
        self.main_layout.addLayout(self.buttons_layout, 0, 1)
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)


    def domainsUI(self):

        cmbbox = ComboBox(items=self.domains.keys(), geometry=[128, 32], alignment=Qt.AlignLeft)
        idx = cmbbox.currentIndex()
        current_domain = list(self.domains.keys())[idx]
        self.interfaces_list = ListWidget(items=self.domains[current_domain], geometry=[230, 400])
        cmbbox.currentIndexChanged.connect(self.domain_activated)
        cmbbox.activated.connect(self.domain_activated)
        label = Label(text='Domains:', geometry=[2, 2, 24, 12], alignment=[Qt.AlignLeft, Qt.AlignVCenter])
        self.interfaces_list.itemDoubleClicked.connect(self.interface_activate)

        widgets = [
            ['widget', label, [0, 0]],
            ['widget', cmbbox, [0, 1]],
            ['widget', self.interfaces_list, [2, 0, 1, 2]],
            ['widget', QWidget(), [0, 3]],
            ['widget', QWidget(), [3, 0, 1, 2]]
        ]
        settings = {
            'hspace': 30, 'vspace':10, 'rect': [2, 2, 200, 200],
            'col_stretch': [[3, 1]], 'row_stretch': [[3, 1]]
        }
        domainUIGridLayout = GridLayout(widgets=widgets, **settings)

        return domainUIGridLayout

    def turbosurfaceUI(self):
        widget = QWidget()
        ts_layout = GridLayout(widgets=[['widget', widget, [0, 0]]])
        return ts_layout

    def controlButtonUI(self):
        btn_settings = [
            {'text': 'Open Directory', 'signals': [['clicked', self.open_directory]]},
            {'text': 'Save to ...', 'signals': [['clicked', self.save_as]]},
            {'text': 'Save template', 'signals': [['clicked', self.save_template]]}
        ]
        buttons = []
        for btn in btn_settings:
            buttons.append(PushButton(**btn))

        qbtns = ButtonGroup(buttons=buttons)

        return qbtns

    def domain_activated(self, idx):
        current_domain = list(self.domains.keys())[idx]
        self.interfaces_list.clear()
        for i, item in enumerate(self.domains[current_domain]):
            qitem = QListWidgetItem(item)
            self.interfaces_list.insertItem(i, qitem)

    def interface_activate(self, item):
        return item.text()

    def open_directory(self):
        open_dir = FileDialog()
        self.res_file_directory = open_dir.open_directory()

    def save_as(self):
        pass

    def save_template(self):
        pass
