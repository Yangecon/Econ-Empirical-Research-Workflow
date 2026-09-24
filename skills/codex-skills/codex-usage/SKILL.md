---
name: codex-usage
description: 查看当前 Codex 用量、剩余额度及重置时间。适用于用户询问“Codex 额度还剩多少”“何时刷新”或需要区分 ChatGPT 套餐额度与 API 用量时。
---

# 查看 Codex 额度

先确认用户使用的是 ChatGPT 套餐登录，还是 API key。两者的用量和限制不同，不能互相代替。

## ChatGPT 套餐

1. 在本机运行 `python scripts/read_usage.py`（路径相对于本 skill）。脚本读取本机 Codex 会话日志中最近一次服务端返回的 `rate_limits`，只输出额度字段，不输出聊天内容或凭据。报告其 `observed_at_local`；这是最近一次记录的快照，并非即时向服务器查询。超过 15 分钟的快照不可称为当前额度。日志字段是本机实现细节，版本变化时需重新核实。
2. 若需要刷新或核对，查看当前 Codex 桌面版或 CLI 会话的 `/status`。桌面版会显示当前聊天的上下文用量和可用的速率限制信息；CLI 可在活动会话中查看剩余额度。若代理不能执行此命令，不能假装已执行。
3. 需要完整账号视图时，打开 [Codex 用量仪表板](https://chatgpt.com/codex/settings/usage)，读取已登录账号页面实际显示的各用量窗口、剩余额度、重置时间和 credits。页面要求登录时说明无法读取实时数字。
4. 报告时注明查看时间和时区，并逐项保留来源的模型、窗口和单位。脚本的 `remaining_percent_approx` 是用 `100 - used_percent` 算出的近似值。不要把上下文窗口剩余量当成账号额度，也不要根据模型消息数估算值反推用户额度。未提供的项目写“未显示”或“未能核实”。

## API key

使用 [OpenAI Platform 用量](https://platform.openai.com/usage) 和 [限制设置](https://platform.openai.com/settings/organization/limits) 查对应组织或项目。API 的费用、预算及请求或 token 速率限制，与 ChatGPT 套餐里的 Codex 额度分开报告。不要为了查询而发送一次付费 API 请求。

## 资料与核实

- [OpenAI Docs：当前用量限制及 `/status`](https://learn.chatgpt.com/docs/pricing)
- [OpenAI Docs：桌面版斜杠命令](https://learn.chatgpt.com/docs/reference/slash-commands)
- [OpenAI Docs：API 速率限制](https://developers.openai.com/api/docs/guides/rate-limits)

官方页面和界面可能变化；遇到入口或字段变化时先重新核实。不读取浏览器凭据或认证文件，不使用非公开网络接口或第三方额度估算工具。
