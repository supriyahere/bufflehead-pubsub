from fastapi import FastAPI

app = FastAPI()

@app.post("/")
def predict(data: dict):
    return {
        "predicted_individualcount": 12.5,
        "input": data
    }
