#!/usr/bin/python
# This file is part of NoWait

DOCUMENTATION = '''
---
module: ec2_search
short_description: ask EC2 for information about other instances.
description:
    - Only supports seatch for hostname by tags currently. Looking to add more later.
version_added: "1.9"
options:
  key:
    description:
      - instance tag key in EC2
    required: false
    default: Name
    aliases: []
  value:
    description:
      - instance tag value in EC2
    required: false
    default: null
    aliases: []
  lookup:
    description:
      - What type of lookup to use when searching EC2 instance info.
    required: false
    default: tags
    aliases: []
  region:
    description:
      - EC2 region that it should look for tags in
    required: false
    default: All Regions
    aliases: []
author:
    - "Michael Schuett (@michaeljs1990)"
extends_documentation_fragment: aws
'''

EXAMPLES = '''
# Note: These examples do not set authentication details, see the AWS Guide for details.

# Basic provisioning example
- ec2_search:
    key: mykey
    value: myvalue

'''
try:
    import boto
    import boto.ec2
    HAS_BOTO = True
except ImportError:
    HAS_BOTO = False

def get_all_ec2_regions(module):
    try:
        regions = boto.ec2.regions()
    except Exception, e:
        module.fail_json('Boto authentication issue: %s' % e)

    return regions

# Connect to ec2 region
def connect_to_region(region, module):
    try:
        conn = boto.ec2.connect_to_region(region.name)
    except Exception, e:
        print module.jsonify('error connecting to region: ' + region.name)
        conn = None
    # connect_to_region will fail "silently" by returning
    # None if the region name is wrong or not supported
    return conn

def main():
    module = AnsibleModule(
        argument_spec = dict(
            key = dict(default='Name'),
            value = dict(),
            lookup = dict(default='tags'),
            region = dict(),
        )
    )

    if not HAS_BOTO:
        module.fail_json(msg='boto required for this module')

    server_info = []

    for region in get_all_ec2_regions(module):
        conn = connect_to_region(region, module)
        try:
            # Run when looking up by tag names, only returning hostname currently
            if module.params.get('lookup') == 'tags':
                ec2_key = 'tag:' + module.params.get('key')
                ec2_value = module.params.get('value')
                reservations = conn.get_all_instances(filters={ec2_key : ec2_value})
                for instance in [i for r in reservations for i in r.instances]:
                    if instance.private_ip_address != None:
                        server_info.append('ip-' + instance.private_ip_address.replace('.', '-'))
        except:
            print module.jsonify('error getting instances from: ' + region.name)

    ansible_facts = {'ec2_search': server_info}
    ec2_facts_result = dict(changed=True, ansible_facts=ansible_facts)

    module.exit_json(**ec2_facts_result)

# import module snippets
from ansible.module_utils.basic import *
from ansible.module_utils.ec2 import *

main()
