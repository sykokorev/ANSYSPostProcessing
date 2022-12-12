from PySide6.QtWidgets import (
    QGridLayout, QWidget, QAbstractItemView
)
from PySide6.QtCore import Qt, Slot


from utils.consts import *
from utils.parse_out import *
from utils.template_keys import *
from gui.gui import *


class InitTab(QGridLayout):
    def __init__(self, **kwargs):
        super(InitTab, self).__init__()

        self.title = kwargs.get('title', 'Settings')
        self.__domains = None
        self.__user_vars = None
               
        self.main_layout = None

        self.initialize()


    @property
    def domains(self):
        return self.__domains

    @property
    def user_vars(self):
        return self.__user_vars

    @domains.setter
    def domains(self, domains: list):
        if hasattr(domains, '__iter__'):
            self.__domains = domains

    @user_vars.setter
    def user_vars(self, vars: list):
        if hasattr(vars, '__iter__'):
            self.__user_vars = vars
        
    def initialize(self):
        cmbbox_geom = [320, 32]
        lbl_geom = [2, 2, 24, 12]

        self.templates_cbbox = ComboBox(items=None, geometry=cmbbox_geom)
        self.templates_cbbox.setEnabled(False)

        context_menu_actions = {
            'Up': lambda: self.item_up(row=self.expression_list.currentRow()),
            'Down': lambda: self.item_down(row=self.expression_list.currentRow()),
            'Edit': self.edit_item,
            'Delete': lambda: self.item_delete(row=self.expression_list.currentRow()),
            'Add': self.item_add
        }
        self.expression_list = ListWidget(
            items=None, min_width=434, min_height=32, 
            drag_n_drop=QAbstractItemView.DragDrop,
            context_menu_actions=context_menu_actions
        )
        self.expression_list.setEnabled(False)

        label_templates = Label(text='Templates:', geometry=lbl_geom, alignment=[Qt.AlignLeft, Qt.AlignVCenter])
        label_expressions = Label(text='Expressions:', geometry=lbl_geom, alignment=[Qt.AlignLeft, Qt.AlignVCenter])

        last_row = 4
        expr_row = 2
        expr_row_lbl = 1
        widgets = [
            ['widget', QWidget(), [0, 0, 1, 2]],

            ['widget', label_templates, [0, 1]],
            ['widget', label_expressions, [expr_row_lbl, 1, 1, 2]],

            ['widget', self.templates_cbbox, [0, 2]],
            ['widget', self.expression_list, [expr_row, 1, 1, 2]],

            ['widget', QWidget(), [0, 3]],
            ['widget', QWidget(), [last_row, 0, 1, 2]]
        ]
        settings = {
            'hspace': 30, 'vspace':10, 'rect': [2, 2, 200, 200],
            'col_stretch': [[0, 1], [3, 1]], 
            'row_stretch': [[expr_row, 0.2]]
        }
        self.main_layout = GridLayout(widgets=widgets, **settings)

    def setup(self):

        self.templates_cbbox.set_items(items=TEMPLATE_KEYS)
        self.templates_cbbox.setEnabled(True)
        template = TEMPLATE_KEYS[self.templates_cbbox.currentText()]
        items = [f"{t['Variable']} = {t['Expression']}" for t in template]
        self.expression_list.set_items(items=items, size_hint=[434, 32])
        self.expression_list.setEnabled(True)
        self.user_vars = self.update_user_vars()
        self.expression_list.itemDoubleClicked.connect(self.launch_expression_editor)

    def update_user_vars(self):
        user_vars = []
        for n in range(self.expression_list.count()):
            user_vars.append(self.expression_list.item(n).text().split(sep='=')[0].strip())
        return user_vars

    @Slot()
    def launch_expression_editor(self, item):

        self.user_vars = self.update_user_vars()
        row = self.expression_list.indexFromItem(item).row()
        self.new_window = ExpressionCalc(
            self.expression_list, domains=self.domains,
            expression=item, user_variables=self.user_vars[:row]
        )
        self.new_window.show()

    @Slot()
    def item_up(self, row: int):
        if row:
            item = self.expression_list.takeItem(row)
            self.expression_list.insertItem(row-1, item)
            self.update_user_vars()

    @Slot()
    def item_down(self, row: int):
        if row < self.expression_list.count():
            item = self.expression_list.takeItem(row)
            self.expression_list.insertItem(row+1, item)
            self.update_user_vars()

    @Slot()
    def item_delete(self, row: int) -> None:
        row = self.expression_list.takeItem(row)
        self.update_user_vars()

    @Slot()
    def item_add(self):
        self.user_vars = self.update_user_vars()
        self.new_window = ExpressionCalc(
            self.expression_list, user_variables=self.user_vars,
            domains=self.domains
        )
        self.new_window.show()

        row = self.expression_list.count()

        if self.new_window.expression:
            self.expression_list.insert_item(item=self.new_window.expression, row=row, size_hint=[434, 32])
        self.update_user_vars()

    @Slot()
    def edit_item(self):
        item = self.expression_list.currentItem()
        self.launch_expression_editor(item=item)
