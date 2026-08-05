# novel-imagepost-serial

**小说→伪纪实图文连载管线**（Hermes Agent skill）

把小说/故事片段改编成第一人称伪纪实悬疑风格的图文连载（抖音 slides 格式），支持跨集角色一致性和连载伏笔管理。

## 这是什么

一个 [Hermes Agent](https://github.com/NousResearch/hermes-agent) 的 skill，包含：

- **剧本方法论**：核心梗定位 → 六要素梗概 → 人物小传 → 起承转合分集 → △分镜体剧本（改编自 GitHub 高星项目 [liangdabiao/Seedance2-Storyboard-Generator](https://github.com/liangdabiao/Seedance2-Storyboard-Generator)，2k★）
- **题材公式**：AI 伪纪实悬疑恐怖图文的结构模板（平静铺垫→异常事件→调查升级→恐怖预警卡→悬念收尾，每集 20-30 图）
- **设定圣经机制**：人物卡 C01+/场景卡 S01+/道具卡 P01+ 编号系统 + 伏笔台账，保证连载跨集一致性
- **生产模板**：`templates/overlay_doc_subtitles.py` —— PIL 叠字脚本（底部字幕 + 相机日期水印 + 恐怖预警卡）

## 目录结构

```
SKILL.md                                  # 主工作流（6阶段管线）
references/
├── sbg-script-and-storyboard.md          # 剧本格式+人物小传+资产编号（图文适配版）
├── sbg-conversion-tool.md                # 故事→剧本转换工具（六要素/镜头语言速查）
└── sbg-original-skill.md                 # SBG 原版 skill 存档（版权归原作者）
templates/
└── overlay_doc_subtitles.py              # 伪纪实叠字模板
```

## 安装

把整个目录复制到 Hermes Agent 的 skills 目录：

```bash
cp -r novel-imagepost-serial ~/.hermes/skills/media/
```

然后在对话中说"把这篇小说改编成伪纪实图文连载"即可触发。

## 依赖

- 图像生成：火山方舟 Ark seedream API（见 Hermes 的 `volcengine-ark-media` skill）
- 叠字：Python PIL（`pip install pillow`）
- 字体：Noto Sans CJK（`/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc`）

## 版权说明

- 剧本/分镜方法论改编自 [liangdabiao/Seedance2-Storyboard-Generator](https://github.com/liangdabiao/Seedance2-Storyboard-Generator)，感谢原作者开源分享
- `references/sbg-original-skill.md` 为原项目 SKILL.md 存档，版权归原作者，仅供学习参考
- 使用本管线改编小说时：需自行获得原著授权或仅做个人二创，画面使用 AI 生成，发布时按平台要求标注 AI 生成声明

## License

MIT（原创部分）；引用的 SBG 内容版权归原作者。
