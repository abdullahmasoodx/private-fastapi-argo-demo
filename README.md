# Private FastAPI Argo CD Demo

This project is a learning project for:

- FastAPI
- Pytest
- Docker
- Private Docker Hub images
- Kubernetes
- Kustomize
- Argo CD GitOps
- Private GitHub repo deployment

## Flow

```text
Developer pushes code
↓
GitHub Actions runs tests
↓
Builds Docker image
↓
Pushes image to private Docker Hub repo
↓
Updates image tag in Kubernetes YAML
↓
Commits YAML change back to GitHub
↓
Argo CD detects Git change
↓
Argo CD deploys to Kubernetes
```

## Local test

```bash
pip install -r requirements.txt
pytest tests -v
uvicorn main:app --reload
```

Open:

```text
http://localhost:8000
http://localhost:8000/health
http://localhost:8000/version
```

## Docker test

```bash
docker build -t private-fastapi-argo-demo:local .
docker run -p 8000:8000 private-fastapi-argo-demo:local
```

## GitHub Secrets

Add these secrets in your private GitHub repo:

```text
DOCKERHUB_USERNAME
DOCKERHUB_TOKEN
```

The workflow uses `GITHUB_TOKEN` automatically to commit the updated image tag back to the repo.

In GitHub repo settings, make sure Actions has write permission:

```text
Settings → Actions → General → Workflow permissions → Read and write permissions
```

## Private Docker image setup

Create a private Docker Hub repository:

```text
abdullahmasoodx/private-fastapi-argo-demo
```

If you use another Docker Hub name, update:

```text
.github/workflows/gitops-ci.yml
k8s/*/deployment.yaml
```

## Kubernetes private image pull secret

Create the image pull secret in every namespace where you deploy.

Dev example:

```bash
kubectl create namespace private-demo-dev
kubectl create secret docker-registry dockerhub-secret \
  --docker-server=https://index.docker.io/v1/ \
  --docker-username=YOUR_DOCKERHUB_USERNAME \
  --docker-password=YOUR_DOCKERHUB_TOKEN \
  --docker-email=YOUR_EMAIL@example.com \
  -n private-demo-dev
```

For staging and production, create the same secret in:

```text
private-demo-staging
private-demo-production
```

## Install Argo CD

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl get pods -n argocd
```

Run UI locally:

```bash
kubectl port-forward svc/argocd-server -n argocd 8081:443
```

Open:

```text
https://localhost:8081
```

Get password on PowerShell:

```powershell
$pass = kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}"
[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($pass))
```

Username:

```text
admin
```

## Connect private GitHub repo in Argo CD

In Argo CD UI:

```text
Settings → Repositories → Connect Repo
```

Use HTTPS and GitHub Personal Access Token.

Repo URL example:

```text
https://github.com/YOUR_GITHUB_USERNAME/private-fastapi-argo-demo.git
```

## Create Argo CD application

Before applying the files, update the repo URL in:

```text
argocd/dev-app.yaml
argocd/staging-app.yaml
argocd/production-app.yaml
```

Apply dev app:

```bash
kubectl apply -f argocd/dev-app.yaml
```

Check:

```bash
kubectl get applications -n argocd
kubectl get pods -n private-demo-dev
kubectl get svc -n private-demo-dev
```

## Branch/environment flow

```text
push dev1 → update k8s/dev → Argo CD deploys dev
push main → update k8s/staging → Argo CD deploys staging
Run workflow from main → update k8s/production → Argo CD deploys production
```

## Important security notes

Do not commit:

```text
.env
kubeconfig.yaml
Test-kubeconfig.yaml
Docker tokens
GitHub tokens
```

Keep secrets in GitHub Secrets or Kubernetes Secrets.
