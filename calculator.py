import asyncio
from time import perf_counter

from models import CalculateResponse, CalculationResult


async def calculate_square(number: float, delay: float) -> CalculationResult:
    started_at = perf_counter()
    await asyncio.sleep(delay)
    square = number * number
    elapsed = perf_counter() - started_at

    return CalculationResult(
        number=number,
        square=square,
        delay=delay,
        time=round(elapsed, 4),
    )


async def calculate(numbers: list[float], delays: list[float]) -> CalculateResponse:
    started_at = perf_counter()
    results = await asyncio.gather(
        *(calculate_square(number, delay) for number, delay in zip(numbers, delays, strict=True))
    )
    total_time = perf_counter() - started_at

    return CalculateResponse(
        results=results,
        total_time=round(total_time, 4),
        parallel_faster_than_sequential=total_time < sum(delays),
    )
