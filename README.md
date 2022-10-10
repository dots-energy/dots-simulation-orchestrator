# DOTS Simulation Orchestrator

Build for GO-e WP3
This simulation orchestrator is controlled by api calls (fastapi) and communicates with the Model Services Orchestrator (MSO) via MQTT protobuf messages.

## Development
Use Python 3.9.*  
Compile the `requirements(-dev).in` by: 
```bash
pip-compile .\requirements.in --output-file .\requirements.txt
```

## Local manual testing
Several components need to be up and running for local testing:
- Mock calculation services
- Local Kind cluster (to run Kubernetes on)  
(with loaded 'calculation service' docker images)
- MQTT client (Mosquitto)
- Model Services Orchestrator

These can be setup by the steps in the repositories below.

### Model Services Orchestrator repository
https://ci.tno.nl/gitlab/dots/model-services-orchestrator  
In the model services orchestrator repository readme in the 'Quickstart' section, follow the 'Start Kind cluster' and 'Start Mosquitto and the MSO itself' sections.  
Now the Kind cluster, MSO and Mosquitto client should be up and running

### Service Template repository
https://ci.tno.nl/gitlab/dots/service-template  
Create two mock projects by using the two mock config files in the base directory:
```bash
cookiecutter service-template --no-input --config-file .\service-template\cookiecutter_service_config_mock1.yaml -f
cookiecutter service-template --no-input --config-file .\service-template\cookiecutter_service_config_mock2.yaml -f
```
This creates a project folder for each mock service.  
Optionally: test the services locally by following the readme in the newly created projects.

In each project follow the 'Deployment - For local simulation testing' section.

Now the docker images for the mock services should loaded into the Kind cluster.

