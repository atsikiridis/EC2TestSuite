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

"""Module of Openstack flavor."""

from testsuite.ec2_flavor import Ec2Flavor

class OpenstackEc2(Ec2Flavor):
    """Openstack class."""
    def httpreq_run_instances(self):
        """Overrides super class."""
        return super(OpenstackEc2, self).httpreq_run_instances()
