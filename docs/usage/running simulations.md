# Running simulations
In order to run a simulation a few things are required:
* An esdl file describing your energy system
* Calculation services 
* A post request describing the simulation parameters

This page is supposed to give guidance on how to come by these elements.

## Creating an ESDL file
The first step of designing a co-simulation with DOTs is building an esdl file. The esdl file defines your whole energy system scenario. From network topology, to weather forecasts, to demand profiles. An esdl file can be created with the [ESDL map editor](https://www.esdl.nl/adviseurs.html#image1-1m) or using the [python package](https://pypi.org/project/pyESDL/) that is offered by the esdl developers. 

Now lets consider an esdl file that has the following energy system in it:

```
                                            Import             WeatherService
                                              |
                                              |
                                          Transformer
                                              |
                                              |
                ElectricityCable ---------- Joint ---------- ElectricityCable
                       |                                             |
                       |                                             |
PVInstallation -- EConnection -- PVInstallation                 EConnection -- PVInstallation
```
First, the energy system that is defined has two connections to the electricity grid (Indicated by EConnection). The two connections are connected to two and one pv panel respectively. Furthermore both connections are connected to a transformer via an electricity cable indicated by the Electricity cable type. The joint represents the connection point both cables have to the transformer. Then the object connected to the top of the transformer is an import object. This can be seen as a node that provides a source for the electricity grid. In a powerflow calculation scenario the econnections can be considered as loads, the electricity cables as lines, the joint object as nodes and the import objects as source. Finally, there is a weatherservice defined this is a time series profile for the weather data.

## Creating calculation services
In order to run a co-simulation calculation services are required that implement the behaviour of the individual entities in the energy system. In the example denoted above that would mean a calculation service for the esdl types `PVInstallation`, `EConnection`, `WeatherSrvice` and `EnergySystem` (`EnergySystem` is the esdl type denoting the electricity grid). Please refer to [calculation services](./calculation%20services.md) documentation for details on how to create calculation services.

## Starting a simulation
### Authentication
In order to make use of the api, an authentication token is required, this token can be obtained by sending a post request to the token endpoint. The username and the password should be send as form-urlencoded parameters.

![Openapi authenticate](https://github.com/dots-energy/dots-simulation-orchestrator/blob/main/docs/images/static/Authentication-token.png?raw=true)

The token in the response can then be used to authenticate with the other endpoints. The username is "DotsUser" and the password can be found with OpenLens. If you click the so-rest container and scroll to the environment section you will find the password by clicking the eye icon of the OAUTH_PASSWORD property. 
![Openapi authenticate](https://github.com/dots-energy/dots-simulation-orchestrator/blob/main/docs/images/static/lens-pwd.png?raw=true)

### Simulation API
Go to the OpenAPI of the Simulation Orchestrator which is running on: `<SO AKS IP>:8001/docs` (&lt;SO AKS IP&gt; is the Simulation Orchestrator Azure IP address), or for local kind cluster: `localhost:8011/docs`. 
First authorize yourself with button in the top right corner. The username is `DotsUser` and the password can be found in the Simulation Orchestrator container's secrets using OpenLens.
Use the POST request, see below, with an base64 encoded (without padding) ESDL file.  
![openapi POST](https://github.com/dots-energy/dots-simulation-orchestrator/blob/main/docs/images/static/openapi-start-post.png?raw=true)  
Most of the parameters in the body are self explanatory. `keep_logs_hours` is the number of hours delay after completion of a simulation. After this delay the pods will be cleaned up and the logs will no longer be accessible. 

For the calculation service paramters, the `number_of_models` sets the number pods that will be started up for that service. If a service is calculation intensive this number could be increased to allow concurrent calculation for the ESDL objects that correspond to the service. A value of `0` will create a pod per ESDL object.
Furthermore, the `esdl_type` is the esdl type that a calculation service simulates. For example, if you have a calculation service that simulates a pv panel the corresponding esdl_type = `PVInstallation`. The `service_image_url` parameter is used to specify the image url the calculation service template publishes image to this organization's image registry. The default URL is: `ghcr.io/dots-energy/$IMAGE_NAME` where `$IMAGE_NAME` should be replaced by the name of the image.

## Queue a simulation
In addition to running a single simulation, it is also possible to queue multiple simulations by doing a post request to the queue endpoint:
![openapi queue simulation](https://github.com/dots-energy/dots-simulation-orchestrator/blob/main/docs/images/static/openapi-queue-post.png?raw=true)

This will put the simulation in a FIFO queue, if the queue is empty the simulation will start directly. Whenever the queue is non empty it will be appended to the queue and start when it is its turn.

## View results
Access the InfluxDB database on `<SO AKS IP>:8086` or `localhost:8096` via [InfluxDB studio](https://github.com/CymaticLabs/InfluxDBStudio/releases) (go to Assets). Or import the database in Grafana which can be accessed on `<SO AKS IP>:3000` or `localhost:3010`. The default user and password for InfluxDB and Grafana are admin, admin. This should have been changed during cloud installation.  
[OpenLens](https://github.com/MuhammedKalkan/OpenLens), make sure to also install this [extension](https://github.com/alebcay/openlens-node-pod-menu#installing-this-extension), can be used to view the logs of the components running on the cluster, including the calculation service models. Connect to the cluster and go to: Workloads, Pods and select the 'dots' namespace, see the image below. The first 5 pods contain the required components described above. Below are the calculation service model pods, which will be cleaned up eventually.
Alternatively an export of all the simulation data can be downloaded via the api.
![Lens screenshot](https://github.com/dots-energy/dots-simulation-orchestrator/blob/main/docs/images/static/lens-screen.png?raw=true)

### Check simulation progress or terminate simulation
After a simulation POST a `simulation_id` is returned, this can be used in a GET request to get the simulation status (progress) or in a DELETE request to terminate a simulation. Additionally a list of simulations can be retrieved.  
![openapi GET DELETE GET](https://github.com/dots-energy/dots-simulation-orchestrator/blob/main/docs/images/static/openapi-get-delete-get.png?raw=true)