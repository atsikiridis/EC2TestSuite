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
        self.flavor = args['flavor']
        self.imageId = args['imageId']
        ec2_interface_class = Ec2Flavor.get_interface(self.flavor)
        self.ec2_interface = ec2_interface_class(EC2_Params, args)
        self.instance_id = '' #It is good practice to instantiate at __init(_)

    def runTest(self):
        """Tests the enpoint for all supported
        or specified by the user command"""
        results_dict = dict()

        #Commands concerning images.
        results_dict['DescribeImages'] = self.__test_describe_images()

        #Before issuing the commands concerning instances, we check whether
        #the image id the user provided is valid.
        if results_dict['DescribeImages'] is True:
            image_is_valid = self.__validate_image(self.imageId)
            if image_is_valid is True:
                results_dict['RunInstances'] = self.__test_run_instances()
                results_dict['DescribeInstances'] = self.__test_describe_instances()
                results_dict['TerminateInstances'] = self.__test_terminate_instances()
            else:
                self.logger.info("The image " + self.imageId +
                    " is not supported. Instances tests will be skipped. ")
        return results_dict

    def __test_describe_images(self):
        """Tests the DescribeImages command."""
        self.logger.info(" Making DescribeImages Request...")
        http_request = self.ec2_interface.httpreq_describe_images()
        self.logger.debug("Http request for DescribeImages: " +
            http_request)
        raw_cloud_response = HttpRequestMaker.connect_endpoint(http_request)
        xml_cloud_response = HttpRequestMaker.format_xml(raw_cloud_response)
        self.images_list_xml = xml_cloud_response
        self.logger.debug(" Xml response for DescribeImages" +
            xml_cloud_response)
        xmldoc = xml.dom.minidom.parseString(xml_cloud_response)
        try:
            self.assertTrue('imagesSet' in xml_cloud_response)
        except AssertionError:
            return False
        return True
            #List is usable by __validate_image(self,imageId).

    def __validate_image(self, imageId):
        """Checks whether the image  the user wants to perform the tests
        with is in the list of valid images (output of describeImages). This
        is necessary, because tests about instances cannot be performed
        otherwise."""
        if imageId in self.images_list_xml:
            return True
        return False

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
            print'hi' 
            node = xmldoc.getElementsByTagName('instanceId')[0].firstChild
        except IndexError:
            return False
        self.instance_id = node.nodeValue
        try:
            error_code = xmldoc.getElementsByTagName('code')[0].firstChild
            print error_code.nodeValue
        except IndexError:
            return False
        try:
            print '0' in error_code.nodeValue
            self.assertTrue( '0' in error_code.nodeValue )
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
        xmldoc = xml.dom.minidom.parseString(xml_cloud_response)
        try:
            error_code = xmldoc.getElementsByTagName('code')[0].firstChild
            print error_code.nodeValue
        except IndexError:
            return False
        try:
            print '0' in error_code.nodeValue
            self.assertTrue( '0' in error_code.nodeValue )
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
            xml_cloud_response)
        xmldoc = xml.dom.minidom.parseString(xml_cloud_response)
        try:
            error_code = xmldoc.getElementsByTagName('code')[0].firstChild
            print error_code.nodeValue
        except IndexError:
            return False
        try:
            print '0' in error_code.nodeValue
            self.assertTrue( '0' in error_code.nodeValue )
        except AssertionError:
            return False
        return True
