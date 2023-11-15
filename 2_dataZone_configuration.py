#
# 0. Install / import boto3 and os libraries
#

import os
import boto3 # pip install boto3
import time

#
# 1. Get the account id
#

stsc = boto3.client('sts')

caller_identity = stsc.get_caller_identity()
account_id = caller_identity.get('Account')

#
# 2. via. the AWS protal create a DataZone domain. Click the quick set up box
#

datazone_domain_id = '<domain_id>'

#
# 2. Create DataZone projects
#

dzc = boto3.client('datazone')

# Producer - Compound Libraries
try:
    r = dzc.create_project(
        domainIdentifier = datazone_domain_id,
        name = 'Producer - Compound Libraries'
    )

    producer_compound_libraries_domain_id = r['domainId']
    
except Exception as e:
    print(e)

    producer_compound_libraries_domain_id = str(e).split()[-1]

# Consumer - High-Throughput Screening
try:
    r = dzc.create_project(
        domainIdentifier = datazone_domain_id,
        name = 'Consumer - High-Throughput Screening'
    ) 

    consumer_high_throughput_screening_domain_id = r['domainId']
    
except Exception as e:
    print(e)

    consumer_high_throughput_screening_domain_id = str(e).split()[-1]
