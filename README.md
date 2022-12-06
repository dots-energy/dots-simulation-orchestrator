# DOTS Simulation Orchestrator

Build for GO-e WP3
This simulation orchestrator is controlled by api calls (FastAPI) and communicates with the Model Services
Orchestrator (MSO) via MQTT protobuf messages.

To use the simulation infrastructure, see the *Usage* section. To test the infrastructure locally, see the section *Test on local cluster*.

## Usage

If the DOTS infrastructure is up and running (on Azure) the following two steps are needed to run a simulation:

### Create Calculation Services

The DOTS [Calculation Service Generator](https://ci.tno.nl/gitlab/dots/calculation-service-generator) can be used to create template calculation service projects, with a
readme on how to develop and deploy the project when it is ready for testing.

### Start Simulation POST request

Fill in a simulation `POST` request on the `/api/v1/simulation/` endpoint with an ESDL file using the [Simulation Orchestrator API](localhost:8001/docs) (see [example POST body](#run-test-simulation)
below).

### Viewing results

The logs can be viewed in [Lens](#lens-model-service-calculation-logs) after connecting to the Kubernetes backplane.
The database results can be viewed using [InfluxDB Studio](#InfluxDB Studio) or [Grafana](#Grafana) after connecting to the InfluxDB instance.

## Deploy on Kubernetes
With Kubernetes up and running, in bash window from `k8s` folder, run:  
`./deploy_dots.sh`

## Test on local cluster

Several components need to be up and running for local test deployment:

For running a simulation:

- MQTT client (Mosquitto)
- InfluxDB
- Local Kind cluster
- DOTS Model Services Orchestrator (MSO)
- DOTS Calculation Services
- DOTS Simulation Orchestrator

For viewing the results:

- Lens Desktop
- InfluxDB Studio
- Grafana

These can be setup by the steps below.

### Model Services Orchestrator repository

https://ci.tno.nl/gitlab/dots/model-services-orchestrator  
In the model services orchestrator repository readme, follow the 'Quickstart' section, until and including the 'Start
Mosquitto and the MSO itself' section.  
Now the Kind cluster, MSO and Mosquitto client should be up and running

### Calculation Service Generator repository

https://ci.tno.nl/gitlab/dots/calculation-service-generator

Create three calculation services with the Calculation Service Generator by using config files from the service template. Run the following command in the root folder of the calculation-service-generator from the WSL/Ubuntu terminal with admin/root privileges. This will generate the services in the root folder of the Calculation Service Generator.

```console
./build.sh -c ./test_dev/test_service_configs/test1_battery_service.yaml
./build.sh -c ./test_dev/test_service_configs/test1_pvpanel_service.yaml
./build.sh -c ./test_dev/test_service_configs/test1_system_service.yaml
```

This creates a project folder for each calculation service.  
Optionally: test the services locally by following the readme in the newly created projects.

In each project follow the 'Deployment - For local simulation testing' section.

Now the docker images for the calculation services should be loaded on the Kind cluster.

### Simulation Orchestrator (this repository)

Copy the .env.template file and start the components:

```console
copy .env.template .env
docker compose --file ./docker-compose.local.yml up --build
```

Now InfluxDB, Grafana and the Simulation Orchestrator should be up and running

### Run Test Simulation

Go to localhost:8001/docs  
'Try it out': POST '/api/v1/simulation/' with the following json body:

```json
{
  "name": "test1 simulation",
  "start_date": "2023-01-25 00:00:00",
  "time_step_seconds": 3600,
  "nr_of_time_steps": 24,
  "keep_logs_hours": 0.05,
  "log_level": "debug",
  "calculation_services": [
    {
      "esdl_type": "EnergySystem",
      "calc_service_name": "system_service",
      "service_image_url": "system_service:0.0.1"
    },
    {
      "esdl_type": "PVPanel",
      "calc_service_name": "pv_panel_service",
      "service_image_url": "pv_panel_service:0.0.1"
    },
    {
      "esdl_type": "Battery",
      "calc_service_name": "battery_service",
      "service_image_url": "battery_service:0.0.1"
    }
  ],
  "esdl_base64string": "PD94bWwgdmVyc2lvbj0nMS4wJyBlbmNvZGluZz0nVVRGLTgnPz4NCjxlc2RsOkVuZXJneVN5c3RlbSB4bWxuczp4c2k9Imh0dHA6Ly93d3cudzMub3JnLzIwMDEvWE1MU2NoZW1hLWluc3RhbmNlIiB4bWxuczplc2RsPSJodHRwOi8vd3d3LnRuby5ubC9lc2RsIg0KICAgICAgICAgICAgICAgICAgIG5hbWU9IkVuZXJneVN5c3RlbSIgaWQ9IjEyMjBhYTA2LWE5MWMtNDM4Ni1iYjI0LTFlNzZlNGQ1MmEzOCINCiAgICAgICAgICAgICAgICAgICBkZXNjcmlwdGlvbj0iU2NyaXB0ZWQgdmVyc2lvbiBvZiBmaXJzdF9FU0RMX0dPZSI+DQogICAgPGluc3RhbmNlIHhzaTp0eXBlPSJlc2RsOkluc3RhbmNlIiBpZD0iaW5zdGFuY2VfaWQiIG5hbWU9Imluc3RhbmNlIj4NCiAgICAgICAgPGFyZWEgeHNpOnR5cGU9ImVzZGw6QXJlYSIgaWQ9ImFyZWFfaWQiIG5hbWU9ImFyZWFfdGl0bGUiPg0KICAgICAgICAgICAgPGFzc2V0IHhzaTp0eXBlPSJlc2RsOkJhdHRlcnkiIGlkPSI0YmViZDhiZC0zYjFiLTQ1MjAtOWQ0Ni1lNTFmYmJkOTEyMjkiIGNoYXJnZUVmZmljaWVuY3k9IjAuOTgiDQogICAgICAgICAgICAgICAgICAgbmFtZT0iYmF0dGVyeTEiIG1heERpc2NoYXJnZVJhdGU9IjUwMDAuMCIgbWF4Q2hhcmdlUmF0ZT0iNTAwMC4wIiBkaXNjaGFyZ2VFZmZpY2llbmN5PSIwLjk4Ig0KICAgICAgICAgICAgICAgICAgIGZpbGxMZXZlbD0iNTAuMCIgY2FwYWNpdHk9IjM2MDAwMDAwLjAiPg0KICAgICAgICAgICAgICAgIDxwb3J0IHhzaTp0eXBlPSJlc2RsOkluUG9ydCIgY2Fycmllcj0iY2Fycmllcl9pZCIgaWQ9Im1vZGVsX2lucG9ydDFfaWQiDQogICAgICAgICAgICAgICAgICAgICAgY29ubmVjdGVkVG89IjEzMjczMWMyLThkNDctNGNkOC1hOWIyLTc5MjE0ODk2ZTYyMCIvPg0KICAgICAgICAgICAgICAgIDxnZW9tZXRyeSB4c2k6dHlwZT0iZXNkbDpQb2ludCIgbG9uPSI1LjMyNjgyNDE4ODIzMjQyMiIgbGF0PSI1MS40NDQzNzg2Mzc0NDk0MDQiLz4NCiAgICAgICAgICAgIDwvYXNzZXQ+DQogICAgICAgICAgICA8YXNzZXQgeHNpOnR5cGU9ImVzZGw6UFZQYW5lbCIgaWQ9Ijg1NzYwZWVkLTBjOWMtNDA5Mi04ZGQxLWVlMGFiODIyOTU0ZiIgcGFuZWxFZmZpY2llbmN5PSIwLjIiDQogICAgICAgICAgICAgICAgICAgcG93ZXI9IjEwMDAuMCIgbmFtZT0icHYtcGFuZWwxIj4NCiAgICAgICAgICAgICAgICA8cG9ydCB4c2k6dHlwZT0iZXNkbDpPdXRQb3J0IiBjYXJyaWVyPSJjYXJyaWVyX2lkIg0KICAgICAgICAgICAgICAgICAgICAgIGlkPSIxMzI3MzFjMi04ZDQ3LTRjZDgtYTliMi03OTIxNDg5NmU2MjAiIGNvbm5lY3RlZFRvPSJtb2RlbF9pbnBvcnQxX2lkIi8+DQogICAgICAgICAgICAgICAgPGdlb21ldHJ5IHhzaTp0eXBlPSJlc2RsOlBvaW50IiBsb249IjUuMzI1NTQ3NDU2NzQxMzM0IiBsYXQ9IjUxLjQ0NTIzNDU2NjEyMjYxNSIvPg0KICAgICAgICAgICAgPC9hc3NldD4NCg0KICAgICAgICA8L2FyZWE+DQogICAgPC9pbnN0YW5jZT4NCiAgICA8ZW5lcmd5U3lzdGVtSW5mb3JtYXRpb24geHNpOnR5cGU9ImVzZGw6RW5lcmd5U3lzdGVtSW5mb3JtYXRpb24iIGlkPSIyYjU5N2I5My1lMmY5LTRjYmYtYTgyNy1iY2ZkODcxZmYzM2YiPg0KICAgICAgICA8Y2FycmllcnMgeHNpOnR5cGU9ImVzZGw6Q2FycmllcnMiIGlkPSJkMjYwZDVhMC1jNTQ3LTRkNDYtODI5Yi00YjI0OGIwZDUyZWEiPg0KICAgICAgICAgICAgPGNhcnJpZXIgeHNpOnR5cGU9ImVzZGw6RWxlY3RyaWNpdHlDb21tb2RpdHkiIG5hbWU9IkVsZWN0cmljaXR5IiBpZD0iY2Fycmllcl9pZCIvPg0KICAgICAgICA8L2NhcnJpZXJzPg0KICAgIDwvZW5lcmd5U3lzdGVtSW5mb3JtYXRpb24+DQo8L2VzZGw6RW5lcmd5U3lzdGVtPg0K"
}
```

### View Results

#### Lens: model service calculation logs

Install Lens Desktop (https://docs.k8slens.dev/main/#download-lens-desktop).
To view the logs from the calculation services, go to the cluster, Workloads, Pods.
The output is quite boring since nothing is done in the calculations, but it shows the data flow and the order of the
calculations. The log level is set be the POST json body.

#### InfluxDB Studio

The database entries can be viewed using InfluxDB studio (https://github.com/CymaticLabs/InfluxDBStudio/releases,
Assets).

#### Grafana

The data from the influxdb can also viewed using grafana, go to http://localhost:3000 and login with admin, admin.

## Development

Create a python virtual environment (3.10) and install the dependencies:

```console
pip-compile ./requirements.in --output-file ./requirements.txt
python -m pip install -r requirements.txt
```
