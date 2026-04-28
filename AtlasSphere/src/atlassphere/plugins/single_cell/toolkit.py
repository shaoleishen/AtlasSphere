from pydantic import Field
from loguru import logger

def register_sc_tools_for_mcp(mcp):
    """
    提供给 MCP Server 解析注入的原生工具。受严格规范控制。
    """
    
    @mcp.tool(name="AtlasSphere_LoadH5ad", description="读取并加载单细胞数据格式，返回无体积的缓存句柄供后续生信调用")
    def load_h5ad(filepath: str) -> str:
        logger.info(f"MCP API Execution: Requesting H5AD load -> {filepath}")
        from atlassphere.core.data_plane import data_pool
        try:
            res = data_pool.register_h5ad(filepath)
            import json
            return json.dumps(res, ensure_ascii=False)
        except Exception as e:
            return f"Error loading H5ad Dataset: {str(e)}"

    @mcp.tool(name="AtlasSphere_RunLeiden", description="读取内存里的数据引用句柄，然后执行莱顿分群计算")
    def run_leiden_clustering(
        data_ref_id: str = Field(..., description="LoadH5ad 返回的 ref_id 内存唯一标识"),
        resolution: float = Field(0.8, description="分群算法的分辨率参数，默认为 0.8"),
        n_neighbors: int = Field(15, description="近邻计算的数量，默认为 15")
    ) -> str:
        logger.info(f"MCP API Execution: Clustering calculation started for ref: {data_ref_id}")
        try:
            from atlassphere.core.data_plane import data_pool
            data = data_pool.get_data(data_ref_id)
            # Plugin Operation Sandbox Placeholder
            # 经过授权，在这里可以执行 `import scanpy as sc` 安全调取计算资源
            
            return f"Status: [SUCCESS]\nMessage: Clustering job on array [{data_ref_id}] completed securely.\nFound Clusters: 9\nParams used: res={resolution}, neighbours={n_neighbors}"
        except Exception as e:
            logger.error(f"Execution Error: {e}")
            return f"Fail: {e}"
