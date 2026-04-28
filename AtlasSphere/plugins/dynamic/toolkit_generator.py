import os
from loguru import logger

DYNAMIC_DIR = os.path.dirname(os.path.abspath(__file__))

def save_new_plugin_code(plugin_name: str, code_content: str) -> str:
    """
    将大模型 (CoderAgent) 吐出的代码文本强行落盘为一个有效的 Python 文件。
    返回保存的完整路径，及挂载名 (module_name)。
    """
    # 确保没有恶意路径穿越
    safe_name = "".join(c for c in plugin_name if c.isalnum() or c == "_")
    target_file = os.path.join(DYNAMIC_DIR, f"{safe_name}.py")
    
    logger.info(f"正在落盘新的微组件脚本: {target_file}")
    
    with open(target_file, "w", encoding="utf-8") as f:
        f.write(code_content)
        
    module_name = f"plugins.dynamic.{safe_name}"
    return module_name
