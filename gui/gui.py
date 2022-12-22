from PySide6.QtWidgets import (
    QGridLayout, QWidget, QTabWidget, QLabel,
    QComboBox, QListWidget,
    QListWidgetItem, QTabWidget,
    QLayout, QVBoxLayout, QHBoxLayout,
    QButtonGroup, QPushButton, QFileDialog,
    QDialog, QMessageBox, QMenu, QToolBar,
    QLineEdit, QCheckBox, QScrollBar, 
)
from PySide6.QtCore import (
    Qt, QRect, QSize, QMimeData, QEvent, Slot
)
from PySide6.QtGui import (
    QFont, QAction, QMouseEvent, QDrag,
    QDragEnterEvent, QDropEvent, QContextMenuEvent,
    QCloseEvent, Qt
)

from utils.consts import *
from utils.parse_out import *


def clicked(btn, func):
    btn.clicked.connect(func)


def pressed(btn, func):
    btn.pressed.connect(func)


def released(btn, func):
    btn.released.connect(func)


def toggled(btn, func):
    btn.toggled.connect(func)


class Action(QAction):
    def __init__(self, parent: QWidget=None, **kwargs):
        super(Action, self).__init__(parent)

        self.setParent(parent)
        actions = kwargs.get('actions', dict())
        for text, func in actions.items():
            self.setText(text)
            self.triggered.connect(func)


class Menu(QMenu):
    def __init__(self, parent: QWidget=None, **kwargs):
        super(Menu, self).__init__(parent)

        self.setParent(parent)
        actions = kwargs.get('actions', dict())

        for text, func in actions.items():
            action = QAction(text, self.parent())
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


class Dialog(QDialog):
    def __init__(self, name, parent=None):
        super(Dialog, self).__init__(parent)
        self.resize(600, 300)
        self.label = QLabel(name, self)


class Label(QLabel):
    def __init__(self, text: str, geometry: list=None, 
                alignment: Qt.AlignmentFlag=[Qt.AlignHCenter, Qt.AlignVCenter], **kwargs):
        super(Label, self).__init__()

        font = kwargs.get('font', FONT)
        qfont = QFont(*font)
        size = kwargs.get('size')

        self.setText(text)
        if geometry:
            rect = QRect(*geometry)
            self.setGeometry(rect)
        
        if size:
            self.resize(QSize(*size))
        self.setAlignment(alignment[0])
        self.setAlignment(alignment[1])
        self.setFont(qfont)
        self.setWordWrap(True)


class ComboBox(QComboBox):
    def __init__(self, parent: QWidget=None, size: list=[], **kwargs):
        super(ComboBox, self).__init__(parent, **kwargs)

        font = kwargs.get('font', FONT)
        min_width = kwargs.get('min_width', 128)
        min_height = kwargs.get('min_width', 32)

        self.setFont(QFont(*font))

        if size:
            size = QSize(*size)
            self.setFixedSize(size)
        elif not size:
            self.setMinimumWidth(min_width)
            self.setMinimumHeight(min_height)

    def set_items(self, items: list):
        if isinstance(items, list):
            self.addItems(items)
        if isinstance(items, dict):
            for row, (key, val) in enumerate(items.items()):
                self.addItem(key)
                self.setItemData(row, key, Qt.AccessibleDescriptionRole)
                for v in val:
                    self.addItem(f'\t{v}')
    
    def update_cmbb(self, item: str):
        self.addItem(item)
        self.setCurrentIndex(self.count()-1)


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
        self.__context_menu = kwargs.get('context_menu', None)
        size = kwargs.get('size')
        scrollbar = kwargs.get('scrollbar', False)

        self.setItemAlignment(alignment)
        self.setWordWrap(True)

        if scrollbar:
            scrollbar = QScrollBar(self)
            self.addScrollBarWidget(scrollbar, Qt.AlignLeft)

        if size:
            self.resize(QSize(*size))

        if not geometry:
            self.setMinimumWidth(min_width)
            self.setMinimumHeight(min_height)
        else:
            self.setGeometry(QRect(geometry))
        self.setFont(qfont)
        if drag_n_drop:
            self.setAcceptDrops(True)
            self.setDragDropMode(drag_n_drop)

    @property
    def context_menu(self):
        return self.__context_menu

    @property
    def item_text(self, row: int):
        if isinstance(row, int):
            return self.item(row).text()
        else:
            return None

    @property
    def list_items(self):
        return [self.item(row) for row in range(self.count())]

    @context_menu.setter
    def context_menu(self, menu: Menu):
        if isinstance(menu, Menu):
            self.__context_menu = menu

    def clicked(self, item: QListWidgetItem):
        print(item.text())

    def set_items(self, items: list, size_hint: list=None):
        if hasattr(items, '__iter__'):
            for item in items:
                wi = QListWidgetItem(self)
                wi.setText(item[0])
                if size_hint:
                    wi.setSizeHint(QSize(*size_hint))
                if item[1]:
                    wi.setToolTip(item[1])
                self.addItem(wi)
            col_size = self.sizeHintForColumn(0)
            for row in range(self.count()):
                if self.width() > col_size:
                    self.item(row).setSizeHint(QSize(self.width(), self.sizeHintForRow(0)))

    def add_item(self, item: list, size_hint: list=None):
        wi = QListWidgetItem(self)
        wi.setText(item[0])
        if item[1]:
            wi.setToolTip(item[1])
        if size_hint:
            wi.setSizeHint(QSize(*size_hint))
        col_size = self.sizeHintForColumn(0)
        if self.width() > col_size:
            wi.setSizeHint(QSize(self.width(), self.sizeHintForRow(0)))

    def set_item(self, item: QListWidgetItem):
        row = self.currentRow()
        self.takeItem(row)
        self.insertItem(row, item)

    def insert_item(self, item: QListWidgetItem, row: int, size_hint: list=[]) -> QListWidgetItem:
        if isinstance(item, QListWidgetItem):
            item.setSizeHint(QSize(*size_hint))
            self.insertItem(row, item)
            return self.item(row)

        return None

    def contextMenuEvent(self, arg__1: QContextMenuEvent) -> None:
        if self.__context_menu:
            self.__context_menu.exec(self.mapToGlobal(arg__1.pos()))
        return super().contextMenuEvent(arg__1)

    @Slot()
    def item_up(self) -> None:
        row = self.currentRow()
        item = self.takeItem(row)
        self.insertItem(row-1, item)

    @Slot()
    def item_down(self) -> None:
        row = self.currentRow()
        item = self.takeItem(row)
        self.insertItem(row+1, item)

    @Slot()
    def delete_item(self) -> None:
        self.takeItem(self.currentRow())
    

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
        size = settings.get('size', None)
        enable = settings.get('enable', True)

        self.setText(text)
        self.setCheckable(checkable)
        self.setFont(QFont(*font))
        self.setEnabled(enable)
        
        if shortcut:
            self.setShortcut(shortcut)
        if size:
            self.setFixedSize(QSize(*size))


