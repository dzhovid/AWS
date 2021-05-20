from typing import Set
import boto3
import os
import json
import sys
from time import sleep
from botocore import endpoint
dynamo_client = boto3.client('dynamodb')
dynamo = boto3.resource("dynamodb")
route53 = boto3.client("route53")


def update_dynamo(Name, Record, Weight, Dynamo):
    try:
        resp = dynamo_client.update_item(TableName=Dynamo, Key={'Name': {'S': Name}, 'Records': {'S': Record}}, AttributeUpdates={'Weight':{'Value':{'N': str(Weight)}}})
        print("Dynamo Updated with: " + Name + " " + Record + " " + str(Weight))
    except Exception as error:
        print(error)



def update_route53_aliastarget(Name,SetID,weight,hostedzoneid,Record,TTL):
    try: 
        response = route53.change_resource_record_sets(
            HostedZoneId='Z063006017GGX7X3V0BUZ', #your own hosted zone id
            ChangeBatch={
                'Comment': 'DR event for SprintQA DevOps team apps from east to west.',
                'Changes': [
                    {
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'Name': Name,
                            'Type': 'A',
                            'SetIdentifier': SetID,
                            'Weight': weight,
                            'AliasTarget': {
                                'HostedZoneId': hostedzoneid, #aws elasticbeanstalk hosted zone id, maintained by aws 
                                'DNSName': Record,
                                'EvaluateTargetHealth': True
                            }
                        }
                    }
                ]
            }
        )
    except Exception as error:
        print(error)

#update_route53_aliastarget(Name,SetID,weight,Record,hostedzoneid)

def lambda_handler(event, context):
    failover_from =os.environ["Failover_from"]
    failover_to =os.environ["Failover_to"]
    Dynamo =os.environ["DynamoTableName"]
    table = dynamo.Table(Dynamo) #line 26 var name
    scan_response = table.scan(AttributesToGet=["Records","Name","Weight","Type","SetIdentifier","TTL"])

    for i in scan_response["Items"]:
        Weight = i["Weight"] # Weight from the table
        Type = i["Type"]
        SetID = i["SetIdentifier"]
        TTL = int(i["TTL"])
        Record = i["Records"]
        Name = i["Name"]
        

        if SetID=='2':
            app_color='blue'
        elif SetID=='1':
            app_color='green'

        if failover_from=='East' and failover_to=='West':
            print('failing over from East to West')
            if app_color=='green':
                Weight=0
                if Type == "ALIAS":
                    weight = 0 # weight from the Route53 record set 
                    hostedzoneid = "Z117KPS5GTRQ2G" #ElasticBeanstalk us-east-1 Route53 hosted zone ID
                    print("Calling Update ALIAS function")
                    print(Name)
                    update_route53_aliastarget(Name,SetID,weight,hostedzoneid,Record,TTL)
                else:
                    response = route53.change_resource_record_sets(HostedZoneId="Z063006017GGX7X3V0BUZ", # your public hosted zone id
                            ChangeBatch = {
                                "Comment" : "",
                                "Changes": [
                                    {
                                        "Action" : "UPSERT",
                                        "ResourceRecordSet" : {
                                            "Name": Name,
                                            "Type" : Type,
                                            "Weight" : 0,
                                            "TTL" : TTL,
                                            "SetIdentifier": SetID,
                                            "ResourceRecords":[{"Value":Record}]
                                            }
                                        }
                                    ]
                                }
                            )
                update_dynamo(Name, Record, Weight, Dynamo)
            elif app_color=='blue':
                Weight=1
                if Type == "ALIAS":
                    weight = 1 # weight from the Route53 record set 
                    hostedzoneid = "Z38NKT9BP95V3O" #ElasticBeanstalk us-west-2 Route53 hosted zone ID
                    print("Calling Update ALIAS function")
                    print(Name)
                    update_route53_aliastarget(Name,SetID,weight,hostedzoneid,Record,TTL)
                else:
                    response = route53.change_resource_record_sets(HostedZoneId="Z063006017GGX7X3V0BUZ", # your public hosted zone id
                            ChangeBatch = {
                                "Comment" : "",
                                "Changes": [
                                    {
                                        "Action" : "UPSERT",
                                        "ResourceRecordSet" : {
                                            "Name": Name,
                                            "Type" : Type,
                                            "Weight" : 1,
                                            "TTL" : TTL,
                                            "SetIdentifier": SetID,
                                            "ResourceRecords":[{"Value":Record}]
                                            }
                                        }
                                    ]
                                }
                            )
                update_dynamo(Name, Record, Weight, Dynamo)
            else:
                pass
        elif failover_from=='West' and failover_to=='East':
            print('failing over from West to East')
            if app_color=='green':
                Weight=1
                if Type == "ALIAS":
                    weight = 1 # weight from the Route53 record set 
                    hostedzoneid = "Z117KPS5GTRQ2G" #ElasticBeanstalk us-east-1 Route53 hosted zone ID
                    print("Calling Update ALIAS function")
                    print(Name)
                    update_route53_aliastarget(Name,SetID,weight,hostedzoneid,Record,TTL)
                else:
                    response = route53.change_resource_record_sets(HostedZoneId="Z063006017GGX7X3V0BUZ", # your public hosted zone id
                            ChangeBatch = {
                                "Comment" : "",
                                "Changes": [
                                    {
                                        "Action" : "UPSERT",
                                        "ResourceRecordSet" : {
                                            "Name": Name,
                                            "Type" : Type,
                                            "Weight" : 1,
                                            "TTL" : TTL,
                                            "SetIdentifier": SetID,
                                            "ResourceRecords":[{"Value":Record}]
                                            }
                                        }
                                    ]
                                }
                            )
                update_dynamo(Name, Record, Weight, Dynamo)
            elif app_color=='blue':
                Weight=0
                if Type == "ALIAS":
                    weight = 0 # weight from the Route53 record set 
                    hostedzoneid = "Z38NKT9BP95V3O" #ElasticBeanstalk us-west-2 Route53 hosted zone ID
                    print("Calling Update ALIAS function")
                    print(Name)
                    update_route53_aliastarget(Name,SetID,weight,hostedzoneid,Record,TTL)
                else:
                    response = route53.change_resource_record_sets(HostedZoneId="Z063006017GGX7X3V0BUZ", # your public hosted zone id
                            ChangeBatch = {
                                "Comment" : "",
                                "Changes": [
                                    {
                                        "Action" : "UPSERT",
                                        "ResourceRecordSet" : {
                                            "Name": Name,
                                            "Type" : Type,
                                            "Weight" : 0,
                                            "TTL" : TTL,
                                            "SetIdentifier": SetID,
                                            "ResourceRecords":[{"Value":Record}]
                                            }
                                        }
                                    ]
                                }
                            )
                update_dynamo(Name, Record, Weight, Dynamo)
            else:
                pass

