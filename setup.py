from setuptools import setup

setup(
    name='Nu',
    version='1.0.1',
    long_description=__doc__,
    packages=['nu'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask', 'behave', 'requests', 'wheel']
)