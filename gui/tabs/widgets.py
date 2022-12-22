from PySide6.QtWidgets import QWidget, QAbstractItemView
from PySide6.QtCore import Slot


from utils.consts import *
from utils.parse_out import *
from gui.gui import *
from gui.expression_editor import ExpressionCalc


class ExpressionList(ListWidget):
    def __init__(self, parent: QWidget=None, **kwargs):
        super(ExpressionList, self).__init__(parent, **kwargs)
        self.setIconSize(QSize(24, 24))
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

    def initialize(self, menu: Menu):
        self.setEnabled(False)
        self.context_menu = menu

    def setEnabled(self, arg__1: bool) -> None:
        return super().setEnabled(arg__1)

    def set_flags(self, item: QListWidgetItem, check_state: Qt.CheckState=Qt.CheckState.Checked):
        item.setFlags(
                item.flags() | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | 
                Qt.ItemFlag.ItemIsUserCheckable
        )
        item.setCheckState(check_state)
        return item

    @Slot()
    def add_item(self, user_vars: list=[], domains: dict={}, size_hint: list=[434, 32]) -> None:
        editor = ExpressionCalc(
            self, user_variables=user_vars, domains=domains
        )
        editor.show()
        editor.exec()

        row = self.count()
        if editor.expression:
            self.set_flags(editor.expression)
            self.insert_item(item=editor.expression, row=row, size_hint=size_hint)

    @Slot()
    def edit_item(self, user_vars: list=[], domains: dict={}) -> None:
        item = self.currentItem()
        row = self.indexFromItem(item).row()
        editor = ExpressionCalc(self, domains=domains, expression=item, 
            user_variables=user_vars[:row])
        editor.show()
        editor.exec()
        
        if editor.expression:
            self.set_flags(editor.expression)
            self.insert_item(item=editor.expression, row=self.currentRow())

    def update_list(self, items: list):
        self.clear()
        # self.set_items(items=items)

        for i, it in enumerate(items):
            item = QListWidgetItem(self)
            item.setText(it[0])
            item.setToolTip(it[1])
            item.setCheckState(CS[it[2]])
            self.insert_item(item=item, row=i)

        for row in range(self.count()):
            item = self.item(row)
            try:
                check_state = items[row][2]
            except:
                check_state = 0
            check_state = Qt.CheckState.Checked if check_state else Qt.CheckState.Unchecked
            self.set_flags(item=item, check_state=check_state)


class PerformanceMap(ExpressionList):
    def __init__(self, parent: QWidget=None, **kwargs):
        super(PerformanceMap, self).__init__(parent, **kwargs)
        self.setWordWrap(False)

    def set_flags(self, item: QListWidgetItem):
        item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
        return item

    @Slot()
    def add_item(self) -> None:
        pass

    @Slot()
    def edit_item(self) -> None:
        pass

    @Slot()
    def update_list(self, items: list):
        self.clear()
        self.set_items(items=items)
        for row in range(self.count()):
            item = self.item(row)
            self.set_flags(item)


class ExpressionCheckBox(CheckBox):
    def __init__(self, parent: QWidget=None, **kwargs):
        super(CheckBox, self).__init__(parent, **kwargs)

        self.label = kwargs.get('text', 'Expression')
        self.check_state = kwargs.get('check_state', Qt.CheckState.Unchecked)

    def initialize(self):
        self.setCheckable(True)
        self.setCheckState(self.check_state)
        self.setText(self.label)

    def update_state(self, widget: QWidget):
        widget.setEnabled(self.isChecked())


class PerformanceCheckBox(ExpressionCheckBox):
    def __init__(self, parent: QWidget=None, **kwargs):
        super(PerformanceCheckBox, self).__init__(parent, **kwargs)

        self.label = kwargs.get('text', 'Performance Map')
        self.check_state = kwargs.get('check_state', Qt.CheckState.Unchecked)


class CurvesCmbb(ComboBox):
    def __init__(self, parent: QWidget=None, **kwargs):
        super(CurvesCmbb, self).__init__(parent, **kwargs)

    def initialize(self):
        self.setEnabled(False)

    @Slot()
    def currentTextChanged(self) -> str:
        return super().currentText()

    @Slot()
    def currentIndexChanged(self) -> int:
        return super().currentIndex()


class InletCmbb(CurvesCmbb):
    def __init__(self, parent: QWidget=None, **kwargs):
        super(InletCmbb, self).__init__(parent, **kwargs)


class OutletCmbb(InletCmbb):
    def __init__(self, parent: QWidget=None, **kwargs):
        super(OutletCmbb, self).__init__(parent, **kwargs)
