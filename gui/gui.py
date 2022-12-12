from PySide6.QtWidgets import (
    QMainWindow, QGridLayout,
    QWidget, QTabWidget, QLabel,
    QComboBox, QListWidget,
    QListWidgetItem, QTabWidget,
    QLayout, QVBoxLayout, QHBoxLayout,
    QButtonGroup, QPushButton, QFileDialog,
    QDialog, QMessageBox, QMenu, QListView, 
    QTextEdit, QToolBar, QAbstractItemView
)
from PySide6.QtCore import (
    Qt, QRect, QSize, QMimeData
)
from PySide6.QtGui import (
    QFont, QAction, QCloseEvent, QMouseEvent, QDrag,
    QDragEnterEvent, QDropEvent, QContextMenuEvent
)

from utils.consts import *
from utils.parse_out import *
from utils.template_keys import *


def clicked(btn, func):
    btn.clicked.connect(func)


def pressed(btn, func):
    btn.pressed.connect(func)


def released(btn, func):
    btn.released.connect(func)


def toggled(btn, func):
    btn.toggled.connect(func)


class Menu(QMenu):
    def __init__(self, parent: QWidget=None, **kwargs):
        super(Menu, self).__init__(parent)

        actions = kwargs.get('actions', dict())
        self.setFont(QFont(*MENU_FONT))
        
        for text, func in actions.items():
            action = QAction(text)
            action.triggered.connect(func)
            self.addAction(action)            


class ToolBar(QToolBar):
    def __init__(self, parent: QWidget=None, **kwargs):
        super(ToolBar, self).__init__(parent)
        
        actions = kwargs.get('actions', dict())
        icon_size = kwargs.get('icon_size', (32, 32))
        self.setIconSize(QSize(*icon_size))
        self.setFont(QFont(*TOOLBAR_FONT))
        self.setMovable(False)
        self.setFloatable(False)

        for btn_text, func in actions.items():
            btn = QAction(btn_text, parent)
            btn.triggered.connect(func)
            self.addAction(btn)


class ExpressionCalc(QMainWindow):
    def __init__(self, parent: QWidget=None, **kwargs):
        super(ExpressionCalc, self).__init__(parent)

        self.resize(600, 300)
        self.setWindowTitle("Expression Editor")
        domains = kwargs.get('domains', dict())
        self.expression = kwargs.get('expression')
        self.user_vars = kwargs.get('user_variables', None)

        if not self.expression:
            self.expression = QListWidgetItem()
            self.expression.setText('')

        solution_vars = SOLUTION_KEYS
        turbo_vars = TURBO_KEYS
        functions = FUNCTION_KEYS

        self.editor = QTextEdit()
        self.editor.setText(self.expression.text())
        self.editor.setFont(QFont(*MSG_FONT))
        self.ok_btn = PushButton(text='Ok', )
        self.ok_btn.clicked.connect(self.close_editor)

        layout = GridLayout(widgets=[
            ['widget', self.editor, [0, 0]], ['widget', self.ok_btn, [1, 0]]
        ])

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.menu = self.menuBar()
        self.variables_menu = self.menu.addMenu("&Variables")
        self.locations_menu = self.menu.addMenu("&Locations")
        self.functions_menu = self.menu.addMenu("&Functions")
        if self.user_vars:
            self.user_vars_menu = self.menu.addMenu('&User Variables')
            self.user_vars_menu.triggered.connect(self.paste_vars)
            for var in self.user_vars:
                action = QAction(var, self)
                action.setText(var)
                self.user_vars_menu.addAction(action)

        self.solution_submenu = self.variables_menu.addMenu("&Solution")
        self.turbo_submenu = self.variables_menu.addMenu("&Turbo")

        self.functions_menu.triggered.connect(self.paste_vars)
        self.solution_submenu.triggered.connect(self.paste_func)
        self.turbo_submenu.triggered.connect(self.paste_func)
        
        for function in functions:
            action = QAction(function, self)
            action.setText(function)
            self.functions_menu.addAction(action)

        for domain, interfaces in domains.items():
            dmn_submenu = self.locations_menu.addMenu(domain)
            dmn_submenu.triggered.connect(self.paste_func)
            for interface in interfaces:
                action = QAction(interface, self)
                action.setText(interface)
                dmn_submenu.addAction(action)

        for var in solution_vars:
            action = QAction(var, self)
            action.setText(var)
            self.solution_submenu.addAction(action)

        for var in turbo_vars:
            action = QAction(var, self)
            action.setText(var)
            self.turbo_submenu.addAction(action)

    def close_editor(self):
        if self.editor.toPlainText():
            self.expression.setText(self.editor.toPlainText())
        else:
            self.expression = None
        self.close()

    def paste_vars(self, action):
        text = action.text()
        self.editor.insertPlainText(text)
    
    def paste_func(self, action):
        text = f'"{action.text()}"'
        self.editor.insertPlainText(text)
    
    def closeEvent(self, event: QCloseEvent) -> None:

        if self.editor.toPlainText():
            self.expression.setText(self.editor.toPlainText())
        else:
            self.expression = None
        return super().closeEvent(event)
        

class Dialog(QDialog):
    def __init__(self, name, parent=None):
        super(Dialog, self).__init__(parent)
        self.resize(600, 300)
        self.label = QLabel(name, self)


