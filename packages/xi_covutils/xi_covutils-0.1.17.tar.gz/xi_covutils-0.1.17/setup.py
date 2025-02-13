#!python
"""
    Setup package
"""
from setuptools import setup
from setuptools import Extension

setup(name='xi_covutils',
      version='0.1.17',
      description='Tools to work with protein covariation',
      url='https://gitlab.com/bioinformatics-fil/xi_covutils',
      author='Javier Iserte',
      author_email='jiserte@leloir.org.ar',
      license='I dont know yet',
      packages=['xi_covutils'],
      include_package_data=True,
      install_requires=['biopython==1.72', 'enum34', 'requests'],
      ext_modules=[Extension('xi_covutils.aux', ['xi_covutils/aux_func.c'])],
      zip_safe=False)
