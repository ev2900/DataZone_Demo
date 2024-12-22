# DataZone Demonstration

<img width="275" alt="map-user" src="https://img.shields.io/badge/cloudformation template deployments-33-blue"> <img width="85" alt="map-user" src="https://img.shields.io/badge/views-705-green"> <img width="125" alt="map-user" src="https://img.shields.io/badge/unique visits-082-green">

This repository provides an easy deployment to set up an environment for demo'ing Amazon DataZone.

The instructions will deploy the architecture depicted in this diagram

<img width="750" alt="bulk_load" src="https://github.com/ev2900/DataZone_Demo/blob/main/README/dataZone_architecture-GitHub.png">

You can use this architecture to learn and demonstrate publishing, subscribing workflows and other aspects of DataZone.

The sample data used for this demo is fake data that represents a few data sets that may be used by a Pharmaceutical company during drug development research and clinical trials.

## Instructions to deploy the demo an in AWS account
1. Launch the CloudFormation stack

[![Launch CloudFormation Stack](https://sharkech-public.s3.amazonaws.com/misc-public/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home#/stacks/new?stackName=data-zone&templateURL=https://sharkech-public.s3.amazonaws.com/misc-public/0_datazone_cloudformation.yaml)

2. Run the following from the terminal of the [Cloud9](https://us-east-1.console.aws.amazon.com/cloud9control/home) environment that was deployed by the CloudFormation stack

```pip install boto3```

```python DataZone_Demo/1_lakeformation_s3_configuration.py```

3. Deploy a DataZone domain from the AWS console

* Navigate to the [DataZone](https://us-east-1.console.aws.amazon.com/datazone/home) home page and click on **Create domain**
* Provide a name for the domain
* Select the check mark next to the *Set-up this account for data consumption and publishing* under the Quick setup section

<img width="500" alt="quick_setup" src="https://github.com/ev2900/DataZone_Demo/blob/main/README/quick_setup_button.png">

* Click on **Create domain**

4. Update the ```datazone_domain_id``` variable in [2_dataZone_configuration.py](https://github.com/ev2900/DataZone_Demo/blob/main/2_dataZone_configuration.py) file and [3_dataZone_configuration.py](https://github.com/ev2900/DataZone_Demo/blob/main/3_dataZone_configuration.py)

To find the domain id of the DataZone domain you just deployed look at the URL for the DataZone portal

For example if the URL is https//dzd_498d049z6o1gkn.datazone.us-east-1.on.aws the domain id is dzd_498d049z6o1gkn

Once you update the variables with the domain id **save the file**

6. Run the following from the terminal of the [Cloud9](https://us-east-1.console.aws.amazon.com/cloud9control/home) environment

```python DataZone_Demo/2_dataZone_configuration.py```

```python DataZone_Demo/3_dataZone_configuration.py```
