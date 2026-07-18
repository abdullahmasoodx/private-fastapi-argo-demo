# Basic GitOps Starter: GitHub Actions + Docker Hub + Kubernetes + Argo CD

This starter project demonstrates the complete beginner GitOps flow:

1. Push application code to GitHub.
2. GitHub Actions builds a Docker image.
3. GitHub Actions pushes the image to Docker Hub.
4. GitHub Actions updates `k8s/deployment.yaml` with the new image tag.
5. Argo CD detects the Git change.
6. You manually sync the application during the first lesson.
7. Kubernetes deploys the new image.

## Project structure

```text
basic-gitops-app/
├── app/main.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .github/workflows/ci.yaml
├── k8s/
│   ├── namespace.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   └── kustomization.yaml
└── argocd/application.yaml
```

## 1. Create the Docker Hub repository

In Docker Hub, create a public repository named:

```text
basic-gitops-app
```

## 2. Create a Docker Hub access token

In Docker Hub:

```text
Account Settings
→ Personal access tokens
→ Generate new token
```

Give it Read and Write permission.

Do not use your Docker Hub account password in GitHub Actions.

## 3. Create the GitHub repository

Create this public GitHub repository:

```text
basic-gitops-app
```

The included Argo CD manifest currently uses:

```text
https://github.com/abdullahmasoodx/basic-gitops-app.git
```

Change `argocd/application.yaml` if your repository URL is different.

## 4. Add GitHub Actions secrets

Open the GitHub repository:

```text
Settings
→ Secrets and variables
→ Actions
→ New repository secret
```

Add these two repository secrets:

```text
DOCKERHUB_USERNAME
```

Value example:

```text
abdullahmasoodx
```

Add:

```text
DOCKERHUB_TOKEN
```

Its value must be your Docker Hub personal access token.

Never commit these values into the repository.

## 5. Push this project to GitHub

```bash
git init
git add .
git commit -m "Initial GitOps starter project"
git branch -M main
git remote add origin https://github.com/abdullahmasoodx/basic-gitops-app.git
git push -u origin main
```

The first push starts GitHub Actions.

Open:

```text
GitHub repository → Actions
```

Wait until the workflow is successful. It will push image tags similar to:

```text
abdullahmasoodx/basic-gitops-app:a1b2c3d
abdullahmasoodx/basic-gitops-app:latest
```

It will also commit the SHA image tag into:

```text
k8s/deployment.yaml
```

## 6. Test locally with Docker

```bash
docker build -t basic-gitops-app:local .
docker run --rm -p 8000:8000 basic-gitops-app:local
```

Open:

```text
http://localhost:8000
http://localhost:8000/health
http://localhost:8000/docs
```

## 7. Install Argo CD

Run this only if Argo CD is not installed:

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

Check Argo CD:

```bash
kubectl get pods -n argocd
```

## 8. Register the application in Argo CD

Apply the Argo CD Application manifest:

```bash
kubectl apply -f argocd/application.yaml
```

Check it:

```bash
kubectl get applications -n argocd
```

At first, it should show `OutOfSync`.

Open the Argo CD dashboard and manually click:

```text
Sync → Synchronize
```

Manual sync is intentional for this beginner lesson.

## 9. Check Kubernetes

```bash
kubectl get all -n gitops-basic
```

Check pods:

```bash
kubectl get pods -n gitops-basic
```

## 10. Access the application

```bash
kubectl port-forward service/basic-gitops-service 8080:80 -n gitops-basic
```

Open:

```text
http://localhost:8080
```

## 11. Test the GitOps flow

Change the message inside:

```text
app/main.py
```

Commit and push:

```bash
git add .
git commit -m "Update application message"
git push
```

The flow will be:

```text
Git push
→ GitHub Actions
→ Docker Hub
→ Kubernetes manifest updated in Git
→ Argo CD becomes OutOfSync
→ Manual Sync
→ Kubernetes deploys the new image
```

## Important notes

- Never store Docker Hub credentials in YAML files.
- `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` must be GitHub repository secrets.
- Git is the source of truth.
- During GitOps practice, change Kubernetes configuration in Git rather than using manual `kubectl edit`.
- If the workflow cannot push its manifest commit, check repository branch protection and GitHub Actions workflow permissions.
