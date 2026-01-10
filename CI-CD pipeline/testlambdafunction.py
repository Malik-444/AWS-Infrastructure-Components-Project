{
  "version": "0",
  "id": "abcd1234-5678-90ef-ghij-1234567890kl",
  "detail-type": "Inspector2 Finding",
  "source": "aws.inspector2",
  "account": "123456789012",
  "time": "2026-01-10T23:00:00Z",
  "region": "us-east-1",
  "resources": [
    "arn:aws:inspector2:us-east-1:123456789012:resource/aws/codecommit/my-static-repo"
  ],
  "detail": {
    "title": "SQL Injection Vulnerability",
    "description": "A potential SQL injection was detected in your repository code.",
    "severity": "HIGH",
    "repository": "my-static-site",
    "branch": "main",
    "filePath": "app/routes/user.js",
    "lineNumber": 42,
    "recommendation": "Validate user inputs and use parameterized queries.",
    "referenceUrls": [
      "https://cwe.mitre.org/data/definitions/89.html",
      "https://docs.aws.amazon.com/inspector/latest/userguide/security-findings.html"
    ]
  }
}
