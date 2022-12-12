# TEMPLATE_KEYS = {
#     'Axial Centrifugal Compressor': 
#     [
#         {'Name': 'DELTA', 'Expression': 'massFlowAve(Total Pressure in Stn Frame)@{interface}/massFlowAve(Total Pressure in Stn Frame)@{interface}',
#          'Description': 'Pressure Ratio'},
#         {'Name': 'TETA', 'Expression': 'massFlowAve(Total Temperature in Stn Frame)@{interface}/massFlowAve(Total Temperature in Stn Frame)@{interface}',
#         'Description': 'Temperature Ratio'}
#     ],
#     'Create a template...': None
# }

TEMPLATE_KEYS = {
    'Aixial Centrifugal Compressor':
    [
        {'Variable': '$n', 'Expression': 44400, 'Description': 'Mechanical Speed [rev min-1]'},
        {'Variable': '$R2', 'Expression': 0.141, 'Description': 'Exit Radius [m]'},
        {'Variable': '$Vcirc', 'Expression': 'pi * $R2 * $n / 30'},
        {'Variable': '$Phi', 'Expression': 'massFlowAve("Velocity Axial", {interface})/$Vcirc'},
    ],
    'Create new template...': None
}