class Menu(QMenu):
    def __init__(self, actions: dict):
        super(Menu, self).__init__()
        for text, action in actions.items():
            self.addAction(text, action)
            

class Label(QLabel):
    def __init__(self, text: str, geometry: list, 
                alignment: Qt.AlignmentFlag=[Qt.AlignHCenter, Qt.AlignVCenter], **kwargs):
        super(Label, self).__init__()

        font = kwargs.get('font', FONT)
        qfont = QFont(*font)

        self.setText(text)
        rect = QRect(*geometry)
        self.setGeometry(rect)
        self.setAlignment(alignment[0])
        self.setAlignment(alignment[1])
        self.setFont(qfont)
        self.setWordWrap(True)


class ComboBox(QComboBox):
    def __init__(self, geometry: list=[], **kwargs):
        super(ComboBox, self).__init__()

        font = kwargs.get('font', FONT)
        qfont = QFont(*font)
        size = QSize(*geometry)
        min_width = kwargs.get('min_width', 128)
        min_height = kwargs.get('min_width', 32)
        self.setFixedSize(size)
        self.setFont(qfont)

        if any([g for g in geometry]):
            size = QSize(*geometry)
            self.setFixedSize(size)
        elif not geometry:
            self.setResizeMode(QListView.Adjust)
            self.setMinimumWidth(min_width)
            self.setMinimumHeight(min_height)

    def set_items(self, items: list):
        if hasattr(items, '__iter__'):
            self.addItems(items)


class DragItem(QListWidgetItem):
    def __init__(self, parent=None):
        super(DragItem, self).__init__()
        self.parent = parent

    def mousePressEvent(self, event: QMouseEvent) -> None:

        if event.buttons() == Qt.LeftButton:
            drag = QDrag(self.parent)
            mime = QMimeData()
            drag.setMimeData(mime)
            drag.exec(Qt.MoveAction)
        return super().mousePressEvent(event)


class ListWidget(QListWidget):
    def __init__(self, geometry: list=[], **kwargs):
        super(ListWidget, self).__init__()

        font = kwargs.get('font', LIST_FONT)
        qfont = QFont(*font)
        alignment = kwargs.get('alignment', Qt.AlignLeft)
        min_width = kwargs.get('min_width', 128)
        min_height = kwargs.get('min_width', 32)
        drag_n_drop = kwargs.get('drag_n_drop', None)
        self.cmenu_actions = kwargs.get('context_menu_actions', None)

        self.setItemAlignment(alignment)
        self.setWordWrap(True)
        self.setWrapping(True)
        if not geometry:
            self.setMinimumWidth(min_width)
            self.setMinimumHeight(min_height)
        else:
            self.setGeometry(QRect(geometry))
        self.setFont(qfont)
        if drag_n_drop:
            self.setAcceptDrops(True)
            self.setDragDropMode(drag_n_drop)

    def set_items(self, items: list, size_hint: list=[]):
        if hasattr(items, '__iter__'):
            for item in items:
                wi = QListWidgetItem(self)
                wi.setText(item)
                wi.setSizeHint(QSize(*size_hint))
                wi.setFlags(
                    Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
                )
                self.addItem(wi)

    def insert_item(self, item: QListWidgetItem, row: int, size_hint: list=[]):
        if isinstance(item, QListWidgetItem):
            item.setSizeHint(QSize(*size_hint))
            item.setFlags(
                Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
            )
            self.insertItem(row, item)

    def mousePressEvent(self, event: QMouseEvent) -> None:

        if event.buttons() == Qt.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)
            drag.exec(Qt.MoveAction)

        return super().mousePressEvent(event)

    def contextMenuEvent(self, arg__1: QContextMenuEvent) -> None:

        if self.cmenu_actions:
            menu = Menu(actions=self.cmenu_actions)
            menu.exec(self.mapToGlobal(arg__1.pos()))
        return super().contextMenuEvent(arg__1)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        event.accept()

    def dragMoveEvent(self, event: QDragEnterEvent) -> None:
        event.accept()

    def dropEvent(self, event: QDropEvent) -> None:
        pos = event.pos()
        event.setDropAction(Qt.MoveAction)
        current_row = self.currentRow()
        current_item = self.item(current_row)
        item = self.itemAt(pos.x(), pos.y())
        row = self.row(item)
        self.insertItem(row, current_item)
        event.accept()


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

        text = settings.get('text', 'Push Me!')
        checkable = settings.get('checkable', True)
        shortcut = settings.get('shortcut', None)
        font = settings.get('font', FONT)

        self.setText(text)
        self.setCheckable(checkable)
        self.setFont(QFont(*font))
        
        if shortcut:
            self.setShortcut(shortcut)


class FileDialog(QFileDialog):
    def __init__(self, **settings):
        super(FileDialog, self).__init__()
        self.title = settings.get('title', 'File Dialog')
        self.filter_ = settings.get('filter', None)
        self.dir = settings.get('directory', '')
        self.setWindowTitle(self.title)

    def open_direcory(self):
        self.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        directory = self.getExistingDirectory(caption=self.title, dir=self.dir)
        return directory

    def open_file(self):
        file = self.getOpenFileName(self, self.title, self.dir, self.filter_)
        return file

    def save_as(self):
        self.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        return self.getSaveFileName(caption=self.title, filter=self.filter_, dir=self.dir)


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
