# DOTS Simulation Orchestrator

Build for GO-e WP3
This simulation orchestrator is controlled by api calls (fastapi) and communicates with the Model Services
Orchestrator (MSO) via MQTT protobuf messages.

## Development

Use Python 3.9.*  
Compile the `requirements(-dev).in` by:

```bash
pip-compile .\requirements.in --output-file .\requirements.txt
```

## Local testing

Several components need to be up and running for local testing:

- Calculation services
- Local Kind cluster (to run Kubernetes on)  
  (with loaded 'calculation service' docker images)
- MQTT client (Mosquitto)
- Model Services Orchestrator

These can be setup by the steps in the repositories below.

### Model Services Orchestrator repository

https://ci.tno.nl/gitlab/dots/model-services-orchestrator  
In the model services orchestrator repository readme, follow the 'Quickstart' section, until and including the 'Start
Mosquitto and the MSO itself' section.  
Now the Kind cluster, MSO and Mosquitto client should be up and running

### Service Template repository @Ruduan update to Code Generator repo

https://ci.tno.nl/gitlab/dots/service-template  
Create three calculation services by using config files in the base directory (from the directory in which the projects
will be placed):

```bash
cookiecutter ..\service-template --no-input --config-file ..\service-template\test_dev\test_service_configs\test1_system_service.yaml -f
cookiecutter ..\service-template --no-input --config-file ..\service-template\test_dev\test_service_configs\test1_pvpanel_service.yaml -f
cookiecutter ..\service-template --no-input --config-file ..\service-template\test_dev\test_service_configs\test1_battery_service.yaml -f
```

This creates a project folder for each calculation service.  
Optionally: test the services locally by following the readme in the newly created projects.

@Ruduan: Protoc .proto message definitions to create _b2.py files

In each project follow the 'Deployment - For local simulation testing' section.

Now the docker images for the calculation services should be loaded on the Kind cluster.

### Run Test Simulation

Run `main.py` in the root of this repository.  
Go to localhost:8001/docs  
'Try it out': POST '/api/v1/simulation/' with the following body:

```json
{
  "name": "test1 simulation",
  "start_date": "2023-01-25 00:00:00",
  "time_step_seconds": 3600,
  "nr_of_time_steps": 24,
  "keep_logs_hours": 0.1,
  "log_level": "info",
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

The logs from the calculation services can be viewed in Lens.
The output is quite boring since nothing is done in the calculations, but it shows the data flow and the order of the
calculations.