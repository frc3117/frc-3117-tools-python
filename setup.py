from setuptools import setup, find_packages

import pathlib


here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='frctools',
    version='0.0.1',
    description='A collection of tools for FRC team 3117.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    author='FRC Team 3117',
    package_dir={'frctools': './frctools'},
    packages=find_packages(),
    install_requires=[
        'robotpy>=2023',
        'robotpy[sim]>=2023',
    ],
    python_requires='>=3.7, <4',
)