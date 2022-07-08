#!/bin/bash

export PATH="/home/vscode/.local/bin:$PATH"

minikube start
minikube addons enable ingress

curl -Lo skaffold https://storage.googleapis.com/skaffold/releases/latest/skaffold-linux-amd64 && \
sudo install skaffold /usr/local/bin/

# helm upgrade --install ingress-nginx ingress-nginx \
#   --repo https://kubernetes.github.io/ingress-nginx \
#   --namespace ingress-nginx --create-namespace