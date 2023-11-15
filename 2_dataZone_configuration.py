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
    
    time.sleep(120)

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
    
    time.sleep(120)

except Exception as e:
    print(e)

    consumer_high_throughput_screening_domain_id = str(e).split()[-1]

#
# 3. Create an enviorment for each project
#

# Get the ID of each enviorment profile
enviorment_profile_dict = {}

r = dzc.list_environment_profiles(domainIdentifier = datazone_domain_id)

for envioronment_profile in r['items']:
    
    enviorment_profile_dict[envioronment_profile['name']] = envioronment_profile['id']

# Create the enviorments 

# Producer - Compound Libraries
try:
    r = dzc.create_environment(
        domainIdentifier = datazone_domain_id,
        environmentProfileIdentifier = enviorment_profile_dict['DataLakeProfile'],
        name = 'Data Lake Environment',
        projectIdentifier = producer_compound_libraries_domain_id
    )
    
    producer_compound_libraries_data_lake_environment_id = r['id']
    
    time.sleep(120)
    
except Exception as e:
    print(e)
    
    producer_compound_libraries_data_lake_environment_id = ''

# Consumer - High-Throughput Screening
try:
    r = dzc.create_environment(
        domainIdentifier = datazone_domain_id,
        environmentProfileIdentifier = enviorment_profile_dict['DataLakeProfile'],
        name = 'Data Lake Environment',
        projectIdentifier = consumer_high_throughput_screening_domain_id
    )

except Exception as e:
    print(e)
    
#
# 4. Create a data source for Glue databases
#

# Producer - Compound Libraries
try:
    r = dzc.create_data_source(
        name = 'Glue Data Catalog Compound Libraries',
        domainIdentifier = datazone_domain_id,
        environmentIdentifier = producer_compound_libraries_data_lake_environment_id,
        projectIdentifier = producer_compound_libraries_domain_id,
        recommendation = {
            'enableBusinessNameGeneration': True
        },
        type = 'glue',
        configuration = {
            'glueRunConfiguration' : {
            'relationalFilterConfigurations': [
                {
                    'databaseName': 'compound_libraries',
                    'filterExpressions': [
                    {
                        'expression': '*',
                        'type': 'INCLUDE'
                    }
                    ]
                }
            ]
            }
        }
    )
    
    producer_compound_libraries_data_source_id = r['id']
    
    time.sleep(120)
    
except Exception as e:
    print(e)
    
    producer_compound_libraries_data_source_id = ''
#
# 5. Run the data source
#

try:
    r = dzc.start_data_source_run(
        dataSourceIdentifier = producer_compound_libraries_data_source_id,
        domainIdentifier = datazone_domain_id
    )

except Exception as e:
    print(e)
