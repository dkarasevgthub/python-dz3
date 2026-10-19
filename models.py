from typing import Annotated, Self

from pydantic import BaseModel, Field, FiniteFloat, model_validator

Delay = Annotated[FiniteFloat, Field(ge=0)]


class CalculateRequest(BaseModel):
    numbers: list[FiniteFloat] = Field(min_length=1)
    delays: list[Delay] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_lengths(self) -> Self:
        if len(self.numbers) != len(self.delays):
            raise ValueError("numbers and delays must have the same length")
        return self


class CalculationResult(BaseModel):
    number: float
    square: float
    delay: float
    time: float


class CalculateResponse(BaseModel):
    results: list[CalculationResult]
    total_time: float
    parallel_faster_than_sequential: bool
