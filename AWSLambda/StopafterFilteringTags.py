import boto3, json
#import logging
 
#setup simple logging for INFO
#logger = logging.getLogger()
#logger.setLevel(logging.INFO)
 
#define the connection
#ec2 = boto3.resource('ec2')
session = boto3.Session(profile_name='development')
east = 'us-east-1'
west = 'us-west-2'
ec2East = session.client('ec2', region_name = east) 
def getPrint():
 
   # Use the filter() method of the instances collection to retrieve
    # all running EC2 instances.
   filters = [
             {
            'Name': 'tag:TechnicalTeam',
            'Values': ['DevOps']
        },
        {
            'Name': 'instance-state-name',
            'Values': ['running']
        }
    ]
 
    #filter the instances
    #ec2 = boto3.client('ec2', region_name=region)
   instances = ec2East.instances.filter(Filters=filters)
 
    #locate all running instances
   RunningInstances = [instance.id for instance in instances]
 
    #print the instances for logging purposes
   print (RunningInstances) 
 
    #make sure there are actually instances to shut down.
   #if len(RunningInstances) > 0:
        #perform the shutdown
        #shuttingDown = ec2East.instances.filter(InstanceIds=RunningInstances).stop()
        #print shuttingDown
   #else:
    #print("Nothing to see here")
getPrint()