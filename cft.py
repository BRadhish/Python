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
     
     
 ----------------------
 
 
 
 from __future__ import division, print_function, unicode_literals
from datetime import datetime
import json
import re
import boto3
import botocore

cf = boto3.client('cloudformation')
sns = boto3.client('sns')
ml = boto3.client('medialive')

def lambda_handler(event, context):
 	for record in event['Records']:
 		message = record['Sns']['Message']
 	data = json.loads(message)
 	stack_name = data.get("stackname")
 	template = json.dumps(data.get("template"))
 	parameter = json.dumps(data.get("parameter"))
 	action = data.get("action")
 	if stack_name !=None and action !=None:
 	    main_start_stop_ml(stack_name,action)
 	elif stack_name !=None and template !=None and action !=None and parameter !=None:
 	    main_cft_create_delete(stack_name,template,action,parameter)

def main_start_stop_ml(stack_name,action):
    channel_id=channel_describe(Stack_name)
    if action.lower() == "start":
 	    start_channel(channel_id)
    elif action.lower() == "stop":
 	    stop_channel(channel_id)
 	    
def main_cft_create_delete(stack_name,template,parameter,action):
 	if action.lower() == "create":
 	    main_cft(stack_name,template,parameter,action)
 	    publish_message()
 	elif action.lower() == "update":
 	    main_cft(stack_name,template,parameter,action)
 	elif action.lower() == "delete":
 	    delete_cfn(stack_name)
 	
 	    
def main_cft(stack_name, template,parameter,action):
 	    for record in event['Records']:
 		    message = record['Sns']['Message']
 	    data = json.loads(message)
 	    stack_name = data.get("stackname")
 	    template = json.dumps(data.get("template"))
 	    parameter = json.dumps(data.get("parameter"))
 	    action = data.get("action")
 	    if stack_name !=None and action !=None:
 	        main_start_stop_ml(stack_name,action)
 	    elif stack_name !=None and template !=None and action !=None and parameter !=None:
 	        main_cft_create_delete(stack_name,template,parameter,action)

def main_start_stop_ml(stack_name,action):
    channel_id=channel_describe(Stack_name)
    if action.lower() == "start":
 	    start_channel(channel_id)
    elif action.lower() == "stop":
 	    stop_channel(channel_id)
 	    
def main_cft(stack_name,template,parameter,action):
 	if action.lower() == "create":
 	    main(stack_name,template,parameter)
 	    publish_message()
 	elif action.lower() == "update":
 	    main(stack_name,template,parameter)
 	elif action.lower() == "delete":
 	    delete_cfn(stack_name)
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
        
def publish_message():

    # print("Received event: " + json.dumps(event, indent=2))
    # sns_arn = 'arn:aws:sns:ap-south-1:515935806825:errorlambdanotification'
    # sns_event = event
    # sns_event["default"] = json.dumps(event)
    try:
        sns.publish(
            TargetArn="arn:aws:sns:ap-south-1:515935806825:errorlambdanotification",
            # Message=json.dumps(sns_event),
            #MessageStructure='json',
            Subject="CFT creation status",
            #PhoneNumber='8681822092'
            Message="Cloud Formation template has been completed"
            
        )
    except Exception as e:
        print(e)
        raise e
def start_channel(channel_id):
    try:
        response = ml.start_channel(ChannelId = channel_id)

        #print("Status code: ", response["ResponseMetadata"]["HTTPStatusCode"])
        print("channel id {}", response["State"]).format(channel_id)
        return "SUCCESS"
    except:
        return "ERROR" 

def stop_channel(channel_id):
    try:
        response = ml.stop_channel(ChannelId = channel_id)
        print(response["State"])
        #print("Status code: ", response["ResponseMetadata"]["HTTPStatusCode"])
        return "SUCCESS"
    except:
        return "ERROR" 

def channel_describe(stack_name):
    try:
        response = cf.describe_stack_resources(StackName = stack_name)
        for resource_list in response["StackResources"]:
            channel_id = resource_list["PhysicalResourceId"]
        return channel_id
    except:
        return "ERROR"
