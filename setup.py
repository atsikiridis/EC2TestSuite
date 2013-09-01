#Copyright (C) 2013 CERN
#
#    Author: Artem Tsikiridis <artem.tsikiridis@cern.ch>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License version 3, as
#    published by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""The setup.py module of the programme."""

from distutils.core import setup
import glob

setup(name = "testsuite",
      version = "0.1",
      description = " A test-suite for EC2 Cloud interfaces",
      author = "Artem Tsikiridis",
      author_email = "artem.tsikiridis@cern.ch",
      packages = ["testsuite"],
      data_files = [('/etc/ec2testsuite/conf',
          ['testsuite/conf/ec2_flavors.conf'])],
      requires = "prettytable",
      scripts = glob.glob('bin/ec2test')
      )
