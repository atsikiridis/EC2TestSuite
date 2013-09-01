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

"""This is the main module of the Test Suite."""

import os
from testsuite.func_unit_tester import FuncUnitTester
import argparse
import logging
from testsuite.reporter import Reporter

class Ec2TestSuite(object):
    """ The main class of the test suite."""

    def run(self ):
        """Runs the testsuite."""
        logging.basicConfig()
        self.parse_args()

    def __init__(self):
        self.ec2_params = Ec2TestSuite.get_ec2_env()
        self.logger = logging.getLogger("Ec2TestSuite")

    @staticmethod
    def get_ec2_env():
        """Gets environmental variables from environment. """
        logger = logging.getLogger("Ec2TestSuite")
        logging.basicConfig()
        required_env = ("EC2_ACCESS_KEY", "EC2_SECRET_KEY","EC2_URL")
        ec2_params = list()
        for env in required_env:
            if not os.getenv(env):
                logger.error("Error: " + env +
                    " environment variable must be set.")
                raise SystemExit
            else:
                ec2_params.append(os.getenv(env))
        return ec2_params

    def parse_args(self):
        """Parses args from command line"""
        parser = argparse.ArgumentParser()
        parser.add_argument('-f', '--flavor', help =
            "valid flavors:openstack (more to come)", required = True)
        parser.add_argument('-i', '--imageId', help =
            "Your image id", required = True)
        parser.add_argument('-d', '--debug', help =
            "Enables debugging", required = False, action =
            "store_true")
        args = vars(parser.parse_args())
        if args["debug"] == True:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)
        self.logger.info(" Starting tests for " + args['flavor'] +' cloud...')
        unit_tester = FuncUnitTester(self.ec2_params, args)
        results = unit_tester.runTest()
        print results
        self.logger.info('\n\n' +
            str(Reporter.get_pretty_params(args)))
        self.logger.info('\n\n' +
            str(Reporter.get_pretty_func(results)))

    @staticmethod
    def print_usage():
        """ Prints help"""
        return """Type -h or --help for help\n"""
