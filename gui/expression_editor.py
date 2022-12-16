from PySide6.QtWidgets import (
    QMainWindow, QWidget, QListWidgetItem, QTextEdit,
    QDialog, QMenuBar
)
from PySide6.QtGui import QAction, QCloseEvent, QFont


from gui.gui import PushButton, GridLayout
from utils.consts import *


class ExpressionCalc(QDialog):
    def __init__(self, parent: QWidget=None, **kwargs):
        super(ExpressionCalc, self).__init__(parent)

        self.resize(600, 300)
        self.setWindowTitle("Expression Editor")
        domains = kwargs.get('domains', {})
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
        self.ok_btn = PushButton(text='Ok')
        self.ok_btn.clicked.connect(self.save_and_close)
        self.cancel_btn = PushButton(text="Cancel")
        self.cancel_btn.clicked.connect(self.close)

        layout = GridLayout(widgets=[
            ['widget', self.editor, [0, 0, 1, 2]], 
            ['widget', self.ok_btn, [1, 0]],
            ['widget', self.cancel_btn, [1, 1]]
        ])

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
        if self.editor.toPlainText():
            text = self.editor.toPlainText().strip()
            self.expression.setText(text)
        else:
            self.expression = None
        self.close()

    def paste_vars(self, action):
        text = action.text()
        self.editor.insertPlainText(text)
    
    def paste_func(self, action):
        text = f'"{action.text()}"'
        self.editor.insertPlainText(text)

    def closeEvent(self, arg__1: QCloseEvent) -> None:
        if self.editor.toPlainText():
            text = self.editor.toPlainText()
            self.expression.setText(text)
        else:
            self.expression = None
        self.close()
