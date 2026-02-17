# FastAPI + SQLModel Sample

Minimal app used as schema source for Atlas.

## Install

```bash
cd atlas_fastapi_sample
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Configure

```bash
cp .env.example .env
export $(grep -v '^#' .env | xargs)
```

## Run

```bash
fastapi dev app/main.py
```

Health endpoint: `GET /healthz`
