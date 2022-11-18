from PySide6.QtWidgets import (
    QMainWindow, QGridLayout,
    QWidget, QTabWidget, QLabel,
    QLineEdit, QComboBox, QListWidget,
    QListWidgetItem, QTabWidget,
    QLayout, QVBoxLayout, QHBoxLayout,
    QButtonGroup, QPushButton, QFileDialog,
    QDialog, QMessageBox, QMenu
)
from PySide6.QtCore import (
    Qt, QRect, QSize, QEvent, QObject
)
from PySide6.QtGui import QFont, QMouseEvent, QContextMenuEvent, QAction

from utils.consts import FONT, MSG_FONT
from utils.parse_out import *



def clicked(btn, func):
    btn.clicked.connect(func)


def pressed(btn, func):
    btn.pressed.connect(func)


def released(btn, func):
    btn.released.connect(func)


def toggled(btn, func):
    btn.toggled.connect(func)


class Dialog(QDialog):
    def __init__(self, actions: dict, parent=None):
        super(Dialog, self).__init__()
        self.actions_ = None

    def eventFilter(self, source: QObject, event: QEvent) -> bool:
        if event == QEvent.ContextMenu and source in (QListWidget):
            menu = QMenu()
            for text, action in self.actions_.items():
                menu.addAction(text)
                if menu.exec(event.globalPos()):
                    item = source.itemAt(event.pos())
                    print(item.text)
            return True

        return super().eventFilter(source, event)

    def set_action(self, actions):
        self.action = actions


class Menu(QMenu):
    def __init__(self, actions):
        super(Menu, self).__init__()
        for action in actions:
            self.addAction(action)


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
    def __init__(self, geometry: list, **kwargs):
        super(ComboBox, self).__init__()

        font = kwargs.get('font', FONT)
        qfont = QFont(*font)
        size = QSize(*geometry)
        self.setFixedSize(size)
        self.setFont(qfont)

    def set_items(self, items: list):
        if hasattr(items, '__iter__'):
            self.addItems(items)


class ListWidget(QListWidget):
    def __init__(self, geometry: list, **kwargs):
        super(ListWidget, self).__init__()

        font = kwargs.get('font', FONT)
        qfont = QFont(*font)
        alignment = kwargs.get('alignment', Qt.AlignLeft)

        self.setItemAlignment(alignment)
        size = QSize(*geometry)
        self.setFixedSize(size)
        self.setFont(qfont)
        self.context_menu = None
        self.actions_ = kwargs.get('actions')

    def set_items(self, items: list):
        if hasattr(items, '__iter__'):
            self.addItems(items)

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        if self.actions_:
            print(self.actions_)
            self.context_menu = Menu(actions=self.actions_)
            
        return super().contextMenuEvent(event)


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

        self.filters = settings.get('filter', None)

    def open_directory(self):
        self.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        self.setOption(QFileDialog.Option.ShowDirsOnly)
        return self.getExistingDirectory()


class MessageBox(QMessageBox):
    def __init__(self, **kwargs):
        super(MessageBox, self).__init__()

        detail = kwargs.get('detail', None)
        information = kwargs.get('information', None)
        title = kwargs.get('title', 'Information')
        buttons = kwargs.get('buttons', None)
        font = kwargs.get('font', MSG_FONT)

        self.setFont(QFont(*font))

        if detail:
            self.setDetailedText(detail)
        if not information:
            self.setInformativeText('Information')
        else:
            self.setInformativeText(information)

        self.setWindowTitle(title)

        if not buttons:
            self.setStandardButtons(QMessageBox.StandardButton.Ok)
        else:
            for text, btn in buttons.items():
                self.addButton(btn)
                btn.setText(text)


class MainWindow(QMainWindow):

    def __init__(self, **kwargs):
        
        super().__init__()

        empty = QWidget()

        size = kwargs.get('size', [1280, 720])
        title = kwargs.get('Title', '')
        self.setWindowTitle(title)
        self.resize(*size)
        self.domains = kwargs.get('domains', None)

        self.init_settings_UI()

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
            'Settings': self.domain_UI_grid_layout,
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

    def init_settings_UI(self):
        self.dmn_cmbbox = ComboBox(items=None, geometry=[128, 32], alingment=Qt.AlignLeft)
        self.dmn_cmbbox.setEnabled(False)
        self.interfaces_list = ListWidget(items=None, geometry=[300, 400])
        self.interfaces_list.setEnabled(False)
        label = Label(text='Domains:', geometry=[2, 2, 24, 12], alignment=[Qt.AlignLeft, Qt.AlignVCenter])

        widgets = [
            ['widget', label, [0, 0]],
            ['widget', self.dmn_cmbbox, [0, 1]],
            ['widget', self.interfaces_list, [2, 0, 1, 2]],
            ['widget', QWidget(), [0, 3]],
            ['widget', QWidget(), [3, 0, 1, 2]]
        ]
        settings = {
            'hspace': 30, 'vspace':10, 'rect': [2, 2, 200, 200],
            'col_stretch': [[3, 1]], 'row_stretch': [[3, 1]]
        }
        self.domain_UI_grid_layout = GridLayout(widgets=widgets, **settings)

    def domains_UI(self):

        self.dmn_cmbbox.set_items(items=self.domains.keys())
        self.dmn_cmbbox.currentIndexChanged.connect(self.domain_activated)
        self.dmn_cmbbox.activated.connect(self.domain_activated)
        self.interfaces_list.clear()
        idx = self.dmn_cmbbox.currentIndex()
        current_domain = list(self.domains.keys())[idx]
        self.interfaces_list.set_items(items=self.domains[current_domain])

    def turbosurfaceUI(self):
        widget = QWidget()
        ts_layout = GridLayout(widgets=[['widget', widget, [0, 0]]])
        return ts_layout

    def controlButtonUI(self):
        btn_settings = [
            {'text': 'Open Directory', 'signals': [['clicked', self.open_directory]]},
            {'text': 'Save to ...', 'signals': [['clicked', self.save_as]]},
            {'text': 'Save template', 'signals': [['clicked', self.save_template]]},
            {'text': 'Load template', 'signals': [['clicked', self.load_template]]}
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
        
        try:
            outfiles = get_files(ext='out', directory=self.res_file_directory)
            if outfiles:
                self.interfaces_list.clear()
                self.dmn_cmbbox.clear()
                self.dmn_cmbbox.setEnabled(True)
                self.interfaces_list.setEnabled(True)
                self.domains = get_domains(outfile=outfiles[0])
                self.domains_UI()
            else:
                msg = 'Out files have not been found.'
                ex = 'Files Not Found'
                diag = MessageBox(title=ex, information=msg)
                diag.show()
                diag.exec()
        except FileNotFoundError as ex:
            pass


    def save_as(self):
        pass

    def save_template(self):
        pass

    def load_template(self):
        pass
