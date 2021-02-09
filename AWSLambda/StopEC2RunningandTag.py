import boto3, json
session = boto3.Session(profile_name='development')
east = 'us-east-1'
west = 'us-west-2'
ec2East = session.client('ec2', region_name = east)
ec2 = boto3.resource('ec2')
def getEC2RunningwithTags():
    ec2IDs = []
    response = ec2East.describe_instances(
        Filters=[
            {
                'Name': 'tag:TechnicalTeam',
                'Values': [
                    'DevOps',
                ]
            },
            {
                'Name': 'instance-state-name',
                'Values': ['running']
            }
        ],
    )
    a = response['Reservations']
    for i in a:
        for j in i['Instances']:
            #print(j['InstanceId'])
            ec2IDs.append(j['InstanceId'])
    #return ec2IDs
    for k in ec2IDs:
        #print(k)
        ec2.Instance(k).stop()
getEC2RunningwithTags()
