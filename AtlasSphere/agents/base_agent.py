import json
from loguru import logger
import litellm
from pydantic import BaseModel
from typing import List, Dict, Optional, Type

from .control_plane import control_plane

class AtlasAgent:
    """
    放弃让 Agent 执行野代码的 `PantheonOS` 传统。
    这是一个具有确定性（Deterministic）、强类型（Strong Typed）的结构化调度 Agent。
    利用 LLM 天然的 Function Calling API 来严禁幻觉。
    """
    def __init__(self, name: str, instructions: str, model: str = "gpt-4o"):
        self.name = name
        self.instructions = instructions
        self.model = model
        self.tools_schema = []
        self.tools_map = {}

    def add_plugin_tool(self, tool_name: str, description: str, pydantic_schema: Type[BaseModel], executor_name: str):
        """
        向大模型端显式的公开一个严谨封装的插件工具。
        这个工具的调用命令只能发送到预先注册在 ControlPlane 上的执行网关，不再能动态生成野脚本。
        """
        schema = pydantic_schema.model_json_schema()
        self.tools_schema.append({
            "type": "function",
            "function": {
                "name": tool_name,
                "description": description,
                "parameters": schema
            }
        })
        self.tools_map[tool_name] = executor_name

    async def execute_intent(self, user_query: str) -> dict:
        """
        分析意图并驱动大模型吐出明确执行函数的结构体，而不是一段可以跑挂系统的 Python 源码。
        """
        logger.info(f"Agent [{self.name}] 正在分析意图...")

        messages = [
            {"role": "system", "content": self.instructions},
            {"role": "user", "content": user_query}
        ]

        response = await litellm.acompletion(
            model=self.model,
            messages=messages,
            tools=self.tools_schema if self.tools_schema else None,
            tool_choice="auto"
        )
        
        res_message = response.choices[0].message
        
        if res_message.tool_calls:
            results = []
            for tool_call in res_message.tool_calls:
                t_name = tool_call.function.name
                t_args = json.loads(tool_call.function.arguments)
                logger.info(f"LLM 结构化决断: 需调用 `{t_name}` 载荷: {t_args}")
                
                # 寻找 Control Plane 中安全的转发目标
                if t_name in self.tools_map:
                    safe_command_target = self.tools_map[t_name]
                    # 发送安全信号
                    res = await control_plane.emit(safe_command_target, t_args)
                    results.append({"tool": t_name, "status": "success", "result": res})
            return {"type": "tool_calls_executed", "data": results}
        else:
            logger.info("大模型回复了正常的语言，没有调用插件。")
            return {"type": "text", "data": res_message.content}
