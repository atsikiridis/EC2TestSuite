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
        config.read("ec2_flavors.conf")
        try:
            ec2_flavor = config.get("EC2_flavors", flavor)
        except ValueError:
            print "exception on %s_EC2!" % flavor
            raise ValueError
        ec2_flavor_module = __import__(ec2_flavor+'_ec2_flavor')
        ec2_class = ec2_flavor.capitalize()
        ec2_flavor = getattr(ec2_flavor_module, ec2_class+'Ec2')
        return ec2_flavor


    @abstractmethod
    def httpreq_run_instances(self):
        """Gets a valid and signed request to run instances."""
        for arg in self.action_args:
            if 'ImageId' in arg:
                image_id_args = arg.split("=")
                image_id = image_id_args[1]
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
            if any("__runInstances__" in B.__dict__ for B in C.__mro__):
                return True
        return NotImplemented

    class Ec2Signer(object):
        """Class signing the requests and making them ready for the endpoint."""
        @staticmethod
        def sign_request(ec2_params, args):
            """Signs the request according to the standard EC2
                           Specifications."""
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
            signature = hmac.new(key=ec2_secret_key, msg=signable,
                digestmod=hashlib.sha256).digest()
            signature = urllib.quote_plus(base64.b64encode(signature))
            return str(ec2_url[0]+'://'+ec2_url[1]+ec2_url[2]+'?'+query
                +'&Signature='+signature)

