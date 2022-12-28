from PySide6.QtWidgets import (
    QWidget, QListWidgetItem, QLineEdit,
    QDialog, QMenuBar
)
from PySide6.QtGui import (
    QAction, QCloseEvent, QFont,
    QRegularExpressionValidator,
    QKeyEvent, Qt
)


from gui.gui import PushButton, GridLayout, Label
from utils.consts import *


class ExpressionCalc(QDialog):
    def __init__(self, parent: QWidget=None, **kwargs):
        super(ExpressionCalc, self).__init__(parent)

        self.resize(600, 150)
        self.setWindowTitle("Expression Editor")
        domains = kwargs.get('domains', {})
        self.expression = kwargs.get('expression', QListWidgetItem())
        self.user_vars = kwargs.get('user_variables', None)

        if not self.expression:
            self.description = ''
        else:
            self.description = self.expression.toolTip()

        solution_vars = SOLUTION_KEYS
        turbo_vars = TURBO_KEYS
        functions = FUNCTION_KEYS

        self.editor = QLineEdit()
        self.editor.clear()
        self.editor.setText(self.expression.text())
        self.editor.setFont(QFont(*MSG_FONT))
        self.editor.setPlaceholderText("$variable_name=expression")
        # reg = "[$]{1}[a-zA-Z_]+[_0-9_]*[=]{1}[a-zA-Z()\"\s\*/\+\-0-9,\.$]+"
        # validator = QRegularExpressionValidator(reg)
        # self.editor.setValidator(validator)

        self.qtext = QLineEdit()
        self.qtext.setText(self.description)
        self.qtext.setFont(QFont(*MSG_FONT))

        self.ok_btn = PushButton(text='Ok', size=[128, 32])
        self.ok_btn.clicked.connect(self.save_and_close)
        self.cancel_btn = PushButton(text="Cancel", size=[128, 32])
        self.cancel_btn.clicked.connect(self.close_unsaved)
        btn_layout = GridLayout(widgets=[
            ['widget', QWidget(), [0, 0]],
            ['widget', self.ok_btn, [0, 1]],
            ['widget', self.cancel_btn, [0, 2]],
            ['widget', QWidget(), [0, 3]]
        ], col_stretch=[[0, 1], [3, 1]])
        btn_layout.setSpacing(5)

        text = "Example: $Density=massFlowAve(\"Density\",\"DomainName\")"
        example = Label(text=text, font=LIST_FONT)

        layout = GridLayout(widgets=[
            ['widget', Label(text='Expression:'), [0, 0]],
            ['widget', Label(text='Description:'), [1, 0]],
            ['widget', self.editor, [0, 1]],
            ['widget', self.qtext, [1, 1]],
            ['layout', btn_layout, [2, 0, 1, 2]],
            ['widget', example, [5, 0, 1, 2]]
        ])
        layout.setHorizontalSpacing(5)
        layout.setVerticalSpacing(5)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setLayout(layout)
        self.menu = QMenuBar()
        self.functions_menu = self.menu.addMenu("&Functions")
        self.variables_menu = self.menu.addMenu("&Variables")

        if domains:
            self.locations_menu = self.menu.addMenu("&Locations")

            for domain, interfaces in domains.items():
                dmn_submenu = self.locations_menu.addMenu(domain)
                dmn_submenu.triggered.connect(self.paste_func)
                for interface in interfaces:
                    action = QAction(interface, self)
                    action.setText(interface)
                    dmn_submenu.addAction(action)

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
        self.layout().setMenuBar(self.menu)

        for function in functions:
            action = QAction(function, self)
            action.setText(function)
            self.functions_menu.addAction(action)

        for var in solution_vars:
            action = QAction(var, self)
            action.setText(var)
            self.solution_submenu.addAction(action)

        for var in turbo_vars:
            action = QAction(var, self)
            action.setText(var)
            self.turbo_submenu.addAction(action)

    def save_and_close(self):
        if self.editor.text():
            text = self.editor.text().strip()
            self.expression.setText(text)
            self.expression.setToolTip(self.qtext.text())
        else:
            self.expression = None
        self.close()

    def close_unsaved(self):
        self.expression = None
        self.editor.setText('')
        self.close()

    def paste_vars(self, action):
        text = action.text()
        self.editor.insert(text)
    
    def paste_func(self, action):
        text = f'"{action.text()}"'
        self.editor.insert(text)

    def closeEvent(self, arg__1: QCloseEvent) -> None:
        if not self.editor.text():
            self.close_unsaved()
        else:
            self.save_and_close
        return super().closeEvent(arg__1)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Escape:
            self.close_unsaved()
        return super().keyPressEvent(event)
