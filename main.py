from fastapi import FastAPI

from calculator import calculate
from models import CalculateRequest, CalculateResponse

app = FastAPI(title="Async Calculator")


@app.post("/calculate/", response_model=CalculateResponse)
async def calculate_numbers(request: CalculateRequest) -> CalculateResponse:
    return await calculate(request.numbers, request.delays)
