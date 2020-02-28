import argparse
from . import _, cmds

parser = argparse.ArgumentParser()
parser.add_argument('cmd', help="test create")
parser.add_argument('-v', help='log', action='store_true')
parser.add_argument('-o', help='output', default=False)
parser.add_argument('-p', help='port', default=5000)
parser.add_argument('-e', help='entity', default='http://localhost:5000/')


args = parser.parse_args()
nutools = _.create(args)
nutools.logger(args)

module = getattr(cmds, args.cmd)

#TODO: MAKE RAISER
if not module: raise Exception()

module.cmd(nutools, args)