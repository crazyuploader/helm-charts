# n8n

Deploys [n8n](https://n8n.io) with PostgreSQL, external task runners (JavaScript + Python), and Redis queue mode.

| Chart version | App version |
| ------------- | ----------- |
| 0.2.0         | 2.35.7      |

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

## AI Assistant

Enable the AI Assistant with a sandbox provider (Daytona or self-hosted n8n-sandbox-service).

### Daytona (managed, recommended for production)

```yaml
aiAssistant:
  enabled: true
  instanceAi:
    enabledModules: "instance-ai"
    modelApiKeyFromExistingSecret: true
    sandbox:
      enabled: true
      provider: daytona
      daytonaApiUrl: "https://app.daytona.io/api"
      daytonaApiKeyFromExistingSecret: true
```

Add `daytona_api_key` and `instance_ai_model_api_key` to `existingSecret`.

### Self-hosted n8n Sandbox Service

Deploy the [n8n-sandbox-service](https://github.com/n8n-io/n8n-sandbox-service/tree/main/charts/n8n-sandbox-service) chart separately, then configure:

```yaml
aiAssistant:
  enabled: true
  instanceAi:
    enabledModules: "instance-ai"
    sandbox:
      enabled: true
      provider: n8n-sandbox
      n8nSandboxServiceUrl: "http://n8n-sandbox-service-api.n8n-sandbox:8080"
      n8nSandboxServiceApiKeyFromExistingSecret: true
```

Add `n8n_sandbox_service_api_key` to `existingSecret`.

### Agents

```yaml
aiAssistant:
  enabled: true
  instanceAi:
    enabledModules: "instance-ai,agents"
  agents:
    enabled: true
    sandbox:
      enabled: true
```
