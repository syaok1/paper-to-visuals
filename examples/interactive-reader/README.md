# 交互阅读器结构预览

下载或克隆仓库后，直接用浏览器打开 [论文导览.html](论文导览.html)。配套 [论文讲解.md](论文讲解.md) 可以独立阅读。

本示例有八章，演示首页简图、章节详细图和连续讲解三个层次。仅 04 使用 DenseReward 的局部实验设计内容；其他章节是结构示意。请勿将本示例标为完整的 DenseReward 论文导读。

`content.json` 和 `figures/` 是生成这两份文件的输入。在仓库根目录运行：

```bash
python3 skills/paper-to-visuals/scripts/build_reader.py \
  examples/interactive-reader/content.json \
  --output-dir output/demo
```

图形来源与许可说明见 [来源与致谢](../../ACKNOWLEDGEMENTS.md)。
