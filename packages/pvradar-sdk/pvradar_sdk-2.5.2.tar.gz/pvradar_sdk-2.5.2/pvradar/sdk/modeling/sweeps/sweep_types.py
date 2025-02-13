from typing import TypedDict

from pvradar.sdk.modeling.basics import ModelRecipe


class SweepRange(TypedDict):
    param_name: str
    min: float
    max: float
    step: float


class ModelSweepRecipe(ModelRecipe):
    ranges: list[SweepRange]
