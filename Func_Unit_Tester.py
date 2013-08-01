# assert: my built xml, with answer from curl

import unittest
from EC2_Flavor import EC2_Flavor
from HTTP_Request_Maker import HTTP_Request_Maker 
import xml.dom.minidom

class Func_Unit_Tester(unittest.TestCase):

    def __init__(self, EC2_Params, flavor, action_args):
        EC2_interface = EC2_Flavor.get_interface(flavor)
        self.ec2_interface = EC2_interface(EC2_Params, action_args)
        
    
    def test_cloud(self):
        results_dict = dict()
        runInstances_result = self.testRunInstances()
        results_dict['RunInstances']=runInstances_result
        describeInstances_result = self.testDescribeInstances()
        results_dict['DescribeInstances']=describeInstances_result
        terminateInstances_result = self.testTerminateInstances()
        results_dict['TerminateInstances']=terminateInstances_result        
        return results_dict

        #different because xml building will be different. TODO Mock Response Constructor? Well, for now I just want to know if ok:)
    def testRunInstances(self):
        http_request = self.ec2_interface.httpreq_runInstances() #mockRunInstances!!!
        cloud_response = HTTP_Request_Maker.__make_request__(http_request)
        xmldoc = xml.dom.minidom.parseString(cloud_response)
        self.instanceId = xmldoc.getElementsByTagName('instanceId')[0].firstChild.nodeValue
        try:
            self.assertTrue('<code>0</code>' in cloud_response)
        except:
            return False
        return True


    def testDescribeInstances(self):
        http_request = self.ec2_interface.httpreq_describeInstances()
        cloud_response = HTTP_Request_Maker.__make_request__(http_request)
        try:        
            self.assertTrue('<code>0</code>' in cloud_response)
        except:
            return False
        return True


    def testTerminateInstances(self):
        http_request = self.ec2_interface.httpreq_terminateInstances(self.instanceId)
        cloud_response = HTTP_Request_Maker.__make_request__(http_request)
        try:        
            self.assertTrue('<code>0</code>' in cloud_response)
        except:
            return False
        return True