class FileDialog(QFileDialog):
    def __init__(self, **settings):
        super(FileDialog, self).__init__()
        self.title = settings.get('title', 'File Dialog')
        self.filter_ = settings.get('filter', None)
        self.dir = settings.get('directory', '')
        self.buttons = settings.get('buttons')
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
    
    def open_files(self):
        files = self.getOpenFileNames(self, self.title, self.dir, self.filter_)
        return files


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

class PopUpLineEdit(QDialog):
    def __init__(self, parent: QWidget=None, **kwargs):
        super(PopUpLineEdit, self).__init__(parent)

        title = kwargs.get('title', 'Enter...')
        size = kwargs.get('size', [312, 64])
        editor_size = kwargs.get('editor_size', [306, 60])

        self.setFixedSize(*size)
        self.setWindowTitle(title)

        self.editor = QLineEdit()
        self.editor.resize(QSize(*editor_size))
        self.text = None
        self.ok_btn = PushButton(text='Ok', size=[96, 24])
        self.cancel_btn = PushButton(text='Cancel', size=[96, 24])
        self.cancel_btn.clicked.connect(self.unsave)
        self.ok_btn.clicked.connect(self.save_and_close)

        layout = GridLayout(widgets=[
            ['widget', self.editor, [0, 0, 1, 2]], 
            ['widget', self.ok_btn, [1, 0]], 
            ['widget', self.cancel_btn, [1, 1]]
        ], hspace=2, vspace=2, rect=[0, 0, 312, 64])
        widget = QWidget()
        widget.setLayout(layout)
        self.setLayout(layout)

    def save_and_close(self, event: QEvent):
        self.text = self.editor.text()
        self.close()
        return event

    def changeEvent(self, event: QEvent) -> None:
        return super().changeEvent(event)

    def unsave(self):
        self.close()

    def closeEvent(self, event: QCloseEvent) -> None:
        return super().closeEvent(event)


class CheckBox(QCheckBox):
    def __init__(self, parent: QWidget=None, **kwargs):
        super(CheckBox, self).__init__(parent)

        label = kwargs.get('label', '')
        check_state = kwargs.get('check_state', Qt.CheckState.Unchecked)

        self.setCheckable(True)
        self.setCheckState(check_state)
        self.setText(label)

class LineEdit(QLineEdit):
    def __init__(self, parent: QWidget=None, **kwargs):
        super(LineEdit, self).__init__(parent)

        text = kwargs.get('text')
        mask = kwargs.get('mask')
        size = kwargs.get('size')
        placeholder = kwargs.get('placeholder', '')
        font = kwargs.get('font', FONT)
        self.cmenu_actions = kwargs.get('context_menu')

        if size:
            self.resize(QSize(*size))
        self.setPlaceholderText(placeholder)
        self.setText(text)
        self.setFont(QFont(*font))
        if mask:
            self.setMask(mask)
        
    def contextMenuEvent(self, arg__1: QContextMenuEvent) -> None:

        if self.cmenu_actions:
            menu = Menu(actions=self.cmenu_actions)
            menu.exec(self.mapToGlobal(arg__1.pos()))
        return super().contextMenuEvent(arg__1)
