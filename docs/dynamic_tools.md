# Dynamic Tool Registry

工具体系：

```text
DynamicToolRegistry
├── StaticToolProvider
├── RagToolProvider
├── McpToolProvider
└── SkillToolProvider

ToolPackBuilder
→ ToolPolicy
→ PermissionEngine
→ ToolPack
```

原则：不要 all tools -> model，要 task-specific tool pack -> model。
