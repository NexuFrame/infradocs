# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in InfraDocs Generator, please report it responsibly.

**Please do NOT open a public issue for security vulnerabilities.**

Instead, email us directly at: **security@infradocs.io**

We will:
- Acknowledge receipt within 48 hours
- Investigate and provide updates on our progress
- Coordinate disclosure once the issue is resolved

## Security Considerations

InfraDocs Generator processes local data files and generates static HTML output. It does not:
- Connect to external services
- Store data in the cloud
- Require internet connectivity

However, please be aware that:
- Generated HTML files may contain sensitive infrastructure data
- Keep output directories secure and restrict access appropriately
- Do not commit generated output to public repositories
