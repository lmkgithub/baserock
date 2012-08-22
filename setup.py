# Copyright (C) 2011, 2012  Codethink Limited
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


'''Setup.py for lorry.'''


from distutils.core import setup
from distutils.cmd import Command
from distutils.command.build import build
from distutils.command.clean import clean
import glob
import os
import shutil
import subprocess

import morphlib


class GenerateManpage(build):

    def run(self):
        build.run(self)
        print 'building manpages'
        for x in ['lorry']:
            with open('%s.1' % x, 'w') as f:
                subprocess.check_call(['python', x,
                                       '--generate-manpage=%s.1.in' % x,
                                       '--output=%s.1' % x], stdout=f)


class Clean(clean):

    clean_files = [
        '.coverage',
        'build',
    ]
    clean_globs = [
        '*/*.py[co]',
    ]

    def run(self):
        clean.run(self)
        itemses = ([self.clean_files] +
                   [glob.glob(x) for x in self.clean_globs])
        for items in itemses:
            for filename in items:
                if os.path.isdir(filename):
                    shutil.rmtree(filename)
                elif os.path.exists(filename):
                    os.remove(filename)


class Check(Command):

    user_options = [
    ]

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        subprocess.check_call(['./check'])


setup(name='lorry',
      description='FIXME',
      long_description='''\
FIXME
''',
      author='Baserock',
      author_email='baserock-dev@baserock.org',
      url='http://wiki.baserock.org/',
      scripts=['lorry'],
      data_files=[('share/man/man1', glob.glob('*.[1-8]'))],
      cmdclass={
          'build': GenerateManpage,
          'check': Check,
          'clean': Clean,
      })
