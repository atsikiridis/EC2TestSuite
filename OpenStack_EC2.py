from EC2_Flavor import EC2_Flavor

class OpenStack_EC2(EC2_Flavor):

    # No real changes for now!
    def __httpreq_runInstances__(self):
        return super(OpenStack_EC2, self).__httpreq_runInstances__()
