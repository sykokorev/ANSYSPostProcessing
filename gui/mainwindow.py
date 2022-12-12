from PySide6.QtWidgets import (
    QMainWindow, QGridLayout, QWidget
)
from PySide6.QtCore import Slot


from utils.consts import *
from utils.parse_out import *
from utils.template_keys import *
from gui.gui import *


class MainWindow(QMainWindow):

    def __init__(self, tabs, buttons, **kwargs):
        super(MainWindow, self).__init__()

        TAB_DICT = {
            'Turbo Surfaces': QWidget(),
            'Planes': QWidget(),
            'Images': QWidget(),
            'Report': QWidget(),
            'Presentation': QWidget()
        }

        self.tabs = tabs
        self.domains = None
        self.out_file = None
        self.user_vars = None

        size = kwargs.get('size', [1280, 720])
        title = kwargs.get('Title', '')
        empty = QWidget()

        self.setWindowTitle(title)
        self.resize(*size)

        self.widgets = []
        self.main_layout = QGridLayout()

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

        self.main_layout.addWidget(self.tab_widget, 0, 0)
        self.main_layout.addLayout(self.buttons_layout, 0, 1)
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

    def controlButtonUI(self):
        btn_settings = [
            {'text': 'Open out file'},
            {'text': 'Open res files direcotry'},
            {'text': 'Save...'},
            {'text': 'Save template'},
            {'text': 'Load template'}
        ]
        buttons = []
        for btn in btn_settings:
            buttons.append(PushButton(**btn))

        buttons[0].clicked.connect(
            lambda: self.open_file(filter='Ansys out file (*.out)', instance=self.tabs[0])
        )
        buttons[1].clicked.connect(lambda: self.open_files(ext='res', title='Open res file directory'))
        buttons[2].clicked.connect(lambda: self.open_directory(title="Save to Directory", directory="\\"))
        
        qbtns = ButtonGroup(buttons=buttons)

        return qbtns

    def initialize(self, instance: object) -> None:
        instance.initialize()

    def get_domains(self):
        try:
            if self.out_file:
                self.domains = get_domains(outfile=self.out_file[0])
                self.tabs[0].domains = self.domains
            else:
                msg = 'Out files have not been found.'
                ex = 'Files Not Found'
                diag = MessageBox(title=ex, information=msg)
                diag.show()
                diag.exec()
        except FileNotFoundError as ex:
            pass

    @Slot()
    def open_directory(self, title: str="Open directory", directory: str="\\"):
        open_directory = FileDialog(title=title, directory=directory)
        open_directory.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        self.file_save_directory = open_directory.open_direcory()

    @Slot()
    def open_files(self, ext: str='', filter: str=None, title: str='Open File', directory: str='\\'):
        open_files = FileDialog(title=title, filter=filter, directory=directory)
        ext = ext

        try:
            self.res_file_directory = os.path.abspath(open_files.open_direcory())
        except TypeError as ex:
            pass
        try:
            self.res_files = get_files(ext=ext, directory=self.res_file_directory)
        except FileNotFoundError as ex:
            pass

    @Slot()
    def open_file(self, instance, filter: str='', title='Open file', directory: str='\\'):
        open_file = FileDialog(filter=filter, title=title, directory=directory)
        self.out_file = open_file.open_file()
        if self.out_file[0]:
            instance.setup()
            self.get_domains()

    @Slot()
    def save_as(self, filter: str='', title: str='Save file as', directory='\\', ext: str=None):
        save_as = FileDialog(filter=filter, title=title, directory=directory, ext=ext)
        self.save_template_file = save_as.save_as()

    def setup(self, instance: object) -> None:
        try:
            if self.out_file:
                instance.setup()
            else:
                msg = 'Out files have not been found.'
                ex = 'Files Not Found'
                diag = MessageBox(title=ex, information=msg)
                diag.show()
                diag.exec()
        except FileNotFoundError as ex:
            pass
