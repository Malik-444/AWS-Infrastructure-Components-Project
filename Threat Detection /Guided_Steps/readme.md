### 1️⃣ Enable GuardDuty

1. Open **AWS Console → GuardDuty**
2. Click **Enable GuardDuty**
3. Leave default settings

📸 _Screenshot: GuardDuty dashboard_

---

### 2️⃣ Create SNS Topic (Email Alerts)

1. Go to **SNS → Topics → Create topic**
2. Type: **Standard**
3. Name: `s3-security-alerts`
4. Create topic

#### Add Email Subscription

1. Click **Create subscription**
2. Protocol: `Email`
3. Endpoint: `your-email@example.com`
4. Confirm subscription from inbox

⚠️ **IMPORTANT:** Ensure there is **ONLY ONE email subscription**

📸 _Screenshot: SNS topic with one email subscription_

---

### 3️⃣ Create Lambda IAM Role

Attach this policy to the Lambda execution role:



###4️⃣ Create Lambda Function###

Runtime: Python 3.11

Role: Use the IAM role above

Environment Variable
SNS_TOPIC_ARN = arn:aws:sns:REGION:ACCOUNT_ID:s3-security-alerts




### 🧠 Lambda Function Code (Python) ###
import os
import boto3

sns_client = boto3.client("sns")
s3_client = boto3.client("s3")

SNS_TOPIC = os.environ["SNS_TOPIC_ARN"]

def lambda_handler(event, context):
    source = event.get("source", "")

    if source == "aws.guardduty":
        bucket_name = event["detail"]["resource"]["s3Bucket"]["name"]
        message = (
            "🚨 GuardDuty Alert\n\n"
            f"S3 Bucket: {bucket_name}\n"
            "Issue: Block Public Access Disabled\n\n"
            "🔧 Remediation applied"
        )
        remediate(bucket_name)
    else:
        message = "ℹ️ Lambda invoked with unknown event source"

    sns_client.publish(
        TopicArn=SNS_TOPIC,
        Subject="🚨 S3 Security Alert",
        Message=message
    )

def remediate(bucket_name):
    s3_client.put_public_access_block(
        Bucket=bucket_name,
        PublicAccessBlockConfiguration={
            "BlockPublicAcls": True,
            "IgnorePublicAcls": True,
            "BlockPublicPolicy": True,
            "RestrictPublicBuckets": True
        }
    )

### 5️⃣ Create EventBridge Rule (GuardDuty) ###

Event pattern:

{
  "source": ["aws.guardduty"],
  "detail-type": ["GuardDuty Finding"],
  "detail": {
    "type": ["Policy:S3/BucketBlockPublicAccessDisabled"]
  }
}


Target: Lambda function

No role required (EventBridge handles permissions)

### End Results ###

<img width="1504" height="324" alt="Screenshot 2026-01-08 225531" src="https://github.com/user-attachments/assets/e25d14ab-cceb-4474-b549-314f13085eb6" />

