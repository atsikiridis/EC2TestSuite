"""Module providing an abstract class of an EC2 Flavor and classes to
   prepare a valid request."""

from abc import ABCMeta, abstractmethod
import urlparse
import urllib
import hmac
import hashlib
import base64
import ConfigParser
import time
import os
import logging
import importlib

class Ec2Flavor(object):
    """Abstract class of an EC2 Flavor. All flavors should be based on it"""
    __metaclass__ = ABCMeta

    def __init__(self, ec2_params, action_args):
        self.ec2_params = ec2_params
        self.action_args = action_args

    @staticmethod
    def get_interface( flavor):
        """Factory method providing the appropriate flavor of this  class"""
        config = ConfigParser.ConfigParser()
        config.read(os.path.join('/etc/ec2testsuite/conf',
            'ec2_flavors.conf'))
        logger = logging.getLogger("Ec2TestSuite")
        try:
            ec2_flavors = config.get("EC2_flavors", "Flavors")
        except ConfigParser.NoSectionError:
            logger.critical(""" No EC2_flavors section in cofig file. Wrong
                config file format."""
            )
        except ConfigParser.NoOptionError:
            logger.critical(" No Flavors option")
        ec2_flavor_module = None
        ec2_class = None
        if flavor in ec2_flavors:
            ec2_flavor_module = importlib.import_module('testsuite.'+flavor+
                '_ec2_flavor', package=None)
            ec2_class = flavor.capitalize()
        else:
            logger.error(" "+flavor+
                " flavor is not a valid value in conf file .")
            raise SystemExit
        ec2_flavor = getattr(ec2_flavor_module, ec2_class +'Ec2')
        logger.debug(" Flavor class is " + str(ec2_flavor) )
        return ec2_flavor


    @abstractmethod
    def httpreq_run_instances(self):
        """Gets a valid and signed request to run instances."""
        image_id = self.action_args['imageId']
        args_to_sign = list()
        args_to_sign.append('Action=RunInstances')
        args_to_sign.append('ImageId='+image_id)
        return self.Ec2Signer.sign_request(self.ec2_params, args_to_sign)

    def httpreq_describe_instances(self):
        """Gets a valid and signed request to  describe instances."""
        args_to_sign = list()
        args_to_sign.append('Action=DescribeInstances')
        return self.Ec2Signer.sign_request(self.ec2_params, args_to_sign)


    def httpreq_terminate_instances(self, instanceid):
        """Gets a valid and signed request to terminate instances."""
        args_to_sign = list()
        args_to_sign.append('Action=TerminateInstances')
        args_to_sign.append('InstanceId.1='+instanceid)
        return self.Ec2Signer.sign_request(self.ec2_params, args_to_sign)


    @classmethod
    def __subclasshook__(cls, C):
        if cls is Ec2Flavor:
            if any("httpreq_run_instances" in B.__dict__ for B in
            C.__mro__):
                return True
        return NotImplemented

    class Ec2Signer(object):
        """Class signing the requests and making them ready for the endpoint."""
        @staticmethod
        def sign_request(ec2_params, args):
            """Signs the request according to the standard EC2
                           Specifications."""
            logger = logging.getLogger("Ec2TestSuite")
            ec2_access_key = ec2_params[0]
            ec2_secret_key = ec2_params[1]
            ec2_url = ec2_params[2]
            ec2_url = list(urlparse.urlparse(ec2_url))
            if ec2_url[2] == '':
                ec2_url[2] = '/'
            escaped_args = []
            timestamp = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
            args += ["SignatureMethod=HmacSHA256", "SignatureVersion=2",
              "Version=2011-05-15",
              "AWSAccessKeyId="+ec2_access_key,
              "Timestamp="+timestamp]
            for arg in args:
                name, value = arg.split("=", 1)
                escaped_args.append(urllib.quote_plus(name)+
                '='+urllib.quote_plus(value))
            escaped_args.sort()
            query = '&'.join(escaped_args)
            signable = "\n".join(['GET', ec2_url[1], ec2_url[2], query])
            logger.debug("String to sign is: " + signable)
            signature = hmac.new(key=ec2_secret_key, msg=signable,
                digestmod=hashlib.sha256).digest()
            signature = urllib.quote_plus(base64.b64encode(signature))
            return str(ec2_url[0]+'://'+ec2_url[1]+ec2_url[2]+'?'+query
                +'&Signature='+signature)

