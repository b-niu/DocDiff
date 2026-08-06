# DocDiff (文档差异标红工具)

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![GUI](https://img.shields.io/badge/GUI-PySide6-orange)

DocDiff 是一款开源、本地运行的 Word (`.docx`) 文档差异对比与标红导出工具。

## ✨ 核心特性

- **现代 GUI 界面**：采用 PySide6 打造，界面精美，支持**拖拽 (Drag & Drop)** 选择旧文件与新文件。
- **智能输出命名**：自动生成 `新文件名_tracked.docx` 作为默认导出文件，支持自定义路径。
- **高精度 LCS 算法**：采用最长公共子序列（LCS）段落对齐，避免因段落增删导致后文错位。
- **红字标红与删除线**：新增修改内容标红粗体，删除内容标注红色删除线。
- **完全本地安全**：零网络数据传输，保证企业合同与审计文档的绝对隐私安全。

---

## 🚀 快速开始

### 1. 使用 `uv` 安装与启动

推荐使用 [uv](https://github.com/astral-sh/uv) 进行极速环境管理（默认配置清华镜像源）：

```powershell
# 克隆仓库
git clone https://github.com/b-niu/DocDiff.git
cd DocDiff

# 使用 uv 同步依赖
uv sync

# 启动图形界面
uv run python main.py
```

### 2. 使用传统 pip

```powershell
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
python main.py
```

---

## 📖 详细文档

有关项目的架构设计、核心算法与模块拆分，请参阅 [docs/design.md](docs/design.md)。

---

## 📄 开源协议

本项目基于 [MIT License](LICENSE) 开源。
