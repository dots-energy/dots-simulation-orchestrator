

## DOTs
DOTS (original name: Distributed Orchestrated Time Simulation) was created with the purpose of modeling energy systems consisting of several different energy components (production, consumption, conversion, storage, transport) described using [ESDL](https://energytransition.gitbook.io/esdl/). Developing code that simulates many different components can result in a large, complex and difficult to maintain codebase. A microservices approach can tackle this issue, as well as add flexibility to reuse components in other projects. This micro services approach also allows for horizontal scaling of time consuming calculations. However, setting up a microservice architecture can be a hurdle for some contributors to the code. DOTS has been created with the aim of allowing scientists to focus on implementing logic and physics while developing self-contained scalable calculation services for specific components.

