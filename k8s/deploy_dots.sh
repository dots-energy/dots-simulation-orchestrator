#!/bin/bash

function usage {
    echo "usage: deploy_dots [-k] [-u username] [-p password] [-c context]"
    echo "  -k            create kind cluster (optional, do not use for Azure)"
    echo "  -u username   specify username"
    echo "  -p password   specify password"
    echo "  -c context    kubectl context name to which to deploy to if -k is supplied context will be set to kind-dots-kind"
    exit 1
}

create_kind_cluster=false
# Read parameters
while getopts "hku:p:c:" opt; do
  case $opt in
    h) usage
    ;;
    k) create_kind_cluster=true
    ;;
    u) username="$OPTARG"
    ;;
    p) password="$OPTARG"
    ;;
    c) context="$OPTARG"
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
if [ -z "${context}" ] && [[ $create_kind_cluster == false ]]; then
  echo "ERROR: specify a context"
  usage
fi

username_base64=$(echo -n $username | base64)
password_base64=$(echo -n $password | base64)

if [[ $create_kind_cluster == true ]]; then
  # Start kind cluster
  context="kind-dots-kind"
  if [[ $(kind get clusters) =~ "dots-kind" ]]; then
    echo "INFO: 'dots-kind' cluster already exits."
  else
    kind create cluster --config=./kind-cluster.yaml
  fi
fi

echo setting kubectl context: $context
kubectl config use-context "$context"

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

echo ""
echo "Copy kube api token to secret"
rm -f env-secret-config.yaml
cp env-secret-config_template.yaml env-secret-config.yaml
sed -i -e "s/<<USER>>/${username_base64}/g; s/<<PASSWORD>>/${password_base64}/g" env-secret-config.yaml
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
kubectl apply -f grafana-deployment.yaml -f so-rest-deployment.yaml -f influxdb-deployment.yaml
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
