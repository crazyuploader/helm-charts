# helm-charts

![Release Charts](https://github.com/crazyuploader/helm-charts/actions/workflows/release.yaml/badge.svg)
![Helm](https://img.shields.io/badge/helm-v4-blue)

Helm charts published to an OCI registry.

## Charts

| Chart               | Chart version | App version | Description         |
| ------------------- | ------------- | ----------- | ------------------- |
| [n8n](./charts/n8n) | 0.3.7         | 2.37.10      | Workflow automation |

## Usage

```bash
helm install <release> oci://zot.devjugal.com/helm/charts/<chart> --version <version> -f values.yaml
```

## CI

CI lints and pushes charts to the OCI registry on every push to `main` that touches `charts/**`.

Required repository secrets:

| Secret          | Value                                      |
| --------------- | ------------------------------------------ |
| `OCI_REGISTRY`  | registry hostname, e.g. `zot.devjugal.com` |
| `OCI_USERNAME`  | registry username                          |
| `OCI_PASSWORD`  | registry password                          |
| `OCI_REPO_PATH` | target path, e.g. `helm/charts`            |

## Contributing

1. Add or modify a chart under `charts/<name>/`
2. Bump `version` in `Chart.yaml`
3. Merge to `main`; CI packages and pushes automatically
