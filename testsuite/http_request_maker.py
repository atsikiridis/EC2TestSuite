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
