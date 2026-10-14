## Лабораторна №4 — Helm

Helm-чарт розташований у `helm/task-manager/`. Він параметризує Deployment/Service для backend і frontend, PostgreSQL, ConfigMap, Secret, PVC та необов'язковий Ingress.

- `Chart.yaml`: `version` — версія чарта; `appVersion` — версія застосунку.
- `values.yaml` — значення за замовчуванням; `values-dev.yaml` і `values-prod.yaml` задають параметри середовищ.
- Значення можна перевизначити файлом `-f`; `--set` має вищий пріоритет за `-f`.
- Helm зберігає історію релізів у Kubernetes Secrets (мітка `owner=helm`).

Приклад встановлення:
```powershell
helm upgrade --install task-manager .\helm\task-manager -n devops-task-manager --create-namespace -f .\helm\task-manager\values-dev.yaml --set secret.postgresPassword='local-demo-only'
```
