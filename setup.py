from setuptools import setup, find_packages

version = '0.2'

setup(name                  = 'GCS',
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