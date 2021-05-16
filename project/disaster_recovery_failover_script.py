import boto3,json
import re,sys,os,datetime
from time import sleep
session = boto3.Session(profile_name='development')
east = 'us-east-1'
west = 'us-west-2'
dynamo_client = boto3.client('dynamodb', region_name=east)
dynamo = boto3.resource("dynamodb", region_name=east)
route53 = boto3.client("route53")

# response = dynamo_client.describe_table(
#     TableName='dr_recovery'
# )
# print(response)

def update_dynamo(Name, Record, Weight, Dynamo):
    resp = dynamo_client.update_item(TableName=Dynamo, Key={'Name': {'S': Name}, 'Records': {'S': Record}}, AttributeUpdates={'Weight':{'Value':{'N': str(Weight)}}})
    print("Dynamo Updated with: " + Name + " " + Record + " " + str(Weight))