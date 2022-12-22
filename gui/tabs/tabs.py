from PySide6.QtWidgets import (
    QGridLayout, QWidget, QAbstractItemView
)
from PySide6.QtCore import Qt, Slot


from utils.consts import *
from utils.parse_out import *
from gui.gui import *
from gui.tabs.widgets import *


class InitTab(QGridLayout):
    def __init__(self, parent: QWidget=None, **kwargs):
        super(InitTab, self).__init__(parent)

        self.title = kwargs.get('title', 'Settings')
        self.__domains = {}
        self.__user_vars = None
        self.__curves = {}

        self.template = None
        self.main_layout = None

        # Widgets
        self.expression_list = ExpressionList(items=None, min_width=434, min_height=32, font=LIST_FONT)
        self.performance_map = PerformanceMap(items=None, min_width=434, min_height=32, font=LIST_FONT)
        self.expression_check = ExpressionCheckBox()
        self.performance_check = PerformanceCheckBox()
        self.inlet_cmbb = InletCmbb(size=[360, 24], font=LIST_FONT)
        self.outlet_cmbb = OutletCmbb(size=[360, 24], font=LIST_FONT)
        self.curves_cmbb = CurvesCmbb(size=[360, 24], font=LIST_FONT)

        self.initialize()

    @property
    def domains(self):
        return self.__domains

    @property
    def user_vars(self):
        return self.__user_vars

    @property
    def curves(self):
        return self.__curves

    @domains.setter
    def domains(self, domains: list):
        if hasattr(domains, '__iter__'):
            self.__domains = domains

    @user_vars.setter
    def user_vars(self, vars: list):
        if hasattr(vars, '__iter__'):
            self.__user_vars = vars

    @curves.setter
    def curves(self, curve):
        if isinstance(curve, dict):
            self.__curves.update(curve)

    def initialize(self):

        performance_map_actions = {
            'Add curve': self.add_item,
            'Edit point': self.edit_item,
            'Move up': self.item_position_changed,
            'Move down': self.item_position_changed,
            'Delete point': self.performance_map.delete_item
        }
        expression_actions = {
            'Add expression': self.add_item,
            'Edit expression': self.edit_item,
            'Move up': self.item_position_changed,
            'Move down': self.item_position_changed,
            'Delete expression': self.expression_list.delete_item
        }
        menu = Menu(actions=expression_actions, parent=self.expression_list)
        self.expression_list.initialize(menu=menu)
        self.performance_map.initialize(menu=Menu(actions=performance_map_actions, parent=self.performance_map))
        self.expression_check.initialize()
        self.performance_check.initialize()
        self.inlet_cmbb.initialize()
        self.outlet_cmbb.initialize()
        self.curves_cmbb.initialize()

        self.expression_list.itemDoubleClicked.connect(self.edit_item)
        self.performance_map.itemDoubleClicked.connect(self.edit_item)
        self.curves_cmbb.currentIndexChanged.connect(self.update_performance_map)

        self.expression_check.stateChanged.connect(
            lambda: self.expression_check.update_state(widget=self.expression_list)
        )
        self.performance_check.stateChanged.connect(
            lambda: self.performance_check.update_state(widget=self.performance_map)
        )
        self.performance_check.stateChanged.connect(
            lambda: self.performance_check.update_state(widget=self.inlet_cmbb)
        )
        self.performance_check.stateChanged.connect(
            lambda: self.performance_check.update_state(widget=self.outlet_cmbb)
        )
        self.performance_check.stateChanged.connect(
            lambda: self.performance_check.update_state(widget=self.curves_cmbb)
        )

        last_col = 6
        last_row = 0
        widgets = [
            ['widget', QWidget(), [0, 0]],
            ['widget', self.expression_check, [1, 1]],
            ['widget', self.expression_list, [2, 1, 4, 1]],
            ['widget', self.performance_check, [1, 2, 1, 2]],
            ['widget', Label(text='Curves', size=[32, 24]), [2, 2]],
            ['widget', self.curves_cmbb, [2, 3]],
            ['widget', self.performance_map, [3, 2, 1, 2]],
            ['widget', Label(text='Inlet', size=[24, 32], font=FONT), [4, 2]],
            ['widget', Label(text='Outlet', size=[24, 32], font=FONT), [5, 2]],
            ['widget', self.inlet_cmbb, [4, 3]],
            ['widget', self.outlet_cmbb, [5, 3]],
            ['widget', QWidget(), [0, last_col, last_row, 1]]
        ]
        settings = {
            'hspace': 10, 'vspace':10, 'rect': [2, 2, 600, 600],
            'col_stretch': [[0, 1], [last_col, 1]]
        }
        self.main_layout = GridLayout(widgets=widgets, **settings)

    def update_tab(self, domains: dict) -> None:
        self.domains = domains
        self.inlet_cmbb.set_items(items=self.domains)
        self.outlet_cmbb.set_items(items=self.domains)
        
    def load_template(self, **template):
        expressions = template.get('expressions')
        if expressions:
            self.user_vars = [e['Variable'] for e in expressions]
            items = [(f'{e["Variable"]} = {e["Expression"]}', e["Description"], e["CheckState"]) for e in expressions]
            self.expression_list.update_list(items=items)

    def update_user_vars(self):
        user_vars = []
        for n in range(self.expression_list.count()):
            user_vars.append(self.expression_list.item(n).text().split(sep='=')[0].strip())
        return user_vars

    def update_performance_map(self, row: int):
        curve = self.curves_cmbb.itemText(row)
        files = self.curves.get(curve, None)

        if not files:
            items = ('', '')
        else:
            items = [(f, '') for f in files]
            self.performance_map.update_list(items=items)

    def update_curves(self):
        curve = self.curves_cmbb.currentText()
        self.curves[curve] = [self.performance_map.item(row).text() for row in range(self.performance_map.count())]

    @Slot()
    def item_position_changed(self):
        parent = self.sender().parent()
        sender = self.sender()
        if parent is self.expression_list and isinstance(sender, QAction):
            if sender.text() == 'Move up':
                self.expression_list.item_up()
            elif sender.text() == 'Move down':
                self.expression_list.item_down()
            self.user_vars = self.update_user_vars()
        elif parent is self.performance_map and isinstance(sender, QAction):
            if sender.text() == 'Move up':
                self.performance_map.item_up()
            elif sender.text() == 'Move down':
                self.performance_map.item_down()
            self.update_curves()

    @Slot()
    def add_item(self):

        parent = self.sender().parent()
        sender = self.sender()
        if self.expression_list in (parent, sender):
            self.user_vars = self.update_user_vars()
            self.expression_list.add_item(user_vars=self.user_vars, domains=self.domains)
            self.update_user_vars()
        elif self.performance_map in (parent, sender):
            curve = PopUpLineEdit(parent=self.performance_map)
            curve.show()
            curve.exec()
            if curve.text in self.curves.keys():
                msg = f'Curve with name {curve.text} already exists. Change curve name.'
                msgbox = MessageBox(title='Warning', information=msg)
                msgbox.show()
                msgbox.exec()
            elif curve.text:
                res = FileDialog(title="Add curve points", filter="ANSYS result files (*.res)", directory='\\')
                files = res.open_files()
                if files[0]:
                    items = [(f, f'point{i}') for i, f in enumerate(files[0], 1)]
                    self.performance_map.update_list(items=items)
                    self.curves_cmbb.addItem(curve.text)
                    self.curves_cmbb.setCurrentIndex(self.curves_cmbb.count()-1)
                    self.update_curves()

    @Slot()
    def edit_item(self):
        parent = self.sender().parent()
        sender = self.sender()

        if self.expression_list in (parent, sender) and self.expression_list.count():
            row = self.expression_list.currentRow()
            self.expression_list.edit_item(user_vars=self.user_vars[:row], domains=self.domains)
        elif self.performance_map in (parent, sender) and self.curves_cmbb.currentText():
            res = FileDialog(title="Edit curve point", filter="ANSYS result files (*.res)", directory="\\")
            file = res.open_file()
            if file[0]:
                row = self.performance_map.currentRow()
                item = QListWidgetItem()
                curve = self.curves_cmbb.currentText()
                item.setText(file[0])
                item.setToolTip(f'Curve: {curve}\tPoint:{row}')
                self.performance_map.set_item(item=item)
                self.update_curves()
