"""Module of Openstack flavor."""

from testsuite.ec2_flavor import Ec2Flavor

class OpenstackEc2(Ec2Flavor):
    """Openstack class."""
    def httpreq_run_instances(self):
        """Overrides super class."""
        return super(OpenstackEc2, self).httpreq_run_instances()
