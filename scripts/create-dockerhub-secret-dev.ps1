# Run this after updating the values.
kubectl create namespace private-demo-dev --dry-run=client -o yaml | kubectl apply -f -

kubectl create secret docker-registry dockerhub-secret `
  --docker-server=https://index.docker.io/v1/ `
  --docker-username=YOUR_DOCKERHUB_USERNAME `
  --docker-password=YOUR_DOCKERHUB_TOKEN `
  --docker-email=YOUR_EMAIL@example.com `
  -n private-demo-dev
