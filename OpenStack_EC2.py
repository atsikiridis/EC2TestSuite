from EC2_Flavor import EC2_Flavor

class OpenStack_EC2(EC2_Flavor):

    # No real changes for now!
    def httpreq_runInstances(self):
        return super(OpenStack_EC2, self).httpreq_runInstances()
