import asyncio

import pytest
from fastapi.testclient import TestClient

import calculator
from main import app


def test_calculate_endpoint():
    with TestClient(app) as client:
        response = client.post(
            "/calculate/",
            json={"numbers": [5, -3, 1.5, 0], "delays": [0.02, 0, 0.01, 0]},
        )

    assert response.status_code == 200
    data = response.json()
    assert [item["number"] for item in data["results"]] == [5, -3, 1.5, 0]
    assert [item["square"] for item in data["results"]] == [25, 9, 2.25, 0]
    assert [item["delay"] for item in data["results"]] == [0.02, 0, 0.01, 0]
    assert all(item["time"] >= 0 for item in data["results"])
    assert data["total_time"] >= 0.02
    assert isinstance(data["parallel_faster_than_sequential"], bool)


@pytest.mark.parametrize(
    "payload",
    [
        {"numbers": [], "delays": []},
        {"numbers": [1, 2], "delays": [0]},
        {"numbers": [1], "delays": [0, 0]},
        {"numbers": [1], "delays": [-1]},
        {"numbers": ["invalid"], "delays": [0]},
        {"numbers": ["NaN"], "delays": [0]},
        {"numbers": ["Infinity"], "delays": [0]},
        {"numbers": [1], "delays": ["NaN"]},
        {"numbers": [1], "delays": ["Infinity"]},
        {"numbers": [1]},
    ],
)
def test_invalid_request(payload):
    with TestClient(app) as client:
        response = client.post("/calculate/", json=payload)

    assert response.status_code == 422


def test_tasks_run_concurrently(monkeypatch):
    async def run():
        started = []
        all_started = asyncio.Event()

        async def wait_for_other_tasks(delay):
            started.append(delay)
            if len(started) == 3:
                all_started.set()
            await all_started.wait()

        monkeypatch.setattr(calculator.asyncio, "sleep", wait_for_other_tasks)
        result = await asyncio.wait_for(calculator.calculate([5, 3, 10], [1, 2, 0.5]), timeout=1)

        assert started == [1, 2, 0.5]
        assert [item.square for item in result.results] == [25, 9, 100]

    asyncio.run(run())


@pytest.mark.parametrize("delays, expected", [([1, 2], True), ([0, 0], False)])
def test_time_comparison(monkeypatch, delays, expected):
    async def skip_delay(delay):
        pass

    clock = iter([10, 10, 10.1, 10.1, 10.2, 10.25])
    monkeypatch.setattr(calculator.asyncio, "sleep", skip_delay)
    monkeypatch.setattr(calculator, "perf_counter", lambda: next(clock))

    result = asyncio.run(calculator.calculate([2, 3], delays))

    assert result.total_time == 0.25
    assert [item.time for item in result.results] == [0.1, 0.1]
    assert result.parallel_faster_than_sequential is expected
