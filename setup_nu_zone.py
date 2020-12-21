from setuptools import setup
from pathlib import Path

def globit(st, nd):
    bl = Path(st).glob(nd)
    return [str(b) for b in sorted(bl)]

df = [

    ]

setup(
    name='nu',
    version='1.0.2',
    long_description=__doc__,
    packages=['nu_zone'],
    data_files=df,
    include_package_data=True,
    zip_safe=False,
    install_requires=['PyDispatcher']
)