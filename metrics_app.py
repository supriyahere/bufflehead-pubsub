from fastapi import FastAPI
from prometheus_client import Counter, generate_latest
from fastapi.responses import Response

app = FastAPI()

REQUEST_COUNT = Counter("request_count", "Total requests")

@app.get("/")
def root():
    REQUEST_COUNT.inc()
    return {"message": "Hello"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")
