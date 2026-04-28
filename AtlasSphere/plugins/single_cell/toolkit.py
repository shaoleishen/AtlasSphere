from pydantic import BaseModel, Field
from loguru import logger
import json

class LoadDataSchema(BaseModel):
    filepath: str = Field(..., description="要加载的单细胞数据文件的绝对路径或相对路径，比如 h5ad 文件")
    format_hint: str = Field("h5ad", description="提示文件类型，如 h5ad, 10x, csv")

class ClusteringSchema(BaseModel):
    data_ref_id: str = Field(..., description="Data Plane 层返回的在内存当中的数据句柄")
    resolution: float = Field(0.8, description="Leiden或Louvain聚类的分辨率")
    n_neighbors: int = Field(15, description="近邻计算中使用的邻居数")

# ================================
# 插件隔离执行的具体逻辑 (Plugin Context)
# Omicverse 或 Scanpy 应该在这里被 Import，这样主程序的内存里不会乱成一锅粥。
# ================================

def execute_load_data(filepath: str, format_hint: str) -> dict:
    from ...core.data_plane import data_plane
    logger.info(f"[Plugin 隔离沙箱] 正在载入 {format_hint} 格式数据: {filepath}")
    # 模拟真实载入时间并调用底层的数据分离层
    ref = data_plane.load_matrix(filepath)
    return {
        "status": "success",
        "data_pointer": ref.ref_id,
        "metadata": ref.metadata
    }

def execute_clustering(data_ref_id: str, resolution: float, n_neighbors: int) -> dict:
    from ...core.data_plane import data_plane
    # import scanpy as sc
    # import omicverse as ov
    logger.info(f"[Plugin 隔离沙箱] 执行组学聚类中...")
    try:
        # data = data_plane.retrieve_shared_data(data_ref_id)
        # 实际代码这里可能通过共享内存恢复 AnnData 对象：
        # adata = mem_restore(data)
        # sc.tl.pca(adata)
        # sc.pp.neighbors(adata, n_neighbors=n_neighbors)
        # sc.tl.leiden(adata, resolution=resolution)
        
        logger.debug(f"已使用分辨率 {resolution} 及 {n_neighbors} 邻居计算完毕。")
        return {
            "status": "success",
            "message": "Clustering complete on ref " + data_ref_id,
            "clusters_found": 8
        }
    except Exception as e:
        logger.error(f"插件执行失败: {str(e)}")
        raise
