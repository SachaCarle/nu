
from pathlib import Path
import sys, os, argparse

parser = argparse.ArgumentParser(description='Process .nut file.')
parser.add_argument('files', metavar='F', type=str, nargs='+',
                    help='target file(s).')

res = parser.parse_args(sys.argv)

