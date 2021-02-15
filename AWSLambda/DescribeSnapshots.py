import boto3, json
from datetime import datetime
from datetime import timedelta
session = boto3.Session(profile_name='development')
east = 'us-east-1'
west = 'us-west-2'
ec2East = session.client('ec2', region_name = east)
ec2Resource = session.resource('ec2', region_name=east)
# dt_now = datetime.now()
# print("Current time is: ", dt_now)
UTC_Time = datetime.now() + timedelta(hours=6)
print("UTC corrected time is: ", UTC_Time)

response = ec2East.describe_snapshots(OwnerIds=['459455538052'])


for i in response['Snapshots']:
    # print(type(i['StartTime']))
    date = i['StartTime']
    StartT = date.replace(tzinfo=None) # to get rid of naive time; otherwise python cannot subtract times. 
    delta= UTC_Time - StartT
    age = delta.days
    print("--------------")
    
    
    
    # for j in i['Tags']:
    #     a = j.get('Retention')
    #     if age >= a:
    #         ec2East.delete_snapshot(SnapshotId=i['SnapshotId'])
    # the above operation did not work because of Tags issue. i could not get the value of Retention.

    if age >= 3:
        ec2East.delete_snapshot(SnapshotId=i['SnapshotId'])


