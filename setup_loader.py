from setuptools import setup
from pathlib import Path
from os import environ
import os, sys, subprocess

def globit(st, nd):
    bl = Path(st).glob(nd)
    return [str(b) for b in sorted(bl)]


basedir = str(Path('/', 'nusys').resolve())
pdir = Path(basedir, 'lib', 'python')
npf = Path('.', 'nuloader', 'nupath.py').resolve()
code = """path = '{}'
""".format(str(os.path.join(*(str(pdir).split('\\')))).replace(':nusys', ':\\nusys').replace('\\', '\\\\'))

if npf.exists():
    os.remove(npf)
with npf.open('w') as fd:
    fd.write(code)

setup(
    name='nuloader',
    version='1.0.1',
    long_description=__doc__,
    packages=['nuloader'],
    include_package_data=False,
    zip_safe=False,
    install_requires=[]
)


sys.path.append(basedir)
sys.argv.extend(['--home', basedir])
print ("new command for setup tool", sys.argv)
pdir.mkdir(parents=True, exist_ok=True)
environ['PYTHONPATH'] = str(pdir)

try:
    import setup
except Exception as e:
    raise e

environ['PYTHONPATH'] = ""
subprocess.run(["python", '-m', 'nu', 'install_clean'], shell=True, cwd=str(Path.home()))
environ['PYTHONPATH'] = str(pdir)
subprocess.run(["python", '-m', 'nu', 'install_clean'], shell=True, cwd=str(Path.home()))