#
# 0. Install / import boto3 and os libraries
#

import os
import boto3 # pip install boto3

#
# 1. Get CloudFormation output
#

cfn = boto3.client('cloudformation')

# Set the name of the CloudFormation stack
stack_name = 'data-zone'

response = cfn.describe_stacks(StackName=stack_name)

for stack in response['Stacks']:
    if stack["StackName"] == stack_name:
        for output in stack["Outputs"]:
            if output["OutputKey"] == "IAMRoleARN":
                IAMRoleARN = output["OutputValue"]
                
            elif output["OutputKey"] == "S3BucketARN":
                s3_bucket_arn = output["OutputValue"]
                s3_bucket_name = s3_bucket_arn.split(':')[-1]

#
# 2. Get the account id
#

stsc = boto3.client('sts')

caller_identity = stsc.get_caller_identity()
account_id = caller_identity.get('Account')

#
# 3. Set DataLake Admin, Change defaulr IAM access control for new databases and tables
# 

lfc = boto3.client('lakeformation')

data_lake_settings = {'DataLakeAdmins': [{'DataLakePrincipalIdentifier': 'arn:aws:iam::' + account_id + ':role/Admin'}], 'CreateDatabaseDefaultPermissions': [], 'CreateTableDefaultPermissions': []}

lfc.put_data_lake_settings(DataLakeSettings = data_lake_settings)

# 
# 4. Register DataLake Location - Administration
# 

lfc = boto3.client('lakeformation')

try:
    lfc.register_resource(ResourceArn = s3_bucket_arn, UseServiceLinkedRole = True) # --no-hybrid-access-enabled ?
except lfc.exceptions.AlreadyExistsException:
    print('The s3 bucket ' + s3_bucket_arn + ' is already registered with LakeFormation')

#
# 5. Upload sample data to S3
#

s3c = boto3.client('s3')

# Clinical Trial Data
if os.path.exists('./Clinical_Trial_Data.csv'):
    print("The file Clinical_Trial_Data.csv exists")
else:
    command = 'wget https://sharkech-public.s3.amazonaws.com/sample-data/Clinical_Trial_Data/Clinical_Trial_Data.csv'
    status = os.system(command)

s3c.upload_file('./Clinical_Trial_Data.csv', s3_bucket_name, 'Clinical_Trial/Clinical_Trial.csv')

# Compound Libraries
if os.path.exists('./Compound_Libraries.csv'):
    print("The file Compound_Libraries.csv exists")
else:
    command = 'wget https://sharkech-public.s3.amazonaws.com/sample-data/Compound_Libraries/Compound_Libraries.csv'
    status = os.system(command)

s3c.upload_file('./Compound_Libraries.csv', s3_bucket_name, 'Compound_Libraries/Compound_Libraries.csv')

# High-Throughput Screening Data
if os.path.exists('./High-Throughput_Screening_Data.csv'):
    print("The file High-Throughput Screening Data.csv exists")
else:
    command = 'wget https://sharkech-public.s3.amazonaws.com/sample-data/High-Throughput_Screening_Data/High-Throughput_Screening_Data.csv'
    status = os.system(command)

s3c.upload_file('./High-Throughput_Screening_Data.csv', s3_bucket_name, 'High-Throughput_Screening/High-Throughput_Screening.csv')

#
# 6. Create Glue Data Catalog Databases
#

gluec = boto3.client('glue')

# Clinical Trial
try:
    gluec.create_database(DatabaseInput = {'Name': 'clinical_trial'})
except gluec.exceptions.AlreadyExistsException:
    print('The clinical_trial database already exists in the Glue data catalog')

# Compound Libraries
try:
    gluec.create_database(DatabaseInput = {'Name': 'compound_libraries'})
except gluec.exceptions.AlreadyExistsException:
    print('The compound_libraries database already exists in the Glue data catalog')
  
# High-throughput Screening Libraries
try:
    gluec.create_database(DatabaseInput = {'Name': 'high_throughput_screening_libraries'})
except gluec.exceptions.AlreadyExistsException:
    print('The high_throughput_screening_libraries database already exists in the Glue data catalog')
    
#
# 7. Data LakeFormation premissions to crawler IAM role
#

lfc = boto3.client('lakeformation')

# Premissions on S3 bucket
data_lake_principal = {'DataLakePrincipalIdentifier': IAMRoleARN}
resource = {'DataLocation': {'ResourceArn': s3_bucket_arn}}
permissions = ['DATA_LOCATION_ACCESS']

lfc.grant_permissions(
    Principal = data_lake_principal,
    Resource = resource,
    Permissions = permissions
)

# CREATE_TABLE on clinical_trial
data_lake_principal = {'DataLakePrincipalIdentifier': IAMRoleARN}
resource = {'Database': {'Name': 'clinical_trial'}}
permissions = ['CREATE_TABLE']

lfc.grant_permissions(
    Principal = data_lake_principal,
    Resource = resource,
    Permissions = permissions
)

# CREATE_TABLE on compound_libraries
data_lake_principal = {'DataLakePrincipalIdentifier': IAMRoleARN}
resource = {'Database': {'Name': 'compound_libraries'}}
permissions = ['CREATE_TABLE']

lfc.grant_permissions(
    Principal = data_lake_principal,
    Resource = resource,
    Permissions = permissions
)

# CREATE_TABLE on high_throughput_screening_libraries
data_lake_principal = {'DataLakePrincipalIdentifier': IAMRoleARN}
resource = {'Database': {'Name': 'high_throughput_screening_libraries'}}
permissions = ['CREATE_TABLE']

lfc.grant_permissions(
    Principal = data_lake_principal,
    Resource = resource,
    Permissions = permissions
)

#
# 8. Create Glue crawlers
#

gluec = boto3.client('glue')

# Clinical Trial Crawler
try:
    gluec.create_crawler(
        Name = 'Clinical Trial Crawler',
        Role = IAMRoleARN,
        DatabaseName = 'clinical_trial',
        Targets = {'S3Targets': [{'Path': 's3://' + s3_bucket_name + '/Clinical_Trial/'}]}
    )
except gluec.exceptions.AlreadyExistsException:
    print('Crawler Clinical Trial Crawler already exists')

# Compound Libraries Crawler
try:
    gluec.create_crawler(
        Name = 'Compound Libraries Crawler',
        Role = IAMRoleARN,
        DatabaseName = 'compound_libraries',
        Targets = {'S3Targets': [{'Path': 's3://' + s3_bucket_name + '/Compound_Libraries/'}]}
    )
except gluec.exceptions.AlreadyExistsException:
    print('Crawler Compound Libraries Crawler already exists')

# High-Throughput Screening Crawler
try:
    gluec.create_crawler(
        Name = 'High-Throughput Screening Crawler',
        Role = IAMRoleARN,
        DatabaseName = 'high_throughput_screening_libraries',
        Targets = {'S3Targets': [{'Path': 's3://' + s3_bucket_name + '/High-Throughput_Screening/'}]}
    )
except gluec.exceptions.AlreadyExistsException:
    print('Crawler High-Throughput Screening Crawler already exists')

#
# 9. Run Glue Crawlers
#

gluec = boto3.client('glue')

# Clinical Trial Crawler
try:
    gluec.start_crawler(Name = 'Clinical Trial Crawler')
except Exception as e:
    print(e)

# Compound Libraries Crawler
try:
    gluec.start_crawler(Name = 'Compound Libraries Crawler')
except Exception as e:
    print(e)
    
# High-Throughput Screening Crawler
try:
    gluec.start_crawler(Name = 'High-Throughput Screening Crawler')
except Exception as e:
    print(e)
