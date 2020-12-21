from pathlib import Path
import sys, os, argparse


#-- USAGE --#
parser = argparse.ArgumentParser(description='Create a nuthon interpreter.')
parser.add_argument('--debug', help='Will output debug info', action='store_true')
parser.add_argument('tags', metavar='E', type=str, nargs='+',
                    help='tags for interpreter.')
res = parser.parse_args(sys.argv)
#-- USAGE --#

if res.debug:
    print ("\tDEBUG\targs\t%s" % vars(res))
    for i,j in vars(res).items():
        print ("\tDEBUG\t{}\t{}".format(i, j))
print ("ccommand parsed, construction start")