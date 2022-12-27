

def cse_generator(domains, outfile, header, code, vars):
    out = '!\tuse Math::Trig;\n!\tuse File::Basename;\n!\tuse File::Spec;\n!\tuse warnings;\n!\tuse strict;\n\n'
    out += 'DATA READER:\n\tDomains to Load = '
    for i, d in enumerate(domains):
        out += f'{d},' if not (i+1) == len(domains) else f'{d}\n'
    out += 'END\n'
    out += '> turbo init\n> turbo more_vars\n'
    out += f'!\topen(my $FH, \'>\', "{outfile}") or die;\n'
    out += f'!\tprintf ($FH "'
    for i, h in enumerate(header):
        out += f'{h}, ' if not i+1 == len(header) else f'{h}\\n");\n'
    out += code
    out += '!\t}\n'
    out += '!\tprintf($FH "'
    frm = ['%.3f'] * len(vars)
    out += f'{str(frm)[1:-1]}\\n", '.replace("'", "")
    out += f'{str(vars)[1:-1]});\n'.replace("'", "")
    out += '!\tclose($FH);\n'
    out += '> close'
    return out


def load_file():
    return '> load filename = $f, force_reload=true\n'


def turbo_init():
    return '> update\n> turbo initn\n> turbo more_vars\n'


# Abstract class

class CodeGen:
    def __init__(self, coders):
        self.coders = coders

    def save(self, file, code):
        file.write(code)

    def code(self, codes):
        out = ''
        for coder, code in zip(self.coders, codes):
            out += coder.gen(code)
        return out

class PerlHandler:
    def __init__(self):
        self.code = ''

    def gen(self, code) -> str:
        for c in code:
            self.code += f'!\tmy {c};\n'
        code = self.code
        return code


class GenArray:
    def __init__(self, var: str):
        self.code = f'!\tmy @{var} = ('
    
    def gen(self, vars) -> str:
        for i, var in enumerate(vars):
            self.code += f'"{var}");\n' if (i+1) == len(vars) else f'"{var}", '
        code = self.code
        return code


class PerformanceMap:
    def __init__(self, **kwargs):
        self.code = ''
        self.__inlet = kwargs.get('inlet', '')
        self.__outlet = kwargs.get('outlet', '')

    @property
    def inlet(self):
        return self.__inlet
    
    @property
    def outlet(self):
        return self.__outlet

    @inlet.setter
    def inlet(self, inlet):
        self.__inlet = inlet

    @outlet.setter
    def outlet(self, outlet):
        self.__outlet = outlet

    def gen(self, curve) -> str:
        self.code += f'!\tmy $curve = {curve}\n'
        self.code += f'!\tmy $Pist = areaAve("Pressure", {self.outlet}) / massFlowAve("Total Pressure in stn Frame", "{self.inlet}");\n'
        self.code += f'!\tmy $massFlow = massFlow("{self.inlet}");\n'
        self.code += f'!\tmy $T1tot = massFlowAve("Total Temperature in stn Frame","{self.inlet}");\n'
        self.code += f'!\tmy $T2tot = massFlowAve("Total Temperature in stn Frame","{self.outlet}");\n'
        return self.code
