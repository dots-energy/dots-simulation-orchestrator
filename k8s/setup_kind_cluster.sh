#!/bin/bash

# Start cluster
#kind create cluster --name kind
kind create cluster --config=./kind-cluster.yaml

echo ""
echo "Error is okay if kind cluster was already active."
echo ""

# Setup cluster
kubectl apply -f ./cluster-config.yaml
# Set master node also to be a worker node
kubectl label nodes --overwrite dots-kind-control-plane type=worker

echo ""
echo "Admin kube config should be available at ~/.kube/config."
echo ""

kube_api_token=$(kubectl describe secrets/dots-token-4zfwp --namespace dots  | grep 'token:' | awk -F' ' '{print $2}')
kube_url=$(kubectl config view | grep 'server:' | awk -F'server: ' '{print $2}')
kube_host_and_port=$(echo $kube_url | awk -F'://' '{print $2}')
kube_host=$(echo $kube_host_and_port | awk -F':' '{print $1}')
kube_port=$(echo $kube_host_and_port | awk -F':' '{print $2}')
echo ""
echo "Kubernetes env vars for .env file: "
echo ""
echo "KUBERNETES_API_TOKEN=${kube_api_token}"
echo "KUBERNETES_HOST=${kube_host}"
echo "KUBERNETES_PORT=${kube_port}"
