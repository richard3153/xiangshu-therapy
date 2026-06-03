# Eight Diagrams Numerology Therapy (Bagua Xiangshu)
### 八卦象数疗法 — Interactive Formula Query System

[中文说明](README.md) | English Version

---

## About / 关于

**English:** An interactive query tool for Ba-Gua Eight Diagrams Numerology Therapy (八卦象数疗法), a traditional Chinese wellness practice using specific number combinations to address health concerns.

**中文:** 八卦象数疗法交互式查询工具，源自李山玉老师的自然疗法体系。

**⚠️ Disclaimer / 免责声明:** This software is for **entertainment and reference only**. It cannot replace professional medical diagnosis or treatment. Please seek qualified medical care for any health concerns. / 本软件仅供娱乐参考，不能替代医疗诊断和治疗，如有疾病请及时就医。

---

## Features / 功能特点

- **557+ formulas** / 557+条配方
- **830+ symptom keywords** / 830+个症状关键词
- **Bilingual**: Chinese & English / 双语支持
- **CLI & GUI** versions / 命令行和图形界面版本
- **Copy formula to clipboard** / 一键复制象数到剪贴板
- **Favorites** / 收藏功能

---

## Quick Start / 快速开始

### Bilingual Launcher (Recommended) / 双语启动器（推荐）
```bash
python xiangshu.py
# Select 1 for Chinese, 2 for English
```

### English CLI / 英文命令行
```bash
python xiangshu_en.py
```

### GUI / 图形界面
```bash
python xiangshu_gui.py        # Chinese GUI
python xiangshu_gui_bilingual.py  # Bilingual GUI
```

---

## File Structure / 文件结构

| File | Description |
|------|-------------|
| `xiangshu.py` | Bilingual launcher / 双语启动器 |
| `xiangshu_en.py` | English CLI only / 纯英文命令行 |
| `xiangshu_gui.py` | Chinese GUI / 中文图形界面 |
| `xiangshu_gui_bilingual.py` | Bilingual GUI / 双语图形界面 |
| `xiangshu_data.py` | Formula database (Chinese) / 配方数据库（中文） |
| `xiangshu_data_en.py` | Formula database (English) / 配方数据库（英文） |
| `README.md` | Chinese README / 中文说明 |
| `README_en.md` | English README / 英文说明 |

---

## Eight Trigrams Number Reference / 八卦象数对照

| Number | Trigram | Element | Organ | Function |
|--------|---------|---------|-------|----------|
| **1** | 乾 Qian | Metal | Lung / Large Intestine | 补肺、大肠 |
| **2** | 兑 Dui | Metal | Lung / Large Intestine | 泽肺、利咽 |
| **3** | 离 Li | Fire | Heart / Small Intestine | 安心火、通血脉 |
| **4** | 震 Zhen | Wood | Liver / Gallbladder | 疏肝利胆 |
| **5** | 巽 Xun | Wood | Liver / Gallbladder | 疏风、祛湿 |
| **6** | 坎 Kan | Water | Kidney / Bladder | 补肾、壮骨 |
| **7** | 艮 Gen | Earth | Spleen / Stomach | 健脾胃 |
| **8** | 坤 Kun | Earth | Spleen / Stomach | 养脾 |
| **0** | — | — | — | 调和阴阳、循环辅助 |

---

## Usage / 使用方法

### Search / 搜索
```
search headache
search 心悸
```
- Supports Chinese & English symptoms
- Supports fuzzy matching
- Results sorted by formula

### Formula Explanation / 象数说明
- Each formula = number combination (e.g., `640` = 6坎Kan + 4震Zhen + 0)
- Numbers can be followed by trigram name in parentheses for reference
- `0` = harmonizer, often used between or after main numbers

### Copy / 复制
Double-click a recipe row in GUI, or use `copy` button to copy the number formula to clipboard.

---

## License / 许可证

For entertainment and reference only. Not for medical use.

---

## Credits / 致谢

- Ba-Gua Numerology Therapy originally developed by 李山玉 (Li Shanyu)
- Formula data collected from public sources
- Open source project, welcome contributions
