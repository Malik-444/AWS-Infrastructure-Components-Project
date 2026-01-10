import boto3
import os

sns = boto3.client('sns')
TOPIC_ARN = os.environ['SNS_TOPIC_ARN']
PIPELINE_NAME = os.environ['PIPELINE_NAME']

def lambda_handler(event, context):
    # Inspector finding
    finding = event['detail']
    
    # Extract details
    title = finding.get('title', 'Code Security Finding')
    severity = finding.get('severity', 'UNKNOWN')
    repo = finding.get('repository', 'N/A')
    branch = finding.get('branch', 'N/A')
    
    # Add emojis based on severity
    severity_emoji = {
        'CRITICAL': '🔥',
        'HIGH': '⚠️',
        'MEDIUM': '🔶',
        'LOW': 'ℹ️',
        'UNKNOWN': '❔'
    }.get(severity.upper(), '❔')
    
    # Custom message with emojis
    message = f"""
🚨 Amazon Inspector Alert! 🚨

Repository: 📁 {repo}
Branch: 🌿 {branch}
Severity: {severity_emoji} {severity}
Title: 📝 {title}

🔒 Manual Approval Required:

Please review the Inspector finding before approving deployment.

1️⃣ Open the pipeline in AWS Console:
   🔗 https://console.aws.amazon.com/codesuite/codepipeline/pipelines/{PIPELINE_NAME}/view
2️⃣ Locate the "Manual Approval" stage
3️⃣ Review the finding and click "✅ Approve" or "❌ Reject" to continue

Inspector Dashboard:
🔗 https://console.aws.amazon.com/inspector2/home

Thank you! 🙏
"""
    
    # Publish custom message to SNS
    sns.publish(
        TopicArn=TOPIC_ARN,
        Message=message,
        Subject=f"Inspector Alert {severity_emoji} in {repo}"
    )
