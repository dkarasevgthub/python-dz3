# Асинхронный калькулятор

## Структура

- `main.py` — приложение и эндпоинт `POST /calculate/`.
- `models.py` — модели запроса и ответа, проверка входных данных.
- `calculator.py` — асинхронные вычисления и замеры времени.
- `test_calculator.py` — тесты.

## Запуск

```powershell
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Swagger UI: http://127.0.0.1:8000/docs.

## Запуск тестов

```powershell
python -m pytest -q
```

## Пример запроса

`POST /calculate/`

```json
{
  "numbers": [5, 3, 10],
  "delays": [1, 2, 0.5]
}
```

## Пример ответа


```json
{
  "results": [
    {"number": 5, "square": 25, "delay": 1, "time": 1.002},
    {"number": 3, "square": 9, "delay": 2, "time": 2.001},
    {"number": 10, "square": 100, "delay": 0.5, "time": 0.501}
  ],
  "total_time": 2.002,
  "parallel_faster_than_sequential": true
}
```

