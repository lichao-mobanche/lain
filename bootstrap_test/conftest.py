#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import pytest
import time
import subprocess32 as subproc
from config import CONFIG
import app_ctl


@pytest.fixture(scope="session")
def bootstrap():
    subproc.check_call(
        'sudo /home/jenkins/workspace/lain-bootstrap/bootstrap --pypi-mirror -m https://l2ohopf9.mirror.aliyuncs.com -r docker.io/laincloud --vip={}'.
        format(CONFIG.vip)
    ,shell='true')


@pytest.fixture(scope="session")
def prepare_demo_images(bootstrap):
    subproc.check_call(
        'sudo sh /home/jenkins/workspace/lain-bootstrap/bootstrap_test/prepare_demo_images.sh',shell='true'
    )


@pytest.fixture(scope="session")
def reposit_ipaddr(prepare_demo_images):
    app_ctl.reposit(CONFIG.ipaddr_resource_appname)
    app_ctl.reposit(CONFIG.ipaddr_service_appname)
    app_ctl.reposit(CONFIG.ipaddr_client_appname)
    time.sleep(1)


@pytest.fixture(scope="session")
def deploy_ipaddr(reposit_ipaddr):
    app_ctl.deploy(CONFIG.ipaddr_resource_appname)
    app_ctl.deploy(CONFIG.ipaddr_service_appname)
    time.sleep(60)
    app_ctl.deploy(CONFIG.ipaddr_client_appname)
    time.sleep(30)


@pytest.fixture(scope="session")
def add_node(bootstrap):
    subproc.check_call(
        'cd /home/jenkins/workspace/lain-bootstrap/bootstrap_test && sudo ansible-playbook \
                -i host_vars/test-nodes distribute_ssh_key.yaml',shell='true'
    )
    subproc.check_call(
        'sudo lainctl node add -p /home/jenkins/workspace/lain-bootstrap/playbooks node2:192.168.77.22 ' +
        'node3:192.168.77.23',shell='true'
    )


@pytest.fixture(scope="session")
def scale_ipaddr_client(deploy_ipaddr, add_node):
    app_ctl.scale(CONFIG.ipaddr_client_appname, CONFIG.ipaddr_client_procname,
                  CONFIG.ipaddr_client_num_instances)
    time.sleep(120)
