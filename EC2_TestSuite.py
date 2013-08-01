
import os
import sys
from Func_Unit_Tester import Func_Unit_Tester


class EC2_TestSuite:

    

    def main(self, args):
        self.EC2_params = self.get_EC2_env()
        self.parse_args(args)


    #EC2 auth params must be in OS Environment.
    def get_EC2_env(self):
        required_env = ("EC2_ACCESS_KEY","EC2_SECRET_KEY","EC2_URL")
        EC2_params = list()
        for env in required_env:
            if not os.getenv(env):
                print "Error:", env, "environment variable must be set."
                raise SystemExit
            else:
                EC2_params.append(os.getenv(env))
        return EC2_params
 


    # EC2_flavor is parsed.
    def parse_args(self, args):
        for arg in args:
            if 'flavor=' in arg:
                flavor_args= arg.split("=")
                flavor = flavor_args[1]
                args.remove(arg)
        unit_tester = Func_Unit_Tester(self.EC2_params, flavor, args)
        results = unit_tester.test_cloud()
        print results

    def print_usage(self):
        print 'No doc for my prototype :)'


if __name__ == "__main__":
    testSuite = EC2_TestSuite()
    testSuite.main(sys.argv[1:])
