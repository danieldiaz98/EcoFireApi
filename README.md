# EcoFire API

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.141-009688?logo=fastapi&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063?logo=pydantic&logoColor=white)
![Tests](https://img.shields.io/badge/tests-pytest-0A9EDC?logo=pytest&logoColor=white)

API REST para el cálculo del **índice de riesgo de incendios forestales en Canarias**. A partir de unas coordenadas, consulta las condiciones meteorológicas actuales y aplica un motor de reglas para devolver una puntuación de riesgo (0-100), un nivel cualitativo y recomendaciones de prevención.

## Características

- Validación de coordenadas limitada a la región de Canarias.
- Obtención de datos meteorológicos en tiempo real mediante [Open-Meteo](https://open-meteo.com/).
- Motor de riesgo basado en temperatura, humedad y viento.
- Detección de la regla crítica **30-30-30** (≥30 °C, ≤30 % humedad y ≥30 km/h de viento).
- Clasificación en cinco niveles: `Low`, `Moderate`, `High`, `Very_High` y `Extreme`.
- Recomendaciones de prevención adaptadas a cada nivel.
- Documentación interactiva automática con Swagger UI.
- Tests unitarios del motor de riesgo con `pytest`.

## Stack

| Componente | Tecnología |
| --- | --- |
| Framework | FastAPI |
| Validación / modelos | Pydantic v2 |
| Cliente HTTP | HTTPX |
| Fuente de datos | Open-Meteo API |
| Servidor | Uvicorn |
| Tests | Pytest + pytest-asyncio |

## Estructura del proyecto

```text
EcoFireApi/
├── app/
│   ├── main.py                  # Punto de entrada y definición de endpoints
│   ├── schemas/
│   │   ├── location.py          # Coordenadas y validación geográfica
│   │   ├── weather.py           # Datos meteorológicos
│   │   ├── risk.py              # Enum de niveles de riesgo
│   │   └── fire_risk_response.py
│   └── services/
│       ├── weather_service.py   # Integración con Open-Meteo
│       └── risk_engine.py       # Cálculo del índice y recomendaciones
├── tests/
│   ├── test_api.py
│   └── test_risk_engine.py
├── requirements.txt
├── pytest.ini
└── README.md
```

## Instalación

```bash
git clone https://github.com/danieldiaz98/EcoFireApi.git
cd EcoFireApi

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

## Ejecución

```bash
uvicorn app.main:app --reload
```

- API: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Endpoints

### `POST /api/v1/risk/check_location`

Comprueba que las coordenadas estén dentro de los límites de Canarias.

```bash
curl -X POST http://127.0.0.1:8000/api/v1/risk/check_location \
  -H "Content-Type: application/json" \
  -d '{"latitude": 28.12, "longitude": -15.43}'
```

### `POST /api/v1/risk/fire_risk`

Consulta el tiempo actual de la ubicación y calcula el riesgo de incendio.

```bash
curl -X POST http://127.0.0.1:8000/api/v1/risk/fire_risk \
  -H "Content-Type: application/json" \
  -d '{"latitude": 28.12, "longitude": -15.43}'
```

Respuesta de ejemplo:

```json
{
  "location": { "latitude": 28.12, "longitude": -15.43 },
  "risk_score": 61.4,
  "risk_level": "High",
  "rule_30_active": false,
  "weather": {
    "temperature": 29.5,
    "humidity_percent": 42.0,
    "wind_speed": 24.0
  },
  "recommendation": "Riesgo alto. Restricción de quemas agrícolas y extremar precauciones en uso de barbacoas."
}
```

## Modelo de riesgo

La puntuación total (0-100) suma tres componentes acotadas:

| Factor | Fórmula | Peso máximo |
| --- | --- | --- |
| Temperatura | `(T - 15) * 1.4` | 35 |
| Humedad | `(80 - H) * 0.5` | 35 |
| Viento | `(W - 5) * (30 / 45)` | 30 |

Si se cumple la regla **30-30-30**, la puntuación se eleva a un mínimo de 85 (riesgo extremo).

Niveles resultantes:

| Puntuación | Nivel |
| --- | --- |
| < 25 | Low |
| 25 - 49.9 | Moderate |
| 50 - 69.9 | High |
| 70 - 84.9 | Very_High |
| ≥ 85 | Extreme |

## Tests

```bash
pytest
```

La configuración de `pytest.ini` activa el modo asíncrono y añade la raíz del proyecto al `PYTHONPATH`.

## Variables de entorno

El proyecto no requiere claves para Open-Meteo. Si añades servicios que las necesiten, crea un `.env` (ya ignorado por Git) y cárgalo con `python-dotenv`.

## Licencia

Uso educativo y de portfolio. Consulta con el autor antes de un uso en producción.
