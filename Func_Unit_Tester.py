# assert: my built xml, with answer from curl

import unittest
from EC2_Flavor import EC2_Flavor
from HTTP_Request_Maker import HTTP_Request_Maker 
import xml.dom.minidom

class Func_Unit_Tester(unittest.TestCase):

    def __init__(self, EC2_Params, flavor, action_args):
        EC2_interface = EC2_Flavor.__get_interface__(flavor)
	self.ec2_interface = EC2_interface(EC2_Params, action_args)
	
    
    def __test_cloud__(self):
	results_list = list()
        runInstances_result = self.__testRunInstances__()
	results_list.append(runInstances_result)
        describeInstances_result = self.__testDescribeInstances__()
	results_list.append(describeInstances_result)
        terminateInstances_result = self.__testTerminateInstances__()
        results_list.append(terminateInstances_result)	
	return results_list

	#different because xml building will be different. TODO Mock Response Constructor? Well, for now I just want to know if ok:)
    def __testRunInstances__(self):
        http_request = self.ec2_interface.__httpreq_runInstances__() #mockRunInstances!!!
	cloud_response = HTTP_Request_Maker.__make_request__(http_request)
        xmldoc = xml.dom.minidom.parseString(cloud_response)
	self.instanceId = xmldoc.getElementsByTagName('instanceId')[0].firstChild.nodeValue
	try:
	    self.assertTrue('<code>0</code>' in cloud_response)
	except:
	    return False
	return True


    def __testDescribeInstances__(self):
        http_request = self.ec2_interface.__httpreq_describeInstances__()
	cloud_response = HTTP_Request_Maker.__make_request__(http_request)
	try:	
	    self.assertTrue('<code>0</code>' in cloud_response)
	except:
	    return False
	return True


    def __testTerminateInstances__(self):
        http_request = self.ec2_interface.__httpreq_terminateInstances__(self.instanceId)
	cloud_response = HTTP_Request_Maker.__make_request__(http_request)
	try:	
	    self.assertTrue('<code>0</code>' in cloud_response)
	except:
	    return False
	return True
