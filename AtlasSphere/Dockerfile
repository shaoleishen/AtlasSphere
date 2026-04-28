FROM python:3.10-slim-bookworm

# 禁用 python 在运行期输出 buffering 避免日志打印问题
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 安装必要的编译基础链与 HDF5 (用于装配组学的底层库)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libhdf5-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# (可选) 建议使用最新依赖管理体系 uv 以提升装包速度:
RUN pip install uv

# 拷贝环境要求优先进行层缓存
COPY pyproject.toml .

# 安装运行时依赖。可以通过在启动或构建时控制 optionals,
# 比如 `uv pip install -e ".[omics]"` 来装配庞大的 scanpy 等引擎
RUN uv pip install --system fastapi uvicorn pydantic mcp loguru "litellm>=1.0.0"

# 将 src 代码放入容器
COPY src/ /app/src/

# 安装项目包至系统
RUN uv pip install --system -e .

# 暴露 FastAPI 常规端口
EXPOSE 8000

# 默认启动命令 (API GW 模式) 
# 如果你想借以 MCP stdio 模式执行，可以 override ENTRYPOINT
CMD ["uvicorn", "atlassphere.gateway.server:app", "--host", "0.0.0.0", "--port", "8000"]
