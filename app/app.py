from fastapi import FastAPI
import os
 
app = FastAPI(title="mon-app")
 
ENV = os.getenv("APP_ENV", "development")
 
 
@app.get("/")
def root():
    return {"message": "mon-app is running", "env": ENV}
 
 
@app.get("/health")
def health():
    return {"status": "ok", "env": ENV}
 
 
@app.get("/version")
def version():
    try:
        with open("VERSION") as f:
            return {"version": f.read().strip(), "env": ENV}
    except FileNotFoundError:
        return {"version": "unknown", "env": ENV}
