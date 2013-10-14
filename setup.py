from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(name='redomino_lfs_custom',
      version=version,
      description="LFS defaults for Redomino",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author="Andrea D'Este",
      author_email='info@redomino.com',
      url='http://redomino.com',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
