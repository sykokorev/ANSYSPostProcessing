import os

from PySide6.QtWidgets import QApplication


from utils.parse_out import *
from gui.gui import MainWindow

DIRECROTY = r"E:\Kokorev\temp\post_processing_res"
OUTFILE = r"BL7_Hub_Tipcl_GV1_GV2_v1_80prct_ps1_Steady_with_Cav_Yes_Open2_ps1_004.out"
FILE = os.path.join(DIRECROTY, OUTFILE)

if __name__ == "__main__":

    domains = get_domains(outfile=FILE)

    app = QApplication()
    window = MainWindow(domains=domains, title='ANSYS Post Processing', size=[1280, 720])

    window.show()
    app.exec()
