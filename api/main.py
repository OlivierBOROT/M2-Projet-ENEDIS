# api/main.py
import uvicorn
from fastapi import FastAPI
from routes import predict, model_upload, model_download, model_list

app = FastAPI(title="Energy Prediction API", version="1.0.0")

app.include_router(predict.router)
app.include_router(model_upload.router)
app.include_router(model_download.router)
app.include_router(model_list.router)

@app.get("/")
async def root():
    return {"message": "Hello World! API is working."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
