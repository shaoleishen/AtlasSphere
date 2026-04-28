from fastapi import FastAPI
import uvicorn
from loguru import logger

app = FastAPI(title="AtlasSphere Cloud Hub", version="0.1.0", description="Restful Gateway of Bio Multi-head agent Engine.")

@app.get("/health")
def readiness_probe():
    return {"status": "AtlasSphere Gateway is active and listening HTTP Requests."}

def start():
    """API 服务启动点"""
    logger.info("Initializing AtlasSphere FastAPI Web Gateway...")
    uvicorn.run("atlassphere.gateway.server:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    start()
