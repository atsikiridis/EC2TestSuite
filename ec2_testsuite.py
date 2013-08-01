"""This is the main module of the Test Suite."""

import os
import sys
from func_unit_tester import FuncUnitTester


class Ec2TestSuite(object):
    """ The main class of the test suite."""

    def __init__(self):
        self.ec2_params = Ec2TestSuite.get_ec2_env()

    @staticmethod
    def get_ec2_env():
        """Gets environmental variables from environment. """
        required_env = ("EC2_ACCESS_KEY", "EC2_SECRET_KEY","EC2_URL")
        ec2_params = list()
        for env in required_env:
            if not os.getenv(env):
                print "Error:", env, "environment variable must be set."
                raise SystemExit
            else:
                ec2_params.append(os.getenv(env))
        return ec2_params

    def parse_args(self, args):
        """Parses args from command line"""
        for arg in args:
            if 'flavor=' in arg:
                flavor_args = arg.split("=")
                flavor = flavor_args[1]
                args.remove(arg)
        unit_tester = FuncUnitTester(self.ec2_params, flavor, args)
        results = unit_tester.test_cloud()
        print results

    @staticmethod
    def print_usage():
        """ Prints help"""
        print 'No doc for my prototype :)'

if __name__ == "__main__":
    Ec2TestSuite().parse_args(sys.argv[1:])
