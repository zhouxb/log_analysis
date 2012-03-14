import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name             = "log_analysis",
    version          = "0.0.4",
    author           = "dreamersdw",
    author_email     = "dreamersdw@gmail.com",
    description      = ("Parse DNS logs and do some analysis"),
    license          = "BSD",
    keywords         = "DNS, log",
    url              = "http://packages.python.org/log_analysis",
    packages         = find_packages(),
    long_description = read('README'),
    install_requires = ["puremvc==1.2", 
                        "pyinotify==0.9.1", 
                        "pymongo==2.1.1",
                        "yapsy==1.8", 
                        "jinja2==2.6"],
    entry_points     = {
        'console_scripts': [
            'log_analysis = log_analysis.main:main',
        ]
    },
    classifiers      = [
        "Development Status :: 3 - Alpha",
        "Topic :: Program",
        "License :: OSI Approved :: BSD License",
    ],
)
