# Task Manager Helm chart

## Chart version vs application version

- `version` in `Chart.yaml` is the version of the Helm chart/templates (currently `0.1.0`).
- `appVersion` describes the application version packaged by default (`1.1.0`). It is informational; image tags are controlled by `backend.image.tag` and `frontend.image.tag`.

## Values

| Key | Purpose | Default |
|---|---|---|
| `backend.replicaCount` | Backend replicas | `2` |
| `backend.image.repository` / `backend.image.tag` | Backend image and version | GHCR / `1.1.0` |
| `backend.service.type` / `backend.service.port` | Backend service | `ClusterIP` / `8000` |
| `backend.resources` | Backend CPU/memory requests and limits | see `values.yaml` |
| `frontend.replicaCount` | Frontend replicas | `2` |
| `frontend.image.repository` / `frontend.image.tag` | Frontend image and version | GHCR / `1.1.0` |
| `frontend.service.type` / `frontend.service.port` | Frontend service | `NodePort` / `80` |
| `config.*` | DB host port/name/user config | see `values.yaml` |
| `secret.postgresPassword` | Demo DB password (not a real credential) | placeholder |
| `postgres.storage.enabled` / `postgres.storage.size` | PVC toggle and size | `true` / `1Gi` |
| `ingress.enabled` / `ingress.host` | Enable and configure Ingress | `false` |
| `test.enabled` | Install Helm test hook | `true` |

For real deployments, do not commit credentials. Override `secret.postgresPassword` from a secure secret manager or a local, git-ignored values file.

## Install

Ensure Minikube and the ingress addon are running if using Ingress. Install in the project namespace:

```powershell
helm upgrade --install task-manager .\helm\task-manager -n devops-task-manager --create-namespace -f .\helm\task-manager\values-dev.yaml --set secret.postgresPassword='local-demo-only'
```

Production values (example only; do not deploy production settings to a small local cluster without checking capacity):

```powershell
helm template task-manager .\helm\task-manager -n devops-task-manager -f .\helm\task-manager\values-prod.yaml
helm upgrade --install task-manager-prod .\helm\task-manager -n devops-task-manager --create-namespace -f .\helm\task-manager\values-prod.yaml --set secret.postgresPassword='local-demo-only'
```

## Validation and lifecycle

```powershell
helm lint .\helm\task-manager
helm template task-manager .\helm\task-manager -n devops-task-manager -f .\helm\task-manager\values-dev.yaml
helm diff values .\helm\task-manager\values-dev.yaml .\helm\task-manager\values-prod.yaml
helm list -n devops-task-manager
helm get values task-manager -n devops-task-manager
helm history task-manager -n devops-task-manager
helm upgrade task-manager .\helm\task-manager -n devops-task-manager -f .\helm\task-manager\values-dev.yaml --set backend.image.tag=1.0.0 --set frontend.image.tag=1.0.0 --set secret.postgresPassword='local-demo-only'
helm upgrade task-manager .\helm\task-manager -n devops-task-manager -f .\helm\task-manager\values-prod.yaml --set secret.postgresPassword='local-demo-only'
helm rollback task-manager 1 -n devops-task-manager
helm test task-manager -n devops-task-manager
helm uninstall task-manager -n devops-task-manager
```

`values.yaml` supplies defaults. Values from `-f` override defaults; if multiple `-f` files are supplied, the rightmost wins. `--set` overrides values supplied by files.

Helm stores release state in Kubernetes Secrets by default. Inspect with:

```powershell
kubectl get secrets -n devops-task-manager -l owner=helm
```

## Notes

The chart templates name resources from the Helm release, so multiple releases can coexist. The frontend image's bundled Nginx configuration must proxy API requests to the release-specific backend service (`<release>-task-manager-backend`); if it still points to `backend`, update `frontend/nginx.conf`, rebuild/push the image, and use that image tag.
