import boto3
import json

#Project: Auto backup and DR
#Author: TejeshKumarReddy
#Date: 31-01-2024
#Version: V1
backup_client = boto3.client('backup')
ec2_client = boto3.client('ec2')
sns_client = boto3.client('sns')

BACKUP_VAULT_NAME = "Default"
IAM_ROLE_ARN = "arn:aws:iam::412381766568:role/service-role/AWSBackupDefaultServiceRole"
SNS_TOPIC_ARN = "arn:aws:sns:ap-south-1:412381766568:myfsns"

def lambda_handler(event, context):
    try:
        instance_id = event['detail']['instance-id']
        state = event['detail']['state']
        response = ec2_client.describe_instances(InstanceIds=[instance_id])
        print(response)
        instance_arn = f"arn:aws:ec2:{response['Reservations'][0]['Instances'][0]['Placement']['AvailabilityZone'][:-1]}:{response['Reservations'][0]['Instances'][0]['OwnerId']}:instance/{instance_id}"
        if state in ["stopped","running"]:
            backup_response = backup_client.start_backup_job(BackupVaultName=BACKUP_VAULT_NAME, ResourceArn=instance_arn, IamRoleArn=IAM_ROLE_ARN, StartWindowMinutes=60, CompleteWindowMinutes=120, Lifecycle={"DeleteAfterDays": 7})
            sns_client.publish(
                    TopicArn=SNS_TOPIC_ARN,
                    Subject="AWS Backup Started",
                    Message=f"Backup started for {instance_id} due to {state} event, job ID: {backup_response['BackupJobId']}")
            return {
                    'stateCode': 200,
                    'body': f"Backup started for {instance_id} due to {state} event. Job ID: {backup_response['BackupJobId']}"
                    }
    except Exception as e:
        sns_client.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject="AWS Backup Failed",
                Message=f"Backup falied with error {str(e)}"
                )
        return {
                'statusCode': 500,
                'body': f"Error: {str(e)}"
                }
        }
