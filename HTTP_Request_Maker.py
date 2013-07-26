import xml.dom.minidom
import urllib

class HTTP_Request_Maker:
    
    @staticmethod
    def __make_request__(http_request):
	xml_answer =  xml.dom.minidom.parse(urllib.urlopen(http_request)).toprettyxml()
        return xml_answer
