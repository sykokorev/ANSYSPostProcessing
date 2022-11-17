import re
import os


def get_domains(outfile: str) -> dict:

    dmn_pattern = re.compile(r'domain:\s*\d*\w+\d*')
    bnd_pattern = re.compile(r'boundary:[\s\d\w]*')
    bnd_end_pattern = re.compile(r'domain\s+models:\s*')
    
    domains = {}
    dmn_find = False

    with open(outfile, 'r') as fi:
        for line in fi.readlines():
            if re.fullmatch(pattern=dmn_pattern, string=line.lower().strip()):
                dmn = line.split(sep=':')[1].strip()
                domains[dmn] = []
                dmn_find = True
            if dmn_find:
                if re.fullmatch(pattern=bnd_pattern, string=line.lower().strip()):
                    bnd = line.split(sep=':')[1].strip()
                    domains[dmn].append(bnd)
            if re.fullmatch(pattern=bnd_end_pattern, string=line.lower().strip()):
                dmn_find = False
            
    return domains
            

def get_files(ext: str, directory: str) -> list:
    
    files = []
    for file in os.listdir(directory):
        if file.endswith(f'.{ext}'):
            files.append(os.path.join(directory, file))
    
    return files
