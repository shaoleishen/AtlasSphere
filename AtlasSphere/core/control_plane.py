from typing import List, Dict, Any, Callable
from loguru import logger
import asyncio
import importlib
import sys

class ControlPlane:
    """
    分离出来的信令与控制层 (Control Plane)。
    负责收发轻量级意图 (Intent) 和工具调用元数据 (Tools Metadata)，
    严格禁止将组学原始大块数据混入此队列，防止阻塞或 OOM (Out Of Memory)。
    """
    def __init__(self):
        self._handlers: Dict[str, Callable] = {}
        logger.info("初始化 AtlasSphere 安全信号传递层 (Control Plane)")

    def register_command_handler(self, command_name: str, handler: Callable):
        """注册一个验证通过的，强类型的、安全的函数命令，防止类似代码注入的问题。"""
        self._handlers[command_name] = handler
        logger.debug(f"已注册可信安全指令: {command_name}")

    def hot_load_dynamic_plugin(self, module_name: str, function_name: str, command_name: str):
        """
        动态热加载：让系统在不重启的情况下引入新模块并注册 handler。
        module_name 类似于：plugins.dynamic.your_new_tool
        """
        try:
            logger.info(f"正在进行核心热加载: 模块={module_name}, 函数={function_name}")
            # 如果曾经加载过，强制重载确保是最新的进化版本
            if module_name in sys.modules:
                mod = importlib.reload(sys.modules[module_name])
            else:
                mod = importlib.import_module(module_name)
            
            handler_func = getattr(mod, function_name)
            self.register_command_handler(command_name, handler_func)
            logger.info(f"✨ 热加载成功: 成功将 {module_name}.{function_name} 挂载为了 `{command_name}` !!!")
        except Exception as e:
            logger.error(f"热加载微服务失败，模块可能存在语法故障: {str(e)}")
            raise

    async def emit(self, command_name: str, payload: dict) -> Any:
        """分发经过安全层过滤的执行命令"""
        if command_name not in self._handlers:
            logger.error(f"严重: 未经授权或未注册的安全回调被触发 -> {command_name}")
            raise PermissionError(f"Command '{command_name}' is not registered in the safe control plane namespaces.")
        
        handler = self._handlers[command_name]
        
        logger.info(f"Control Plane 触发信号 -> {command_name}")
        # 如果是异步处理器
        if asyncio.iscoroutinefunction(handler):
            return await handler(**payload)
        return handler(**payload)

control_plane = ControlPlane()
