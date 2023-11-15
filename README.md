# DataZone Demonstration

1. Launch the CloudFormation stack

[![Launch CloudFormation Stack](https://sharkech-public.s3.amazonaws.com/misc-public/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home#/stacks/new?stackName=data-zone&templateURL=https://sharkech-public.s3.amazonaws.com/misc-public/0_datazone_cloudformation.yaml)

2. Run the following from the terminal of the [Cloud9](https://us-east-1.console.aws.amazon.com/cloud9control/home) environment that was deployed by the CloudFormation stack 

```pip install boto3```

```python DataZone_Demo/1_lakeformation_s3_configuration.py```

3. Deploy a DataZone domain from the AWS console

* Navigate to the [DataZone](https://us-east-1.console.aws.amazon.com/datazone/home) home page. Click on **Create domain**
* Provide a name for the domain
* Select the check mark next to the *Set-up this account for data consumption and publishing* under the Quick setup section

<img width="800" alt="cat_indicies_1" src="https://github.com/ev2900/DataZone_Demo/blob/main/README/quick_setup.png">

4. Run the following from the terminal of the [Cloud9](https://us-east-1.console.aws.amazon.com/cloud9control/home) environment

```python DataZone_Demo/2_dataZone_configuration.py```
