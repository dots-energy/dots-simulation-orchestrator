# Examples
There are a few examples available outlining the capabilities of DOTs and the models that are now in the [dots energy services](https://github.com/dots-energy-services/) repositories. For now all the examples describe a low voltage network in which a specific network tariff instrument is active for the consumers. For specifics on the tariff instruments please consult [this](https://doi.org/10.1016/j.segan.2025.101623) paper.

All the examples can be found in the [example repository](https://github.com/dots-energy/dots-examples/).

## Small test example
The first small test example can be found in the [example repository](https://github.com/dots-energy/dots-examples/tree/main/Small%20test%20example). 

The [test.esdl](https://github.com/dots-energy/dots-examples/blob/main/esdls/test.esdl) file contains an energy system with an electricity network and two houses. The houses have the exact same parameters i.e. the same flexible assets, the same load profile and the same heating coefficients. The only difference is that house 1 has a home energy management system (HEMS) and house 2 does not. Both houses still make use of the HEMS calculation service only for house 2 the HEMS does not perform any optimizations.

Next the [post-small-test-example.json](https://github.com/dots-energy/dots-examples/blob/main/Small%20test%20example/test-post-small-test-file.json) is a json file containing the Base64 encoding of the `test.esdl` file as well as a mapping for the different esdl files and their associated calculation services. 

![small example results apparent power](../images/static/small-example-sequence_diagram.svg?raw=true)
To get an idea of the interactions that take place during a DOTs co-simulation please have a look at the sequence diagram above. In this example all the calculation services act with the same timestep size being 900 seconds. So in every simulation time step of 900 seconds the above messages are exchanged between the respective calculation services. Observe that once a calculation service has received all its respective inputs the calculation is executed which is denoted by a self message arrow.

When the json file is submitted to the simulation API the DOTs framework will start the co-simulation. The status API endpoint or OpenLens can be used to monitor the status of the simulation. The outputted simulation data will be available in the InfluxDB as soon as the simulation is finished. The pictures below show the results of the co-simulation in a Grafana dashboard. To reproduce the figures below the [Grafana-dashboard.json](https://github.com/dots-energy/dots-examples/blob/main/Small%20test%20example/Grafana-dashboard.json) can be uploaded and imported to Grafana. Make sure a data source has been added to Grafana  which is pointing to the InfluxDB on the cluster. The queries in that dashboard need to be updated to select the correct simulation id. Another option would be to download the data as a collection of csv files and process the data using more suffisticated tools. 

![small example results apparent power](../images/static/apparent-power-graph-small-example.png?raw=true)
![small example flexible assets and transformer](../images/static/test-small-example-flexible-assets-transformer-loading.png?raw=true)

First observe that in the firs two graphs the apparent power profiles for house 1 and house 2 differ significantly despite having the same load profile. This is the result of what the HEMS has done for us namely, economically optimizing the flexible load for the household. This difference in power profile can also be seen in the third graph where the active power dispatch of the different flexible assets is shown. Second of all the transformer in this small network is not overloaded. Meaning that this network is not suffering from congestion.

## Bandwidth tariff example
One of the net-tariff instruments that can be analyzed using the DOTs framework and existing calculation services is the Bandwidth tariff. The description of this tariff can be found in [this paper](https://doi.org/10.1016/j.segan.2025.101623).

The networks used in all the examples (execept for the small test example) consists of a LV-network with 60 households every household in this network has an ems and every household has a dynamic energy contract. This means that the energy management systems in this network will try to financially optimize the energy usage in the household using the household's flexible assets depending on the energy price throughout the day. The esdl files in the base case example as well as the bandwidth example contain load and price profiles for a 3 summer days in august.

Let's say you want to see if one of the tariff has any positive effect on the transformer and or cable loading in the network. The first step would be to run the base case example and see what the behaviour of the LV network is without any tariff instruments active. The base case example can be run by using the [base-case-example.json](github.com/dots-energy/dots-examples/blob/main/Base%20case%20example/base-case-example.json). 

![transformer loading base case](../images/static/test-base-case-transformer-loading.png?raw=true)

Once the simulation is finished the transformer loading can be plotted using Grafana. The transformer loading for the base case can be seen in the figure above. The figure shows that the transformer is briefly overloaded in this scenario.

Now we want to know if the bandwidth tariff instrument might help solve the transformer overloading. This can be done by running the bandwidth example with the [test-post-bandwitdh.json](https://github.com/dots-energy/dots-examples/blob/main/Bandwitdh%20example/test-post-bandwitdh.json).

![transformer loading base case](../images/static/test-bandwidth-transformer-loading.png?raw=true)

The above figure shows the new tranformer loading profile plotted in Grafana. Observe that the transformer is no longer being overloaded and thus the tariff instrument helps to solve the transformer overloading problem.

Finally, be aware that there are endless posibilities in the scenario definitions i.e. number of households containing a HEMS, simulating a summer days or winter days and the active tariff instrument.

## Other examples
The other examples found in the [example repository](https://github.com/dots-energy/dots-examples/) all contain the same network from the [archetype dataset](https://www.projectgo-e.nl/rekenen-aan-flexibiliteit-in-distributienetten/) only with other tariff instruments active. The name of the folder describes the name of the used tariff instrument. 