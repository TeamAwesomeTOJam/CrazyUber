from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Crazy Uber',
    version='0.1.0',

    description='An obviously saterical Crazy Taxi inspired game of vehicular mayhem.',
    long_description=long_description,

    url='https://github.com/TeamAwesomeTOJam/awesomeengine',
    author='Team Awesome',
    author_email='jonathan@jdoda.ca',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],

    packages=['crazyuber'],

    package_data = {
        'crazyuber': ['res/*/*'],
    },
    
    entry_points = {
        'gui_scripts' : [
            'crazyuber = crazyuber.main:go'
        ]
    },
    
    install_requires=[
        'awesomeengine>=0.0.1',
        'Box2D>=2.3'
    ],
)
