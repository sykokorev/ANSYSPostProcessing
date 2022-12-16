from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Slot


from utils.consts import *
from utils.parse_out import *
from gui.gui import *
from gui.expression_editor import ExpressionCalc


class ExpressionList(ListWidget):
    def __init__(self, parent: QWidget=None, **kwargs):
        super(ExpressionList, self).__init__(parent, **kwargs)

    def initialize(self, menu: Menu):
        self.setEnabled(False)
        self.context_menu = menu

    def setEnabled(self, arg__1: bool) -> None:
        return super().setEnabled(arg__1)
    
    @Slot()
    def add_item(self, user_vars: list=[], domains: dict={}, size_hint: list=[434, 32]) -> None:
        editor = ExpressionCalc(
            self, user_variables=user_vars, domains=domains
        )
        editor.show()
        editor.exec()

        row = self.count()
        if editor.expression:
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
            size_hint = [self.sizeHintForColumn(0), self.sizeHintForRow(0)]
            self.insert_item(item=editor.expression, row=self.currentRow(), size_hint=size_hint)

    def update_list(self, items: list):
        self.clear()
        self.set_items(items=items)


class PerformanceMap(ExpressionList):
    def __init__(self, parent: QWidget=None, **kwargs):
        super(PerformanceMap, self).__init__(parent, **kwargs)
        self.setWordWrap(False)

    @Slot()
    def add_item(self) -> None:
        pass

    @Slot()
    def edit_item(self) -> None:
        pass


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
