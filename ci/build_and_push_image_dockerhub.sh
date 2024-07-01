#!/bin/bash

# login first: docker login -u dotsenergyframework

VERSION=0.1.0
REPOSITORY="dotsenergyframework/simulation-orchestrator"

docker build -t ${REPOSITORY}:${VERSION} ./..

docker push ${REPOSITORY}:${VERSION}
