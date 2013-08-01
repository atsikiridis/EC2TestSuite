#EC2TestSuite

* Amazon's *EC2* Cloud interface is a de facto standard in cloud computing. Several Cloud Infrastructure as a Service (IaaS) providers provide an 'EC2 like' interface.
* Sometimes, differences may be noticed between different interfaces (e.g. Openstack, AWS) althought there are several well known *flavors*
* This aspires to be a test suite that will perform *black-box testing* to cloud endpoints using *EC2 HTTP API* and *pyunit*, to determine:
	1)Whether the Cloud Endpoint is functional and behaves as an EC2 interface.
	2)Performance Tests

* The current version is a toy prototype whick checks an OpenStack Cloud in terms of minimal functionality. That is: *running*, *describing* and *terminating* one instance.

* The project will be *under heavy development* the following weeks (yay :) )! 

* All code is written in python.



#How to use (currently OpenStack only)

1) Source into your system the variables EC2_ACCESS_KEY, EC2_SECRET_KEY and EC2_URL.
2) run from bash: $python ec2_testsuite.py flavor=OpenStack 
ImageId=*yourimage*


#Big TODO (5 stuff at the time)

* Write setup.py and manage dependencies and packages.
* Make command line robust and extensible. Support --debug .
* Logger. (out, err).
* Write Reporter functionality (with tables etc.).
* Manage all configuration. If not in ini file, THEN on the command line

#License

This project is under "Do whatever you want" MIT License => http://www.tldrlegal.com/license/mit-license

However, all the other Open source frameworks/technologies used in this project come with their own respective licenses.


