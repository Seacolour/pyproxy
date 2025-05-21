from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
import httpx
import io

app = FastAPI()

@app.get("/fetch-pdf")
async def fetch_pdf(url: str = Query(...)):
    try:
        async with httpx.AsyncClient(timeout=60.0, follow_redirects=True) as client:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            }
            response = await client.get(url, headers=headers)
            response.raise_for_status()

            content_type = response.headers.get("content-type", "")
            print("🧾 Content-Type:", content_type)
            print("📦 Size:", len(response.content), "bytes")

            # 只过滤 HTML 错误页，其它允许通过
            if "text/html" in content_type.lower():
                return {"error": "返回的是 HTML 页面，可能是错误提示", "content_type": content_type}

            return StreamingResponse(io.BytesIO(response.content),
                                     media_type="application/pdf")
    except Exception as e:
        return {"error": str(e)}
