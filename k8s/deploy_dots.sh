#!/bin/bash

function usage {
    echo "usage: deploy_dots [-k] [-u username] [-p password]"
    echo "  -k            create kind cluster (optional, do not use for Azure)"
    echo "  -u username       specify username"
    echo "  -p password   specify password"
    exit 1
}

create_kind_cluster=false
# Read parameters
while getopts "hku:p:" opt; do
  case $opt in
    h) usage
    ;;
    k) create_kind_cluster=true
    ;;
    u) username="$OPTARG"
    ;;
    p) password="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    exit 1
    ;;
  esac

  case $OPTARG in
    -*) printf "Option '%s' needs a valid argument\n" "$opt"
    exit 1
    ;;
  esac
done

if [ -z "${username}" ]; then
  echo "ERROR: specify a username"
  usage
fi
if [ -z "${password}" ]; then
  echo "ERROR: specify a password"
  usage
fi

username_base64=$(echo -n $username | base64)
password_base64=$(echo -n $password | base64)

if [[ $create_kind_cluster == true ]]; then
  # Start kind cluster
  if [[ $(kind get clusters) =~ "dots-kind" ]]; then
    echo "ERROR: 'dots-kind' cluster already exits."
    exit 1
  else
    kind create cluster --config=./kind-cluster.yaml
  fi
fi

# Setup cluster
kubectl apply -f ./cluster-config.yaml
# Set master node also to be a worker node
kubectl label nodes --overwrite dots-kind-control-plane type=worker

echo ""
echo "Admin kube config should be available at ~/.kube/config."
echo ""

# Get kubernetes details
so_secret=$(openssl rand -hex 32)
so_user_pass=$(tr -dc A-Za-z0-9 </dev/urandom | head -c 13; echo)
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
sed -i -e "s/<<KUBE_API_TOKEN>>/${kube_api_token_base64}/g; s/<<USER>>/${username_base64}/g; s/<<PASSWORD>>/${password_base64}/g" env-secret-config.yaml
so_secret_base64=$(echo -n ${so_secret} | base64 -w0)
sed -i -e "s/<<SECRET_KEY>>/${so_secret_base64}/g" env-secret-config.yaml
so_user_pass_base64=$(echo -n ${so_user_pass} | base64 -w0)
sed -i -e "s/<<OAUTH_PASSWORD>>/${so_user_pass_base64}/g" env-secret-config.yaml
sleep 2

echo ""
echo "Deploy env vars, secrets and config ..."
kubectl apply -f env-secret-config.yaml
sleep 2

echo ""
echo "Deploy grafana, influxdb, mosquitto, dots MSO and dots SO ..."
kubectl apply -f grafana-deployment.yaml -f influxdb-deployment.yaml -f so-rest-deployment.yaml
sleep 2

echo ""
echo "Set k8s namespace to 'dots'"
kubectl config set-context --current --namespace=dots

rm -f env-secret-config.yaml

echo ""
echo "Credentials for InfluxDB and Grafana:"
printf "Username: '%s'\n" "$username"
printf "Password: '%s'\n" "$password"
echo "Deploy DOTS finished"
