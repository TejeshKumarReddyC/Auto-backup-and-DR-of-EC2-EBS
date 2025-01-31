import boto3
#Author: TejeshKumarReddy
#Version: V1
#Use_case: AWS backup recovery

ec2 = boto3.client('ec2')
backup = boto3.client('backup')
BACKUP_VAULT_NAME = "Default"
INSTANCE_ID = "i-0727bae889d7b4e7a"
def lambda_handler(event, context):
    response = backup.list_recovery_points_by_backup_vault(BackupVaultName=BACKUP_VAULT_NAME)
    latest_backup = sorted(response['RecoveryPoints'], key=lambda x: x['CreationDate'],
            reverse=True)[0]
    restore_response = backup.start_restore_job(RecoveryPointArn=latest_backup['RecoveryPointArn'],Metadata={'availabilityZone': 'ap-south-1b'}, IamRoleArn="arn:aws:iam::412381766568:role/service-role/AWSBackupDefaultServiceRole")
    return {"statusCode": 200, "body": f"restoration started:{restore_response['RestoreJobId']}"}
