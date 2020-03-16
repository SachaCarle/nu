from .env import ExecuteJs
import glob, os

path = os.path.split(__file__)[0]
path = os.path.join(path, 'js')

files = [f for f in glob.glob(path + "/*.js", recursive=True)]

scripts = { p.split('.js')[0].replace(path, '').replace('\\', ''): p
    for p in files }

all = [
    "ExecuteJs", "scripts"
]

