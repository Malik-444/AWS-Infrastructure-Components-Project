# Secure Static Website on AWS

<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/1266f9be-2eb4-4306-bf07-004d13b72e2e" />

## Project Overview

This project demonstrates how to host a **secure static website** on AWS using S3, CloudFront, Route 53, and WAF, with **automated security monitoring and CI/CD pipelines**. It’s fully modular and educational, supporting both **Terraform automation** and **manual AWS setup**.

## Key Features

- **Static Website Hosting**
  - S3 for storing website files
  - CloudFront for global distribution and caching
  - Route 53 for DNS management
  - WAF for protecting against web attacks

- **Automated Security Monitoring**
  - GuardDuty detects suspicious activity
  - EventBridge filters findings and triggers actions
  - Lambda functions perform automated remediation
  - SNS sends alerts to security teams

- **CI/CD Pipeline**
  - CodePipeline and CodeBuild automate deployments
  - Integration with GitHub or CodeCommit
  - Optional security scans and notifications

- **Detection and Infrastructure as Code**
  - Terraform examples for S3, CloudFront, WAF, GuardDuty, Lambda, SNS, and CI/CD
  - Optional manual setup guides included for learning purposes

## Architecture Overview

The architecture integrates security, deployment, and hosting components to provide a **robust, enterprise-ready static website solution**.

1. **User Requests:** Routed through Route 53 → CloudFront
2. **CloudFront + WAF:** Delivers content and blocks malicious traffic
3. **S3 Bucket:** Stores website files securely
4. **Security Monitoring:** GuardDuty detects threats → EventBridge filters → Lambda remediates → SNS alerts
5. **CI/CD Pipeline:** Automates website updates and deployment


## How the Components Complement Each Other

- **CloudFront + WAF:** Protects globally from web attacks
- **GuardDuty + Lambda + SNS:** Detects and remediates threats automatically
- **CI/CD Pipeline:** Ensures updates are deployed safely and consistently
- **Terraform:** Provides repeatable and auditable infrastructure




