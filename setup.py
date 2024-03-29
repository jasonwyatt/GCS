from setuptools import setup, find_packages
import re

try:
    version = re.search('\((.*)\)', open('debian/changelog').readline()).group(1)
except:
    version = '1.0.0'

setup(name                  = 'gcs',
      version               = version,
      description           = "Geographic Coordinate System types and functions",      
      author                = 'TransLoc',
      author_email          = 'nathan@transloc.com',
      url                   = 'http://transloc.com',
      license               = 'All rights reserved',
      packages              = find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data  = False,
      zip_safe              = True,
      install_requires      = open('requirements.txt').readlines()
      )
