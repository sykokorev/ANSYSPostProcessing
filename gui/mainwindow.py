import json

from PySide6.QtWidgets import (
    QMainWindow, QGridLayout, QWidget
)
from PySide6.QtCore import Slot, Qt


from utils.consts import *
from utils.parse_out import *
from gui.gui import *


class MainWindow(QMainWindow):

    def __init__(self, tabs, **kwargs):
        super(MainWindow, self).__init__()

        TAB_DICT = {
            'Turbo Surfaces': QWidget(),
            'Planes': QWidget(),
            'Images': QWidget(),
            'Report': QWidget(),
            'Presentation': QWidget()
        }

        self.expressions = None

        self.tabs = tabs
        self.domains = None
        self.out_file = None
        self.user_vars = None
        self.template_file = None
        self.perfomance_map = {}
        self.res_files = ('', '')
        self.file_save_directory = None

        size = kwargs.get('size', [1280, 720])
        title = kwargs.get('title', '')
        empty = QWidget()

        self.setWindowTitle(title)
        self.resize(*size)

        self.widgets = []
        self.main_layout = QGridLayout()
        self.main_layout.setVerticalSpacing(10)
        self.main_layout.setHorizontalSpacing(10)

        tabs_setting = dict((t.title, t.main_layout) for t in self.tabs)
        tabs_setting.update(TAB_DICT)

        self.tab_widget = TabWidget(tabs=tabs_setting)
        self.widgets.append(self.tab_widget)
        
        self.buttons = self.controlButtonUI()
        self.buttons_layout = GridLayout(
            widgets=[
                *[['widget', btn, [row, 0]] for row, btn in enumerate(self.buttons.buttons())],
                ['widget', empty, [len(self.buttons.buttons()), 0]]
            ]
        )
        self.buttons_layout.setVerticalSpacing(20)
        self.buttons_layout.setHorizontalSpacing(10)

        self.main_layout.addWidget(self.tab_widget, 0, 0)
        self.main_layout.addLayout(self.buttons_layout, 0, 1)
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

    def controlButtonUI(self):
        btn_size = [160, 32]
        btn_settings = [
            {'text': 'Load out file', 'size': btn_size},
            {'text': 'Load template', 'size': btn_size},
            {'text': 'Save template', 'size': btn_size},
            {'text': 'Add res files', 'enable': False, 'size': btn_size},
            {'text': 'Save to...', 'enable': False, 'size': btn_size},
            {'text': 'Run', 'enable': False, 'size': btn_size}
        ]
        buttons = []
        for btn in btn_settings:
            buttons.append(PushButton(**btn))

        buttons[0].clicked.connect(
            lambda: self.open_file(filter='Ansys out file (*.out)')
        )
        buttons[1].clicked.connect(
            lambda: self.load_template_file(title="Load template", directory="\\", filter="Template file (*.tmp)")
        )
        buttons[2].clicked.connect(
            lambda: self.save_template_as(title="Save template as", directory="\\", filter="Template files (*.tmp)")
        )
        buttons[3].clicked.connect(
            lambda: self.open_files(ext='res', title='Add ANSYS result files', filter='ANSYS result files (*.res)')
        )
        buttons[4].clicked.connect(lambda: self.open_directory(title="Save to Directory", directory="\\"))
        buttons[5].clicked.connect(self.run)
        qbtns = ButtonGroup(buttons=buttons)
        self.set_enabled(qbtns, True)
        return qbtns

    def initialize(self, instance: object) -> None:
        instance.initialize()

    def get_domains(self):
        try:
            if self.out_file[0]:
                self.domains = get_domains(outfile=self.out_file[0])
            else:
                msg = 'Out files have not been found.'
                ex = 'Files Not Found'
                diag = MessageBox(title=ex, information=msg)
                diag.show()
                diag.exec()
        except FileNotFoundError as ex:
            pass

    @Slot()
    def set_enabled(self, buttons: QButtonGroup, enabled: bool=True):
        for btn in buttons.buttons():
            btn.setEnabled(enabled)

    @Slot()
    def open_directory(self, title: str="Open directory", directory: str="\\"):
        open_directory = FileDialog(title=title, directory=directory)
        open_directory.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        self.file_save_directory = open_directory.open_direcory()

    @Slot()
    def open_files(self, ext: str='', filter: str=None, title: str='Open File', directory: str='\\'):
        open_files = FileDialog(title=title, filter=filter, directory=directory)
        ext = ext
        self.res_files = open_files.open_files()


    @Slot()
    def open_file(self, filter: str='', title='Open file', directory: str='\\'):
        open_file = FileDialog(filter=filter, title=title, directory=directory)
        self.out_file = open_file.open_file()
        if self.out_file[0]:
            self.get_domains()
            self.tabs[0].update_tab(domains=self.domains)

    @Slot()
    def save_template_as(self, filter: str='', title: str='Save file as', directory='\\'):
        save_as = FileDialog(filter=filter, title=title, directory=directory)
        self.template_file = save_as.save_as()

        if self.template_file[0]:
            expressions = []

            for row in range(self.tabs[0].expression_list.count()):
                var, exp = (t.strip() for t in self.tabs[0].expression_list.item(row).text().split('='))
                desc = self.tabs[0].expression_list.item(row).toolTip()
                check_state = 0 if self.tabs[0].expression_list.item(row).checkState() == Qt.CheckState.Unchecked else 1
                expressions.append({'Variable': var, 'Expression': exp, 'Description': desc, 'CheckState': check_state})

            with open(self.template_file[0], 'w') as tmp:
                json_data = {'expressions': expressions}
                json.dump(json_data, tmp)

    @Slot()
    def load_template_file(self, filter: str='', title: str='Load file', directory='\\'):

        load_file = FileDialog(filter=filter, title=title, directory=directory)
        self.template_file = load_file.open_file()
        if self.template_file[0]:
            with open(self.template_file[0], 'r') as tmp:
                try:
                    template = json.load(tmp)
                    self.tabs[0].load_template(**template)
                except json.JSONDecodeError:
                    msg = 'Invalid format of template file.'
                    ex = 'Invalid format'
                    diag = MessageBox(title=ex, information=msg)
                    diag.show()
                    diag.exec()
        self.template_file = None

    def load(self, instance: object):
        try:
            if self.template_file[0]:
                instance.load()
            else:
                msg = 'File has not been loaded.'
                ex = 'Invalid file'
                diag = MessageBox(title=ex, information=msg)
                diag.show()
                diag.exec()
        except FileNotFoundError as ex:
            pass

    def run(self):
        # Get expressions
        row = self.tabs[0].expression_list.count()
        if self.tabs[0].expression_check.checkState() == Qt.CheckState.Checked:
            self.expressions = [
                {
                    'expression': self.tabs[0].expression_list.item(i).text(),
                    'description': self.tabs[0].expression_list.item(i).toolTip(),
                    'add': True if self.tabs[0].expression_list.item(i).checkState() == Qt.CheckState.Checked else False
                } for i in range(row)
            ]
        else:
            self.expressions = None
        self.domains = self.tabs[0].domains
        self.close()
