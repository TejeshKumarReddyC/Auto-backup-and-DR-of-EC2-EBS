**Workflow:-**  EC2_or_EBS ---> EventBridge --->  Lambda ---> Auto_backup(AWS_Backup) ---> If_backup_fails_send_notification(SNS).

-->**Introduction:**
In this project whenever an **EC2** instance's is powered on or powered off then it triggers the **LAMBDA** via **EVENTBRIDGE**. That **LAMBDA_function** starts the backup job in **AWS_BACKUP_VAULT**, if backup job is failed then an alert will be sent by the **SNS**.
