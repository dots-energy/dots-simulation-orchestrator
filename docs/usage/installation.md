# Installation
To run a simulation a number of components needs to be up and running on Kubernetes. Secondly, docker images of the calculation services need to be available.

## Required running components
- **Simulation Orchestrator**
- **InfluxDB**: database
- **Grafana**: analytics and visualization (optional)

## Deploy on Azure Kubernetes Service
All components can be deployed on [AKS](https://learn.microsoft.com/en-us/azure/aks/). On Azure use [deploy_dots.sh](https://github.com/dots-energy/dots-simulation-orchestrator/blob/main/k8s/deploy_dots.sh) to deploy DOTS:
```bash
./deploy_dots.sh -u <user_name> -p <password> -c <context>
```
The supplied `<user_name>` and `<password>` will be used for InfluxDB and Grafana. The supplied `<context>` is the name of the context in your kube config that is connected to an azure kubernetes cluster.
This script will do the following:
- setup a cluster (on Azure or Kind) with dots namespace
- grep the kubernetes api token and put it in a k8s secret for the SO
- deploy k8s env vars and secrets containing influxdb and grafana passwords
(the default password values in env-secret-config_template.yaml should be updated for Azure)
- deploy grafana, influxdb and SO

For the SO the 'imagePullPolicy' is set to 'Always'. Furthermore, a password for the api user account `DotsUser` is generated and put in the Simulation Orchestrator container's environment variable.

## Deploy on local cluster
Alternatively a local cluster could be used for testing, for instance [kind](https://kind.sigs.k8s.io/). With kind and [kubectl](https://kubernetes.io/docs/tasks/tools/) installed run [deploy_dots.sh](https://github.com/dots-energy/dots-simulation-orchestrator/blob/main/k8s/deploy_dots.sh) but with the `-k` flag. This will result in the same steps as above but will start by creating a cluster. For more information, and a test POST body for a test simulation, see the [Simulation Orchestrator README](https://github.com/dots-energy/dots-simulation-orchestrator?tab=readme-ov-file#simulation-orchestrator-for-the-energy-system-microservices-cloud-simulator). If you are deploying the cluster locally for the first time don't forget to add the execution permission to the `deploy_dots.sh` file i.e. run `chmod +x *.sh`.