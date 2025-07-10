# Examples
There are a few examples available outlining the capabilities of DOTs and the models that are now in the [dots energy services](https://github.com/dots-energy-services/) repositories. For now all the examples describe a low voltage network in which a specific net tariff instrument is active for the consumers. For specifics on the tarif instruments please consult [this](https://doi.org/10.1016/j.segan.2025.101623) paper.

All the examples can be found in the [example repository](https://github.com/dots-energy/dots-examples/).

## Small test example
The first small test example can be found in the [example repository](https://github.com/dots-energy/dots-examples/tree/main/Small%20test%20example). 

The [test.esdl](https://github.com/dots-energy/dots-examples/blob/main/esdls/test.esdl) file contains an energy system with an electricity network and two houses. The houses have the exact same parameters i.e. the same flexible assets, the same load profile and the same heating coefficients. The only difference is that house 1 has a home energy management system (HEMS) and house 2 does not.

Next the [post-small-test-example.json](https://github.com/dots-energy/dots-examples/blob/main/Small%20test%20example/test-post-small-test-file.json) is a json file containing the Base64 encoding of the `test.esdl` file as well as a mapping for the different esdl files and their associated calculation services. 

![small example results apparent power](https://github.com/dots-energy/dots-simulation-orchestrator/blob/main/docs/images/static/small-example-sequence_diagram.svg?raw=true)
To get an idea of the interactions that take place during a calculations have a look at the sequence diagram above. In this example all the calculation services act with the same timestep size being 900 seconds. So in every simulation time step of 900 seconds the above messages are exchanged between the respective calculation services. Observe that once a calculation service has received all its respective inputs the calculation is executed which is denoted by a self message arrow.

When the json file is submitted to the simulation api the DOTs framework will start the co-simulation. The status api endpoint or openlens can be used to monitor the status of the simulation. The outputted simulation data will be available as soon as the simulation is finished. The pictures below show the results of the co-simulation in a Grafana dashboard. Another option would be to download the data as a collection of csv files and process the data using more suffisticated tools. 

![small example results apparent power](https://github.com/dots-energy/dots-simulation-orchestrator/blob/main/docs/images/static/apparent-power-graph-small-example.png?raw=true)
![small example flexible assets and transformer](https://github.com/dots-energy/dots-simulation-orchestrator/blob/main/docs/images/static/test-small-example-flexible-assets-transformer-loading.png?raw=true)

First observe that in the firs two graphs the apparent power profiles for house 1 and house 2 differ significantly despite having the same load profile. This is the result of what the HEMS has done for us namely, economically optimizing the flexible load for the household. This difference in power profile can also be seen in the third graph where the active power dispatch of the different flexible assets is shown. Second of all the transformer in this small network is not overloaded. Meaning that this network is not suffering from congestion.

## Other examples
The other examples found in the example repository all contain the same network from the [archetype dataset](https://www.projectgo-e.nl/rekenen-aan-flexibiliteit-in-distributienetten/) only with other tariff instruments active. 