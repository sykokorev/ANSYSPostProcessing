from PySide6.QtWidgets import (
    QGridLayout, QWidget, QAbstractItemView
)
from PySide6.QtCore import Qt, Slot


from utils.consts import *
from utils.parse_out import *
from utils.template_keys import *
from gui.gui import *
from gui.expression_editor import ExpressionCalc


class InitTab(QGridLayout):
    def __init__(self, parent: QWidget=None, **kwargs):
        super(InitTab, self).__init__(parent)

        self.title = kwargs.get('title', 'Settings')
        self.__domains = {}
        self.__user_vars = None
        self.template = None
        self.main_layout = None

        self.perfomance_map_size = [434, 32]
        self.curves = {}
        self.user_variables = []

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

        exp_context_menu_actions = {
            'Up': lambda: self.item_up(row=self.expression_list.currentRow(), obj=self.expression_list),
            'Down': lambda: self.item_down(row=self.expression_list.currentRow(), obj=self.expression_list),
            'Edit': self.edit_item,
            'Delete': lambda: self.item_delete(row=self.expression_list.currentRow(), obj=self.expression_list),
            'Add': self.item_add
        }
        pm_context_menu = {
            'Move up': lambda: self.item_up(row=self.perfomance_map.currentRow(), obj=self.perfomance_map),
            'Move down': lambda: self.item_down(row=self.perfomance_map.currentRow(), obj=self.perfomance_map),
            'Delete point': lambda: self.item_delete(row=self.perfomance_map.currentRow(), obj=self.perfomance_map),
            'Add curve': self.add_curve
        }

        self.expression_list = ListWidget(
            items=None, min_width=434, min_height=32, 
            drag_n_drop=QAbstractItemView.DragDrop,
            context_menu_actions=exp_context_menu_actions,
            font=FONT
        )

        self.perfomance_map = ListWidget(
            items=None, min_width=self.perfomance_map_size[0], 
            min_height=self.perfomance_map_size[1],
            context_menu_actions=pm_context_menu,
            font=LIST_FONT, scrollbar=True
        )

        self.expression_check = CheckBox(label='Expressions:', check_state=Qt.CheckState.Unchecked)
        self.expression_check.stateChanged.connect(
            lambda: self.update_list(state=self.expression_check.checkState(), obj=self.expression_list)
        )
        self.perfomance_map_check = CheckBox(label='Performance map', check_state=Qt.CheckState.Unchecked)
        self.perfomance_map_check.stateChanged.connect(
            lambda: self.update_list(state=self.perfomance_map_check.checkState(), obj=self.perfomance_map)
        )
        self.perfomance_map_check.stateChanged.connect(
            lambda: self.update_list(state=self.perfomance_map_check.checkState(), obj=self.inlet)
        )
        self.perfomance_map_check.stateChanged.connect(
            lambda: self.update_list(state=self.perfomance_map_check.checkState(), obj=self.outlet)
        )
        self.perfomance_map_check.stateChanged.connect(
            lambda: self.update_list(state=self.perfomance_map_check.checkState(), obj=self.curves_cmb)
        )

        self.curves_cmb = ComboBox(geometry=[360, 24])
        self.curves_cmb.setEnabled(False)
        self.curves_cmb.currentIndexChanged.connect(self.curve_change)

        self.expression_list.setEnabled(False)
        self.perfomance_map.setEnabled(False)

        self.inlet = ComboBox(geometry=[360, 24], font=LIST_FONT)
        self.outlet = ComboBox(geometry=[360, 24], font=LIST_FONT)
        self.inlet.setEnabled(False)
        self.outlet.setEnabled(False)

        last_col = 6
        last_row = 0
        widgets = [
            ['widget', QWidget(), [0, 0]],
            ['widget', self.expression_check, [1, 1]],
            ['widget', self.expression_list, [2, 1, 4, 1]],
            ['widget', self.perfomance_map_check, [1, 2, 1, 2]],
            ['widget', Label(text='Curves', size=[32, 24]), [2, 2]],
            ['widget', self.curves_cmb, [2, 3]],
            ['widget', self.perfomance_map, [3, 2, 1, 2]],
            ['widget', Label(text='Inlet', size=[24, 32], font=FONT), [4, 2]],
            ['widget', Label(text='Outlet', size=[24, 32], font=FONT), [5, 2]],
            ['widget', self.inlet, [4, 3]],
            ['widget', self.outlet, [5, 3]],
            ['widget', QWidget(), [0, last_col, last_row, 1]]
        ]
        settings = {
            'hspace': 10, 'vspace':10, 'rect': [2, 2, 600, 600],
            'col_stretch': [[0, 1], [last_col, 1]]
        }
        self.main_layout = GridLayout(widgets=widgets, **settings)

    def setup(self, templates: dict=None):

        if templates:
            items = []
            for t in templates['expressions']:
                print(t)
                var = t.get('Variable', '')
                expr = t.get('Expression', '')
                desc = t.get('Description', '')
                items.append((f"{var} = {expr}", desc))
            self.expression_list.clear()
            self.expression_list.set_items(items=items, size_hint=[434, 32])
        else:
            self.expression_list.clear()
        if self.domains:
            self.outlet.set_items(items=self.domains)
            self.inlet.set_items(items=self.domains)

        self.user_vars = self.update_user_vars()
        self.expression_list.itemDoubleClicked.connect(self.launch_expression_editor)

    def update(self, templates: dict) -> None:
        self.setup(templates=templates)
        
    def load(self, **kwargs):
        expressions = kwargs.get('expressions')
        if expressions:
            self.setup(template=expressions)

    def update_user_vars(self):
        user_vars = []
        for n in range(self.expression_list.count()):
            user_vars.append(self.expression_list.item(n).text().split(sep='=')[0].strip())
        return user_vars

    def update_curves_cmb(self, curve: str=None) -> None:
        if curve:
            self.curves_cmb.addItem(curve)
            files = [(os.path.split(f)[1], '') for f in self.curves[curve]]
            self.perfomance_map.set_items(items=files)

    @Slot()
    def curve_change(self, curve_idx):
        self.perfomance_map.clear()
        curve = self.curves_cmb.itemText(curve_idx)
        items = [(os.path.split(f)[1], '') for f in self.curves[curve]]
        self.perfomance_map.set_items(items=items)

    @Slot()
    def launch_expression_editor(self, item):

        self.user_vars = self.update_user_vars()
        row = self.expression_list.indexFromItem(item).row()
        self.new_window = ExpressionCalc(
            self.expression_list, domains=self.domains,
            expression=item, user_variables=self.user_vars[:row]
        )
        self.new_window.show()
        self.new_window.exec()

    @Slot()
    def item_up(self, row: int, obj: QListWidget):
        if row:
            item = obj.takeItem(row)
            obj.insertItem(row-1, item)
            self.update_user_vars()

    @Slot()
    def item_down(self, row: int, obj: QListWidget):
        if row < obj.count():
            item = obj.takeItem(row)
            obj.insertItem(row+1, item)
            self.update_user_vars()

    @Slot()
    def item_delete(self, row: int, obj: QListWidget) -> None:
        row = obj.takeItem(row)
        self.update_user_vars()

    @Slot()
    def item_add(self):
        self.user_vars = self.update_user_vars()
        self.new_window = ExpressionCalc(
            self.expression_list, user_variables=self.user_vars,
            domains=self.domains
        )
        self.new_window.show()
        self.new_window.exec()

        row = self.expression_list.count()

        if self.new_window.expression:
            self.expression_list.insert_item(item=self.new_window.expression, row=row, size_hint=[434, 32])
        self.update_user_vars()

    @Slot()
    def edit_item(self):
        item = self.expression_list.currentItem()
        self.launch_expression_editor(item=item)

    @Slot()
    def add_curve(self):
        curve_name = PopUpLineEdit(self.perfomance_map, title='Curve name')
        curve_name.show()
        curve_name.exec()
        if curve_name.text:
            add_point = FileDialog(title='Add perfomance map point', 
                filter='ANSYS result file (*.res)', directory='\\')
            self.res_files = add_point.open_files()
            files = [(os.path.split(f)[1], '') for f in self.res_files[0]]
            if self.res_files[0]:
                self.perfomance_map.clear()
                self.perfomance_map.set_items(items=files)
                self.curves[curve_name.text] = self.res_files[0]
                self.curves_cmb.addItem(curve_name.text)
                self.curves_cmb.setCurrentIndex(self.curves_cmb.count()-1)

    @Slot()
    def update_list(self, state, obj: QListWidget):
        if state == Qt.CheckState.Checked:
            obj.setEnabled(True)
        else:
            obj.setEnabled(False)
