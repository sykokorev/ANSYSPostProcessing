import os
from PySide6.QtCore import Qt

FONT = ['Calibri', 14]
MSG_FONT = ['Calibri', 12]
LIST_FONT = ['Calibri', 10]
TOOLBAR_FONT = ['Calibri', 12]
MENU_FONT = ['Calibri', 12]

FUNCTION_KEYS = [
    'area', 'areaAve', 'areaInt', 'ave', 'massFlow', 'massFlowAve', 'massFlowInt',
    'massFlowAveAbs', 'maxVal', 'minVal', 'sum', 'volume', 'volumeAve', 'volumeInt'
]
SOLUTION_KEYS = [
    'Radius', 'Absolute Pressure', 'Density', 'Dynamic Viscosity', 'Eddy Viscosity',
    'Isoentropic Compression Efficiency', 'Mach Number', 'Mach Number in Stn Frame',
    'Mass Flow', 'Polytropic Compression Efficiency', 'Pressure', 'Static Enthalpy',
    'Static Entropy', 'Temperature', 'Total Density', 'Total Density in Rel Frame',
    'Total Density in Stn Frame', 'Total Entalpy', 'Total Entalpy in Stn Frame',
    'Total Pressure', 'Total Pressure in Rel Frame', 'Total Pressure in Stn Frame',
    'Total Temperature', 'Total Temperature in Rel Frame', 'Total Temperature in Stn Frame',
    'Specific Heat Capacity at Constant Pressure', 'Specific Heat Capacity at Constant Volume'
]
TURBO_KEYS = [
    'Velocity Axial', 'Velocity Circumferential', 'Velocity Flow Angle', 
    'Velocity in Stn Frame Circumferential', 'Velocity in Stn Frame Flow Angle',
    'Velocity Radial', 'Velocity Spanwise', 'Velocity Streamwise'
]

HERE = os.path.dirname(__file__)

CS = [Qt.CheckState.Unchecked, Qt.CheckState.Checked]
