# DevOps Task Manager — Kubernetes Deployment

## Опис проєкту

Цей проєкт демонструє розгортання Task Manager у Kubernetes за допомогою Minikube. Застосунок складається з frontend, backend і бази даних PostgreSQL.

Під час виконання лабораторної роботи було підготовлено Docker-образи, створено Kubernetes-маніфести, налаштовано конфігурацію та секрети, перевірено доступність застосунку, масштабування, самовідновлення Pod-ів і оновлення Deployment.

## Архітектура

Застосунок містить такі компоненти:

- **Frontend** — користувацький інтерфейс застосунку.
- **Backend** — серверна частина, яка обробляє запити.
- **PostgreSQL** — база даних для зберігання даних.
- **Kubernetes Services** — забезпечують мережевий доступ до компонентів.
- **Ingress** — ресурс для налаштування зовнішнього HTTP-доступу.
- **PersistentVolumeClaim (PVC)** — запит на постійне сховище для PostgreSQL.
- **ConfigMap** — зберігає параметри конфігурації.
- **Secret** — зберігає пароль бази даних.

Backend і frontend розгортаються по дві репліки. PostgreSQL працює з однією реплікою та використовує постійне сховище.

## Використані технології

- Docker
- Kubernetes
- Minikube
- kubectl
- Git та GitHub
- GitHub Container Registry (GHCR)
- PostgreSQL

## Docker-образи

Образи застосунку опубліковано в GitHub Container Registry.

**Backend**

- `ghcr.io/lyarmoliuk/devops_task_manager-backend:1.0.0`
- `ghcr.io/lyarmoliuk/devops_task_manager-backend:1.1.0`

**Frontend**

- `ghcr.io/lyarmoliuk/devops_task_manager-frontend:1.0.0`
- `ghcr.io/lyarmoliuk/devops_task_manager-frontend:1.1.0`

Теги версій дають змогу виконувати оновлення застосунку та повертатися до попередньої версії образу.

## Структура Kubernetes-маніфестів

Маніфести розташовані в директорії `k8s/`:

| Файл | Призначення |
|---|---|
| `00-namespace.yaml` | Створення namespace |
| `01-configmap.yaml` | Параметри конфігурації |
| `02-secret.yaml` | Секретні параметри |
| `03-postgres.yaml` | PostgreSQL і його сховище |
| `04-backend.yaml` | Backend Deployment і Service |
| `05-frontend.yaml` | Frontend Deployment і Service |
| `06-ingress.yaml` | Налаштування Ingress |

Усі ресурси застосунку розгортаються в namespace `devops-task-manager`.

## Передумови

Перед початком роботи потрібно встановити:

- Docker Desktop
- Minikube
- kubectl

Переконайтеся, що Docker Desktop запущений.

## Запуск проєкту

### 1. Запустити Minikube

У PowerShell виконайте:

```powershell
minikube start --driver=docker
```

Перевірте стан вузла:

```powershell
kubectl get nodes
```

### 2. Увімкнути необхідні доповнення

```powershell
minikube addons enable ingress
minikube addons enable metrics-server
```

Перевірте системні Pod-и:

```powershell
kubectl get pods -n kube-system
```

Перевірте доступність метрик:

```powershell
kubectl top nodes
```

### 3. Застосувати Kubernetes-маніфести

Перейдіть до кореня репозиторію та виконайте:

```powershell
kubectl apply -f k8s/
```

Перевірте ресурси в namespace:

```powershell
kubectl get all -n devops-task-manager
kubectl get pvc -n devops-task-manager
kubectl get ingress -n devops-task-manager
```

Перевірте готовність Deployment:

```powershell
kubectl rollout status deployment/backend -n devops-task-manager
kubectl rollout status deployment/frontend -n devops-task-manager
```

### 4. Перевірити Pod-и та Services

```powershell
kubectl get pods -n devops-task-manager
kubectl get services -n devops-task-manager
```

Очікуваний стан після успішного запуску:

- Backend — 2 готові репліки.
- Frontend — 2 готові репліки.
- PostgreSQL — 1 готова репліка.
- PVC PostgreSQL — стан `Bound`.

### 5. Відкрити застосунок

Для доступу до frontend через Minikube виконайте:

```powershell
minikube service frontend -n devops-task-manager
```

Minikube відкриє адресу сервісу. Якщо для доступу запускається окремий процес або тунель, залишайте відповідне вікно термінала відкритим, поки користуєтеся застосунком.

