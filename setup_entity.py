from setuptools import setup
from pathlib import Path

def globit(st, nd):
    bl = Path(st).glob(nd)
    return [str(b) for b in sorted(bl)]

df = [

    ]

setup(
    name='NuEntity',
    version='1.0.1',
    long_description=__doc__,
    packages=['entity', 'common'],
    data_files=df,
    include_package_data=True,
    zip_safe=False,
    install_requires=['']
)