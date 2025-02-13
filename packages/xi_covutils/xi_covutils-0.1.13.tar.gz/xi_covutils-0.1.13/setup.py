from setuptools import setup
import inspect
from os import chdir
from os.path import dirname
from os.path import join
from os.path import abspath
from subprocess import call
from sys import argv
from os import getcwd
from os import environ

def make_docs():
    dst = join(dirname(inspect.stack()[0][1]), "docs")
    wd = dirname(abspath(inspect.stack()[0][1]))
    mod_folder = join("..", "xi_covutils")
    chdir(dst)
    print("... Entering docs/")
    old_python_path = environ.get("PYTHONPATH", "") 
    environ["PYTHONPATH"] = wd
    try:
        print("... Building documenatation")
        retcode = call("pdoc --html --overwrite {}".format(mod_folder).split())
    except:
        pass
    print("... Leaving docs/, returning to {}".format(wd))
    environ["PYTHONPATH"] = old_python_path
    chdir(wd)

try:
    if 'sdist' in argv:
        print("Creating distribution documentation")
        make_docs()
except:
    pass

setup(name='xi_covutils',
      version='0.1.13',
      description='Tools to work with protein covariation',
      url='https://gitlab.com/bioinformatics-fil/xi_covutils',
      author='Javier Iserte',
      author_email='jiserte@leloir.org.ar',
      license='I dont know yet',
      packages=['xi_covutils'],
      zip_safe=False)

