import os.path, pprint
from pathlib import Path

pp = pprint.PrettyPrinter(indent=4)

def print_code(code, ind=0):
    inden = ''
    for i in range(ind):
        inden += '_'
    inden += '\t\t\t'
    for x in code.lines.values():
        if not isinstance(x, tuple):
            print (inden + x.head())
            print_code(x, ind + 1)
        else:
            print (inden, x[1])

def cmd(_, args, **kwargs):
    assert args.target
    print ()
    try:
        code = _.parser(args.target)
        if args.o == False:
            print ('__FINISHED__\n\n\n\n')
            #pp.pprint (code())
            print_code(code)
        else:
            with Path(args.o).open('w') as output:
                output.write(code())
        # args.o for output
    except Exception as e:
        raise e


