"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
setup(
    name='pybcl',  # Required
    version='0.0.1',  # Required
    description='PyBCL: Illumina BCL file handling in Python',  # Required
    long_description="PyBCL is an open-source pure-Python package for handling Illumina sequencing BCL files. Note that PyBCL was created from scratch by referring to the bcl2fastq manual (which can be found publicly on Illumina's website). PyBCL did not rely on any reverse-engineering of any proprietary Illumina code."
    long_description_content_type='text/plain',  # Optional (see note above)
    url='https://github.com/niemasd/PyBCL',  # Optional
    author='Niema Moshiri',  # Optional
    author_email='niemamoshiri@gmail.com',  # Optional
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='tree phylogenetics fast',  # Optional
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required
    extras_require={  # Optional
        'dev': ['check-manifest'],
    },
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/niemasd/PyBCL/issues',
        'Source': 'https://github.com/niemasd/PyBCL',
    },
)
