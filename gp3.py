import boto3
import botocore
import os 

#Author:awssteph 02/2021
#https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/monitoring-volume-modifications.html
client = boto3.client('ec2')
#get addresses
response = client.describe_volumes()

if 'DRYRUN' in os.environ:
    if os.environ['DRYRUN'] == 'False':
        DryRun = False
    elif os.environ['DRYRUN'] == 'True':
        DryRun = True
else: DryRun = True


for result in response['Volumes']:
    VolumeId = result['VolumeId']
    VolumeType = result['VolumeType']
    Size = result['Size']
    IOP = result['Iops']
    try:
        if Size < 1000 and IOP < 3000 and (VolumeType  == 'gp2' or VolumeType == 'io1'):
            modify = client.modify_volume(VolumeId=VolumeId,VolumeType='gp3', DryRun=DryRun)
            print(f"{VolumeId} chnaged to gp3")
        else: 
            print(f"{VolumeId} does not fit criteria")
    except botocore.exceptions.ClientError as error:
        print(error)