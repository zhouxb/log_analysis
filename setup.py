import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name             = "log_analysis",
    version          = "0.0.1",
    author           = "dreamersdw",
    author_email     = "dreamersdw@gmail.com",
    description      = ("Parse DNS logs and do some analysis"),
    license          = "BSD",
    keywords         = "DNS, log",
    packages         = find_packages(),
    long_description = read('README'),
    install_requires = ["puremvc==1.2", 
                        "pyinotify==0.9.1", 
                        "pymongo==2.1.1",
                        "yapsy==1.8", 
                        "jinja2==2.6"],
    scripts          = [
                        "database/mongodb-linux-x86_64-2.0.3/bin/mongod",
                        "database/mongodb-linux-x86_64-2.0.3/bin/bsondump",
                        "database/mongodb-linux-x86_64-2.0.3/bin/mongo",
                        "database/mongodb-linux-x86_64-2.0.3/bin/mongod",
                        "database/mongodb-linux-x86_64-2.0.3/bin/mongodump",
                        "database/mongodb-linux-x86_64-2.0.3/bin/mongoexport",
                        "database/mongodb-linux-x86_64-2.0.3/bin/mongofiles",
                        "database/mongodb-linux-x86_64-2.0.3/bin/mongoimport",
                        "database/mongodb-linux-x86_64-2.0.3/bin/mongorestore",
                        "database/mongodb-linux-x86_64-2.0.3/bin/mongos",
                        "database/mongodb-linux-x86_64-2.0.3/bin/mongosniff",
                        "database/mongodb-linux-x86_64-2.0.3/bin/mongostat",
                        "database/mongodb-linux-x86_64-2.0.3/bin/mongotop"
                       ],
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
