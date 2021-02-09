import boto3, json
session = boto3.Session(profile_name='development')
east = 'us-east-1'
west = 'us-west-2'
ec2East = session.client('ec2', region_name = east)
def getEC2withTags():
    ec2IDs = []
    response = ec2East.describe_instances(
        Filters=[
            {
                'Name': 'tag:TechnicalTeam',
                'Values': [
                    'DevOps',
                ]
            },
        ],
    )
    print(response)
getEC2withTags()