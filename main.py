import os
import ctypes
import sys
import re

from PySide6.QtWidgets import QApplication


from utils.parse_out import *
from utils.cse_generator import *
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
    output_dir = os.path.abspath(save_to)    

    cse_code = CodeGenerator()

    res_files = [] if not (f:=window.res_files[0]) else f
    expressions = [] if not (exp:=window.expressions) else [e['expression'] for e in exp]
    header = [] if not (header:=window.expressions) else [
        h['expression'].split('=')[0].strip().lstrip('$') for h in header
    ]
    variables = [f'${h}' for h in header]
    var_format = ['%.5f'] * len(variables)
    desc = [] if not (d:=window.expressions)  else [di['description'] for di in d]
    domains = [] if not (d:=window.domains) else list(d.keys())

    cse = os.path.join(output_dir, 'output.cse')
    csv = os.path.join(output_dir, 'output.csv')
    csv = convert_path(csv)
    cse = convert_path(cse)

    res_files_array_name = 'files'
    filename = '$f'

    code = cse_code.gen_init(domains=domains)
    # Compute efficiency subroutine
    code += cse_code.perl_eff_subroutine()
    # Compute Expressions
    if res_files:
        code += cse_code.turbo_init()
        code += cse_code.gen_perl_open_file(filename=csv)
        code += cse_code.write_to_file(code='"file,'+str(header)[1:-1].replace("'",'')+'\\n"')
        code += cse_code.gen_perl_array(variables=res_files, varname=res_files_array_name)

        code_inside_loop = cse_code.load_file(filename=filename)
        code_inside_loop += cse_code.gen_perl_expressions(expressions=expressions)
        code_to_write = f'"%s,' + str(var_format)[1:-1].replace("'", '') + f'\\n", basename({filename}),' + str(variables)[1:-1].replace("'", '')
        code_inside_loop += cse_code.write_to_file(code=code_to_write)
        code += cse_code.gen_perl_loop(code=code_inside_loop, array_var=res_files_array_name)

    # performance map code
    pm_csv = os.path.join(output_dir, 'performance_map.csv')
    pm_csv = convert_path(pm_csv)

    performance_map = window.performance_map
    if performance_map:
        code += cse_code.load_domains(domains=domains)
        code += cse_code.turbo_init()
        code += cse_code.gen_perl_open_file(filename=pm_csv)
        code_to_write = '"CurveName, Inlet, Outlet, Gcorr, Pi_ts, Pi_tt, Eff\\n"'
        code += cse_code.write_to_file(code=code_to_write)
        for curve, data in performance_map.items():
            files = [] if not (f:=data['files']) else f
            inlet = '' if not (i:=data['inlet']) else i
            outlet = '' if not (o:=data['outlet']) else o
            code += cse_code.gen_perl_array(variables=files, varname='files')
            code_inside_loop = cse_code.load_file(filename='$f')
            code_inside_loop += cse_code.pm_expressions(curve=curve, 
                inlet=inlet, outlet=outlet)
            code_to_write = f'"%s, %s, %s, %.5f, %.5f, %.5f\\n", "{curve}", "{inlet}", "{outlet}", $massFlow, $Pist, $Pitt, $eff'
            code_inside_loop += cse_code.write_to_file(code=code_to_write)
            code += cse_code.gen_perl_loop(code=code_inside_loop, array_var='files')
        code += cse_code.gen_perl_close_file()

    if not os.path.exists(os.path.split(cse)[0]):
        try:
            os.mkdir(os.path.split(cse)[0])
        except PermissionError:
            sys.exit(-1)

    with open(cse, 'w') as f:
        f.write(code)
