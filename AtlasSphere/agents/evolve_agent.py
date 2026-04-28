import litellm
from loguru import logger
from ..core.sandbox_eval import verify_code_safety, dry_run_with_benchmark_data
from ..plugins.dynamic.toolkit_generator import save_new_plugin_code
from ..core.control_plane import control_plane

# Coder Agent 指引，指明了双架构的设计与高级要求
CODER_PROMPT = """
你是一个高级生信专家型工程师（CoderAgent）。你的任务是将用户提供的关于单细胞“高级处理、细胞通讯（如CellphoneDB）、空间对接分析”等需求转化为有效的 AtlasSphere 插件。
必须满足双层结构：
1. 提供该函数的 Pydantic Schema 用于入参定义（入参必须包含 data_ref_id 以对接基础数据平面）.
2. 提供隔离的 execute 函数。请只在这个函数内部 import 组学包（比如 scanpy, squidpy，cellphonedb 等），不要写在全局，以避免主系统 OOM。

请仅直接返回原生 Python 代码字符串，不需要用 markdown 标签包围，也不需要解释，纯粹的代码文本。
"""

class EvolveOrchestrator:
    """处理自动自我升级与测试循环的大脑"""
    def __init__(self, model_name: str = "claude-3-5-sonnet"):
        # 用户确认拥有良好生成能力的先进模型: 如 glm, opus 或 kimi
        self.model = model_name
        
    async def run_evolution_pipeline(self, requirement: str, plugin_name_hint: str):
        logger.info(f"[EvolveOrchestrator] 开启进化管线，分析需求: {requirement}")
        
        # 1. 向大模型下达构建代码意图 (CoderAgent phase)
        messages = [
            {"role": "system", "content": CODER_PROMPT},
            {"role": "user", "content": requirement}
        ]
        
        try:
            logger.info("正在唤起先进大模型推理编写底层算法框架...")
            response = await litellm.acompletion(
                model=self.model,
                messages=messages
            )
            raw_code = response.choices[0].message.content.strip()
            # 移除可能带有 ```python 的包裹
            raw_code = raw_code.replace("```python", "").replace("```", "").strip()
            
            # 2. AST 安全审查 (Sandbox check phase 1)
            if not verify_code_safety(raw_code):
                raise ValueError("代码未通过 AST 静态安全审查，内含危险函数。")
            
            # 3. 落地持久化代码
            logger.info("代码安全审核通过，进行保存...")
            module_name = save_new_plugin_code(plugin_name_hint, raw_code)
            
            # 这里的函数名称可以通过大模型结构化的响应约束，或者通过抽象解析获得。
            # 为了范例简单，我们假定模型总是生成 `execute_algorithm`
            expected_func_name = "execute_algorithm"
            
            # 4. 干跑测试 (Sandbox check phase 2 - 依托 PBMC3K)
            is_valid = dry_run_with_benchmark_data(module_name, expected_func_name)
            
            if is_valid:
                # 5. 一切就绪，执行全网系热加载 (Hot Reload API)
                control_plane.hot_load_dynamic_plugin(module_name, expected_func_name, command_name=f"Safe_{plugin_name_hint}")
                logger.success(f"[EvolveOrchestrator] 系统能力进化成功！！！已装载：{plugin_name_hint}")
                return "进化且沙盒测试成功，系统已装载该新沟通功能！"
            else:
                return "新模块验证未通过，被驳回修改。"
                
        except Exception as e:
            logger.error(f"智能体进化队列异常: {str(e)}")
            return f"发生了异常：{str(e)}"

evolve_orchestrator = EvolveOrchestrator(model_name="claude-3-5-sonnet")  # 默认值，可以改用更强的
