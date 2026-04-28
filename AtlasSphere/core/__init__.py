# AtlasSphere 核心引擎

架构准则：
- 数据层：`data_plane.py` 负责隔离大量数据并对外提供内存引用（或Arrow共享内存池）句柄。
- 控制层：`control_plane.py` 用于接收、分发和调度无数据的命令与JSON Schema验证。

此模块拒绝大模型幻觉代码直接运行，必须通过限定的插件沙盒中严格类型的回调执行。
