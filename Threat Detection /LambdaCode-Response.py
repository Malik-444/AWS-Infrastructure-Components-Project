import boto3
import json
import os
from datetime import datetime

# AWS clients
s3 = boto3.client("s3")
sns = boto3.client("sns")

# SNS topic from environment variable
SNS_TOPIC_ARN = os.environ.get("SNS_TOPIC_ARN")

def lambda_handler(event, context):
    detail = event.get("detail", {})
    finding_type = detail.get("type", "")
    severity = detail.get("severity", 0)
    region = detail.get("region", "unknown")
    account_id = detail.get("accountId", "unknown")
    description = detail.get("description", "No description provided")

    # Only handle S3 Block Public Access disabled findings
    if finding_type != "Policy:S3/BucketBlockPublicAccessDisabled":
        print(f"✅ Skipping non-S3 Block Public Access finding: {finding_type}")
        return {"status": "skipped"}

    # Remediate affected buckets
    buckets = detail.get("resource", {}).get("s3BucketDetails", [])
    remediated_buckets = []

    for bucket in buckets:
        bucket_name = bucket.get("name")
        if bucket_name:
            print(f"🔒 Re-enabling Block Public Access for bucket: {bucket_name}")
            s3.put_public_access_block(
                Bucket=bucket_name,
                PublicAccessBlockConfiguration={
                    "BlockPublicAcls": True,
                    "IgnorePublicAcls": True,
                    "BlockPublicPolicy": True,
                    "RestrictPublicBuckets": True
                }
            )
            remediated_buckets.append(bucket_name)

    # Construct emoji-enhanced SNS message
    if SNS_TOPIC_ARN and remediated_buckets:
        message = f"""
🚨 *GuardDuty Alert: S3 Block Public Access Disabled* 🚨

📅 Timestamp: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}
🏦 Account ID: {account_id}
🌍 Region: {region}
⚠️ Severity: {severity}
📝 Description: {description}

✅ Buckets Secured:
"""
        for b in remediated_buckets:
            message += f"   🔒 {b}\n"

        message += "\n🛡 Lambda auto-remediation executed successfully!"

        try:
            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject="🚨 GuardDuty Alert: S3 Block Public Access Disabled",
                Message=message
            )
            print("📧 SNS notification sent successfully.")
        except Exception as e:
            print(f"❌ Failed to send SNS notification: {e}")
    else:
        print("⚠️ No SNS_TOPIC_ARN set or no buckets remediated. Skipping SNS.")

    return {"status": "remediated", "buckets": remediated_buckets}
