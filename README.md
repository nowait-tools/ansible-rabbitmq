RabbitMQ
=========

RabbitMQ playbook that enables you to spin up a simple server or cluster them together. If you are integrating this into another repo make sure that rabbitmq goes in the roles folder and that you have a top level folder called lookup_plugins with find_by_tag.py in it or this play will not be able to auto cluster. Currently only EC2 is supported but feel free to request support for other services you may want to use this with.

Requirements
------------

Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required.

Role Variables
--------------

    # enables the management plugin for rabbitmq
    rabbitmq_manage: true
    # enables clustering and ensures the same cookie is used
    rabbitmq_cluster: false
    # create a rabbitmq user
    make_rabbitmq_user: true
    # .erlang.cookie file value don't use this value
    rabbitmq_cookie: XPVTRGPZHAQYKQHKEBUF
    # RabbitMQ user premissions
    rabbitmq_configure_priv: .*
    rabbitmq_read_priv: .*
    rabbitmq_write_priv: .*
    rabbitmq_user_state: present
    # RabbitMQ (rabbitmq.config)
    rabbitmq_amqp_port: 5672
    rabbitmq_loopback_user: guest
    rabbitmq_default_vhost: /
    rabbitmq_default_user: ansible
    rabbitmq_default_pass: ansible
    rabbitmq_default_user_tags: administrator
    rabbitmq_disk_free_limit: 0.7
    rabbitmq_high_watermark: 0.4
    rabbitmq_high_watermark_paging: 0.5

Example Playbook
----------------

Simple playbook that is enabled for use of clustering. Never use the default key in production:

    ---
    - hosts: localhost
      connection: local
      sudo: yes
      vars:
        rabbitmq_cluster: true
      roles:
        - rabbitmq

Auto Clustering (EC2)
---------------------

This playbook has auto clustering support built in with the exception that you need to configure a few things.

You must first create a Launch Configuration (LC) that contains a user data file available via the advanced features dropdown on the Configure Details tab. An example file that you may want to place here would look like this.

    #!/bin/bash -ex
    exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1

    echo "BEGIN USER-DATA"

    export AWS_ACCESS_KEY_ID='XXX'
    export AWS_SECRET_ACCESS_KEY='XXX'

    # install needed packages for ansible
    apt-get -y update
    apt-get install -y -q python-paramiko python-yaml python-jinja2 python-simplejson python-setuptools
    apt-get install -y -q git-core python-pip

    pip install boto ansible

    # setup hosts
    echo "[local]" > ~/ansible_hosts
    echo "localhost" >> ~/ansible_hosts
    export ANSIBLE_HOSTS=~/ansible_hosts
    export HOME=/root

    mkdir /tmp/ansible
    ansible-pull -U https://github.com/nowait-tools/rabbitmq.git -d /tmp/ansible --purge playbook.yml --accept-host-key

    echo "END USER-DATA"

    exit 0

You must also ensure that your servers are in the same security group and have the proper ports open to each other as well as being in the same VPC. The ports that need to be open can be found in the rabbitmq documentation. You will likely only need 4369, 25672, 15672, and 5672. If you are having issues open up all ports to everything for testing to ensure the security group is not the issue.

Add the LC you have made to an Auto Scale Group (ASG) and set the number of servers to spin up.

License
-------

BSD

Author Information
------------------

Produced by NoWait
