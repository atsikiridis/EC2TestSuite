"""The setup.py module of the programme."""

from distutils.core import setup
import glob

setup(name = "testsuite",
      version = "0.1",
      description = " A test-suite for EC2 Cloud interfaces",
      author = "Artem Tsikiridis",
      author_email = "atsik@dmst.aueb.gr",
      packages = ["testsuite"],
      data_files = [('/etc/ec2testsuite/conf',
          ['testsuite/conf/ec2_flavors.conf'])],
      requires = "prettytable",
      scripts = glob.glob('bin/ec2test')
      )
