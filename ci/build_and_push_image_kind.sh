#!/bin/bash

VERSION=0.0.2

docker build -t service_name:${VERSION} ./..

# for local testing load in kind
kind load docker-image simulation_orchestrator:${VERSION} --name dots-kind

# for production push to dockerhub: public or https://hub.docker.com/orgs/tnodocker?
