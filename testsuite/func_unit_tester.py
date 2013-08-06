"""This module performs the actual unit tests to the cloud endpoint """

import unittest
from testsuite.ec2_flavor import Ec2Flavor
from testsuite.http_request_maker import HttpRequestMaker
import xml.dom.minidom
import logging

class FuncUnitTester(unittest.TestCase):
    """The Unit Tester class."""
    def __init__(self, EC2_Params, args):
        super(FuncUnitTester, self).__init__()
        self.logger = logging.getLogger("Ec2TestSuite")
        ec2_interface_class = Ec2Flavor.get_interface(args['flavor'])
        self.ec2_interface = ec2_interface_class(EC2_Params, args)
        self.instance_id = '' #It is good practice to instantiate at __init(_)

    def runTest(self):
        """Tests the enpoint for all supported
        or specified by the user command"""
        results_dict = dict()
        run_instances_result = self.__test_run_instances()
        results_dict['RunInstances'] = run_instances_result
        describe_instances_result = self.__test_describe_instances()
        results_dict['DescribeInstances'] = describe_instances_result
        terminate_instances_result = self.__test_terminate_instances()
        results_dict['TerminateInstances'] = terminate_instances_result
        return results_dict

    def __test_run_instances(self):
        """Tests the RunInstances command."""
        self.logger.info(" Making RunInstances Request...")
        http_request = self.ec2_interface.httpreq_run_instances()
        self.logger.debug(" Http request for RunInstances: " + http_request)
        raw_cloud_response = HttpRequestMaker.connect_endpoint(http_request)
        xml_cloud_response = HttpRequestMaker.format_xml(raw_cloud_response)
        self.logger.debug (" Xml response for RunInstances: " +
            xml_cloud_response )
        xmldoc = xml.dom.minidom.parseString(xml_cloud_response)
        try:
            node = xmldoc.getElementsByTagName('instanceId')[0].firstChild
        except IndexError:
            return False
        self.instance_id = node.nodeValue
        try:
            self.assertTrue('<code>0</code>' in xml_cloud_response)
        except AssertionError:
            return False
        return True


    def __test_describe_instances(self):
        """Tests the DescribeInstances command."""
        self.logger.info(" Making DescribeInstances Request...")
        http_request = self.ec2_interface.httpreq_describe_instances()
        self.logger.debug( " Http request for DescribeInstances: " +
            http_request)
        raw_cloud_response = HttpRequestMaker.connect_endpoint(http_request)
        xml_cloud_response = HttpRequestMaker.format_xml(raw_cloud_response)
        self.logger.debug(" Xml response for DescribeInstances: " +
            xml_cloud_response)
        try:
            self.assertTrue('<code>0</code>' in xml_cloud_response)
        except AssertionError:
            return False
        return True


    def __test_terminate_instances(self):
        """Tests the TerminateInstances command."""
        ec2 = self.ec2_interface
        self.logger.info(" Making TerminateInstances Request... ")
        http_request = ec2.httpreq_terminate_instances(self.instance_id)
        self.logger.debug(" Http request for TerminateInstances: " +
            http_request)
        raw_cloud_response = HttpRequestMaker.connect_endpoint(http_request)
        xml_cloud_response = HttpRequestMaker.format_xml(raw_cloud_response)
        self.logger.debug(" Xml response for TerminateInstances: " +
            http_request)
        try:
            self.assertTrue('<code>0</code>' in xml_cloud_response)
        except AssertionError:
            return False
        return True
