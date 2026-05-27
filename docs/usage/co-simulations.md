# CO-simulation semantics in general
Co-simulation has emerged as a key paradigm in energy system research, enabling the integrated analysis of complex, multi-domain systems by coupling independent simulation models into a coordinated workflow. Rather than relying on a single monolithic model, co-simulation adopts a modular architecture in which specialized simulators—each representing distinct subsystems such as power networks, communication infrastructures, or market dynamics—interact through well-defined interfaces. The aim of the DOTS platform is to simplify the software engineering challenges that arise when developing a co-simulation.

Distributed Orchestrated Time Simulation (DOTS) is a Co-simulation platform for bottom-up large-scale energy systems. Within the DOTS framework, the notion of simulation time plays a central role, as a global (or coordinated) simulation clock orchestrates the exchange of data between components while ensuring temporal consistency. At the same time, individual simulators often operate at different internal timing resolutions, reflecting the physical dynamics they capture; for example, electromagnetic transients may require sub-millisecond steps, whereas market models may evolve in minutes or hours. DOTS co-simulation platform therefore manages the synchronization of these heterogeneous time scales, balancing accuracy and computational efficiency, and enabling researchers to study cross-domain interactions in a flexible and scalable manner.

## Developing a co-simulation the user's perspective
![co-simulation-phases.svg](https://github.com/dots-energy/dots-simulation-orchestrator/blob/main/docs/images/static/co-simulation-phases.svg?raw=true)

When researchers define a co-simulation in DOTS, they have to go through four phases. These phases are depicted in the workflow described in Figure above. In the first phase, researchers think about the scenario of the energy system they want to simulate. This is the most tricky part of the process. This phase is depicted by the leftmost rectangle in Figure above. Such a scenario would describe the distribution grid, the connected assets and their parameters, and/or, the market mechanisms active in the system. Data required for this phase can come from a variety of different sources and can brought together in a scenario definition. After the scenario is defined a researcher will think about the models they want to use, depicted by the second left rectangle in Figure above. This step includes finding suitable existing models or developing new models. Then the co-simulation framework should simulate the defined scenario with the help of the handpicked simulation models. Once the co-simulation is finished i.e. the right-most rectangle in the above Figure, the final phase is analyzing the data from the co-simulation and drawing conclusions. 

### Phase 1 Defining a scenario with DOTS 
The first step of designing a co-simulation with DOTs is building an ESDL file. The esdl file defines your whole energy system scenario. From network topology, to weather forecasts, to demand profiles. 

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
First, the energy system that is defined has two connections to the electricity grid (Indicated by EConnection). The two connections are connected to two and one pv panel respectively. Furthermore both connections are connected to a transformer via an electricity cable indicated by the Electricity cable type. The joint represents the connection point both cables have to the transformer. Then the object connected to the top of the transformer is an import object. This can be seen as a node that provides a source for the electricity grid. In a powerflow calculation scenario the econnections can be considered as loads, the electricity cables as lines, the joint object as nodes and the import objects as source. Finally, there is a weatherservice defined this is a time series profile for the weather data. Of course simulation scenario's 

### Phase 2 Picking required models
Calculation services are at the heart of a DOTs co-simulation. These services implement logic that simulates a specific entity of the energy system e.g. a PVInstallation, heatpump or Home Energy Management System (HEMS). The idea of calculation services is that they can easily be reused in a wide variety of co-simulations. Each calculation service can have multiple calculations with each their own resolution frequency. For example, a HEMS model might send a prognosis every 24 hours to an aggregator and its energy usage every 15 minutes to a network simulator calculation service. In DOTS this would then consist of two calculations one with a resolution frequency of 24h and one with a resolution frequency of 15 minutes.

Existing calculation services can be found in the [dots energy services](https://github.com/dots-energy-services/) organization.

When you are developing a co-simulation use-case you can start by looking at our available calculation services. See if they can fit your use-case and either develop a new one yourself or propose changes to an existing calculation service and implement them. Detailed information on calculation services and how they can be developed can be found in: [calculation services](./calculation%services.md)

### Phase 3 timing semantics of a DOTS co-simulation
A co-simulation in DOTS can be started using the simulation api. In the [running simulations](./running%simulations.md) section it is explained how this can be done. During a DOTS co-simulation the simulation time is managed globally by Helics. The simulation time is defined as the amount of time that is simulated e.g. 1 hour, 12 hours or 1 day.

While the global simulation time is progressing the DOTS environment makes sure that the calculations are executed according to their timing specification.

![Timing-calculations.svg](https://github.com/dots-energy/dots-simulation-orchestrator/blob/main/docs/images/static/Timing-calculations.svg?raw=true)

In the figure above an example is shown of two calculations executing in their specified period. One has a period of 300 seconds and one has a period of 900 seconds.

There are two important things to note about timing in DOTS:
- Calculations that have no inputs will execute at times defined by their period.
- Calculations that have multiple inputs will execute if and only if they have received all their inputs.

To get a bit of an intuition of what this actually means let's consider two calculation services:


| Calculation service 1 | Calculation service 2 |
|--------|--------|
| ![CS1Period300.png](https://github.com/dots-energy/dots-simulation-orchestrator/blob/main/docs/images/static/CS1Period900.png?raw=true) | ![image2.png](https://github.com/dots-energy/dots-simulation-orchestrator/blob/main/docs/images/static/CS2Period300.png?raw=true) |


In the above example test service 1's calculation has a period of 900 seconds and test service 2's calculation has a period of 300 seconds. Because test service 2's calculation is dependent on the output of test service 1's calculation, test service 2's calculation will only execute every 900 seconds despite its period of 300 seconds.


| Calculation service 1 | Calculation service 2|
|--------|--------|
| ![CS2Period300.png](https://github.com/dots-energy/dots-simulation-orchestrator/blob/main/docs/images/static/CS2Period300.png?raw=true) | ![CS2Period900.png](https://github.com/dots-energy/dots-simulation-orchestrator/blob/main/docs/images/static/CS2Period900.png?raw=true) |


Similar to the previous example when the periods of the two calculations are swapped, the execution of the first of test service 2's calculation will become 300 seconds instead of 900 seconds.

### Phase 4
Visualization can be done in two ways:
- Building a dashboard in Grafana
- Exporting the output data to csv's and using custom tooling

The output can be exported by using one of the simulations api's endpoints.
