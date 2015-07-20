## Usage: lookup('find_by_tag')
import boto
import boto.vpc
import boto.ec2

from sets import Set
from ansible import utils

class LookupModule(object):

    def __init__(self, basedir=None, **kwargs):
        self.basedir = basedir

    def run(self, terms, inject=None, **kwargs):

        terms = utils.listify_lookup_plugin_terms(terms, self.basedir, inject)

        if isinstance(terms, basestring):
           terms = [ terms ]

        ret = []

        try:
            regions = ec2.regions()
            print regions
            exit()
        except Exception, e:
            utils.warnings('Boto authentication issue: %s' % e)

        for term in terms:
            eligible_subnets = vpc.get_all_subnets(filters={"tag:tier": term})

        return Set(ret)

    # Connect to ec2 region
    def connect(self, region):
        ''' create connection to api server'''
        if self.eucalyptus:
            conn = boto.connect_euca(host=self.eucalyptus_host)
            conn.APIVersion = '2010-08-31'
        else:
            conn = ec2.connect_to_region(region)
        # connect_to_region will fail "silently" by returning None if the region name is wrong or not supported
        if conn is None:
            self.fail_with_error("region name: %s likely not supported, or AWS is down.  connection to region failed." % region)
        return conn
