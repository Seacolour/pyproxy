from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
import httpx
import io

app = FastAPI()

@app.get("/fetch-pdf")
async def fetch_pdf(url: str = Query(...)):
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            return StreamingResponse(io.BytesIO(response.content),
                                     media_type="application/pdf")
    except Exception as e:
        return {"error": str(e)}
