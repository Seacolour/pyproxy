from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
import httpx
import io

app = FastAPI()

async def fetch_pdf_bytes(url: str) -> bytes:
    async with httpx.AsyncClient(timeout=60.0, follow_redirects=True) as client:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = await client.get(url, headers=headers)
        response.raise_for_status()

        content_type = response.headers.get("content-type", "")
        if "text/html" in content_type:
            raise ValueError("返回的是 HTML 页面，可能是错误页")

        return response.content

# ✅ 1. 在线预览接口（Content-Disposition 不设置）
@app.get("/fetch-pdf")
async def fetch_pdf_preview(url: str = Query(...)):
    try:
        content = await fetch_pdf_bytes(url)
        return StreamingResponse(io.BytesIO(content), media_type="application/pdf")
    except Exception as e:
        return {"error": str(e)}

# ✅ 2. 下载接口（设置 Content-Disposition）
@app.get("/fetch-pdf-download")
async def fetch_pdf_download(url: str = Query(...), filename: str = "downloaded.pdf"):
    try:
        content = await fetch_pdf_bytes(url)
        return StreamingResponse(
            io.BytesIO(content),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        return {"error": str(e)}
