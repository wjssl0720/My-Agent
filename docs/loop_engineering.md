# Loop Engineering

loop 骨架：

```text
1. Build context
2. Resolve tools
3. Load skills
4. Plan task
5. Build dynamic system prompt
6. Model decides next action
7. Execute tool or subagent
8. Append observation
9. Compact context
10. Stop or continue
```

生产时把 `LocalModelPolicy` 换成 `AgentScopeModelPolicy`。
