**Workflow:-**  EC2_or_EBS ---> EventBridge --->  Lambda ---> Auto_backup(AWS_Backup) ---> If_backup_fails_send_notification(SNS).

-->**Introduction:**
In this project whenever an **EC2** instance is powered on or powered off then it triggers the **LAMBDA** via **EVENTBRIDGE**. That **LAMBDA_function** starts the backup job in **AWS_BACKUP_VAULT**, if backup job is failed then an alert will be sent by the **SNS**.

-->**Configurations:**

I. Launch an **EC2** instance.
II. Create a **EVENTBUS** and create a **rule** with the below pattern in that eventbus.
    Note: Replace the instance_id with yours.
    {
  "source": ["aws.ec2"],
  "detail-type": ["EC2 Instance State-change Notification"],
  "detail": {
    "state": ["stopped", "running"],
    "instance-id": ["i-0727bae889d7b4e7a"]
  }
}


III. Create an **SNS_TOPIC** and subscribe to that with the email.
IV. Create a **LAMBDA_FUNCTION** .
V. Create the backup vault in **AWS_BACKUP**.
