from PySide6.QtWidgets import (
    QMainWindow, QGridLayout,
    QWidget, QTabWidget, QLabel,
    QLineEdit, QComboBox, QListWidget,
    QListWidgetItem, QListView, QTabWidget,
    QLayout, QVBoxLayout, QHBoxLayout
)
from PySide6.QtCore import Qt, QRect, QSize, QPoint
from PySide6.QtGui import QFont


FONT = ['Calibri', 14]


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


class GriDLayout(QGridLayout):
    def __init__(self, widgets: list, **settings):
        super(GriDLayout, self).__init__()

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
        

class MainWindow(QMainWindow):

    def __init__(self, **kwargs):
        
        super().__init__()
        size = kwargs.get('size', [1280, 720])
        title = kwargs.get('Title', '')
        self.setWindowTitle(title)
        self.resize(*size)
        self.domains = kwargs.get('domains')
        self.domain_layout = self.domainsUI()

        tabs = {
            'Settings': self.domain_layout,
            'Turbo Surfaces': QWidget(),
            'Images': QWidget(),
            'Report': QWidget(),
            'Presentation': QWidget()
        }

        self.tab_widget = TabWidget(tabs=tabs)
        self.turbosurface_layout = self.turbosurfaceUI()
        self.setCentralWidget(self.tab_widget)


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
        domainUIGridLayout = GriDLayout(widgets=widgets, **settings)

        return domainUIGridLayout

    def turbosurfaceUI(self):
        ts_layout = QGridLayout()


    def domain_activated(self, idx):
        current_domain = list(self.domains.keys())[idx]
        self.interfaces_list.clear()
        for i, item in enumerate(self.domains[current_domain]):
            qitem = QListWidgetItem(item)
            self.interfaces_list.insertItem(i, qitem)

    def interface_activate(self, item):
        return item.text()
