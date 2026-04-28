from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from loguru import logger

from ..agents.base_agent import AtlasAgent
from ..plugins.single_cell.toolkit import LoadDataSchema, ClusteringSchema, execute_load_data, execute_clustering
from ..core.control_plane import control_plane
from ..agents.evolve_agent import evolve_orchestrator

app = FastAPI(title="AtlasSphere API Gateway", version="0.1.0", description="AtlasSphere 无头生物智能调度网关")

# 1. 在平台初始化时注册所有受信任且校验的工具进 ControlPlane
control_plane.register_command_handler("Safe_LoadData", execute_load_data)
control_plane.register_command_handler("Safe_Clustering", execute_clustering)

# 2. 建立统御代理并赋予工具声明
sc_agent = AtlasAgent(
    name="Atlas-ScRNA-Orchestrator",
    instructions="""
    你是一个专业的单细胞生物信息专家系统的指挥官。
    当你收到分析指令时，你必须使用提供的工具进行串行任务调度。
    如果你发现用户的需求超出了现有的处理插件（比如高级的细胞通讯分析），
    你应当调用 `SubmitEvolutionRequest` 把需求发送给底层系统进化处理引擎去尝试自编写工具！
    绝对不要自己编造源码，只允许返回工具的 JSON 规范载荷。
    """
)

sc_agent.add_plugin_tool(
    tool_name="LoadOmicsData",
    description="读取各种生信分析文件返回脱敏的内存引用句柄",
    pydantic_schema=LoadDataSchema,
    executor_name="Safe_LoadData"
)

sc_agent.add_plugin_tool(
    tool_name="LeidenClustering",
    description="利用指定的内存引用句柄对数据进行 leiden 降维聚类",
    pydantic_schema=ClusteringSchema,
    executor_name="Safe_Clustering"
)

# 注册全新的高阶能力触点：发起自进化队列
class EvolveSchema(BaseModel):
    requirement: str
    plugin_name_hint: str

async def trigger_evolution_engine(requirement: str, plugin_name_hint: str):
    logger.info(f"被前端意图触发，交托给进化沙箱处理任务...")
    # 这个动作是在后台执行一连串闭环测试的
    res = await evolve_orchestrator.run_evolution_pipeline(requirement, plugin_name_hint)
    return {"evolution_feedback": res}

control_plane.register_command_handler("Safe_SubmitEvolution", trigger_evolution_engine)

sc_agent.add_plugin_tool(
    tool_name="SubmitEvolutionRequest",
    description="当现有工具满足不了更高级分析请求（如细胞通讯分析、高级图谱连接），提交需求启动后台生信专家系统自动进写代码的管线",
    pydantic_schema=EvolveSchema,
    executor_name="Safe_SubmitEvolution"
)

# API 请求与响应结构
class ChatRequest(BaseModel):
    query: str

@app.post("/api/v1/analyze")
async def handle_analyze_request(req: ChatRequest):
    """
    统一网关接入点。接收自然语言，通过 LLM 转义为具体控制面指令 (Control Intent)，
    最后经过沙箱化的 Plugin 运算完毕后，流出或一次性返回结果。
    如果是涉及到进化的请求，这还会触发底层的长时循环（Evolve Loop）。
    """
    logger.info(f"API GW: 收到来自前端的分析请求: {req.query}")
    try:
        response = await sc_agent.execute_intent(req.query)
        return {"status": "success", "agent_reply": response}
    except Exception as e:
        logger.exception("代理调度出现意外崩溃")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "AtlasSphere is running."}
