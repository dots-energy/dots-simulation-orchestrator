# Simulation Orchestrator for the Energy System Microservices Cloud Simulator

Build for GO-e WP3. Previous working name DOTS.  
This simulation orchestrator is controlled by api calls (FastAPI) and communicates with the Model Services
Orchestrator (MSO) via MQTT protobuf messages.

On the [MCS wiki](https://ci.tno.nl/gitlab/groups/dots/-/wikis/home) you can find a description of the framework along with installation and usage details.

# Development

## Python environment
Create a python virtual environment (3.10) and install the dependencies:
```console
pip install pip-tools==6.10
pip-compile ./requirements.in --output-file ./requirements.txt
python -m pip install -r requirements.txt
```

## Push image
In the `ci` folder there are two scripts to push the image to ci.tno.nl or to a local kind cluster.

## Deploy
An Azure Kubernetes cluster needs to be available, or [kind](https://kind.sigs.k8s.io/) and [kubectl](https://kubernetes.io/docs/tasks/tools/) have to to installed to use a local cluster for testing.   
In the `k8s` folder you can find the `deploy_dot_azure.sh` and `deploy_dot_kind.sh` scripts which:
- setup a cluster (on Azure or Kind) with `dots` namespace
- grep the kubernetes api token and put it in a k8s secret for the MSO
- deploy k8s env vars and secrets containing mosquitto, influxdb and grafana passwords, and ci.tno.nl token  
  (the default password values in `env-secret-config_template.yaml` should be updated for Azure)
- deploy grafana, influxdb, mosquitto, MSO and SO

For the MSO and SO the 'imagePullPolicy' is set to 'Always'.

After deployment the simulator should be ready for use, see [MCS wiki](https://ci.tno.nl/gitlab/groups/dots/-/wikis/home).