# Hooks Lifecycle

`hooks/` 负责确定性生命周期钩子：

- before_prompt_build
- after_prompt_build
- before_model_call
- after_model_call
- before_tool_call
- after_tool_call
- before_subagent_dispatch
- after_subagent_finish
- before_final_answer
- on_error

Hooks 用于规则校验、审计、脱敏、指标、告警、外部系统联动。
