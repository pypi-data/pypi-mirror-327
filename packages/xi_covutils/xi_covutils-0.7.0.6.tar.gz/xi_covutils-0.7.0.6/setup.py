#!python
"""
Setup package
"""
from setuptools import setup
from setuptools import Extension

setup(
  ext_modules=[
    Extension(
      name='xi_covutils.auxl',
      sources=['xi_covutils/aux_func.c']
    )
  ]
)
