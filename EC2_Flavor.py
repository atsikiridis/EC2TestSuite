from abc import ABCMeta, abstractmethod
import urlparse
import urllib
import hmac
import hashlib
import base64
import ConfigParser
import time

class EC2_Flavor:
    __metaclass__ = ABCMeta


    def __init__(self, ec2_params, action_args):
        self.ec2_params = ec2_params
	self.action_args = action_args

    @staticmethod
    def __get_interface__( flavor):
       config = ConfigParser.ConfigParser()
       config.read("ec2_flavors.conf")
       try:   
           ec2_flavor = config.get("EC2_flavors",flavor)
       except:
	   print "exception on %s_EC2!" % flavor 
       ec2_flavor_module = __import__(ec2_flavor)
       ec2_flavor = getattr(ec2_flavor_module, flavor+'_EC2')			
       return ec2_flavor


    @abstractmethod
    def __httpreq_runInstances__(self):
	for arg in self.action_args:
	    if 'ImageId' in arg:
	        imageId_args = arg.split("=")
		image_id = imageId_args[1]
	args_to_sign = list()
	args_to_sign.append('Action=RunInstances')
	args_to_sign.append('ImageId='+image_id)
	return self.EC2_Signer.__sign_request__(self.ec2_params, args_to_sign)
        

    def __httpreq_describeInstances__(self):
	args_to_sign = list()
	args_to_sign.append('Action=DescribeInstances')
	return self.EC2_Signer.__sign_request__(self.ec2_params, args_to_sign)


    def __httpreq_terminateInstances__(self, instanceid):
	args_to_sign = list()
	args_to_sign.append('Action=TerminateInstances')
	args_to_sign.append('InstanceId.1='+instanceid)
	return self.EC2_Signer.__sign_request__(self.ec2_params, args_to_sign)


    @classmethod
    def __subclasshook__(cls, C):
        if cls is EC2_flavor:
            if any("__runInstances__" in B.__dict__ for B in C.__mro__):
                return True
        return NotImplemented




    class EC2_Signer:
        
        @staticmethod
	def __sign_request__(ec2_params,args):
	    ec2_access_key = ec2_params[0]
	    ec2_secret_key = ec2_params[1]
	    ec2_url = ec2_params[2]
	    ec2_url = list(urlparse.urlparse(ec2_url))
            if ec2_url[2] == '': 
	        ec2_url[2] = '/'
	    ec2_path = ec2_url[1]+ec2_url[2]
	    escaped_args = []
	    timestamp = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
	    args += ["SignatureMethod=HmacSHA256", "SignatureVersion=2",
              "Version=2011-05-15",
              "AWSAccessKeyId="+ec2_access_key,
              "Timestamp="+timestamp]
            for arg in args:
		name,value = arg.split("=",1)
		escaped_args.append(urllib.quote_plus(name)+
		'='+urllib.quote_plus(value))
            escaped_args.sort()
	    query = '&'.join(escaped_args)
	    signable = "\n".join(['GET',ec2_url[1],ec2_url[2],query])
	    signature = hmac.new(key=ec2_secret_key, msg=signable,
	        digestmod=hashlib.sha256).digest()
	    signature = urllib.quote_plus(base64.b64encode(signature))
	    return str(ec2_url[0]+'://'+ec2_url[1]+ec2_url[2]+'?'+query
		+'&Signature='+signature)

