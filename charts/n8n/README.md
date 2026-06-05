# n8n

Deploys [n8n](https://n8n.io) with PostgreSQL, external task runners (JavaScript + Python), and Redis queue mode.

| Chart version | App version |
| ------------- | ----------- |
| 0.1.0         | 2.25.4      |

## Prerequisites

Create the Secret:

```bash
kubectl create secret generic n8n-secret \
  --from-literal=db_password=<pg-password> \
  --from-literal=encryption_key=<random-32-char-string> \
  --from-literal=runner_auth_token=<random-32-char-string>
```

Add `smtp_password` when `config.smtp.enabled: true`.  
Add `user_management_jwt_secret` when `config.userManagement.jwtSecretFromExistingSecret: true`.

## Minimal values

```yaml
config:
  host: n8n.example.com

database:
  host: postgres.example.com

existingSecret: n8n-secret
```

## Key values

| Key                           | Default                | Notes                                                   |
| ----------------------------- | ---------------------- | ------------------------------------------------------- |
| `config.host`                 | `""`                   | required; public hostname                               |
| `config.timezone`             | `UTC`                  | timezone for cron/schedule triggers                     |
| `config.executionsMode`       | `main`                 | set to `queue` for Redis-backed workers                 |
| `database.host`               | `""`                   | required; PostgreSQL host                               |
| `existingSecret`              | `""`                   | required; see prerequisites                             |
| `runner.enabled`              | `true`                 | deploys external task runner (JS + Python)              |
| `runner.types`                | `[javascript, python]` | drop `python` to reduce memory                          |
| `runner.python.stdlibAllow`   | `""`                   | stdlib modules for Python Code nodes; `"*"` = all       |
| `runner.python.externalAllow` | `""`                   | third-party packages for Python Code nodes; `"*"` = all |
| `config.smtp.enabled`         | `false`                | enables password reset, invites, 2FA emails             |
| `persistence.size`            | `5Gi`                  | PVC size for `/home/node/.n8n`                          |
| `config.binaryData.mode`      | `default`              | `default` (memory), `filesystem`, or `s3`               |

## Queue mode

```yaml
config:
  executionsMode: queue

queue:
  redis:
    host: redis.example.com
```

## SMTP

```yaml
config:
  smtp:
    enabled: true
    host: smtp.example.com
    port: 587
    user: user@example.com
    sender: "n8n <noreply@example.com>"
```

Add `smtp_password` to `existingSecret`.
