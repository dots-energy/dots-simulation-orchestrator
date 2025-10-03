# Simulation Orchestrator for the Energy System Microservices Cloud Simulator

This simulation orchestrator is controlled by api calls (FastAPI) and uses helics to orchestrate a distributed simulation.

In the [documentation](https://dots-simulation-orchestrator.readthedocs.io/en/latest/) you can find a description of the framework along with installation and usage details.

## Push image
When a push is done to a new branch and a pull request is created the github actions workflow will start a built and publish a new SO image with the branch name as version number.

## Repository Structure

The repository contains several folders with different purposes:

- **k8s:** Contains kubernetes deployment scripts and yaml files.
- **simulation_orchestrator/rest:** FastApi app.
- **simulation_orchestrator:** Code for managing simulations and hosting the fastapi.
- **.dockerignore:** A file containing which files and directories to ignore when submitting this repo as a Docker
  build context. In other words, it prevents the entries from being sent to Docker when the Docker image is build.
- **.gitignore:** A file containing which files and directories not to add to the git repository.
- **.github/workflows** The steps executed by the Github CI workflows when a new commit is pushed to the main branch of the repository
- **Dockerfile:** The build file for the Docker image.
- **pyproject.toml:** The project file describing metadata of the python project as well as dependencies.
- **test_post.json:** POST request body for a test simulation.
