from pydantic import BaseModel, Field


class FmuInputVariable(BaseModel):
    fmu_input_name: str = Field(
        default="<<FmuInputName>>",
        description="The name of the input variable as defined in the FMU model",
    )
    esdl_type_input: str = Field(
        default="<<EsdlTypeInput>>",
        description="The ESDL type that the calculation service simulates which ouputs the required input variable e.g. 'PVInstallation'",
    )
    calculation_service_input_name: str = Field(
        default="<<CalculationServiceInputName>>",
        description="The name of the output variable of the calculation service that should be mapped to the FMU input variable",
    )
