from setuptools import setup
from pathlib import Path
def globit(st, nd):
    bl = Path(st).glob(nd)
    return [str(b) for b in sorted(bl)]

df = [
        ('nu/_', globit('nu/_/', '*.py')),
        ('nu/cmds', globit('nu/cmds/', '*.py')),
        ('nu/abstract', globit('nu/abstract/', '*.py')),
        ('nu/abstract', globit('nu/abstract/', '*.html')),
        ('nu/components', globit('nu/components/', '*.py')),
        ('nu/components/src', globit('nu/components/src', '*.vue')),
        ('nu/entity', globit('nu/entity/', '*.py')),
        ('nujs/js', globit('nujs/js/', '*.js')),
    ]

setup(
    name='Nu',
    version='1.0.1',
    long_description=__doc__,
    packages=['nu', 'nuthon', 'nujs'],
    data_files=df,
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask', 'flask_script', 'behave', 'requests', 'wheel']
)