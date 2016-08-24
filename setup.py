#!/usr/bin/env python

from distutils.core import setup

setup(name='intron_retention_utils',
      version='0.1.0beta',
      description='Python tools for processing chimeric reads',
      author='Yuichi Shiraishi',
      author_email='friend1ws@gamil.com',
      url='https://github.com/friend1ws/chimera_utils',
      package_dir = {'': 'lib'},
      packages=['chimera_utils'],
      scripts=['chimera_utils'],
      license='GPL-3'
     )

