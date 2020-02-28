import argparse
from . import _, cmds

parser = argparse.ArgumentParser()
parser.add_argument('cmd', help="test create")
parser.add_argument('-v', help='Print nu log', action='store_true')
parser.add_argument('-o', help='oupout on the system, a path', action='store')


args = parser.parse_args()
nutools = _.create(args)
nutools.logger(args)

module = getattr(cmds, args.cmd)

#TODO: MAKE RAISER
if not module: raise Exception()

module.cmd(nutools, args)