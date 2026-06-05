# helm-charts

A collection of Helm charts. Charts are automatically packaged and pushed to an OCI registry on every merge to `main`.

## Charts

| Chart               | Version | App Version | Description         |
| ------------------- | ------- | ----------- | ------------------- |
| [n8n](./charts/n8n) | 0.1.0   | 2.25.4      | Workflow automation |

## Usage

```bash
helm install my-n8n oci://zot.devjugal.com/charts/n8n --version 0.1.0 -f values.yaml
```

## Contributing

1. Add or modify a chart under `charts/<name>/`
2. Bump `version` in `Chart.yaml`
3. Merge to `main` — CI packages and pushes automatically
