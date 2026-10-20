# 来源与致谢

## 阅读框架

六部分阅读结构参考了设计过程中提供的论文阅读模板，原来源标识为“论文标书的 Zoey_bilibili”。此仓库重新组织了说明文字，并增加可视化表达、交互分层、实验对照和证据核对要求。仓库未收录原始模板文件；来源标识不表示原作者参与或认可本项目。

## Skill 组织与安装

仓库组织和安装说明参考：

- [Vercel Agent Skills](https://github.com/vercel-labs/agent-skills)：按 skill 目录组织，并在 README 提供用途与安装入口。
- [Skills CLI](https://github.com/vercel-labs/skills)：GitHub 仓库安装、选择 skill 与选择 agent 的方式。
- [Codex skills 文档](https://developers.openai.com/codex/skills/)：`SKILL.md`、引用资料、脚本及 `agents/openai.yaml` 的组织方式。

本项目独立维护，与上述项目无隶属或官方背书关系。

## DenseReward 局部示例

原文：Yu Fang 等，*DenseReward: Dense Reward Learning via Failure Synthesis for Robotic Manipulation*，arXiv:2607.13033v1。

- [原文 HTML](https://arxiv.org/html/2607.13033v1)
- [版本与作者信息](https://arxiv.org/abs/2607.13033v1)
- 使用范围：§4.1–4.4 与附录 C 的实验比较设置。

`examples/interactive-reader/figures/04-densereward.png` 是根据上述方法说明重新制作、经逐项查看核对的 AI 辅助示意图。图中的机器人场景用于解释流程，未直接复制论文图像，不代表真实实验照片。它展示离线评分、候选动作评分和策略学习中的比较关系，不报告新的实验结果。

示例其余章节用于说明阅读结构。所有示例均不构成论文作者的官方材料，也不表示完成了科学实验复现。
