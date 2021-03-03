from __future__ import division, print_function, unicode_literals
from datetime import datetime
import json
import re
import boto3
import botocore

cf = boto3.client('cloudformation')  

def lambda_handler(event, context):
 	for record in event['Records']:
 		message = record['Sns']['Message']
 	data = json.loads(message)
 	
 	stack_name = data["stackname"]
 	template = json.dumps(data["template"])
 	parameter = json.dumps(data["parameter"])
 	action = data["action"]
 	
 	if action.lower() == "create":
 	    main(stack_name,template,parameter)
 	elif action.lower() == "update":
 	    main(stack_name,template,parameter)
 	elif action.lower() == "delete":
 	    delete_cfn(stack_name)
 	    
def main(stack_name, template,parameters):
    
    'Update or create stack'
    template_data = parse_template(template)
    parameter_data = json.loads(parameters)
    #delete_action =  delete_cfn(stack_name)
    params = {
        'StackName': stack_name,
        'TemplateBody': template_data,
        'Parameters': parameter_data,
        'Capabilities': ['CAPABILITY_IAM']
    }
    try:
        if stack_exists(stack_name):
            print('Updating {}'.format(stack_name))
            stack_result = cf.update_stack(**params)
            waiter = cf.get_waiter('stack_update_complete')
        else:
            print('Creating {}'.format(stack_name))
            stack_result = cf.create_stack(**params)
            waiter = cf.get_waiter('stack_create_complete')
        print("...waiting for stack to be ready...")
        waiter.wait(StackName=stack_name)
    except botocore.exceptions.ClientError as ex:
        error_message = ex.response['Error']['Message']
        if error_message == 'No updates are to be performed.':
            print("No changes")
        else:
            raise
    else:
        print(json.dumps(
            cf.describe_stacks(StackName=stack_result['StackId']),
            indent=2,
            default=json_serial
        ))

def parse_template(template):
    result_data=cf.validate_template(TemplateBody=template)
    print(result_data)
    return template

def stack_exists(stack_name):
    stacks = cf.list_stacks()['StackSummaries']
    for stack in stacks:
        if stack['StackStatus'] == 'DELETE_COMPLETE':
            continue
        if stack_name == stack['StackName']:
            return True
    return False
    
def delete_cfn(stack_name):
    try:
        response = cf.delete_stack(StackName = stack_name)
        print("Status code: ", response["ResponseMetadata"]["HTTPStatusCode"])
        return "SUCCESS"
    except:
        return "ERROR"
