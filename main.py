import os
import ctypes
import sys
import re

from PySide6.QtWidgets import QApplication


from utils.parse_out import *
from utils.generate_cse import *
from gui.mainwindow import MainWindow
from gui.tabs.tabs import InitTab
from utils.consts import HERE


def convert_path(path: str):
    sep = os.path.sep
    if sep != '/':
        path = path.replace(os.path.sep, '/')
    return path


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

    save_to = (HERE + os.sep + 'post') if not (d := window.file_save_directory) else d
    res_files = [] if not (f:=window.res_files[0]) else f
    expressions = [] if not (exp:=window.expressions) else [e['expression'] for e in exp]
    header = [] if not (header:=window.expressions) else [
        h['expression'].split('=')[0].strip().lstrip('$') for h in header
    ]
    variables = [f'${h}' for h in header]
    desc = [] if not (d:=window.expressions)  else [di['description'] for di in d]
    domains = [] if not (d:=window.domains) else list(d.keys())

    output_dir = os.path.abspath(save_to)
    cse = os.path.join(output_dir, 'output.cse')
    csv = os.path.join(output_dir, 'output.csv')
    csv = convert_path(csv)

    array_var_name = 'files'
    perl = PerlHandler()
    perl.code += f'!\tmy $f (@{array_var_name})' + '{\n'
    perl.code += '> load filename = $f, force_reload=true\n> update\n'
    array = GenArray(array_var_name)

    generators = {
        array: res_files,
        perl: expressions
    }


    coder = CodeGen(list(generators.keys()))
    
    code = coder.code(list(generators.values()))
    cse_out = cse_generator(outfile=csv, header=header, code=code, domains=domains, vars=variables)

    if not (path:=os.path.exists(os.path.split(cse)[0])):
        try:
            os.mkdir(path)
        except PermissionError:
            sys.exit(-1)

    with open(cse, 'w') as f:
        f.write(cse_out)
