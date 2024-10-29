#!/bin/bash

# Setup cluster
kubectl apply -f ./cluster-config.yaml
# Set master node also to be a worker node
kubectl label nodes --overwrite aks-agentpool-12841752-vmss000000 type=worker

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

echo ""
echo "Copy kube api token to secret"
rm -f env-secret-config.yaml
cp env-secret-config_template.yaml env-secret-config.yaml
kube_api_token_base64=$(echo -n ${kube_api_token} | base64 -w0)
sed -i -e "s/<<KUBE_API_TOKEN>/${kube_api_token_base64}/g" env-secret-config.yaml

echo ""
echo "Deploy env vars, secrets and config ..."
sleep 2
kubectl apply -f env-secret-config.yaml

echo ""
echo "Deploy grafana, influxdb, mosquitto, dots MSO and dots SO ..."
sleep 2
kubectl apply -f grafana-deployment.yaml -f influxdb-deployment.yaml -f so-rest-deployment.yaml

echo ""
echo "Set k8s namespace to 'dots'"
kubectl config set-context --current --namespace=dots

echo ""
echo "Deploy DOTS finished"