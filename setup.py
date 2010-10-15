from setuptools import setup, find_packages

version = '0.1'

setup(name='Geographic coordinate system',
      version=version,
      description="Geographic Coordinate System types and functions",
      long_description="",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='TransLoc',
      author_email='nathan@transloc.com',
      url='http://transloc.com',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'geopy',          
          'shapely'
      ],
      entry_points="",
      )
