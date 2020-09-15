from setuptools import setup
import os
import sys

_here = os.path.abspath(os.path.dirname(__file__))

if sys.version_info[0] < 3:
    with open(os.path.join(_here, 'README.md')) as f:
        long_description = f.read()
else:
    with open(os.path.join(_here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()


setup(
    name='pydaisy',
    version='0.2.4',
    description=('Various helper classes to read and manipulate Daisy input and output files.'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Jacob Gudbjerg',
    author_email='jacobgudbjerg@gmail.com',
    url='https://github.com/JacobGudbjerg/PyDaisy',
    license='MPL-2.0',
    packages=['pydaisy'],
    install_requires=[
        'pandas',
        'numpy'
    ],
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.7'],
    )
