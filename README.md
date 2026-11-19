# MatrixPhysics · 多 Agent 物理仿真沙盒

基于多 Agent 的沉浸式物理实验动态仿真沙盒，使用 [Streamlit](https://streamlit.io) 构建。
通过内联 HTML/Canvas 渲染引擎，实现高帧率粒子系统物理模拟（如 Maxwell-Boltzmann 速率分布等），无需外部 API 与 CDN。

## 功能特性

- 🧮 内置多套物理实验预设（抛体运动、光的折射与全反射、导体棒切割磁感线等）
- 🎛️ 三项核心可调参数，可在仿真画布底部实时拖动，无需重新生成页面
- 📊 实时速率直方图 + 理论 Maxwell-Boltzmann 分布拟合曲线
- ⚛️ 内联 Canvas 高帧率粒子引擎，零外部依赖
- 🧠 多 Agent 流水线：物理原理拆解 → 仿真引擎 → 代码合规自检
- 📝 考点卡片、易错点、典型例题与答案解析

## 环境要求

- Python 3.9+
- Streamlit ≥ 1.32

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 运行应用
streamlit run app.py
```

然后在浏览器中打开终端输出的本地地址（默认 http://localhost:8501）。

## 项目结构

```
.
├── app.py            # 主应用：Streamlit UI + 物理仿真引擎 + 渲染管线
└── requirements.txt  # Python 依赖
```

## 技术说明

- 仿真与渲染全部通过 `components.html` 注入的自包含 HTML/Canvas 前端完成
- 后端由多 Agent 流水线将物理模型规格化并生成对应的实时渲染脚本
- 物理实验参数（温度/玻璃折射率/磁感应强度等）在前端实时可调并即时生效
