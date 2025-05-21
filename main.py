from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
import httpx
import io

app = FastAPI()

@app.get("/fetch-pdf")
async def fetch_pdf(url: str = Query(...)):
    try:
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            }
            response = await client.get(url, headers=headers)
            response.raise_for_status()

            content_type = response.headers.get("content-type", "")
            if "application/pdf" not in content_type:
                return {"error": "目标返回的不是 PDF", "content_type": content_type}

            return StreamingResponse(io.BytesIO(response.content),
                                     media_type="application/pdf")
    except Exception as e:
        return {"error": str(e)}
