# lookup('find_by_tag', 'key=Name value=rabbitmq')
import boto
import boto.ec2

from ansible import utils

class LookupModule(object):

    def __init__(self, basedir=None, **kwargs):
        self.basedir = basedir

    def run(self, terms, inject=None, **kwargs):
        terms = utils.listify_lookup_plugin_terms(terms, self.basedir, inject)

        if isinstance(terms, basestring):
           terms = [ terms ]

        meta_params = dict(key=None, value=None)

        for term in terms:
            params = term.split()
            try:
                for param in params:
                    key, value = param.split('=')
                    assert(key in meta_params)
                    if key == 'key':
                        meta_params['key'] = 'tag:' + value
                    if key == 'value':
                        meta_params['value'] = value
            except (ValueError, AssertionError) as e:
                utils.warnings(e)

        try:
            regions = boto.ec2.regions()
        except Exception, e:
            utils.warnings('Boto authentication issue: %s' % e)

        server_info = []

        for region in regions:
            conn = self.connect(region)
            try:
                reservations = conn.get_all_instances(filters={meta_params['key'] : meta_params['value']})
                for instance in [i for r in reservations for i in r.instances]:
                    server_info.append('ip-' + instance.private_ip_address.replace('.', '-'))
            except:
                utils.warning('error connecting to: ' + region.name)

        return server_info

    # Connect to ec2 region
    def connect(self, region):
        try:
            conn = boto.ec2.connect_to_region(region.name)
        except Exception, e:
            utils.warning('error connecting to region: ' + region.name)
            conn = None
        # connect_to_region will fail "silently" by returning
        # None if the region name is wrong or not supported
        return conn
