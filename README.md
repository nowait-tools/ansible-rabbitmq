RabbitMQ
=========

RabbitMQ playbook that enables you to spin up a simple server or cluster them together.

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

License
-------

BSD

Author Information
------------------

Produced by NoWait
