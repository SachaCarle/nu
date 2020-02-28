from setuptools import setup
from pathlib import Path

def globit(st, nd):
    bl = Path(st).glob(nd)
    return [str(b) for b in sorted(bl)]

df = [
        ('_', globit('nu/_/', '*.py')),
        ('cmds', globit('nu/cmds/', '*.py')),
        ('abstract', globit('nu/abstract/', '*.py')),
        ('abstract', globit('nu/abstract/', '*.html')),
        ('entity', globit('nu/entity/', '*.py')),
    ]

setup(
    name='Nu',
    version='1.0.1',
    long_description=__doc__,
    packages=['nu'],
    data_files=df,
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask', 'behave', 'requests', 'wheel']
)