import typing

from pydantic import BaseModel, Field

class EnvironmentVariable(BaseModel):
    name : str = Field(default='<<VariableName>>', description="Variable name")
    value : str = Field(default='<<VariableValue>>', description="Variable value")