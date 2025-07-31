

# DOTs
DOTS (original name: Distributed Orchestrated Time Simulation) was created with the purpose of modeling energy systems consisting of several different energy components (production, consumption, conversion, storage, transport) described using [ESDL](https://energytransition.gitbook.io/esdl/). Developing code that simulates many different components can result in a large, complex and difficult to maintain codebase. A microservices approach can tackle this issue, as well as add flexibility to reuse components in other projects. This micro services approach also allows for horizontal scaling of time consuming calculations. However, setting up a microservice architecture can be a hurdle for some contributors to the code. DOTS has been created with the aim of allowing scientists to focus on implementing logic and physics while developing self-contained scalable calculation services for specific components.

The platform has been used as part of the GO-e project. Within this project the effectiveness of different network tariff instruments have been explored.
To get an impression of the types of studies performed with DOTs please have a look at [this report](https://www.projectgo-e.nl/wp-content/uploads/2024/06/GO-e_WP33B_rapport_V1_25062024-1.pdf) and/or [this paper](https://doi.org/10.1016/j.segan.2025.101623).

Please consider citing DOTs if you are using the platform in your research, find our citations on our [citations](./info/citations.md)  page.

```{toctree}
:caption: "User Manual"
:maxdepth: 2
usage/introduction
usage/installation
usage/running simulations
usage/calculation services
usage/examples
info/citations
```