### Run Test Simulation
Run `main.py` in the root of this repository.  
Go to localhost:8001/docs  
'Try it out': POST '/api/v1/simulation/' with the following body:
```json
{
  "name": "simulation name",
  "start_date": "2023-01-25 00:00:00",
  "time_step_seconds": 3600,
  "nr_of_time_steps": 24,
  "calculation_services": [
    {
      "esdl_type": "Import",
      "calc_service_name": "mock_service1",
      "service_image_url": "mock_service1:0.0.1"
    },
    {
      "esdl_type": "ElectricityNetwork",
      "calc_service_name": "mock_service2",
      "service_image_url": "mock_service2:0.0.1"
    }
  ],
  "esdl_base64string": "PD94bWwgdmVyc2lvbj0nMS4wJyBlbmNvZGluZz0nVVRGLTgnPz4NCjxlc2RsOkVuZXJneVN5c3RlbSB4bWxuczp4c2k9Imh0dHA6Ly93d3cudzMub3JnLzIwMDEvWE1MU2NoZW1hLWluc3RhbmNlIiB4bWxuczplc2RsPSJodHRwOi8vd3d3LnRuby5ubC9lc2RsIg0KICAgICAgICAgICAgICAgICAgIG5hbWU9IkVuZXJneVN5c3RlbSIgaWQ9IjEyMjBhYTA2LWE5MWMtNDM4Ni1iYjI0LTFlNzZlNGQ1MmEzOCINCiAgICAgICAgICAgICAgICAgICBkZXNjcmlwdGlvbj0iU2NyaXB0ZWQgdmVyc2lvbiBvZiBmaXJzdF9FU0RMX0dPZSI+DQogICAgPGluc3RhbmNlIHhzaTp0eXBlPSJlc2RsOkluc3RhbmNlIiBpZD0iaW5zdGFuY2VfaWQiIG5hbWU9Imluc3RhbmNlIj4NCiAgICAgICAgPGFyZWEgeHNpOnR5cGU9ImVzZGw6QXJlYSIgaWQ9ImFyZWFfaWQiIG5hbWU9ImFyZWFfdGl0bGUiPg0KICAgICAgICAgICAgPGFzc2V0IHhzaTp0eXBlPSJlc2RsOkVsZWN0cmljaXR5TmV0d29yayIgaWQ9IjRiZWJkOGJkLTNiMWItNDUyMC05ZDQ2LWU1MWZiYmQ5MTIyOSIgdm9sdGFnZT0iMjMwLjAiIG5hbWU9Im5ldHdvcmsiPg0KICAgICAgICAgICAgICAgIDxwb3J0IHhzaTp0eXBlPSJlc2RsOkluUG9ydCIgY2Fycmllcj0iY2Fycmllcl9pZCIgaWQ9Im1vZGVsX2lucG9ydDFfaWQiDQogICAgICAgICAgICAgICAgICAgICAgY29ubmVjdGVkVG89IjEzMjczMWMyLThkNDctNGNkOC1hOWIyLTc5MjE0ODk2ZTYyMCIvPg0KICAgICAgICAgICAgICAgIDxnZW9tZXRyeSB4c2k6dHlwZT0iZXNkbDpQb2ludCIgbG9uPSI1LjMyNjgyNDE4ODIzMjQyMiIgbGF0PSI1MS40NDQzNzg2Mzc0NDk0MDQiLz4NCiAgICAgICAgICAgIDwvYXNzZXQ+DQogICAgICAgICAgICA8YXNzZXQgeHNpOnR5cGU9ImVzZGw6SW1wb3J0IiBpZD0iODU3NjBlZWQtMGM5Yy00MDkyLThkZDEtZWUwYWI4MjI5NTRmIiBwb3dlcj0iMTAwMDAwMC4wIiBuYW1lPSJpbXBvcnQiDQogICAgICAgICAgICAgICAgICAgcHJvZFR5cGU9IkZPU1NJTCI+DQogICAgICAgICAgICAgICAgPHBvcnQgeHNpOnR5cGU9ImVzZGw6T3V0UG9ydCIgY2Fycmllcj0iY2Fycmllcl9pZCINCiAgICAgICAgICAgICAgICAgICAgICBpZD0iMTMyNzMxYzItOGQ0Ny00Y2Q4LWE5YjItNzkyMTQ4OTZlNjIwIiBjb25uZWN0ZWRUbz0ibW9kZWxfaW5wb3J0MV9pZCIvPg0KICAgICAgICAgICAgICAgIDxnZW9tZXRyeSB4c2k6dHlwZT0iZXNkbDpQb2ludCIgbG9uPSI1LjMyNTU0NzQ1Njc0MTMzNCIgbGF0PSI1MS40NDUyMzQ1NjYxMjI2MTUiLz4NCiAgICAgICAgICAgIDwvYXNzZXQ+DQoNCiAgICAgICAgPC9hcmVhPg0KICAgIDwvaW5zdGFuY2U+DQogICAgPGVuZXJneVN5c3RlbUluZm9ybWF0aW9uIHhzaTp0eXBlPSJlc2RsOkVuZXJneVN5c3RlbUluZm9ybWF0aW9uIiBpZD0iMmI1OTdiOTMtZTJmOS00Y2JmLWE4MjctYmNmZDg3MWZmMzNmIj4NCiAgICAgICAgPGNhcnJpZXJzIHhzaTp0eXBlPSJlc2RsOkNhcnJpZXJzIiBpZD0iZDI2MGQ1YTAtYzU0Ny00ZDQ2LTgyOWItNGIyNDhiMGQ1MmVhIj4NCiAgICAgICAgICAgIDxjYXJyaWVyIHhzaTp0eXBlPSJlc2RsOkVsZWN0cmljaXR5Q29tbW9kaXR5IiBuYW1lPSJFbGVjdHJpY2l0eSIgaWQ9ImNhcnJpZXJfaWQiLz4NCiAgICAgICAgPC9jYXJyaWVycz4NCiAgICA8L2VuZXJneVN5c3RlbUluZm9ybWF0aW9uPg0KPC9lc2RsOkVuZXJneVN5c3RlbT4NCg==",
  "log_level": "info"
}
```

The logs from the calculation services can be viewed in Lens. For now you have to be quick, since the pods are deleted right after completion (to be updated).