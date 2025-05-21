# 使用官方 Python 精简镜像（Alpine 可选）
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件和代码
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 暴露端口（默认 uvicorn 监听）
EXPOSE 4799

# 启动服务（使用 uvicorn）
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4799"]
