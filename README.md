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

## 一键安装

```bash
# 一键克隆、创建虚拟环境、安装依赖并启动（Linux / macOS / Git Bash）
git clone https://github.com/Nicky-eight/physics-simulation.git
cd physics-simulation
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

### Windows PowerShell 一键安装

```powershell
git clone https://github.com/Nicky-eight/physics-simulation.git
cd physics-simulation
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

> 💡 若希望一次性完成「安装 + 运行」，可将依赖安装与启动合并为一条命令：
> `pip install -r requirements.txt && streamlit run app.py`

## 部署与运行步骤

### 1. 本地运行
```bash
streamlit run app.py
```
浏览器会自动打开终端输出的本地地址（默认 `http://localhost:8501`）。如需修改端口：
```bash
streamlit run app.py --server.port 8501
```

### 2. 局域网访问
在启动命令中加入 `--server.address`，让局域网内其他设备也可访问：
```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

### 3. 云端一键部署（Streamlit Community Cloud）
1. 将代码推送到本仓库 `main` 分支；
2. 登录 [Streamlit Community Cloud](https://streamlit.io/cloud)，点击 **New app**；
3. 选择本仓库与分支 `main`，主入口文件填写 `app.py`；
4. 点击 **Deploy** 即可生成公网访问链接。

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

## 使用的组件与技术说明

- **Streamlit**：用于构建 Web 应用整体页面框架、侧边栏实验大纲导航与交互控件，并通过 `streamlit.components.v1.html` 内嵌仿真前端。
- **HTML5 Canvas & JavaScript**：用于驱动物理运动计算、刚体碰撞与反弹、实时 v-t 曲线绘制以及动画帧循环。
- **多 Agent 流水线**：将物理模型规格化并生成对应的实时渲染脚本，实现「物理原理拆解 → 仿真引擎 → 代码合规自检」。
- **零外部依赖**：仿真与渲染全部通过 `components.html` 注入的自包含 HTML/Canvas 前端完成，无需外部 API 与 CDN；物理实验参数（温度/玻璃折射率/磁感应强度等）在前端实时可调并即时生效。

## 华为云码道在项目开发中的应用总结

在本次项目开发中，我围绕“高中物理课堂可直接演示”的核心目标，借助华为云码道完成了从功能原型搭建到界面与交互优化的全流程迭代：

- **快速构建多模块仿真框架**：通过自然语言描述教学场景与实验需求，快速生成包含力学/碰撞、电磁学、光学与波动、热学等模块的交互应用骨架。
- **高效定位与修复交互问题**：针对界面文字对比度不足、组件位置重叠、缺少碰撞与暂停控制、需要实时 v-t 曲线等问题，通过多轮对话持续优化前端布局与仿真逻辑。
- **聚焦产品设计与验收把关**：依托码道加速代码实现，让我能够把精力集中在课堂教学实用性、界面清晰度与演示效果验收上，高效完成了作品开发。
