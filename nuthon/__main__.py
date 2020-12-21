from pathlib import Path
import sys, os, argparse


#-- USAGE --#
parser = argparse.ArgumentParser(description='Create a nuthon interpreter.')
parser.add_argument('--debug', help='Will output debug info', action='store_true')
parser.add_argument('--silent', help='Will not output construction info', action='store_true')
parser.add_argument('args', metavar='E', type=str, nargs='+',
                    help='tags for interpreter.')
res = parser.parse_args(sys.argv)
#-- USAGE --#

#-- DEBUG --#
if res.debug:
    from . import parse_symbole
    print ("\tDEBUG\targs\t%s" % vars(res))
    for i,j in vars(res).items():
        print ("\tDEBUG\t{}\t{}".format(i, j))
        if i == "args":
            for k in j:
                print ("\t\t*\t{}".format(parse_symbole(k)))
#-- DEBUG --#
if not res.silent:
    print ("command parsed, construction starting")

