# Workspace / Sandbox Layer

`workspace/` 负责：

- workspace 生命周期
- 文件系统隔离
- artifact 管理
- Python / Shell 执行器
- sandbox policy
- cleanup policy

生产中可以替换为 Docker / Kubernetes / Firecracker / 内部沙箱服务。
