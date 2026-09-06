# Security notes

This project is an educational portfolio application, not a hardened production service.

Before exposing it to untrusted users, add:

- authentication and authorization
- rate limiting and quotas
- request and upload size limits
- malware/content scanning for uploads
- SSRF protection and egress allow-lists for web tools
- secret management
- network isolation for model serving
- managed database/vector storage with backups
- audit logging and alerting

The built-in tool registry is intentionally allow-listed and does not dynamically execute arbitrary functions.
