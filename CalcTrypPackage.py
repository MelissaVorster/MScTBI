from pyteomics import parser
print(len(parser.cleave('AKAKBK', parser.expasy_rules['trypsin'], 0)))
{'AK', 'BK'}
parser.xcleave('AKAKBK', 'trypsin', 0)
[(0, 'AK'), (2, 'AK'), (4, 'BK')]