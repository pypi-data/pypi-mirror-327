#!python
from setuptools import setup
import inspect
from os import chdir
from os.path import dirname
from os.path import join
from os.path import abspath
from subprocess import call
from subprocess import check_output
from sys import argv
from os import getcwd
from os import environ
from os.path import join
from os.path import dirname
from os import access
from os import makedirs
from os import R_OK
import codecs


def module_file(m):
    mbase = join("docs", *m.name.split('.'))
    if m.is_package():
        return join(mbase, pdoc.html_package_name)
    else:
        return '%s%s' % (mbase, pdoc.html_module_suffix)

def html_out(m):
    f = module_file(m)
    dirpath = dirname(f)
    if not access(dirpath, R_OK):
        makedirs(dirpath)
    with codecs.open(f, 'w+', 'utf-8') as w:
        out = m.html(external_links=False,
                        link_prefix="",
                        http_server=False,
                        source=True)
        w.write(out)
    for submodule in m.submodules():
        html_out(submodule)

def make_docs():
    print("... Building html files")
    module = pdoc.import_module("xi_covutils")
    module = pdoc.Module(module, docfilter=None,
                        allsubmodules=False)
    html_out(module)

try:
    if 'sdist' in argv:
        print("Creating distribution documentation")
        import pdoc
        make_docs()
except:
    pass

setup(name='xi_covutils',
      version='0.1.16',
      description='Tools to work with protein covariation',
      url='https://gitlab.com/bioinformatics-fil/xi_covutils',
      author='Javier Iserte',
      author_email='jiserte@leloir.org.ar',
      license='I dont know yet',
      packages=['xi_covutils'],
      include_package_data=True,
      install_requires=["biopython==1.72", "enum34"],
      zip_safe=False)
