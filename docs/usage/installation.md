# Installation
To run a simulation first a deploy of the DOTS platform needs to be done. This can either be local or online kubernetes cluster. Secondly, docker images of the calculation services need to be available.

## Deployment
For a deployment to a local cluster, two items need to be installed first: [kind](https://kind.sigs.k8s.io/) and [kubectl](https://kubernetes.io/docs/tasks/tools/). Installing kind and kubectl on Windows on WSL works well, other local cluster options have not been tried. For deployment to an online kubernetes cluster, the cluster needs to be configured in the kube config file and needs to have an associated context.

In the `k8s` folder of the simulation orchestrator's repository you can find the `deploy_dots.sh` scripts which will:
- set up a cluster (on Azure or Kind) with `dots` namespace
- configure a kubernetes service account for the so to deploy pods
- deploy k8s env vars and secrets containing influxdb and grafana passwords
- deploy grafana, influxdb and SO

For the SO the 'imagePullPolicy' is set to 'Always'. Furthermore, a password for the api user account `DotsUser` is generated and put in the Simulation Orchestrator container's environment variable.
 
### Deploy on Azure Kubernetes Service
All components can be deployed on [AKS](https://learn.microsoft.com/en-us/azure/aks/). On Azure use [deploy_dots.sh](https://github.com/dots-energy/dots-simulation-orchestrator/blob/main/k8s/deploy_dots.sh) to deploy DOTS:
```bash
./deploy_dots.sh -u <user_name> -p <password> -c <context>
```
The supplied `<user_name>` and `<password>` will be used for InfluxDB and Grafana. The supplied `<context>` is the name of the context in your kube config that is connected to an azure kubernetes cluster.

### Deploy on local cluster
With kind and [kubectl](https://kubernetes.io/docs/tasks/tools/) installed run [deploy_dots.sh](https://github.com/dots-energy/dots-simulation-orchestrator/blob/main/k8s/deploy_dots.sh) but with the `-k` flag. This will result in the same steps as above but will start by creating a cluster. For more information, and a test POST body for a test simulation, see the [Simulation Orchestrator README](https://github.com/dots-energy/dots-simulation-orchestrator?tab=readme-ov-file#simulation-orchestrator-for-the-energy-system-microservices-cloud-simulator). If you are deploying the cluster locally for the first time don't forget to add the execution permission to the `deploy_dots.sh` file i.e. run `chmod +x *.sh`.

After deployment the simulator should be ready for use, see [running simulations](running%20simulations.md) to get started on running the simulations.

### Local testing

There is a dummy calculation services which can be used to test the framework.
On `<SO AKS IP>:8001/docs` (<SO AKS IP> is the Simulation Orchestrator Azure IP address), or for local kind cluster
`localhost:8011/docs`, do a POST request with `test_json.json` as body.  
This should run a simulation without errors, this can be checked in [Lens](https://github.com/MuhammedKalkan/OpenLens),
make sure to also install this [extension](https://github.com/alebcay/openlens-node-pod-menu#installing-this-extension).
An example cluster with a running simulation is displayed below:  
![docs/test_simulation_lens.png](docs/test_simulation_lens.png)
The first 5 pods contain the base components which should always be running. The other pods contain calculation service
models which will be cleaned up after the simulation.