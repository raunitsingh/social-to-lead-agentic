from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()
app.mount("/ui", StaticFiles(directory="ui"), name="ui")

@app.get("/")
def root():
    return FileResponse("ui/index.html")

@app.get("/health")
def health():
    return {"status": "ok"}
