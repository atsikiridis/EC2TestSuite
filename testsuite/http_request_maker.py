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

"""Module providing methods concerning the connection to the cloud endpoint"""

import xml.dom.minidom
import urllib

class HttpRequestMaker(object):
    """The class that performs the requests to the cloud endpoint.
       Moreover, provides methods to get answer in readable xml formats."""

    @staticmethod
    def connect_endpoint(http_request):
        """Connect to the cloud endpoint via HTTP."""
        answer = urllib.urlopen(http_request)
        return answer

    @staticmethod
    def format_xml(answer):
        """Returns a pretty xml of the answer
           of the cloud by the cloud endpoint."""
        xml_answer =  xml.dom.minidom.parse(answer).toprettyxml()
        return xml_answer
