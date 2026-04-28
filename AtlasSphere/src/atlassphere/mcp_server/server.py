import sys
from loguru import logger
from mcp.server.fastmcp import FastMCP

# 根据绝对包路径引入工具
from atlassphere.plugins.single_cell.toolkit import register_sc_tools_for_mcp

def main():
    """MCP 服务器入口（StdIO）"""
    logger.remove()
    logger.add(sys.stderr, level="INFO")  # 避免破坏 StdIO 标准流通讯阻塞 MCP 协议

    logger.info("Starting AtlasSphere MCP Endpoint Server ...")
    
    mcp = FastMCP("AtlasSphere-Omni-Engine", dependencies=["scanpy", "loguru"])
    register_sc_tools_for_mcp(mcp)
    
    try:
        # FastMCP 会挂载事件队列，开始接受 Claw Code CLI, Claude Desktop 的 RPC 唤醒调用
        mcp.run()
    except Exception as e:
        logger.exception("MCP Subsystem Crash")

if __name__ == "__main__":
    main()
