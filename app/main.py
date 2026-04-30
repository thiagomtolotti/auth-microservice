from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def ping():
    return {"message": "Service is alive"}
