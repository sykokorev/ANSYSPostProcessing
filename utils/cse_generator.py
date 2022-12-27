

class CodeGenerator:
    def __init__(self):
        self.__code = ''
    
    @property
    def code(self):
        return self.__code

    def gen_init(self, domains: list=None) -> str:
        out = '!\tuse Math::Trig;\n!\tuse File::Basename;\n!\tuse File::Spec;\n!\tuse warnings;\n\n'
        out += '' if not domains else 'DATA READER:\n\tDomains to Load = '
        out += '' if not domains else str(domains)[1:-1].replace("'", '') + '\n'
        out += '' if not domains else 'END\n\n'
        return out

    def load_domains(self, domains: list=None):
        out = '' if not domains else 'DATA READER:\n\tDomains to Load = '
        out += '' if not domains else str(domains)[1:-1].replace("'", '') + '\n'
        out += '' if not domains else 'END\n\n'
        return out

    def load_file(self, filename: str) -> str:
        return f'> load filename={filename}, force_reload=true\n'

    def turbo_init(self) -> str:
        return f'> update\n> turbo init\n> turbo more_vars\n'

    def domain_turbo_init(case, domain) -> str:
        out = 'DATA READER:\n'
        out += f'\tDOMAINS:{domain}\n'
        out += f'\t\tComponents To Initialize = {domain}\n'
        out += '\tEND\n'
        out += 'END\n'
        return out

    def gen_perl_array(self, variables: list, varname: str='var', vartype: str='string') -> str:
        out = f"!\tmy @{varname} = ("
        if vartype == 'string':
            out += str(variables)[1:-1] + ");\n"
        elif vartype == 'numeric':
            out += str(variables)[1:-1].replace("'", '') + ");\n"
        return out

    def gen_perl_expressions(self, expressions: list) -> str:
        out = ''
        for exp in expressions:
            out += f'!\tmy {exp};\n'
        return out

    def gen_perl_loop(self, code: str, array_var: str, arr_name: str='f') -> str:
        out = f'!\tfor my ${arr_name} (@{array_var}) ' + '{\n'
        out += code
        out += '!\t};\n'
        return out

    def gen_perl_open_file(self, filename: str, filevar='FH', open_as: str='>') -> str:
        return F'!\topen (my ${filevar}, \'{open_as}\', "{filename}") or die;\n'
    
    def write_to_file(self, code: str, filevar: str='FH') -> str:
        return f'!\tprintf (${filevar} {code});\n'

    def gen_perl_close_file(self, filevar: str='FH') -> str:
        return f'!\tclose(${filevar});\n'

    def pm_expressions(self, curve: str, inlet: str, outlet: str):
        out = f'!\tmy $massFlow = massFlow("{inlet}");\n'
        out += f'!\tmy $T1tot = massFlowAve("Total Temperature in Stn Frame","{inlet}");\n'
        out += f'!\tmy $T3tot = massFlowAve("Total Temperature in Stn Frame","{outlet}");\n'
        out += f'!\tmy $P1tot = massFlowAve("Total Pressure in Stn Frame","{inlet}");\n'
        out += f'!\tmy $P3tot = massFlowAve("Total Pressure in Stn Frame","{outlet}");\n'
        out += f'!\tmy $P3st = areaAve("Pressure", "{outlet}");\n'
        out += '!\tmy Pist = $P3st / $P1tot;\n'
        out += '!\tmy Pitt = $P3tot / $P1tot;\n'
        out += f'!\tmy $eff = comp_eff($T1tot, $T3tot, $P1tot, $P3tot);\n'
        return out

    def perl_eff_subroutine(self):
        out = """
!\tsub comp_eff
!\t{
!\t\tmy $a1 = 3.5683962; 
!\t\tmy $a2 = -0.000678729429;
!\t\tmy $a3 = 0.00000155371476;
!\t\tmy $a4 = -3.2993706e-12;
!\t\tmy $a5 = -4.66395387e-13;
!\t\tmy $pi = $_[3]/$_[2];
!\t\tmy $c1 = $a1*($_[0]) + $a2*($_[0])**2/2 + $a3*($_[0])**3/3 + $a4*($_[0])**4/4 + $a5*($_[0])**5/5;
!\t\tmy $c2 = $a1*($_[1]) + $a2*($_[1])**2/2 + $a3*($_[1])**3/3 + $a4*($_[1])**4/4 + $a5*($_[1])**5/5;
!\t\tmy $T3_iz = $_[1];
!\t\tmy $T3_iz_prev = $T3_iz + 100;
!\t\tmy $i = 1;
!\t\twhile (abs ($T3_iz - $T3_iz_prev)>0.1)
!\t\t{
!\t\t\t$T3_iz_prev = $T3_iz;
!\t\t\t$f1 = ($a1/$T3_iz + $a2 + $a3*$T3_iz + $a4*($T3_iz)**2 + $a5*($T3_iz)**3);
!\t\t\t$f2 = ($a1*log($T3_iz) + $a2*$T3_iz + $a3*($T3_iz)**2/2 + $a4*($T3_iz)**3/3 + $a5*($T3_iz)**4/4) - ($a1*log($_[0]) + $a2*$_[0] + $a3*$_[0]**2/2 + $a4*$_[0]**3/3 + $a5*$_[0]**4/4) - log($pi);
!\t\t\t$T3_iz = $T3_iz - $f2/$f1;
!\t\t\t$c2_iz = $a1*($T3_iz) + $a2*($T3_iz)**2/2 + $a3*($T3_iz)**3/3 + $a4*($T3_iz)**4/4 + $a5*($T3_iz)**5/5;
!\t\t\t$efficiency = ($c2_iz - $c1)/($c2 - $c1);
!\t\t\t$i++;
!\t\t};
!\treturn $efficiency;
!\t};
"""
        return out
