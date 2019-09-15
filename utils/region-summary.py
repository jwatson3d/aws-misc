#!/usr/bin/env python3
################################################################################
# Copyright 2019 Keith D Gregory
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
################################################################################
#
# Examines all regions for resources that incur charges. 
#
# Invocation:
#
#   region-summary.py
#
# Where:
#
#   ROLE_NAME   is the simple name (including path) of an assumable role in
#               the current account.
#   ROLE_ARN    is the ARN of an assumable role from any account.
#   MFA_CODE    is the 6-digit code from a virtual MFA device
#
#
################################################################################

import boto3
import json
import logging
import os
import re
import sys
import uuid

logging.basicConfig()
logging.getLogger().setLevel(level=logging.INFO)


# this array is accessible from the default session, but the only way to get to
# the default session is via a private method, so I'll just replicate it here
# (plus, this lets me control order)

regions = [
            'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2',
            'ca-central-1',
            'eu-central-1', 'eu-north-1', 'eu-west-1', 'eu-west-2', 'eu-west-3',
            'ap-east-1', 'ap-northeast-1', 'ap-northeast-2', 'ap-south-1', 'ap-southeast-1', 'ap-southeast-2',
            'sa-east-1'
          ]

def retrieve_ec2_instance_ids(region):
    result = {}
    try:
        logging.info(f'processing EC2 region {region}')
        ec2 = boto3.resource('ec2', region_name=region)
        unterminated_instances = []
        for x in ec2.instances.all():
            if x.state['Name'] != 'terminated':
                unterminated_instances.append(x.id)
        result[region] = unterminated_instances
    except:
        logging.warn(f'exception processing EC2 region {region}')
    return result

def retrieve_unattached_volume_ids(region):
    result = {}
    try:
        logging.info(f'processing volumes in region {region}')
        ec2 = boto3.resource('ec2', region_name=region)
        unattached_volumes = []
        for x in ec2.volumes.all():
            if not x.attachments:
                unattached_volumes.append(x.id)
        result[region] = unattached_volumes
    except:
        logging.warn(f'exception processing volumes in region {region}')
    return result


def report(serviceName, resultMap):
    for region in resultMap:
        ids = resultMap.get(region, [])
        if len(ids) > 0:
            print(f'{serviceName} {region}: {len(ids)}')


if __name__ == "__main__":
    for region in regions:
        report('EC2', retrieve_ec2_instance_ids(region))
        report('Volumes', retrieve_unattached_volume_ids(region))
