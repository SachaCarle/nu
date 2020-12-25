from . import Scope
import os

# OPEN ARGPARSE_0
import argparse, sys
parser = argparse.ArgumentParser(description='Create a nuthon interpreter.')
    # UTILITY LEVEL
parser.add_argument('-i', '--input', help='input file to be interpreted')
parser.add_argument('-c', '--console', help='run the console', action='store_true')
parser.add_argument('-o', '--output', help='file name for python interpreter')
    # BASE LEVEL
parser.add_argument('args', metavar='SYMBOLS', type=str, nargs='+',
                    help='Symboles for interpreter.')
    # VERBOSE LEVEL
parser.add_argument('--debug', help='Will output debug info', action='store_true')
parser.add_argument('--silent', help='Will not output construction info', action='store_true')
# CLOSE ARGPARSE_0



# OPEN ARGPARSE_1
arg_res = parser.parse_args(sys.argv)
# CLOSE ARGPARSE_1

#-- DEBUG --#
if arg_res.debug:
    from . import parse_symbole
    print ("\tDEBUG\targs\t%s" % vars(arg_res))
    for i,j in vars(arg_res).items():
        print ("\tDEBUG\t{}\t{}".format(i, j))
        if i == "args":
            for k in j:
                print ("\t\t*\t{}".format(parse_symbole(k)))
#-- DEBUG --#
if not arg_res.silent:
    print ("command parsed, construction starting")

# OPEN MAIN_0
from code import InteractiveConsole
global_scope = Scope()
console = InteractiveConsole(global_scope, "<nuthon-console>")
# CLOSE MAIN_0

# OPEN INTERPRETER
from pathlib import Path
if isinstance(arg_res.input, str):
    f = Path(arg_res.input).resolve()
    assert f.exists()
    with f.open('r'):
        txt = f.read_text()
    res = console.runsource(txt, arg_res.input)
    if res is False:
        console.showsyntaxerror()
    else:
        print ("RESULT =", res)
        print ('INCOMLETE ??')
# CLOSE INTERPRETER

# OPEN CONSOLE
if arg_res.console is True:
    console.interact()
# CLOSE CONSOLE

# OPEN OUTPUT
if isinstance(arg_res.output, str):
    from . import main_output
    main_output.write_interpreter(arg_res.output)
# CLOSE OUTPUT
