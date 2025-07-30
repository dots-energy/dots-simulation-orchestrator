# Introduction
A simulation framework to model energy systems described in [ESDL](https://energytransition.gitbook.io/esdl/). The framework allows for independent development of calculation services for specific energy objects or services (e.g. PV panel, battery, EV, weather prediction, DSO). The simulations are run on a (cloud) cluster, the results are stored in an [influxdb](https://www.influxdata.com/) database which can be analyzed and viewed online using [grafana](https://grafana.com/), see the component diagram below.  
![dots component diagram](https://github.com/EES-TUe/dots-simulation-orchestrator/blob/main/docs/images/static/dots_go-e_component_diagram.png)

## Repositories
The following repositories are used:
- [Simulation Orchestrator](https://github.com/dots-energy/dots-simulation-orchestrator/): Start and manage simulations and calculation service models via a REST API (_[FastAPI](https://fastapi.tiangolo.com/)_, _[pyESDL](https://pypi.org/project/pyESDL/)_)
- [Dots Infrastructure](https://github.com/dots-energy/dots-infrastructure): python package that contains code to set up a calculation service and integrate into the Dots [helics federation](https://docs.helics.org/en/latest/user-guide/fundamental_topics/helics_terminology.html).
- [Calculation Service Template](https://github.com/dots-energy/Dots-calculation-service-template): Create calculation a calculation service by creating a new repository using this Github Template.
- [Dots Examples](https://github.com/dots-energy/dots-examples): A repository containing example ESDL files and example post requests to try out and see the full capabilities of DOTs.
- [Calculation service repositories](https://github.com/dots-energy-services/): Calculation service repositories for different energy components (from 'Calculation Service' template). 
Each repository contains a README with more information.

## Terminology
- **calculation service**: a code repository containing calculation logic aimed at a specific energy (ESDL) object, for instance a PV installation, battery or heat pump. Alternatively there are general services, for instance a weather service or aggregator.
- **calculation model**: a running instance of a calculation service, created from a docker image in the service repository. Multiple models can exist for a single service, set in the calculation service definition.
- **calculation service definition**: describes which calculation service is used with which ESDL object type. And the calculation service docker image url (on dockerhub) and number of models (each model runs in a separate container).

## Calculation flow
What happens when a simulation is started is described in a detailed the sequence diagram below:
![dots sequence diagram](../images/static/dots_go-e_sequence_diagram.png?raw=true)