Ingress також налаштований маніфестом `06-ingress.yaml`. Фактичний спосіб доступу через Ingress залежить від його конфігурації та налаштувань Minikube.

## Конфігурація та секрети

### ConfigMap

ConfigMap `task-manager-config` містить параметри підключення до бази даних:

- `POSTGRES_DB`
- `POSTGRES_USER`
- `DB_HOST`
- `DB_PORT`

Перевірити ConfigMap можна командою:

```powershell
kubectl get configmap task-manager-config -n devops-task-manager
```

### Secret

Secret `task-manager-secret` містить пароль бази даних.

Перевірити наявність Secret, не виводячи його значення:

```powershell
kubectl get secret task-manager-secret -n devops-task-manager
```

Для реального середовища не слід зберігати справжні паролі у відкритому вигляді в репозиторії. Використовуйте безпечне керування секретами та не додавайте реальні облікові дані до Git.

## Масштабування

Збільшити кількість реплік backend до трьох:

```powershell
kubectl scale deployment/backend --replicas=3 -n devops-task-manager
```

Перевірити результат:

```powershell
kubectl get deployment backend -n devops-task-manager
```

Повернути дві репліки:

```powershell
kubectl scale deployment/backend --replicas=2 -n devops-task-manager
```

## Самовідновлення Pod-ів

Kubernetes Deployment підтримує задану кількість реплік. Якщо Pod видалити, контролер Deployment створить заміну.

Перевірити поточні Pod-и:

```powershell
kubectl get pods -n devops-task-manager
```

Для перевірки можна видалити один Pod backend:

```powershell
kubectl delete pod <POD_NAME> -n devops-task-manager
```

Замість `<POD_NAME>` потрібно вказати реальну назву Pod-а з попередньої команди.

Переконатися, що Kubernetes створив заміну:

```powershell
kubectl get pods -n devops-task-manager -w
```

Команда з `-w` продовжує відстежувати зміни; завершити її можна комбінацією `Ctrl+C`.

## Оновлення застосунку

Оновити backend до версії `1.1.0`:

```powershell
kubectl set image deployment/backend backend=ghcr.io/lyarmoliuk/devops_task_manager-backend:1.1.0 -n devops-task-manager
```

Відстежити завершення оновлення:

```powershell
kubectl rollout status deployment/backend -n devops-task-manager
```

Оновити frontend:

```powershell
kubectl set image deployment/frontend frontend=ghcr.io/lyarmoliuk/devops_task_manager-frontend:1.1.0 -n devops-task-manager
```

Перевірити Deployment-и:

```powershell
kubectl get deployments -n devops-task-manager -o wide
```

## Відкат версії

Щоб повернути backend до попередньої ревізії Deployment:

```powershell
kubectl rollout undo deployment/backend -n devops-task-manager
```

Перевірити завершення відкату:

```powershell
kubectl rollout status deployment/backend -n devops-task-manager
```

Переглянути історію змін:

```powershell
kubectl rollout history deployment/backend -n devops-task-manager
kubectl rollout history deployment/frontend -n devops-task-manager
```

Після відкату перевіряйте версію образу й узгодженість стану кластера з маніфестами в `k8s/`.

## Діагностика

### Перевірка Pod-ів

```powershell
kubectl get pods -n devops-task-manager
```

### Опис Pod-а та події

```powershell
kubectl describe pod <POD_NAME> -n devops-task-manager
```

### Перегляд логів

```powershell
kubectl logs deployment/backend -n devops-task-manager
kubectl logs deployment/frontend -n devops-task-manager
```

### Перевірка ресурсів

```powershell
kubectl top nodes
kubectl top pods -n devops-task-manager
```

Якщо Pod не запускається, перевірте його стан, Events через `kubectl describe` та логи контейнера. Для `ImagePullBackOff` окремо перевірте назву образу, тег і доступ до реєстру.

## Очищення ресурсів

Щоб видалити ресурси, створені маніфестами:

```powershell
kubectl delete -f k8s/
```

Ця команда видаляє ресурси, описані в маніфестах. Видалення PVC або інших ресурсів зі сховищем може призвести до втрати даних залежно від конфігурації сховища. Перед очищенням переконайтеся, що потрібні дані збережено.

Щоб зупинити Minikube:

```powershell
minikube stop
```

## Результат

У межах лабораторної роботи розгорнуто Task Manager у Minikube, використано окремий namespace, ConfigMap, Secret, Services, Ingress і постійне сховище для PostgreSQL. Перевірено стан Pod-ів, метрики ресурсів, масштабування, самовідновлення та механізми оновлення й відкату Deployment.
