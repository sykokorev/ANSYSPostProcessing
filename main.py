import os
import ctypes
import sys

from PySide6.QtWidgets import QApplication, QWidget


from utils.parse_out import *
from utils.generate_cse import Table
# from gui.gui import MainWindow, MessageBox
from gui.mainwindow import MainWindow
from gui.tabs.tabs import InitTab


if __name__ == "__main__":

    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0)/2, user32.GetSystemMetrics(1)/2

    app = QApplication()
    btns = [
        {'text': 'Open out file'},
        {'text': 'Open res files direcotry'},
        {'text': 'Save...'},
        {'text': 'Save template'},
        {'text': 'Load template'}
    ]

    init_tab = InitTab(title='Expressions')
    tabs = [init_tab]

    window = MainWindow(
        title='ANSYS Post Processing', size=screensize,
        tabs=tabs, buttons=btns
    )

    window.show()
    app.exec()

    # output_directory = window.file_save_directory
    # try:
    #     cst_file = os.path.join(output_directory, 'out.cst')
    # except TypeError:
    #     msgbox = MessageBox(information='Output directory has noe been choisen', title='Error Message')
    #     msgbox.show()
    #     msgbox.exec()
    #     sys.exit(-1)

    # expressions = [(exp.split(sep='=')[0].strip(), exp.split(sep='=')[1].strip()) for exp in window.get_expressions()]
    # expressions = dict(expressions)
    # table_cst = Table(list(expressions.values()), table_name='ACC')

    # table_cst.gen_expression()
    # code_cst = table_cst.gen_cse_code()

    # with open(cst_file, 'w') as cse:
    #     for case in window.res_files:
    #         cse.write(f'>load filename={case}, force_reload=true\n>update\n')
    #         cse.write(code_cst)
        