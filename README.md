
<h1 align="center">🌌 AtlasSphere</h1>

<p align="center">
  <strong>下一代为生物信息与医学 Agent 打造的“零拷贝”分布式调度与自代码进化引擎</strong>
</p>

<p align="center">
  <a href="https://github.com/shaoleishen/AtlasSphere/stargazers"><img src="https://img.shields.io/github/stars/shaoleishen/AtlasSphere?style=for-the-badge&color=yellow" alt="Stars Badge"/></a>
  <a href="https://github.com/shaoleishen/AtlasSphere/network/members"><img src="https://img.shields.io/github/forks/shaoleishen/AtlasSphere?style=for-the-badge&color=orange" alt="Forks Badge"/></a>
  <a href="https://python.org/"><img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python Badge"/></a>
  <a href="https://scanpy.readthedocs.io/en/stable/"><img src="https://img.shields.io/badge/Powered_by-Scanpy_%7C_Omicverse-4bc51d?style=for-the-badge" alt="Scanpy Badge"/></a>
  <a href="https://github.com/shaoleishen/AtlasSphere/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-purple?style=for-the-badge" alt="MIT License"/></a>
</p>

---

## 💡 Why AtlasSphere?

当大语言模型（LLM）遇见海量的单细胞多组学数据（30GB+ `.h5ad`），传统 Agent 正在遭遇毁灭性的打击。**AtlasSphere 正是为了终结这些噩梦而诞生的基础设施！**

| 传统生物信息 Agent 的痛点 ❌ | AtlasSphere 洁净室架构 ✅ |
| :--- | :--- |
| **严重内存溢出 (OOM)**: 将巨型矩阵数据直接压入通讯流，瞬间撑爆服务器。| **物理分离与零拷贝**: 引入“数据层与控制层双平面解耦”，沙盒间全程仅传输 UUID 句柄！|
| **裸奔的盲目执行**: 简单粗暴地让模型 `exec()` 它想出的一大串 Python 字符。| **基于 MCP 与 Pydantic 的沙河隔离**: 强制要求结构化调用，并在 AST 测试池中干跑验证！|
| **算法库跟不上时代**: 提前封死的计算库只能做固定事，碰到极前沿的新算法直接罢工。| **代码即时自治进化（Code Evolution）**: Coder+Critic自主写代码 -> 干跑验证 -> **核心免重启热插拔（Hot-reload）！** |

---


## 🚀 极其精简的部署 (10 秒极速拉起)

抛弃沉冗且环境不一的代码库。AtlasSphere 提倡极度精干轻量级的底盘，它按需下载真正属于你的重型生信包。

### 1. 独立安装（首推使用 `uv`）

```bash
git clone https://github.com/shaoleishen/AtlasSphere.git
cd AtlasSphere

# 闪电配置环境
uv venv --python 3.10

# 仅在这时候引入包含 Scanpy / Anndata 在内的核心组学轮子
uv pip install -e .[omics]
```

### 2. 守护模式起动
```bash
atlas-api
# Server runs gracefully at http://127.0.0.1:8000
```
*(同时支持无缝衔接模型上下文协议 `MCP`，实现 Claude Desktop 本地超强挂载能力。)*

---

## 📂 整洁的工业级项目结构
每一个文件，都是解决性能或安全妥协的关键拼图：

```text
AtlasSphere/
├── agents/
│   ├── base_agent.py          # 纯 Function Calling 驱动的强类型代理 
│   └── evolve_agent.py        # 负责代码升级自进化的神级 Coder 引擎
├── core/
│   ├── data_plane.py          # 💾 管理 50GB 数据零拷贝传递的内存引用锁
│   ├── control_plane.py       # ⚡ 包含 importlib 高频热加载引擎的微服务神经中枢
│   └── sandbox_eval.py        # 🛡️ 基于 AST 以及 PBMC 仿真的隔离验毒池
├── gateway/
│   └── server.py              # 对外的轻盈躯盘接口
└── plugins/
    ├── single_cell/           # 静态原子业务算子集合
    └── dynamic/               # 🌀 存放所有由大模型自反馈新生成的算法文件地带！
```

---

## 🛠 开发扩展属于你的流

AtlasSphere 强制规范每一次的新工具并轨。
不再有毫无章法的写进全局的 `import scanpy as sc`（这会卡死并发队列），在 AtlasSphere 中只需如下规整你的单细胞微服务：

```python
# plugins/my_plugin.py
def execute_my_shiny_algorithm(data_ref_id: str, threshold: float) -> dict:
    # 💥 必须通过分离面的 UUID 进行数据打通！
    from ...core.data_plane import data_plane 
    
    # 🧊 强制要求在计算执行域内部按需懒加载 (Lazy Import) 生信厚库，保护宿主机内存。
    import scanpy as sc 

    # 享受隔离沙暴带给你的纯净计算体验...
    return {"status": "success", "msg": "分析圆满执行于沙盒中！"}
```
随后，向控制面递交该新武备：
```python
control_plane.register_command_handler("Safe_Shiny", execute_my_shiny_algorithm)
```

---

## 🤝 诚邀贡献 (Contributing)

我们欢迎任何关于新分析图谱加入、分布式调度改进及动态框架健壮性的 PR 与 Issue！在这个领域，由 AI 生成的每一行可靠的生物计算新指令，都意味着更贴近下一次生物医学的重大突破！

## 📜 协议 (License)
遵循 [MIT License](LICENSE) 开源发布。
*Crafted for the future of decentralized bio-informatics scaling.*
