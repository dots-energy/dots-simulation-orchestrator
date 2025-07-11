# Calculation services
Calculation services are at the heart of a DOTs co-simulation. These services implement logic that simulates a specific entity of the energy system e.g. a PVInstallation, heatpump or HEMS. The idea of calculation services is that they can easily be reused in a wide variety of co-simulations. Existing calculation services can be found in the [dots energy services](https://github.com/dots-energy-services/) organization.

## Creating a new calculation service (short steps)
To create a new calculation service follow the following steps (For a more detailed explenation see below):
1. Create a new github repository with the [calculation service template repository](https://github.com/dots-energy/Dots-calculation-service-template).
2. Create a new python virtual environment and install the dependencies in the `pyproject.toml` with `pip install -e ./`.
3. Edit the `input.json` file based upon your needs i.e. define the correct calculations for the calculation service.
4. Run the code generator with: `python code_gen.py`.
5. Copy the calculation method signatures from `src/<<CalculationServiceName>>_base.py` into `src/<<CalculationServiceName>>.py`. Where `<<CalculationServiceName>>` is the name supllied in `input.json`.
6. Add an import to the base class in `src/<<CalculationServiceName>>.py`.
7. Edit the `Test<<CalculationServiceName>>.py` to test your calculations indepedently in a python unit test.

## Updating a calculation service
If you want to update the calculation service i.e. add new calculation, update documentation strings or add new in and outputs please follow the following steps:
1. Edit the `input.json` file based upon your needs i.e. define the correct calculations for the calculation service.
2. Run the code generator with: `python code_gen.py`.
3. Add the newly generated method signatures from `src/<<CalculationServiceName>>_base.py` into `src/<<CalculationServiceName>>.py`.

## Creating a calculation service (detailed steps)
A calculation service defines the simulation logic for a specific `esdl_type`. The initial `input.json` defines the simulation logic for the `esdl_type`, `EConnection`. Below an example of a calculation service with two calculations is defined. The service defines the logic for the `EConnection` type in ESDL. These calculations are called `test calculation` and `test calculation 2` respectively. Let's take a look at the definition of the first calculation:

```json
{
    "name": "test",
    "esdl_type" : "EConnection",
    "description" : "this is a test description",
    "relevant_links" : [
        {
            "name" : "test link",
            "url" : "https://example.com/test",
            "description" : "this is a test link"
        },
        {
            "name" : "another test link",
            "url" : "https://example.com/anothertest",
            "description" : "this is another link"
        }
    ],
    "calculations" : [
        {
            "name": "test calculation",
            "description" : "test",
            "time_period_in_seconds" : 900,
            "offset_in_seconds" : 0,
            "inputs" : [
                {
                    "name" : "input1",
                    "esdl_type" : "PVInstallation",
                    "data_type" : "DOUBLE",
                    "description" : "input 1 description",
                    "unit" : "K"
                }
            ],
            "outputs" : [
                {
                    "name" : "output1",
                    "data_type" : "DOUBLE",
                    "description" : "output 1 description",
                    "unit" : "W"
                },
                {
                    "name" : "output2",
                    "data_type" : "DOUBLE",
                    "description" : "output 2 description",
                    "unit" : "W"
                }
            ]
        },
        {
            "name": "test calculation 2",
            "description" : "test",
            "time_period_in_seconds" : 900,
            "offset_in_seconds" : 100,
            "inputs" : [
            ],
            "outputs" : [
                {
                    "name" : "output3",
                    "data_type" : "DOUBLE",
                    "description" : "output 3 description",
                    "unit" : "W"
                }
            ]
        }
    ]
}
```

First, every calculation has generic parameters these being the `name`, `description` (used for documentation purposes), `time_period_in_seconds` and `offset_in_seconds`. The first two are self explanatory the second two might need some explanation. The `time_period_in_seconds` and `offset_in_seconds` parameters specify the execution time for calculation services that have **NO** inputs. The `time_period_in_seconds` specifies the execution frequency of the calculation, and, the `offset_in_seconds` parameter specifies the offset from the initial simulation time. Hence, the calculation will be executed at simulation times `offset_in_seconds + n * time_period_in_seconds` where `n` is the timestep for the calculation service that is being excuted. To clarify, in the above example, the second calculation i.e. `test calculation 2`, has no inputs, `time_period_in_seconds=900` and `offset_in_seconds=100`, which means that this calculation will be executed every `900` seconds with an offset of `100` i.e. at simulation times `1000, 1900, 2800` and so on. 
Calculations that do have inputs will be executed whenever **ALL** their inputs have been received. In the above example calculation `test calculation` will only be executed at the simulation time where the servcie has received `input1` from a connected `PVInstallation`.

Second, you can see a list called `inputs`. This list defines the inputs of the calculation. In this case the calculation has one input that is supposed to come from the ESDL type called `PVInstallation` as specified by the `esdl_type` parameter. Next, the `name` parameter describes the name of the value that the `PVInstallation` produces. Finally, the `input_unit` and `input_type` describe the input's unit and type respectively. 

The second list describes the publications or outputs of the calculation. Observe that for the outputs similar properties as for the inputs need to be defined except the `esdl_type`.

When your calculations with their respective inputs and outpus are defined the code generator can be used to generate a base class for your calculation service and documentation. The generator will also rename the example test file and the example implementation files that fit the name that you have specified in the `input.json` file. In order to implement the calculations yourself you need to either create a new python file and inherit from the generated base class or edit the supplied example implementation file.

The generated code adds the calculations to a new calculation service and ensures that the calculation is executed during a running co-simulation. Every added calculation will become a [helics federate](https://docs.helics.org/en/latest/user-guide/fundamental_topics/helics_terminology.html) with their own timing parameters as defined in the `calculation_information`. To get an idea of how helics timing works have a look at this [page](https://docs.helics.org/en/latest/user-guide/fundamental_topics/timing_configuration.html) of the helics documentation.

```python
class CalculationServiceTest(CalculationServiceTestBase):

    def init_calculation_service(self, energy_system: esdl.EnergySystem):
        LOGGER.info("init calculation service")
        for esdl_id in self.simulator_configuration.esdl_ids:
            LOGGER.info(f"Example of iterating over esdl ids: {esdl_id}")

    def test_calculation(self, param_dict : dict, simulation_time : datetime, time_step_number : TimeStepInformation, esdl_id : EsdlId, energy_system : EnergySystem):
        ret_val = {}
        single_input1_value = get_single_param_with_name(param_dict, "input1") 
        all_input1_values = get_vector_param_with_name(param_dict, "input1") 
        ret_val = TestDataClass(output1=5, output2="test")
        self.influx_connector.set_time_step_data_point(esdl_id, "EConnectionDispatch", simulation_time, ret_val.output1)
        return ret_val
    
    def test_calculation_2(self, param_dict : dict, simulation_time : datetime, time_step_number : TimeStepInformation, esdl_id : EsdlId, energy_system : EnergySystem):
        ret_val = {}
        ret_val["output3"] = 3.0
        return ret_val

if __name__ == "__main__":

    helics_simulation_executor = CalculationServiceTest()
    helics_simulation_executor.start_simulation()
    helics_simulation_executor.stop_simulation()
```
The example implementation file is shown above. As you can see the the implementation class inhertis from the generated base class and the calculations are implemented in here.

When the simulation starts there will be an initialization stage and a calculating stage. In the initialization phase a calculation service can initialize variables that are required in the calculation stage. This can be done by adjusting the `init_calculation_service` function. The esdl that is associated with the simulated scenario is given as a parameter to this function.

## Implementing a calculation
When implementing a calculation, you need to be aware of the following. New inputs can be read and new outputs can be generated. An example of getting inputs, returning outputs and writing to the influx db can be found in the example above.

### Parameters
In the calculation phase the calculation functions are called periodically for each simulated esdl entity. The `esdl_id` of the simulated entity is passed as a parameter to the calculation function. Furhtermore, the `simulation_time` specifies the current time in the co-simulation. The `energy_system` parameter is the parsed esdl energy system that was supplied by the user. Finally, the `time_step_number` parameter denotes the timestep the co-simulation is in as well as the amount of timesteps in terms of the calculation service's `time_period_in_seconds`. For example, if the calculation's `time_period_in_seconds=900`, the total duration of the co-simulation is `2700` seconds and the `simulation_time=900` seconds, then, `time_step_number` parameter has `time_step_number.max_time_step_number=3` and on  `time_step_number.max_time_step_number=1`

### Getting inputs from a calculation service
The input parameters provided by other calculation services are provided by the `param_dict` parameter in the calculation. Whenever the calculation function `e_connection_dispatch` is called, the param dict for the calculation `e_connection_dispatch` could look like:

```
param_dict = {
    "PVInstallation/PV_Dispatch/1f60ceb9-9708-4d89-b079-482abc1408ea" : 5,
    "PVInstallation/PV_Dispatch/468f4332-4306-4b74-a5c2-eb8a7aa0a8d9" : 3,
}
```

This would mean that the associated esdl entity is connected to two `PVInstallation` entities with id `1f60ceb9-9708-4d89-b079-482abc1408ea` and `468f4332-4306-4b74-a5c2-eb8a7aa0a8d9` respectively. There are two ways to retrieve the values from the dictionary. First, by the python way of retrieving values from a dictiononary i.e. `param_dict[key]` this would require you to know the keys of dictionary. 
The second option is to use the helper functions in `dots_infrastructure.CalculationServiceHelperFunctions` (as shown in the above example). The function `get_single_param_with_name` will get the first value in `param_dict` with a specific input name. In the above example the input called `PV_Dispatch` is fetched and thus the function will return the vaule `5`. The other function to help retrieve values is called `get_vector_param_with_name` and will return all the values with a specific `input_name` as a list. In this example it wil return the list `[5, 3]`. Observe that the names of the inputs retrieved and the outputs that are set must match the names specified in the `input.json`.

### Providing outputs
Part of the generated code are dataclasses. Output to a calculation function can be provided in two ways:
1. Instantiating the associated output dataclass and setting the correct values, see `test_calculation` above (prefferred).
2. Building a dictionary with key value pairs where the keys are the exact name provided in the `input.json`, see `test_calculation_2` above.

Once either of the following is done simply return the dictionary or instance of the dataclass.

### Storing values in the database
Every calculation service has an instance of `InfluxDBConnector` this class can be used to write values to the influx database. See the implementation of `test_calculation` above for an example.

## Testing a calculation service

1. Create a new python virtual environment
2. Install package `pip install -e .`
3. Run `cd test`
4. Run `python -m unittest discover -s ./ -p 'Test*.py'`

## Building a docker image such that it can be used 

1. Adjust `<<ImageName>>` to the name of the calculation service's image in the file `.github/workflows/publish-image.yml`
2. Push your changes to a new branch
3. Create a pull request
4. A github action will now run building the calculation service as a docker image and pushing it to the registry, as long as the pull request is not merged in the main branch the version number will be equal to the branch name.
5. When finished complete the pull request and a new docker image will be built and pushed with version number `latest`
6. Change the visibility of the package to public, follow the steps detail [here](https://docs.github.com/en/enterprise-server@3.12/packages/learn-github-packages/configuring-a-packages-access-control-and-visibility#configuring-visibility-of-packages-for-an-organization).