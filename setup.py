
from distutils.core import setup

import os

def is_package(path):
    return (
        os.path.isdir(path) and
        os.path.isfile(os.path.join(path, '__init__.py'))
        )

def find_packages(path='.', base='' ):
    """ Find all packages in path """
    packages = {}
    for item in os.listdir(path):
        directory = os.path.join(path, item)
        if is_package( directory ):
            if base:
                module_name = '%(base)s.%(item)s' % vars()
            else:
                module_name = item
            packages[module_name] = directory
            packages.update(find_packages(directory, module_name))
    if base:
        return packages
    return packages.keys()

setup(
        name='handywsgi',
        description='A webapp framework for python 3.x, inspired by web.py.',
        author='haxwithaxe',
        author_email='spam@haxwithaxe.net',
        url='https://github.com/haxwithaxe/handywsgi',
        packages=find_packages()
        )
