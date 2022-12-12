import string

class Table:
    def __init__(self, expressions: list, header: list=[], table_name: str="Table 1"):
        
        self.expressions = expressions
        self.table_name = table_name
        self.expressions_cst = []
        self.cse_code = ''
        self.columns = list(string.ascii_uppercase)
        self.rows = [i for i in range(1, 201)]
        
    def gen_expression(self):
        for col, expression in enumerate(self.expressions):
            self.expressions_cst.append(f'{self.columns[col]}{1} = "={expression}"')
        return self.expressions_cst

    def gen_cse_code(self):
        self.cse_code += f'TABLE: {self.table_name}\n'
        self.cse_code += f'  Table Exists = True\n'
        self.cse_code += '  TABLE CELLS:\n'

        for expression in self.expressions_cst:
            self.cse_code += f'    {expression}\n'

        self.cse_code += '  END\n'
        self.cse_code += 'END\n'
        return self.cse_code

class Perl:
    def __init__(self, csv: str, expressions: list, header: list=[]):
        self.expressions = expressions
        self.csv = csv
        self.header = header

    def gen_expressions(self):
        pass
