from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
import httpx
import time
import io

app = FastAPI()

async def fetch_pdf_bytes(url: str) -> bytes:
    print(f"\n🔍 请求 URL: {url}")
    t0 = time.time()

    async with httpx.AsyncClient(timeout=60.0, follow_redirects=True) as client:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        # Step 1: 发起请求并接收响应头
        t1 = time.time()
        response = await client.get(url, headers=headers)
        t2 = time.time()

        print(f"⏱️ 连接 & 首包耗时: {t2 - t1:.2f}s")

        # Step 2: 响应校验
        response.raise_for_status()
        content_type = response.headers.get("content-type", "")
        if "text/html" in content_type:
            raise ValueError("返回的是 HTML 页面，可能是错误页")

        # Step 3: 下载内容体
        content = response.content  # `.content` 会触发剩余字节的下载
        t3 = time.time()

        print(f"⏱️ 内容下载耗时: {t3 - t2:.2f}s")
        print(f"✅ 总耗时: {t3 - t0:.2f}s，类型: {content_type}, 大小: {len(content)} bytes")
        return content

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
