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

datazone_domain_id = 'dzd_dlw5mvh11a4giv'

#
# 3. Get the id of the projects in DataZone
#

dzc = boto3.client('datazone')

project_dict = {}

r = dzc.list_projects(domainIdentifier = datazone_domain_id)

for project in r['items']:
    
    project_dict[project['name']] = project['id']

#
# 4. Create an enviorment for each project
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
        name = 'Compound Libraries Data Lake Environment',
        projectIdentifier = project_dict['Producer - Compound Libraries']
    )
    
    producer_compound_libraries_data_lake_environment_id = r['id']
    
except Exception as e:
    print(e)
    
    # If the enviorment already exists get the ID
    enviorment_dict = {}
    
    r = dzc.list_environments(domainIdentifier = datazone_domain_id, projectIdentifier = project_dict['Producer - Compound Libraries'])
    
    for enviorment in r['items']:
        
        enviorment_dict[enviorment['name']] = enviorment['id']
    
    producer_compound_libraries_data_lake_environment_id = enviorment_dict['Compound Libraries Data Lake Environment']
    
# Consumer - High-Throughput Screening
try:
    r = dzc.create_environment(
        domainIdentifier = datazone_domain_id,
        environmentProfileIdentifier = enviorment_profile_dict['DataLakeProfile'],
        name = 'High-Throughput Screening Data Lake Environment',
        projectIdentifier = project_dict['Consumer - High-Throughput Screening']
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
        projectIdentifier = project_dict['Producer - Compound Libraries'],
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
    
    # If the data source already exists get the ID
    data_source_dict = {}
    
    r = dzc.list_data_sources(
        domainIdentifier = datazone_domain_id,
        environmentIdentifier = producer_compound_libraries_data_lake_environment_id,
        projectIdentifier = project_dict['Producer - Compound Libraries']
    )
    
    for data_source in r['items']:
        
        data_source_dict[data_source['name']] = data_source['dataSourceId']
        
    producer_compound_libraries_data_source_id = data_source_dict['Glue Data Catalog Compound Libraries']
    
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

#
# 6. Create glossary
#

try:
    r = dzc.create_glossary(
        description = 'Glossary terms for compond libraries data set(s)',
        domainIdentifier = datazone_domain_id,
        name = 'Compound Libraries',
        owningProjectIdentifier = project_dict['Producer - Compound Libraries'],
        status = 'ENABLED'
    )

    compound_libraries_glossary_id = r['id']

except Exception as e:
    print(e)
    
#
# 7. Create glossary terms
#
