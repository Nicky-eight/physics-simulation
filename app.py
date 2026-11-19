"""MatrixPhysics: 基于多 Agent 的沉浸式物理实验动态仿真沙盒。"""

from __future__ import annotations

import html as html_lib
import os
import re
from typing import Any, Dict, List, Tuple

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="MatrixPhysics · 多 Agent 物理仿真沙盒",
    page_icon="⚛",
    layout="wide",
    initial_sidebar_state="expanded",
)

PAGE_CSS = """
<style>
:root{
  --mp-bg:#09090b;
  --mp-cy:#22d3ee;
  --mp-pu:#a855f7;
  --mp-gd:#fbbf24;
}
.stApp{
  background:
    radial-gradient(1100px 560px at 6% -12%, rgba(34,211,238,.12), transparent 62%),
    radial-gradient(900px 520px at 96% 2%, rgba(168,85,247,.13), transparent 60%),
    #09090b;
}
header[data-testid="stHeader"]{background:transparent;}
section[data-testid="stSidebar"]{
  background:linear-gradient(180deg,#0b0b0f,#09090b);
  border-right:1px solid rgba(34,211,238,.14);
}
section[data-testid="stSidebar"] *{color:#f4f4f5 !important;}
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p{color:#e8e8ec !important;}
section[data-testid="stSidebar"] .mp-meta code{color:#f4f4f5 !important;background:rgba(34,211,238,.14);}
section[data-testid="stSidebar"] [data-testid="stSelectbox"] input,
section[data-testid="stSidebar"] [data-testid="stSelectbox"] div[role="combobox"],
section[data-testid="stSidebar"] div[data-baseweb="select"] input,
section[data-testid="stSidebar"] div[data-baseweb="select"] div[role="button"]{
  color:#0b0b0f !important;-webkit-text-fill-color:#0b0b0f !important;
  caret-color:#0b0b0f !important;
}
section[data-testid="stSidebar"] div[data-baseweb="select"] span,
section[data-testid="stSidebar"] div[data-baseweb="select"] div{
  color:#0b0b0f !important;-webkit-text-fill-color:#0b0b0f !important;
}
section[data-testid="stSidebar"] [data-testid="stSelectbox"] button svg,
section[data-testid="stSidebar"] div[data-baseweb="select"] svg{
  fill:#0b0b0f !important;color:#0b0b0f !important;
}
[role="listbox"]{background:#ffffff !important;}
[role="listbox"] [role="option"],
[role="listbox"] [role="option"] *,
div[data-baseweb="popover"],
div[data-baseweb="popover"] li,
div[data-baseweb="popover"] div,
div[data-baseweb="popover"] span{
  color:#0b0b0f !important;-webkit-text-fill-color:#0b0b0f !important;
  background-color:transparent !important;
}
div[data-baseweb="popover"] ul{background:#ffffff !important;}
.mp-hero{
  padding:14px 0 6px;
  border-bottom:1px solid rgba(34,211,238,.10);
  margin-bottom:10px;
}
.mp-hero h1{
  font-family:ui-monospace,"SF Mono",Menlo,Consolas,monospace;
  font-size:30px;font-weight:800;letter-spacing:.10em;margin:0;
  background:linear-gradient(92deg,#22d3ee 0%,#a855f7 55%,#f472b6 100%);
  -webkit-background-clip:text;background-clip:text;color:transparent;
}
.mp-hero p{
  margin:6px 0 0;color:#a1a1aa;font-size:12px;letter-spacing:.16em;
  font-family:ui-monospace,monospace;text-transform:uppercase;
}
.mp-tag{
  display:inline-block;margin-left:10px;padding:2px 8px;border-radius:99px;
  font-size:10px;letter-spacing:.1em;color:#67e8f9;
  border:1px solid rgba(34,211,238,.35);background:rgba(34,211,238,.06);
  vertical-align:middle;
}
div.stButton > button{
  border-radius:10px;
  border:1px solid rgba(34,211,238,.30);
  background:rgba(12,12,16,.72);
  color:#d4d4d8;font-size:12.5px;font-family:ui-monospace,monospace;
  letter-spacing:.02em;transition:all .16s ease;
}
div.stButton > button:hover{
  border-color:#22d3ee;color:#67e8f9;
  box-shadow:0 0 20px rgba(34,211,238,.25);transform:translateY(-1px);
}
div.stButton > button[kind="primary"]{
  background:linear-gradient(92deg,rgba(34,211,238,.16),rgba(168,85,247,.18));
  border-color:rgba(34,211,238,.55);color:#e0f2fe;font-weight:700;
}
div[data-testid="stTextInput"] input{
  background:rgba(9,9,11,.82);
  border:1px solid rgba(34,211,238,.28);
  border-radius:10px;color:#e4e4e7;
  font-family:ui-monospace,monospace;font-size:13.5px;
}
div[data-testid="stTextInput"] input:focus{
  border-color:#22d3ee;box-shadow:0 0 0 1px rgba(34,211,238,.45),0 0 22px rgba(34,211,238,.18);
}
.mp-pipe{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:2px 0 10px;}
.mp-card{
  padding:10px 12px;border-radius:12px;
  background:rgba(12,12,16,.66);
  border:1px solid rgba(63,63,70,.6);
  font-family:ui-monospace,monospace;
}
.mp-card .k{font-size:10px;letter-spacing:.16em;color:#8b8b93;text-transform:uppercase;}
.mp-card .t{font-size:12.5px;color:#d4d4d8;margin-top:3px;font-weight:600;}
.mp-card.on{border-color:rgba(34,211,238,.45);box-shadow:0 0 18px rgba(34,211,238,.10);}
.mp-card.on .k{color:#22d3ee;}
.mp-card.on .t{color:#a5f3fc;}
.mp-card.done{border-color:rgba(168,85,247,.42);}
.mp-card.done .k{color:#a855f7;}
.mp-updateAndRender{
  border-radius:16px;overflow:hidden;
  border:1px solid rgba(34,211,238,.22);
  box-shadow:0 0 60px rgba(34,211,238,.08),0 0 120px rgba(168,85,247,.06);
}
.mp-meta{
  font-family:ui-monospace,monospace;font-size:12px;color:#a1a1aa;
  letter-spacing:.04em;line-height:1.8;
}
.mp-meta b{color:#22d3ee;font-weight:600;}
.katex,.katex *{color:#e2e2e8 !important;}
[data-testid="stExpander"] [data-testid="stMarkdownContainer"] p,
[data-testid="stExpander"] [data-testid="stMarkdownContainer"] li,
[data-testid="stExpander"] [data-testid="stMarkdownContainer"] strong,
[data-testid="stExpander"] [data-testid="stMarkdownContainer"] td,
[data-testid="stExpander"] [data-testid="stMarkdownContainer"] th,
[data-testid="stExpander"] [data-testid="stAlert"] p,
[data-testid="stExpander"] [data-testid="stAlert"] li{color:#e2e2e8 !important;}
[data-testid="stExpanderHeader"],[data-testid="stExpanderHeader"] *{color:#f4f4f5 !important;}
.katex .mord,.katex .mbin,.katex .mrel,.katex .mopen,.katex .mclose{color:#e2e2e8 !important;}
.mp-meta code{
  background:rgba(34,211,238,.08);color:#67e8f9;
  padding:1px 6px;border-radius:5px;font-size:11px;
}
</style>
"""

MODULES: Dict[str, Dict[str, Any]] = {
    "经典力学篇": {
        "icon": "◍",
        "desc": "运动学 · 牛顿定律 · 圆周运动 · 非线性混沌",
        "experiments": ["自由落体运动", "平抛运动", "牛顿第二定律", "匀速圆周运动", "一维碰撞与动量守恒", "混沌双摆运动"],
    },
    "电磁学篇": {
        "icon": "∿",
        "desc": "静电场 · 洛伦兹力 · 电磁感应",
        "experiments": ["洛伦兹力回旋", "库仑定律电场线", "导体棒切割磁感线"],
    },
    "光学与波动篇": {
        "icon": "⌁",
        "desc": "双缝干涉 · 折射与全反射",
        "experiments": ["双缝干涉与衍射", "光的折射与全反射"],
    },
    "热学与原子物理篇": {
        "icon": "✳",
        "desc": "分子动理论 · 玻尔氢原子模型",
        "experiments": ["理想气体分子热运动", "氢原子玻尔模型"],
    },
    "图像实验室": {
        "icon": "📈",
        "desc": "常考图像专题 · x-t / v-t / a-t 三联图",
        "experiments": ["匀变速运动图像", "简谐振动图像"],
    },
}

DEFAULT_EXPERIMENT = "自由落体运动"

PRESETS: List[Tuple[str, str]] = [
    ("⌁ 双缝干涉", "双缝干涉与衍射"),
    ("◍ 双摆混沌", "混沌双摆运动"),
    ("∿ 洛伦兹回旋", "洛伦兹力回旋"),
    ("✳ 理想气体", "理想气体分子热运动"),
]

DOMAIN_LIBRARY: Dict[str, Dict[str, Any]] = {
    "freefall": {
                "live": "h = ½<span data-k='0'>g</span>t<sup>2</sup>　v = <span data-k='0'>g</span>t　a = <span data-k='0'>g</span> − <span data-k='1'>k</span>v<br>h₀ = <span data-k='2'>h₀</span>　v₀ = <span data-k='3'>v₀</span>",
        "exam": {
          "points": [
            "自由落体是 v₀ = 0、a = g 的匀加速直线运动",
            "基本关系：h = ½gt²、v = gt、v² = 2gh"
          ],
          "pitfalls": [
            "有空气阻力时不再是严格自由落体，a 随速度变化",
            "无阻力时落地时间与质量无关，不要误加成质量"
          ],
          "example": "从 20 m 高处自由落体，g 取 10 m/s²，求落地时间与落地速度。",
          "answer": "t = √(2h/g) = 2 s；v = gt = 20 m/s。"
        },
"engine": "freefall",
        "domain": "经典力学 / 运动学",
        "formula": "h = ½gt² ；v = gt ；a = g − k·v²",
        "latex": r"""\begin{aligned}
        h &= \tfrac{1}{2}gt^{2}\\
        v &= gt\\
        a &= g - kv
        \end{aligned}""",
        "laws": ["自由落体运动规律", "牛顿第二定律", "空气阻力与终端速度"],
        "initial": ["初速度 v₀ = 0 m/s", "初始下落高度 h₀ 由滑块给定", "空气阻力与速度平方成正比"],
        "params": [
            {"label": "重力加速度 g", "min": 0.1, "max": 100.0, "value": 9.8, "step": 0.1, "unit": "m/s²", "hint": "决定下落加速度"},
            {"label": "空气阻力系数 k", "min": 0.0, "max": 6.0, "value": 0.15, "step": 0.05, "unit": "—", "hint": "k=0 为理想真空落体"},
            {"label": "初始高度 h₀", "min": 0.5, "max": 40.0, "value": 10.2, "step": 0.5, "unit": "m", "hint": "改变落地时间"},
            {"label": "初速度 v₀", "min": 0.0, "max": 20.0, "value": 0.0, "step": 0.5, "unit": "m/s", "hint": "v₀>0 相当于向下抛出"},
        ],
        "hud": [
            ("时间 t", "h-t", "cy"),
            ("速度 v", "h-v", "pu"),
            ("高度 h", "h-h", "cy"),
            ("加速度 a", "h-a", "gd"),
            ("帧率", "h-fps", "gd"),
        ],
        "tip": "FREE FALL / KINEMATICS",
    },
    "projectile": {
                "live": "x = <span data-k='0'>v₀</span>t　y = ½<span data-k='1'>g</span>t<sup>2</sup><br>h₀ = <span data-k='2'>h₀</span>　v<sub>y</sub> = <span data-k='1'>g</span>t",
        "exam": {
          "points": [
            "平抛运动可分解为水平匀速 + 竖直自由落体",
            "飞行时间只由高度决定：t = √(2h/g)"
          ],
          "pitfalls": [
            "水平位移 x = v₀t 与高度和初速都有关，不能只凭高度判断射程",
            "速度方向随时间变化，v_y = gt 不断增大"
          ],
          "example": "以 10 m/s 水平抛出，抛出点高 5 m，g 取 10 m/s²，求落地时间、水平射程。",
          "answer": "t = √(2×5/10) = 1 s；x = v₀t = 10 m。"
        },
"engine": "projectile",
        "domain": "经典力学 / 抛体运动",
        "formula": "x = v₀t ；y = ½gt² ；v_y = gt ；tanθ = v_y / v₀",
        "latex": r"""\begin{aligned}
        x &= v_0 t\\
        y &= \tfrac{1}{2}gt^{2}\\
        v_y &= gt\\
        \tan\theta &= \frac{v_y}{v_0}
        \end{aligned}""",
        "laws": ["运动的独立性原理", "平抛运动分解", "重力场中的匀变速曲线运动"],
        "initial": ["水平初速度 v₀ 沿 +x 方向", "竖直初速度 v_y0 = 0", "忽略空气阻力"],
        "params": [
            {"label": "水平初速度 v₀", "min": 0.2, "max": 40.0, "value": 3.6, "step": 0.2, "unit": "m/s", "hint": "决定水平射程"},
            {"label": "重力加速度 g", "min": 0.2, "max": 100.0, "value": 9.8, "step": 0.1, "unit": "m/s²", "hint": "决定竖直下落快慢"},
            {"label": "发射高度 h₀", "min": 0.5, "max": 36.0, "value": 8.1, "step": 0.5, "unit": "m", "hint": "决定飞行时间"},
        ],
        "hud": [
            ("时间 t", "h-t", "cy"),
            ("水平位移 x", "h-x", "cy"),
            ("竖直位移 y", "h-y", "pu"),
            ("v_x", "h-vx", "cy"),
            ("v_y", "h-vy", "pu"),
            ("合速度 v", "h-v", "gd"),
            ("帧率", "h-fps", "gd"),
        ],
        "tip": "PROJECTILE MOTION / PARABOLA",
    },
    "newton": {
                "live": "<span data-k='0'>F</span> − <span data-k='2'>μ</span><span data-k='1'>m</span><span data-k='3'>g</span> = <span data-k='1'>m</span>a　v = at",
        "exam": {
          "points": [
            "F_net = ma，先受力分析再列方程",
            "滑动摩擦 f = μN，静止时用最大静摩擦判断是否启动"
          ],
          "pitfalls": [
            "μ 是动摩擦因数，静摩擦不一定等于 μN",
            "合力方向与加速度方向一致，不要与速度方向混淆"
          ],
          "example": "质量 6 kg 的物块受 40 N 水平拉力，μ = 0.15，g 取 9.8 m/s²，求加速度。",
          "answer": "f = μmg = 8.82 N，a = (40 − 8.82)/6 ≈ 5.20 m/s²。"
        },
"engine": "newton",
        "domain": "经典力学 / 动力学",
        "formula": "F_net = F − μmg ；a = F_net / m ；v = at ；x = ½at²",
        "latex": r"""\begin{aligned}
        F_{\text{net}} &= F - \mu mg\\
        a &= \frac{F_{\text{net}}}{m}\\
        v &= at,\quad x = \tfrac{1}{2}at^{2}
        \end{aligned}""",
        "laws": ["牛顿第二定律", "滑动摩擦力定律", "最大静摩擦力判据"],
        "initial": ["物块静止于水平面 x₀ = 0", "竖直方向受力平衡 N = mg", "拉力沿水平 +x 方向恒定"],
        "params": [
            {"label": "水平拉力 F", "min": 0, "max": 400, "value": 40, "step": 5, "unit": "N", "hint": "小于最大静摩擦时物块不动"},
            {"label": "物块质量 m", "min": 0.1, "max": 100.0, "value": 6.0, "step": 0.5, "unit": "kg", "hint": "m 越大加速度越小"},
            {"label": "摩擦系数 μ", "min": 0.0, "max": 2.0, "value": 0.15, "step": 0.01, "unit": "—", "hint": "μ=0 为光滑水平面"},
            {"label": "重力加速度 g", "min": 0.1, "max": 60.0, "value": 9.8, "step": 0.1, "unit": "m/s²", "hint": "改变支持力与最大静摩擦"},
        ],
        "hud": [
            ("加速度 a", "h-a", "cy"),
            ("速度 v", "h-v", "pu"),
            ("位移 x", "h-x", "cy"),
            ("摩擦力 f", "h-f", "gd"),
            ("合外力 F_net", "h-nf", "pu"),
            ("帧率", "h-fps", "gd"),
        ],
        "tip": "NEWTON SECOND LAW / FREE BODY",
    },
    "circular": {
                "live": "v = <span data-k='0'>ω</span><span data-k='1'>r</span>　a = <span data-k='0'>ω</span><sup>2</sup><span data-k='1'>r</span><br>F = <span data-k='2'>m</span><span data-k='0'>ω</span><sup>2</sup><span data-k='1'>r</span>　θ₀ = <span data-k='3'>θ₀</span>",
        "exam": {
          "points": [
            "v = ωr、a_c = ω²r = v²/r、T = 2π/ω",
            "向心力由实际力提供，不是额外的力"
          ],
          "pitfalls": [
            "向心力是效果力，受力分析时不能重复添加",
            "速度沿切线，加速度指向圆心，二者始终垂直"
          ],
          "example": "半径 2 m、角速度 3 rad/s 的匀速圆周运动，求线速度与向心加速度。",
          "answer": "v = ωr = 6 m/s；a_c = ω²r = 18 m/s²。"
        },
"engine": "circular",
        "domain": "经典力学 / 圆周运动",
        "formula": "v = ωr ；a_c = ω²r = v²/r ；T = 2π/ω ；F = mω²r",
        "latex": r"""\begin{aligned}
        v &= \omega r\\
        a_c &= \omega^{2}r = \frac{v^{2}}{r}\\
        T &= \frac{2\pi}{\omega}\\
        F &= m\omega^{2}r
        \end{aligned}""",
        "laws": ["匀速圆周运动学", "向心力公式", "牛顿第二定律的法向形式"],
        "initial": ["小球以角速度 ω 做匀速圆周运动", "轨道半径 r 由滑块给定", "绳长方向恒指向圆心"],
        "params": [
            {"label": "角速度 ω", "min": 0.01, "max": 16.0, "value": 1.4, "step": 0.05, "unit": "rad/s", "hint": "决定线速度与周期"},
            {"label": "轨道半径 r", "min": 0.2, "max": 16.0, "value": 3.9, "step": 0.1, "unit": "m", "hint": "r 越大向心加速度越大"},
            {"label": "小球质量 m", "min": 0.05, "max": 40.0, "value": 1.5, "step": 0.1, "unit": "kg", "hint": "决定所需向心力"},
            {"label": "初始相位 θ₀", "min": 0, "max": 360, "value": 0, "step": 5, "unit": "°", "hint": "选择小球起始位置"},
        ],
        "hud": [
            ("相位 θ", "h-th", "cy"),
            ("线速度 v", "h-v", "pu"),
            ("向心加速度", "h-ac", "cy"),
            ("周期 T", "h-tp", "pu"),
            ("向心力 F", "h-f", "gd"),
            ("帧率", "h-fps", "gd"),
        ],
        "tip": "UNIFORM CIRCULAR MOTION / CENTRIPETAL",
    },
    "mechanics": {
                "live": "g = <span data-k='0'>g</span>　m₂/m₁ = <span data-k='1'>μ</span>　阻尼 = <span data-k='2'>c</span><br>E = T + V",
        "exam": {
          "points": [
            "双摆是确定性混沌系统，对初值极其敏感",
            "无阻尼时机械能守恒；有阻尼时 E 单调减小"
          ],
          "pitfalls": [
            "混沌不等于随机，方程完全确定",
            "小角度才近似简谐，大角度必须用非线性方程"
          ],
          "example": "为什么双摆两次释放的轨迹几乎不可能完全重复？",
          "answer": "因为混沌系统对初值呈指数敏感，微小差异会被迅速放大。"
        },
"engine": "mechanics",
        "domain": "经典力学 / 非线性动力学",
        "formula": "d²θ₁/dt² 与 d²θ₂/dt² 由拉格朗日量 L = T − V 导出 ；E = T + V",
        "latex": r"""\begin{aligned}
        \ddot\theta_1 &= f(\theta_1,\theta_2,\dot\theta_1,\dot\theta_2)\\
        \ddot\theta_2 &= g(\theta_1,\theta_2,\dot\theta_1,\dot\theta_2)\\
        E &= T + V
        \end{aligned}""",
        "laws": ["牛顿第二定律（拉格朗日形式）", "能量守恒与耗散", "对初值极端敏感的确定性混沌"],
        "initial": ["θ₁ = 2.20 rad，θ₂ = 2.40 rad", "ω₁ = ω₂ = 0 rad·s⁻¹", "两杆等长 l₁ = l₂ = 1.0 m"],
        "params": [
            {"label": "重力加速度 g", "min": 0.1, "max": 80.0, "value": 9.8, "step": 0.1, "unit": "m/s²", "hint": "拖动可瞬间改变重力场"},
            {"label": "质量比 m₂/m₁", "min": 0.05, "max": 20.0, "value": 1.0, "step": 0.05, "unit": "—", "hint": "改变耦合强度"},
            {"label": "空气阻尼 c", "min": 0.0, "max": 1.0, "value": 0.0, "step": 0.005, "unit": "—", "hint": "0 为理想守恒系统"},
        ],
        "hud": [
            ("θ₁", "h-t1", "cy"),
            ("θ₂", "h-t2", "pu"),
            ("ω₁", "h-w1", "cy"),
            ("ω₂", "h-w2", "pu"),
            ("总能量 E", "h-e", "gd"),
            ("帧率", "h-fps", "gd"),
        ],
        "tip": "CHAOTIC DOUBLE PENDULUM / RK4",
    },
    "em": {
                "live": "F = <span data-k='1'>q</span>(<span data-k='2'>E</span> + v × <span data-k='0'>B</span>)<br>r = mv/(<span data-k='1'>q</span><span data-k='0'>B</span>)　粒子数 = <span data-k='3'>n</span>",
        "exam": {
          "points": [
            "洛伦兹力 F = qv × B，方向由左手/右手定则判断",
            "回旋半径 r = mv/(|q|B)，周期 T = 2πm/(|q|B)"
          ],
          "pitfalls": [
            "洛伦兹力永远不做功，只改变速度方向",
            "B 与 v 平行时不受洛伦兹力，粒子做直线运动"
          ],
          "example": "电荷 q = 1 C、速度 3 m/s 垂直进入 B = 1 T 的磁场，求回旋半径（取 m = 1 kg）。",
          "answer": "r = mv/(|q|B) = 1×3/(1×1) = 3 m；周期 T = 2πm/(|q|B) ≈ 6.28 s。"
        },
"engine": "em",
        "domain": "电磁学 / 带电粒子动力学",
        "formula": "F = q(E + v × B) ；r_L = m·v⊥ / (|q|·B) ；T_L = 2πm / (|q|·B)",
        "latex": r"""\begin{aligned}
        \mathbf{F} &= q(\mathbf{E} + \mathbf{v}\times\mathbf{B})\\
        r_L &= \frac{m v_\perp}{|q|B}\\
        T_L &= \frac{2\pi m}{|q|B}
        \end{aligned}""",
        "laws": ["洛伦兹力定律", "Boris 能量守恒旋转推进", "E × B 漂移"],
        "initial": ["粒子束沿 +x 方向注入，v ≈ 150 px/s", "磁场沿 ±z 方向均匀分布", "比荷 q/m = 1.0"],
        "params": [
            {"label": "磁感应强度 B", "min": 0.0, "max": 20.0, "value": 1.0, "step": 0.1, "unit": "T", "hint": "B 变大则回旋半径变小"},
            {"label": "电荷量 q", "min": -40.0, "max": 40.0, "value": 1.5, "step": 0.5, "unit": "C", "hint": "负值使回旋方向反转"},
            {"label": "外加电场 E", "min": -40.0, "max": 40.0, "value": 0.0, "step": 0.5, "unit": "V/m", "hint": "非零时出现 E×B 漂移"},
            {"label": "粒子数 n", "min": 1, "max": 40, "value": 5, "step": 1, "unit": "个", "hint": "同时注入的粒子束数量"},
        ],
        "hud": [
            ("磁感应 B", "h-b", "cy"),
            ("电荷 q", "h-q", "pu"),
            ("电场 E", "h-e", "gd"),
            ("回旋半径 r", "h-r", "cy"),
            ("回旋周期 T", "h-t", "pu"),
            ("速率 v", "h-v", "gd"),
            ("帧率", "h-fps", "gd"),
        ],
        "tip": "LORENTZ FORCE / BORIS ROTATION",
    },
    "coulomb": {
                "live": "F = k<span data-k='0'>q₁</span><span data-k='1'>q₂</span> / <span data-k='2'>d</span><sup>2</sup>　E = kQ/r<sup>2</sup>",
        "exam": {
          "points": [
            "库仑定律 F = kq₁q₂/r²，k = 9×10⁹ N·m²/C²",
            "电场线疏密表示场强大小，切线表示方向"
          ],
          "pitfalls": [
            "距离加倍，库仑力变为原来的 1/4，不是 1/2",
            "电场线不相交，也不表示运动轨迹"
          ],
          "example": "两个 +10 μC 的点电荷相距 0.3 m，求它们之间的库仑力。",
          "answer": "F = 9×10⁹ × (10⁻⁵)² / 0.09 ≈ 10 N，方向相互排斥。"
        },
"engine": "coulomb",
        "domain": "电磁学 / 静电场",
        "formula": "E = kQ/r² ；F = k·q₁q₂/r² ；场线切线方向即 E 的方向",
        "latex": r"""\begin{aligned}
        E &= k\frac{Q}{r^{2}}\\
        F &= k\frac{q_1q_2}{r^{2}}
        \end{aligned}""",
        "laws": ["库仑定律", "电场叠加原理", "电场线的基本性质"],
        "initial": ["两个点电荷固定在水平轴上", "场线由正电荷发出、终止于负电荷", "介质为真空，k = 9×10⁹ N·m²/C²"],
        "params": [
            {"label": "电荷量 q₁", "min": -200.0, "max": 200.0, "value": 10.0, "step": 2.0, "unit": "μC", "hint": "正值发出场线，负值汇入场线"},
            {"label": "电荷量 q₂", "min": -200.0, "max": 200.0, "value": -6.0, "step": 2.0, "unit": "μC", "hint": "同号相斥、异号相吸"},
            {"label": "电荷间距 d", "min": 0.5, "max": 60.0, "value": 7.5, "step": 0.5, "unit": "cm", "hint": "距离加倍则库仑力变为 1/4"},
        ],
        "hud": [
            ("中点场强 E", "h-e", "cy"),
            ("库仑力 F", "h-f", "pu"),
            ("电荷间距 d", "h-d", "gd"),
            ("帧率", "h-fps", "gd"),
        ],
        "tip": "COULOMB LAW / ELECTRIC FIELD LINES",
    },
    "induction": {
                "live": "ε = <span data-k='0'>B</span><span data-k='2'>L</span><span data-k='1'>v</span><br>I = ε/R　F = <span data-k='0'>B</span>I<span data-k='2'>L</span>",
        "exam": {
          "points": [
            "动生电动势 ε = BLv，方向用右手定则",
            "感应电流的磁场总要阻碍原磁通量的变化（楞次定律）"
          ],
          "pitfalls": [
            "ε 与 v 有关，静止导体棒不产生动生电动势",
            "安培力方向始终阻碍相对运动，不是促进"
          ],
          "example": "B = 1 T、L = 1 m、v = 3 m/s，求感应电动势与电流（R = 1 Ω）。",
          "answer": "ε = BLv = 3 V；I = ε/R = 3 A；F = BIL = 3 N。"
        },
"engine": "induction",
        "domain": "电磁学 / 电磁感应",
        "formula": "ε = BLv ；I = ε/R ；F_A = BIL ；P = εI",
        "latex": r"""\begin{aligned}
        \varepsilon &= BLv\\
        I &= \frac{\varepsilon}{R}\\
        F_A &= BIL\\
        P &= \varepsilon I
        \end{aligned}""",
        "laws": ["法拉第电磁感应定律", "右手定则", "安培力与楞次定律"],
        "initial": ["匀强磁场垂直纸面向内", "导体棒在平行导轨上匀速右移", "回路总电阻 R = 1.0 Ω"],
        "params": [
            {"label": "磁感应强度 B", "min": 0.0, "max": 20.0, "value": 1.0, "step": 0.1, "unit": "T", "hint": "B 越大感应电动势越大"},
            {"label": "棒速度 v", "min": 0.0, "max": 60.0, "value": 3.0, "step": 0.5, "unit": "m/s", "hint": "v 越大电动势越大"},
            {"label": "导轨间距 L", "min": 0.1, "max": 9.0, "value": 2.0, "step": 0.1, "unit": "m", "hint": "L 越大感应电动势越大"},
        ],
        "hud": [
            ("电动势 ε", "h-emf", "cy"),
            ("电流 I", "h-i", "pu"),
            ("安培力 F", "h-f", "gd"),
            ("功率 P", "h-p", "cy"),
            ("帧率", "h-fps", "gd"),
        ],
        "tip": "MOTIONAL EMF / LENZ LAW",
    },
    "waves": {
                "live": "Δy = <span data-k='0'>λ</span>L / <span data-k='1'>d</span><br>I = I₀cos²(π<span data-k='1'>d</span>sinθ / <span data-k='0'>λ</span>)　流速 = <span data-k='2'>倍</span>",
        "exam": {
          "points": [
            "双缝干涉条纹间距 Δy = λL/d",
            "波程差为波长整数倍时加强，半波长奇数倍时减弱"
          ],
          "pitfalls": [
            "d 增大条纹变密，不是变疏",
            "λ 是光的波长，不是缝宽"
          ],
          "example": "λ = 550 nm、d = 0.42 mm、L = 1 m，求相邻亮纹间距。",
          "answer": "Δy = λL/d ≈ 1.31 mm。"
        },
"engine": "waves",
        "domain": "波动光学 / 干涉与衍射",
        "formula": "∂²u/∂t² = v²∇²u ；ΔL = d·sinθ ；I = I₀·cos²(πd·sinθ/λ)",
        "latex": r"""\begin{aligned}
        \frac{\partial^{2}u}{\partial t^{2}} &= v^{2}\nabla^{2}u\\
        \Delta L &= d\sin\theta\\
        I &= I_0\cos^{2}\!\left(\frac{\pi d\sin\theta}{\lambda}\right)
        \end{aligned}""",
        "laws": ["惠更斯—菲涅耳次波原理", "线性波叠加原理", "夫琅禾费远场衍射"],
        "initial": ["双缝等幅同相相干次波源 φ₀ = 0", "入射平面波波前垂直于光轴", "环境折射率 n = 1.0"],
        "params": [
            {"label": "波长 λ", "min": 200, "max": 1000, "value": 550, "step": 10, "unit": "nm", "hint": "λ 越小条纹越密"},
            {"label": "缝间距 d", "min": 0.02, "max": 1.80, "value": 0.42, "step": 0.01, "unit": "mm", "hint": "d 越小条纹越疏"},
            {"label": "时间流速", "min": 0.01, "max": 10.0, "value": 1.0, "step": 0.05, "unit": "倍", "hint": "波前传播速度倍率"},
        ],
        "hud": [
            ("波长 λ", "h-lam", "cy"),
            ("缝间距 d", "h-sep", "pu"),
            ("条纹间距 Δy", "h-dy", "gd"),
            ("相位 φ", "h-phase", "cy"),
            ("帧率", "h-fps", "gd"),
        ],
        "tip": "DOUBLE SLIT / WAVE SUPERPOSITION",
    },
    "refraction": {
                "live": "sin<span data-k='0'>θ₁</span> = <span data-k='1'>n₂</span>sinθ₂<br>θ_c = arcsin(1/<span data-k='1'>n₂</span>)　强度 = <span data-k='2'>I</span>",
        "exam": {
          "points": [
            "折射定律 n₁sinθ₁ = n₂sinθ₂",
            "临界角 θ_c = arcsin(n₂/n₁)，仅光密→光疏时存在"
          ],
          "pitfalls": [
            "入射角增大到临界角后发生全反射，没有折射光",
            "折射率越大，临界角越小"
          ],
          "example": "光从空气射入 n = 1.5 的玻璃，入射角 42°，求折射角与临界角。",
          "answer": "sinθ₂ = sin42°/1.5 → θ₂ ≈ 26.5°；θ_c = arcsin(1/1.5) ≈ 41.8°。"
        },
"engine": "refraction",
        "domain": "波动光学 / 折射与全反射",
        "formula": "n₁sinθ₁ = n₂sinθ₂ ；θ_c = arcsin(n₂/n₁) ；反射角等于入射角",
        "latex": r"""\begin{aligned}
        n_1\sin\theta_1 &= n_2\sin\theta_2\\
        \theta_c &= \arcsin\!\left(\frac{n_2}{n_1}\right)
        \end{aligned}""",
        "laws": ["斯涅尔折射定律", "全反射与临界角", "反射定律"],
        "initial": ["光由空气（n₁ = 1.00）射向玻璃（n₂ 可调）", "入射光线位于界面法线左侧", "光束为单色平行光"],
        "params": [
            {"label": "入射角 θ₁", "min": 0, "max": 89, "value": 42, "step": 1, "unit": "°", "hint": "超过临界角即发生全反射"},
            {"label": "玻璃折射率 n₂", "min": 1.00, "max": 8.00, "value": 1.50, "step": 0.01, "unit": "—", "hint": "n 越大临界角越小"},
            {"label": "光束强度 I", "min": 0.01, "max": 6.0, "value": 1.0, "step": 0.05, "unit": "倍", "hint": "控制光线辉光与线宽"},
        ],
        "hud": [
            ("入射角 θ₁", "h-i", "cy"),
            ("折射角 θ₂", "h-r", "pu"),
            ("临界角 θ_c", "h-c", "gd"),
            ("光路状态", "h-mode", "cy"),
            ("折射率 n₂", "h-n", "pu"),
            ("帧率", "h-fps", "gd"),
        ],
        "tip": "REFRACTION / TOTAL INTERNAL REFLECTION",
    },
    "thermal": {
                "live": "P = <span data-k='1'>N</span>kT / <span data-k='2'>V</span><br>T = <span data-k='0'>T</span>",
        "exam": {
          "points": [
            "理想气体状态方程 PV = NkT",
            "温度是分子平均动能的标志，压强由碰撞冲量产生"
          ],
          "pitfalls": [
            "温度升高，分子平均速率增大，但并非每个分子都变快",
            "体积减半、温度不变时压强加倍"
          ],
          "example": "容器体积减半、温度保持不变，压强如何变化？",
          "answer": "由 PV = 常量，体积减半，压强变为原来的 2 倍。"
        },
"engine": "thermal",
        "domain": "热学 / 统计物理",
        "formula": "P·V = N·k_B·T ；P = Σ|2m·v_n| / (Δt·L) ；f(v) ∝ v²·exp(−mv²/2k_BT)",
        "latex": r"""\begin{aligned}
        PV &= Nk_BT\\
        P &= \frac{\sum |2mv_n|}{\Delta t\,L}\\
        f(v) &\propto v^{2}e^{-mv^{2}/2k_BT}
        \end{aligned}""",
        "laws": ["理想气体状态方程", "麦克斯韦—玻尔兹曼速率分布", "分子动理论的动量—压强关系"],
        "initial": ["N 个刚性小球均匀分布于容器", "速率服从麦克斯韦分布", "器壁碰撞为完全弹性（e = 1.0）"],
        "params": [
            {"label": "温度 T", "min": 15, "max": 6000, "value": 300, "step": 15, "unit": "K", "hint": "改变分子平均动能"},
            {"label": "粒子数 N", "min": 20, "max": 1200, "value": 320, "step": 10, "unit": "个", "hint": "统计涨落随 N 增大而减小"},
            {"label": "活塞位置 V", "min": 0.10, "max": 1.0, "value": 1.0, "step": 0.01, "unit": "倍", "hint": "压缩体积可实时观察压强上升"},
        ],
        "hud": [
            ("温度 T", "h-t", "cy"),
            ("压强 P", "h-p", "pu"),
            ("粒子数 N", "h-n", "gd"),
            ("平均速率", "h-v", "cy"),
            ("壁面碰撞", "h-c", "pu"),
            ("帧率", "h-fps", "gd"),
        ],
        "tip": "IDEAL GAS / MAXWELL DISTRIBUTION",
    },
    "collision": {
                "live": "<span data-k='0'>m₁</span><span data-k='3'>v₁</span> + <span data-k='1'>m₂</span><span data-k='4'>v₂</span> = <span data-k='0'>m₁</span>v₁′ + <span data-k='1'>m₂</span>v₂′<br><span data-k='2'>e</span> = (v₂′ − v₁′)/(v₁ − v₂)",
        "exam": {
          "points": [
            "碰撞过程系统动量守恒",
            "恢复系数 e = (v₂′ − v₁′)/(v₁ − v₂)，e = 1 弹性、e = 0 完全非弹性"
          ],
          "pitfalls": [
            "只有弹性碰撞动能守恒，非弹性碰撞动能一定减少",
            "速度需带方向（正负号），不能只代大小"
          ],
          "example": "m₁ = 2 kg、v₁ = 3 m/s 与 m₂ = 4 kg、v₂ = −1.5 m/s 碰撞，e = 0.8，求碰后速度。",
          "answer": "由动量守恒与 e 定义联立，得 v₁′ ≈ −2.1 m/s、v₂′ ≈ 1.05 m/s，动能损失约 36%。"
        },
"engine": "collision",
        "domain": "经典力学 / 动量与碰撞",
        "formula": "m₁v₁ + m₂v₂ = m₁v₁′ + m₂v₂′ ；e = (v₂′ − v₁′)/(v₁ − v₂)",
        "latex": r"""\begin{aligned}
        m_1v_1 + m_2v_2 &= m_1v_1' + m_2v_2'\\
        e &= \frac{v_2' - v_1'}{v_1 - v_2}
        \end{aligned}""",
        "laws": ["动量守恒定律", "恢复系数定义", "弹性碰撞与完全非弹性碰撞"],
        "initial": ["两球在光滑水平轨道上相向运动", "碰撞瞬间系统动量守恒", "e=1 为完全弹性，e=0 为完全非弹性"],
        "params": [
            {"label": "质量 m₁", "min": 0.1, "max": 100.0, "value": 2.0, "step": 0.5, "unit": "kg", "hint": "质量越大惯性越大"},
            {"label": "质量 m₂", "min": 0.1, "max": 100.0, "value": 4.0, "step": 0.5, "unit": "kg", "hint": "决定碰撞后速度分配"},
            {"label": "恢复系数 e", "min": 0.0, "max": 1.0, "value": 0.80, "step": 0.01, "unit": "—", "hint": "e=1 弹性碰撞，e=0 完全非弹性"},
            {"label": "初速度 v₁", "min": 0.1, "max": 100.0, "value": 3.5, "step": 0.5, "unit": "m/s", "hint": "向右为正方向"},
            {"label": "初速度 v₂", "min": -100.0, "max": -0.1, "value": -1.5, "step": 0.5, "unit": "m/s", "hint": "负值表示向左运动"},
        ],
        "hud": [
            ("总动量 p", "h-p", "cy"),
            ("总动能 E_k", "h-k", "pu"),
            ("碰撞次数", "h-n", "gd"),
            ("最近 Δp", "h-dp", "cy"),
            ("帧率", "h-fps", "gd"),
        ],
        "tip": "COLLISION / MOMENTUM CONSERVATION",
    },
    "graphmotion": {
                "live": "x = <span data-k='0'>v₀</span>t + ½<span data-k='1'>a</span>t<sup>2</sup><br>v = <span data-k='0'>v₀</span> + <span data-k='1'>a</span>t　t_max = <span data-k='2'>t</span>",
        "exam": {
          "points": [
            "x–t 图像斜率表示速度",
            "v–t 图像斜率表示加速度，面积表示位移"
          ],
          "pitfalls": [
            "图像是曲线时，切线斜率才是瞬时速度",
            "v–t 图线在时间轴下方表示反向运动，面积需带正负"
          ],
          "example": "v–t 图像中 0–4 s 为从 0 匀增到 8 m/s，求 4 s 内位移。",
          "answer": "面积 = ½×4×8 = 16 m。"
        },
"engine": "graphmotion",
        "domain": "运动学 / 图像专题",
        "formula": "x = v₀t + ½at² ；v = v₀ + at ；a = 常量",
        "latex": r"""\begin{aligned}
        x &= v_0 t + \tfrac{1}{2}at^{2}\\
        v &= v_0 + at\\
        a &= \text{const}
        \end{aligned}""",
        "laws": ["x–t 图像斜率表示速度", "v–t 图像斜率表示加速度、面积表示位移", "a–t 图像面积表示速度变化"],
        "initial": ["初速度 v₀ 由滑块给定", "加速度 a 恒定（可取负值）", "t = 0 时刻 x = 0"],
        "params": [
            {"label": "初速度 v₀", "min": -200, "max": 200, "value": 10, "step": 1, "unit": "m/s", "hint": "图像纵轴截距"},
            {"label": "加速度 a", "min": -60.0, "max": 60.0, "value": 2.0, "step": 0.1, "unit": "m/s²", "hint": "v–t 图像斜率"},
            {"label": "时间上限 t_max", "min": 0.5, "max": 60.0, "value": 8.0, "step": 0.5, "unit": "s", "hint": "横轴显示范围"},
        ],
        "hud": [
            ("时间 t", "h-t", "cy"),
            ("位移 x", "h-x", "pu"),
            ("速度 v", "h-v", "cy"),
            ("加速度 a", "h-a", "gd"),
            ("帧率", "h-fps", "gd"),
        ],
        "tip": "KINEMATIC GRAPHS / x-t · v-t · a-t",
    },
    "graphshm": {
                "live": "x = <span data-k='0'>A</span>cos(<span data-k='1'>ω</span>t + <span data-k='2'>φ</span>)<br>a = −<span data-k='1'>ω</span><sup>2</sup>x",
        "exam": {
          "points": [
            "x = A cos(ωt + φ)，v 超前 x 90°，a 与 x 反相",
            "a = −ω²x，周期 T = 2π/ω"
          ],
          "pitfalls": [
            "位移最大时速度为零、加速度最大",
            "加速度方向始终指向平衡位置"
          ],
          "example": "A = 2 m、ω = π rad/s 的简谐振动，求周期与最大速度。",
          "answer": "T = 2π/ω = 2 s；v_max = Aω ≈ 6.28 m/s。"
        },
"engine": "graphshm",
        "domain": "振动与波 / 图像专题",
        "formula": "x = A·cos(ωt+φ) ；v = −Aω·sin(ωt+φ) ；a = −Aω²·cos(ωt+φ)",
        "latex": r"""\begin{aligned}
        x &= A\cos(\omega t + \varphi)\\
        v &= -A\omega\sin(\omega t + \varphi)\\
        a &= -\omega^{2}x
        \end{aligned}""",
        "laws": ["简谐振动位移图像", "速度与位移相差 90°", "加速度始终与位移反向"],
        "initial": ["振幅 A、角频率 ω、初相 φ 由滑块给定", "平衡位置 x = 0", "忽略阻尼"],
        "params": [
            {"label": "振幅 A", "min": 0.05, "max": 20.0, "value": 1.5, "step": 0.1, "unit": "m", "hint": "曲线的峰值"},
            {"label": "角频率 ω", "min": 0.05, "max": 20.0, "value": 1.6, "step": 0.05, "unit": "rad/s", "hint": "ω 越大周期越短"},
            {"label": "初相 φ", "min": 0, "max": 6.28, "value": 0, "step": 0.05, "unit": "rad", "hint": "决定曲线左右平移"},
        ],
        "hud": [
            ("时间 t", "h-t", "cy"),
            ("位移 x", "h-x", "pu"),
            ("速度 v", "h-v", "cy"),
            ("加速度 a", "h-a", "gd"),
            ("周期 T", "h-tp", "pu"),
            ("帧率", "h-fps", "gd"),
        ],
        "tip": "SHM GRAPHS / x-t · v-t · a-t",
    },
    "bohr": {
                "live": "E = −13.6/<span data-k='0'>n</span><sup>2</sup><br>hν = E<span data-k='0'>n</span> − E<span data-k='1'>n′</span>　速率 = <span data-k='2'>倍</span>",
        "exam": {
          "points": [
            "能级 E_n = −13.6/n² eV，轨道半径 r_n = n²a₀",
            "跃迁时吸收或发射光子，hν = |E_n − E_n′|"
          ],
          "pitfalls": [
            "n 越大能量越接近 0（越高），不是越低",
            "跃迁到 n = 1 的光子能量最大、波长最短"
          ],
          "example": "氢原子从 n = 3 跃迁到 n = 1，求光子能量与波长。",
          "answer": "ΔE = 13.6(1 − 1/9) ≈ 12.09 eV；λ = 1240/ΔE ≈ 103 nm。"
        },
"engine": "bohr",
        "domain": "原子物理 / 玻尔模型",
        "formula": "E_n = −13.6/n² eV ；r_n = n²a₀ ；hν = E_n − E_n′",
        "latex": r"""\begin{aligned}
        E_n &= -\frac{13.6}{n^{2}}\ \text{eV}\\
        r_n &= n^{2}a_0\\
        h\nu &= E_n - E_{n'}
        \end{aligned}""",
        "laws": ["玻尔定态与跃迁假设", "角动量量子化", "光子能量与波长关系"],
        "initial": ["电子处于主量子数 n 的圆轨道", "轨道半径 r_n = n²a₀", "跃迁时吸收或发射光子"],
        "params": [
            {"label": "主量子数 n", "min": 1, "max": 6, "value": 3, "step": 1, "unit": "—", "hint": "n 越大轨道半径越大"},
            {"label": "跃迁目标 n′", "min": 1, "max": 6, "value": 1, "step": 1, "unit": "—", "hint": "n′ 与 n 不同时发射光子"},
            {"label": "电子速度倍率", "min": 0.05, "max": 5.0, "value": 1.0, "step": 0.05, "unit": "倍", "hint": "仅改变动画播放速度"},
        ],
        "hud": [
            ("当前能级 n", "h-n", "cy"),
            ("能级能量 E_n", "h-en", "pu"),
            ("轨道半径 r_n", "h-rn", "cy"),
            ("电子速率 v_n", "h-vn", "pu"),
            ("跃迁能量 ΔE", "h-de", "gd"),
            ("光子波长 λ", "h-lam", "cy"),
            ("帧率", "h-fps", "gd"),
        ],
        "tip": "BOHR MODEL / QUANTUM TRANSITION",
    },
}

EXPERIMENT_INDEX: Dict[str, str] = {}
MODULE_OF: Dict[str, str] = {}
ENGINE_TO_EXPERIMENT: Dict[str, str] = {}
for _mod, _cfg in MODULES.items():
    for _exp in _cfg["experiments"]:
        MODULE_OF[_exp] = _mod
EXPERIMENT_INDEX.update({
    "自由落体运动": "freefall",
    "平抛运动": "projectile",
    "牛顿第二定律": "newton",
    "匀速圆周运动": "circular",
    "一维碰撞与动量守恒": "collision",
    "混沌双摆运动": "mechanics",
    "洛伦兹力回旋": "em",
    "库仑定律电场线": "coulomb",
    "导体棒切割磁感线": "induction",
    "双缝干涉与衍射": "waves",
    "光的折射与全反射": "refraction",
    "理想气体分子热运动": "thermal",
    "氢原子玻尔模型": "bohr",
    "匀变速运动图像": "graphmotion",
    "简谐振动图像": "graphshm",
})

for _name, _eng in EXPERIMENT_INDEX.items():
    ENGINE_TO_EXPERIMENT.setdefault(_eng, _name)

KEYWORDS: Dict[str, List[str]] = {
    "freefall": ["自由落体", "落体", "自由下落", "落球"],
    "projectile": ["平抛", "抛体", "斜抛", "抛物线", "投射"],
    "newton": ["牛顿第二定律", "受力", "加速度", "摩擦力", "动力学"],
    "circular": ["圆周", "向心", "角速度", "线速度"],
    "mechanics": ["摆", "混沌", "单摆", "双摆", "弹簧", "振子"],
    "em": ["洛伦兹", "回旋", "磁场", "带电", "等离子", "加速器"],
    "coulomb": ["库仑", "电场线", "点电荷", "静电场", "场强"],
    "induction": ["切割", "感应", "电动势", "导体棒", "楞次", "安培力"],
    "waves": ["双缝", "干涉", "衍射", "驻波", "条纹", "波动"],
    "refraction": ["折射", "全反射", "临界角", "斯涅尔", "光路"],
    "thermal": ["气体", "分子", "压强", "温度", "布朗", "统计", "麦克斯韦"],
    "bohr": ["玻尔", "氢原子", "能级", "跃迁", "光子", "量子"],
}


def classify(exp_name: str) -> str:
    text = exp_name or ""
    scores = {k: 0.0 for k in KEYWORDS}
    for domain, words in KEYWORDS.items():
        for w in words:
            if w and w in text:
                scores[domain] += 1.0 + 0.1 * len(w)
    best = max(scores, key=lambda k: scores[k])
    return best if scores[best] > 0 else "waves"


def agent_physics(exp_name: str) -> Dict[str, Any]:
    name = (exp_name or "").strip() or PRESETS[0][1]
    key = EXPERIMENT_INDEX.get(name) or classify(name)
    base = DOMAIN_LIBRARY[key]
    spec: Dict[str, Any] = {
        "title": name,
        "engine": base["engine"],
        "domain": base["domain"],
        "formula": base["formula"],
        "latex": base["latex"],
        "live": base["live"],
        "exam": base["exam"],
        "laws": list(base["laws"]),
        "initial": list(base["initial"]),
        "params": [dict(p) for p in base["params"]],
        "hud": list(base["hud"]),
        "tip": base["tip"],
        "agent": "Agent 1 · 物理原理与参数拆解专家",
    }
    return spec


SHELL_HEAD = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>@@TITLE@@</title>
<style>
*{box-sizing:border-box;}
html,body{width:100%;height:100vh;margin:0;padding:0;overflow:hidden;background:#09090b;}
body{
  font-family:ui-monospace,"SF Mono",Menlo,Consolas,monospace;color:#e4e4e7;
  background:
    radial-gradient(880px 520px at 18% -6%,rgba(34,211,238,.09),transparent 62%),
    radial-gradient(760px 480px at 86% 4%,rgba(168,85,247,.10),transparent 60%),
    #09090b;
}
#stage{position:fixed;inset:0;width:100%;height:100vh;overflow:hidden;background:#09090b;}
#cv,#fx{position:absolute;inset:0;width:100%;height:100%;display:block;}
#fx{pointer-events:none;}
.hud{
  position:absolute;left:14px;top:14px;min-width:198px;
  padding:11px 14px;border-radius:14px;
  background:rgba(9,9,11,.66);
  border:1px solid rgba(34,211,238,.26);
  box-shadow:0 0 34px rgba(34,211,238,.12),inset 0 0 22px rgba(34,211,238,.05);
  backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);
  font-size:12px;line-height:1.85;letter-spacing:.02em;color:#d4d4d8;
  pointer-events:none;
}
.hud h4{
  margin:0 0 6px;font-size:9.5px;letter-spacing:.18em;text-transform:uppercase;
  color:#22d3ee;font-weight:700;
}
.hud .row{display:flex;justify-content:space-between;gap:16px;white-space:nowrap;}
.hud .row span{color:#a1a1aa;}
.hud .row b{color:#e4e4e7;font-weight:600;}
.hud .row b.cy{color:#67e8f9;}
.hud .row b.pu{color:#c084fc;}
.hud .row b.gd{color:#fbbf24;}
.panel{
  position:absolute;left:14px;right:14px;bottom:14px;
  display:grid;grid-template-columns:repeat(auto-fit,minmax(146px,1fr));gap:10px 16px;
  padding:12px 16px 14px;border-radius:14px;
  background:rgba(9,9,11,.74);
  border:1px solid rgba(168,85,247,.26);
  box-shadow:0 0 34px rgba(168,85,247,.12);
  backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);
}
.ctl label{
  display:flex;justify-content:space-between;gap:8px;
  font-size:11.5px;letter-spacing:.05em;color:#e4e4e7;
  margin-bottom:10px;flex-wrap:nowrap;
}
.ctl label b{color:#67e8f9;font-weight:700;font-size:12px;}
input[type=range]{
  -webkit-appearance:none;appearance:none;
  width:100%;height:5px;border-radius:99px;
  background:linear-gradient(90deg,rgba(34,211,238,.85),rgba(168,85,247,.85));
  outline:none;cursor:pointer;display:block;
}
input[type=range]::-webkit-slider-thumb{
  -webkit-appearance:none;width:14px;height:14px;border-radius:50%;
  background:#09090b;border:2px solid #22d3ee;
  box-shadow:0 0 12px rgba(34,211,238,.9);
  transition:box-shadow .15s ease;
}
input[type=range]::-webkit-slider-thumb:hover{box-shadow:0 0 18px rgba(34,211,238,1);}
input[type=range]::-moz-range-thumb{
  width:12px;height:12px;border-radius:50%;background:#09090b;
  border:2px solid #22d3ee;box-shadow:0 0 12px rgba(34,211,238,.9);
}
.ctl .unit{color:#8b8b93 !important;white-space:nowrap;}
.ctl label > span{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0;}
.ctl label > b{flex:0 0 auto;white-space:nowrap;}
.ctl .crow{display:flex;align-items:center;gap:9px;}
.ctl .crow input[type=range]{flex:1 1 auto;min-width:0;}
.ctl .num{
  flex:0 0 70px;width:70px;
  background:rgba(24,24,28,.96);
  border:1px solid rgba(34,211,238,.40);
  border-radius:7px;
  color:#f4f4f5;font-family:ui-monospace,monospace;font-size:11.5px;font-weight:600;
  padding:4px 6px;text-align:center;
}
.ctl .num:focus{outline:none;border-color:#22d3ee;box-shadow:0 0 10px rgba(34,211,238,.40);}
.ctl .num::-webkit-inner-spin-button,.ctl .num::-webkit-outer-spin-button{-webkit-appearance:none;margin:0;}
.hud .tools{
  pointer-events:auto;margin-top:9px;padding-top:8px;
  border-top:1px solid rgba(34,211,238,.20);
  display:grid;grid-template-columns:repeat(3,1fr);gap:8px 7px;
}
.hud .tools .tbtn{
  font-family:ui-monospace,monospace;font-size:9.5px;font-weight:600;
  letter-spacing:.02em;color:#c4c4cc;background:rgba(24,24,27,.92);
  border:1px solid rgba(34,211,238,.30);border-radius:6px;padding:6px 3px;
  cursor:pointer;transition:all .14s ease;
}
.hud .tools .tbtn:hover{color:#67e8f9;border-color:#22d3ee;background:rgba(34,211,238,.10);}
.hud .tools .tbtn.active{color:#09090b;background:#22d3ee;border-color:#22d3ee;box-shadow:0 0 10px rgba(34,211,238,.6);}
.hud .fbar{
  margin-top:9px;padding-top:8px;border-top:1px solid rgba(34,211,238,.20);
  width:266px;font-size:10.5px;line-height:1.75;color:#c4c4cc;white-space:normal;
}
.hud .fbar span[data-k]{color:#e4e4e7;transition:color .16s ease,text-shadow .16s ease;}
.hud .fbar span[data-k].hot{color:#67e8f9;text-shadow:0 0 10px rgba(34,211,238,.95);font-weight:700;}
body.wide .hud{
  left:14px;right:14px;top:12px;min-width:0;
  display:flex;flex-wrap:wrap;align-items:center;gap:10px 24px;
  padding:10px 16px;
}
body.wide .hud h4{margin:0;}
body.wide .hud .row{flex:0 0 auto;min-width:132px;}
body.wide .hud .tools{margin:0;padding:0;border-top:none;display:flex;gap:8px;}
.tip{
  position:absolute;right:16px;bottom:98px;
  font-size:9.5px;letter-spacing:.16em;color:#8b8b93;text-transform:uppercase;
  pointer-events:none;
}
</style>
</head>
<body class="@@BODYCLS@@">
<div id="stage">
<canvas id="cv"></canvas>
<canvas id="fx"></canvas>
<aside class="hud"><h4>@@HUDTITLE@@</h4>@@HUD@@
<div class="tools">
<button class="tbtn" id="btn-pause" type="button">⏸ 暂停</button>
<button class="tbtn" id="btn-step" type="button">⏭ 单步</button>
<button class="tbtn" id="btn-reset" type="button">⟲ 重置</button>
<button class="tbtn" id="btn-r05" type="button">0.5×</button>
<button class="tbtn active" id="btn-r1" type="button">1×</button>
<button class="tbtn" id="btn-r2" type="button">2×</button>
</div>
<div class="fbar">@@LIVE@@</div>
</aside>
<div class="panel">@@SLIDERS@@</div>
</div>
"""

SHELL_JS = r"""
const $ = (id) => document.getElementById(id);
function setText(id, v){ const e = $(id); if(e) e.textContent = v; }
function fpsTick(now){
  if(!window.__lt) window.__lt = now;
  const d = now - window.__lt; window.__lt = now;
  if(d > 0 && d < 400){ window.__fps = (window.__fps || 60) * 0.9 + (1000/d) * 0.1; }
  return window.__fps || 60;
}
function bindRange(i, fn, dec){
  const el = $('s' + i), out = $('v' + i), num = $('n' + i);
  if(!el) return;
  const lo = parseFloat(el.min), hi = parseFloat(el.max);
  const show = (v) => { if(out) out.textContent = dec != null ? Number(v).toFixed(dec) : String(v); };
  const clamp = (v) => Math.max(lo, Math.min(hi, v));
  const apply = (v) => { if(!isFinite(v)) return; const c = clamp(v); show(c); fn(c); return c; };
  const onRange = () => {
    const c = apply(parseFloat(el.value));
    if(num && c != null) num.value = String(c);
    flashParam(i);
  };
  el.addEventListener('input', onRange);
  el.addEventListener('change', onRange);
  if(num){
    num.addEventListener('input', () => {
      const raw = num.value;
      if(raw === '' || raw === '-' || raw === '.' || raw === '-.') return;
      const v = parseFloat(raw);
      if(!isFinite(v)) return;
      const c = clamp(v);
      el.value = String(c);
      show(c);
      fn(c);
      flashParam(i);
    });
    num.addEventListener('change', () => {
      const v = parseFloat(num.value);
      const c = isFinite(v) ? clamp(v) : parseFloat(el.value);
      num.value = String(c);
      el.value = String(c);
      apply(c);
    });
  }
  const init = parseFloat(el.value);
  show(init);
  if(num) num.value = String(init);
  fn(init);
}
function makeCanvasPair(){
  const cv = $('cv'), fx = $('fx');
  const ctx = cv.getContext('2d'), fxc = fx.getContext('2d');
  let W = 0, H = 0, DPR = 1;
  const resize = () => {
    const r = cv.getBoundingClientRect();
    W = Math.max(260, r.width || window.innerWidth);
    H = Math.max(320, r.height || window.innerHeight);
    const raw = Math.min(2, window.devicePixelRatio || 1);
    const budget = Math.sqrt(1800000 / (W * H));
    DPR = Math.max(1, Math.min(raw, budget));
    cv.width = Math.round(W * DPR); cv.height = Math.round(H * DPR);
    fx.width = cv.width; fx.height = cv.height;
    ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    fxc.setTransform(DPR, 0, 0, DPR, 0, 0);
    return { W, H };
  };
  window.addEventListener('resize', resize, { passive: true });
  return { cv, fx, ctx, fxc, resize, get W(){ return W; }, get H(){ return H; } };
}
const SIM = { paused: false, step: 0, rate: 1, last: performance.now() };
function simDt(now) {
  const raw = Math.min(0.05, Math.max(0.0001, (now - SIM.last) / 1000));
  SIM.last = now;
  if (SIM.step > 0) { SIM.step -= 1; return 1 / 60; }
  if (SIM.paused) return 0;
  return raw * SIM.rate;
}
function safeX() {
  return Math.min(318, Math.round((window.innerWidth || 1280) * 0.335));
}
function gridBackground(c2d, w, h, step) {
  step = step || 40;
  c2d.strokeStyle = 'rgba(63,63,72,0.22)';
  c2d.lineWidth = 1;
  c2d.beginPath();
  for (let x = step; x < w; x += step) {
    c2d.moveTo(x, 0);
    c2d.lineTo(x, h);
  }
  for (let y = step; y < h; y += step) {
    c2d.moveTo(0, y);
    c2d.lineTo(w, y);
  }
  c2d.stroke();
}
function flashParam(i) {
  document.querySelectorAll('.fbar span[data-k="' + i + '"]').forEach(function (el) {
    el.classList.add('hot');
    clearTimeout(el.__hot);
    el.__hot = setTimeout(function () { el.classList.remove('hot'); }, 1100);
  });
}
function initTools() {
  const pause = $('btn-pause');
  if (!pause) return;
  const setPause = (p) => {
    SIM.paused = p;
    pause.textContent = p ? '▶ 继续' : '⏸ 暂停';
    pause.classList.toggle('active', p);
  };
  pause.addEventListener('click', () => setPause(!SIM.paused));
  const step = $('btn-step');
  if (step) step.addEventListener('click', () => { setPause(true); SIM.step = 1; });
  const reset = $('btn-reset');
  if (reset) reset.addEventListener('click', () => {
    if (typeof window.__simReset === 'function') window.__simReset();
    else window.location.reload();
  });
  const rates = { 'btn-r05': 0.5, 'btn-r1': 1, 'btn-r2': 2 };
  Object.keys(rates).forEach((id) => {
    const b = $(id);
    if (!b) return;
    b.addEventListener('click', () => {
      SIM.rate = rates[id];
      Object.keys(rates).forEach((k) => { const e = $(k); if (e) e.classList.remove('active'); });
      b.classList.add('active');
    });
  });
}
initTools();
"""

HUD_TITLES = {
    "freefall": "FREE FALL",
    "projectile": "PROJECTILE",
    "newton": "NEWTON II",
    "circular": "CIRCULAR MOTION",
    "coulomb": "FIELD LINES",
    "induction": "MOTIONAL EMF",
    "refraction": "REFRACTION",
    "bohr": "BOHR MODEL",
    "collision": "MOMENTUM",
    "graphmotion": "KINEMATICS",
    "graphshm": "SHM",
    "waves": "DOUBLE SLIT",
    "mechanics": "CHAOTIC PENDULUM",
    "em": "LORENTZ FORCE",
    "thermal": "IDEAL GAS",
}


def _fmt_num(v: Any) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, float):
        s = f"{v:.4g}"
        return s
    return str(v)


def sliders_html(spec: Dict[str, Any]) -> str:
    blocks = []
    for i, p in enumerate(spec["params"]):
        label = html_lib.escape(str(p.get("label", f"参数 {i + 1}")))
        unit = html_lib.escape(str(p.get("unit", "")))
        hint = html_lib.escape(str(p.get("hint", "")))
        blocks.append(
            '<div class="ctl" title="{hint}">'
            '<label><span>{label} <span class="unit">/ {unit}</span></span>'
            '<b id="v{i}">{val}</b></label>'
            '<div class="crow">'
            '<input type="range" id="s{i}" min="{mn}" max="{mx}" step="{st}" value="{val}">'
            '<input type="number" class="num" id="n{i}" min="{mn}" max="{mx}" step="{st}" value="{val}" inputmode="decimal">'
            "</div>"
            "</div>".format(
                hint=hint,
                label=label,
                unit=unit,
                i=i,
                val=_fmt_num(p["value"]),
                mn=_fmt_num(p["min"]),
                mx=_fmt_num(p["max"]),
                st=_fmt_num(p["step"]),
            )
        )
    return "".join(blocks)


def hud_html(spec: Dict[str, Any]) -> str:
    rows = []
    for label, hid, cls in spec.get("hud", []):
        rows.append(
            '<div class="row"><span>{}</span><b class="{}" id="{}">--</b></div>'.format(
                html_lib.escape(str(label)), cls, hid
            )
        )
    return "".join(rows)


def shell_open(spec: Dict[str, Any]) -> str:
    return (
        SHELL_HEAD.replace("@@TITLE@@", html_lib.escape(str(spec["title"])))
        .replace("@@HUDTITLE@@", HUD_TITLES.get(spec["engine"], "PHYSICS SANDBOX"))
        .replace("@@HUD@@", hud_html(spec))
        .replace("@@SLIDERS@@", sliders_html(spec))
        .replace("@@TIP@@", html_lib.escape(str(spec.get("tip", ""))))
        .replace("@@LIVE@@", str(spec.get("live", "")))
        .replace("@@BODYCLS@@", "wide" if spec["engine"] in ("graphmotion", "graphshm") else "")
    )


def shell_close() -> str:
    return "</script></body></html>"


def tpl_waves(spec: Dict[str, Any]) -> str:
    return shell_open(spec) + "<script>" + SHELL_JS + SCRIPT_WAVES + shell_close()


def tpl_mechanics(spec: Dict[str, Any]) -> str:
    return shell_open(spec) + "<script>" + SHELL_JS + SCRIPT_MECHANICS + shell_close()


def tpl_em(spec: Dict[str, Any]) -> str:
    return shell_open(spec) + "<script>" + SHELL_JS + SCRIPT_EM + shell_close()


def tpl_thermal(spec: Dict[str, Any]) -> str:
    return shell_open(spec) + "<script>" + SHELL_JS + SCRIPT_THERMAL + shell_close()


def tpl_freefall(spec: Dict[str, Any]) -> str:
    return shell_open(spec) + "<script>" + SHELL_JS + SCRIPT_FREEFALL + shell_close()


def tpl_projectile(spec: Dict[str, Any]) -> str:
    return shell_open(spec) + "<script>" + SHELL_JS + SCRIPT_PROJECTILE + shell_close()


def tpl_newton(spec: Dict[str, Any]) -> str:
    return shell_open(spec) + "<script>" + SHELL_JS + SCRIPT_NEWTON + shell_close()


def tpl_circular(spec: Dict[str, Any]) -> str:
    return shell_open(spec) + "<script>" + SHELL_JS + SCRIPT_CIRCULAR + shell_close()


def tpl_coulomb(spec: Dict[str, Any]) -> str:
    return shell_open(spec) + "<script>" + SHELL_JS + SCRIPT_COULOMB + shell_close()


def tpl_induction(spec: Dict[str, Any]) -> str:
    return shell_open(spec) + "<script>" + SHELL_JS + SCRIPT_INDUCTION + shell_close()


def tpl_refraction(spec: Dict[str, Any]) -> str:
    return shell_open(spec) + "<script>" + SHELL_JS + SCRIPT_REFRACTION + shell_close()


def tpl_bohr(spec: Dict[str, Any]) -> str:
    return shell_open(spec) + "<script>" + SHELL_JS + SCRIPT_BOHR + shell_close()


def tpl_collision(spec: Dict[str, Any]) -> str:
    return shell_open(spec) + "<script>" + SHELL_JS + SCRIPT_COLLISION + shell_close()


def tpl_graphmotion(spec: Dict[str, Any]) -> str:
    return shell_open(spec) + "<script>" + SHELL_JS + SCRIPT_GRAPHMOTION + shell_close()


def tpl_graphshm(spec: Dict[str, Any]) -> str:
    return shell_open(spec) + "<script>" + SHELL_JS + SCRIPT_GRAPHSHM + shell_close()


TEMPLATES = {
    "freefall": tpl_freefall,
    "projectile": tpl_projectile,
    "newton": tpl_newton,
    "circular": tpl_circular,
    "mechanics": tpl_mechanics,
    "em": tpl_em,
    "coulomb": tpl_coulomb,
    "induction": tpl_induction,
    "waves": tpl_waves,
    "refraction": tpl_refraction,
    "thermal": tpl_thermal,
    "bohr": tpl_bohr,
    "collision": tpl_collision,
    "graphmotion": tpl_graphmotion,
    "graphshm": tpl_graphshm,
}

SCRIPT_COLLISION = r"""
const scene = makeCanvasPair();
const ctx = scene.ctx;
let W = scene.W, H = scene.H;

const P = { m1: 2.0, m2: 4.0, e: 0.80, v1: 3.5, v2: -1.5 };
const SCALE = 40;

let x1 = 0, x2 = 0, v1 = 0, v2 = 0, r1 = 18, r2 = 24;
let left = 0, right = 0, ground = 0;
let hits = 0, flash = 0, dp = 0, flashX = 0, lastLoss = null;

function radiusOf(m) { return 14 + Math.sqrt(m) * 8; }
function reset() {
  r1 = radiusOf(P.m1);
  r2 = radiusOf(P.m2);
  x1 = left + (right - left) * 0.24;
  x2 = left + (right - left) * 0.74;
  v1 = P.v1 * SCALE;
  v2 = P.v2 * SCALE;
  hits = 0;
  flash = 0;
  dp = 0;
  lastLoss = null;
}
function relayout() {
  const s = scene.resize();
  W = s.W; H = s.H;
  left = safeX() + 24;
  right = W - 44;
  ground = H - 182;
  reset();
}

bindRange(0, val => { P.m1 = val; reset(); }, 1);
bindRange(1, val => { P.m2 = val; reset(); }, 1);
bindRange(2, val => { P.e = val; reset(); }, 2);
bindRange(3, val => { P.v1 = val; reset(); }, 1);
bindRange(4, val => { P.v2 = val; reset(); }, 1);
window.addEventListener('resize', relayout, { passive: true });
relayout();

function collide() {
  const m1 = P.m1, m2 = P.m2, e = P.e;
  const u1 = v1, u2 = v2;
  const nv1 = ((m1 - e * m2) * u1 + (1 + e) * m2 * u2) / (m1 + m2);
  const nv2 = ((m2 - e * m1) * u2 + (1 + e) * m1 * u1) / (m1 + m2);
  v1 = nv1;
  v2 = nv2;
  const overlap = (x1 + r1) - (x2 - r2);
  if (overlap > 0) { x1 -= overlap * 0.5; x2 += overlap * 0.5; }
  const kb = 0.5 * m1 * (u1 / SCALE) * (u1 / SCALE) + 0.5 * m2 * (u2 / SCALE) * (u2 / SCALE);
  const ka = 0.5 * m1 * (v1 / SCALE) * (v1 / SCALE) + 0.5 * m2 * (v2 / SCALE) * (v2 / SCALE);
  lastLoss = kb > 0.0001 ? (kb - ka) / kb * 100 : 0;
  dp = Math.abs(m1 * (v1 - u1) + m2 * (v2 - u2));
  flash = 1;
  flashX = (x1 + r1 + x2 - r2) * 0.5;
  hits++;
}

function step(dt) {
  if (dt <= 0) return;
  x1 += v1 * dt;
  x2 += v2 * dt;
  if (x1 + r1 >= x2 - r2 && (v1 - v2) > 0) collide();
  if (x1 - r1 < left) { x1 = left + r1; v1 = Math.abs(v1); }
  if (x2 + r2 > right) { x2 = right - r2; v2 = -Math.abs(v2); }
  if (flash > 0) flash = Math.max(0, flash - dt * 2.2);
}

function drawTrack() {
  ctx.strokeStyle = 'rgba(34,211,238,0.85)';
  ctx.lineWidth = 2.4;
  ctx.beginPath();
  ctx.moveTo(left, ground);
  ctx.lineTo(right, ground);
  ctx.stroke();

  ctx.strokeStyle = 'rgba(34,211,238,0.12)';
  ctx.lineWidth = 1;
  for (let i = -2; i <= 24; i++) {
    const xx = left + i * 40;
    if (xx > right + 20) break;
    ctx.beginPath();
    ctx.moveTo(xx, ground);
    ctx.lineTo(xx + 22, ground + 22);
    ctx.stroke();
  }

  ctx.fillStyle = 'rgba(208,208,218,0.95)';
  ctx.font = '13px ui-monospace,monospace';
  ctx.fillText('光滑水平轨道 · 碰撞瞬间动量守恒', left, ground + 50);
}

function drawBall(x, y, r, color, m, v, tag) {
  const rg = ctx.createRadialGradient(x, y, 0, x, y, r * 2.8);
  rg.addColorStop(0, color + '0.42)');
  rg.addColorStop(1, color + '0)');
  ctx.fillStyle = rg;
  ctx.beginPath();
  ctx.arc(x, y, r * 2.8, 0, Math.PI * 2);
  ctx.fill();

  const body = ctx.createRadialGradient(x - r * 0.3, y - r * 0.35, 1, x, y, r);
  body.addColorStop(0, color + '0.95)');
  body.addColorStop(1, color + '0.35)');
  ctx.fillStyle = body;
  ctx.strokeStyle = color + '1)';
  ctx.lineWidth = 1.8;
  ctx.beginPath();
  ctx.arc(x, y, r, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();

  ctx.fillStyle = 'rgba(9,9,11,0.88)';
  ctx.font = 'bold 10px ui-monospace,monospace';
  ctx.fillText(tag, x - (r > 20 ? 14 : 9), y + 4);

  if (Math.abs(v) > 2) {
    const len = Math.min(96, Math.abs(v) * 0.34);
    const dir = v > 0 ? 1 : -1;
    const sx = x + dir * (r + 4);
    const ex = sx + dir * len;
    ctx.strokeStyle = 'rgba(251,191,36,0.9)';
    ctx.fillStyle = 'rgba(251,191,36,0.9)';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(sx, y);
    ctx.lineTo(ex, y);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(ex, y);
    ctx.lineTo(ex - dir * 8, y - 5);
    ctx.lineTo(ex - dir * 8, y + 5);
    ctx.closePath();
    ctx.fill();
    ctx.font = '10.5px ui-monospace,monospace';
    ctx.fillText((v / SCALE).toFixed(1) + ' m/s', ex - dir * 48, y - 10);
  }
}

function drawFlash() {
  if (flash <= 0.01) return;
  const rr = 26 + (1 - flash) * 46;
  const rg = ctx.createRadialGradient(flashX, ground - 30, 0, flashX, ground - 30, rr);
  rg.addColorStop(0, 'rgba(255,255,255,' + (flash * 0.85).toFixed(3) + ')');
  rg.addColorStop(0.4, 'rgba(251,191,36,' + (flash * 0.45).toFixed(3) + ')');
  rg.addColorStop(1, 'rgba(251,191,36,0)');
  ctx.fillStyle = rg;
  ctx.beginPath();
  ctx.arc(flashX, ground - 30, rr, 0, Math.PI * 2);
  ctx.fill();
}

function drawBars() {
  const bw = Math.min(880, W - safeX() - 90);
  if (bw < 280) return;
  const bx = safeX() + (W - safeX() - bw) * 0.5;
  const gy = 96;
  const p = P.m1 * v1 + P.m2 * v2;
  const p0 = P.m1 * P.v1 + P.m2 * P.v2;
  const k = 0.5 * P.m1 * (v1 / SCALE) * (v1 / SCALE) + 0.5 * P.m2 * (v2 / SCALE) * (v2 / SCALE);
  const k0 = 0.5 * P.m1 * P.v1 * P.v1 + 0.5 * P.m2 * P.v2 * P.v2;
  const pM = p / SCALE;
  const scaleP = Math.max(0.01, Math.abs(pM), Math.abs(p0));

  ctx.fillStyle = 'rgba(214,214,224,0.98)';
  ctx.font = 'bold 15px ui-monospace,monospace';
  ctx.fillText('总动量 p（碰撞前 / 后）', bx, gy - 14);
  ctx.fillStyle = 'rgba(34,211,238,0.30)';
  ctx.fillRect(bx, gy, bw * Math.abs(p0) / scaleP, 26);
  ctx.fillStyle = 'rgba(34,211,238,0.95)';
  ctx.fillRect(bx, gy + 34, bw * Math.abs(pM) / scaleP, 26);
  ctx.fillStyle = 'rgba(220,220,230,0.98)';
  ctx.font = 'bold 13.5px ui-monospace,monospace';
  ctx.fillText(p0.toFixed(2) + ' → ' + pM.toFixed(2) + ' kg·m/s', bx, gy + 86);

  ctx.fillStyle = 'rgba(214,214,224,0.98)';
  ctx.font = 'bold 15px ui-monospace,monospace';
  ctx.fillText('总动能 E_k（碰撞前 / 后）', bx, gy + 128);
  const scaleK = Math.max(0.001, k0, k);
  ctx.fillStyle = 'rgba(168,85,247,0.28)';
  ctx.fillRect(bx, gy + 140, bw * k0 / scaleK, 26);
  ctx.fillStyle = 'rgba(168,85,247,0.95)';
  ctx.fillRect(bx, gy + 174, bw * k / scaleK, 26);
  ctx.fillStyle = 'rgba(220,220,230,0.98)';
  ctx.font = 'bold 13.5px ui-monospace,monospace';
  const lossText = lastLoss == null ? '尚未碰撞' : '最近碰撞损失 ' + lastLoss.toFixed(1) + '%';
  ctx.fillText(k0.toFixed(2) + ' → ' + k.toFixed(2) + ' J（' + lossText + '）', bx, gy + 226);

  ctx.fillStyle = 'rgba(103,232,249,0.92)';
  ctx.font = 'bold 19px ui-monospace,monospace';
  ctx.fillText('m₁v₁ + m₂v₂ = m₁v₁′ + m₂v₂′', bx, gy + 274);
}

let hudAcc = 0;
function updateAndRender(now) {
  const dt = simDt(now);
  const fps = fpsTick(now);
  step(dt);

  ctx.fillStyle = '#09090b';
  ctx.fillRect(0, 0, W, H);
  gridBackground(ctx, W, H);
  drawTrack();
  drawBars();
  drawBall(x1, ground - r1, r1, 'rgba(34,211,238,', P.m1, v1, 'm₁');
  drawBall(x2, ground - r2, r2, 'rgba(168,85,247,', P.m2, v2, 'm₂');
  drawFlash();

  hudAcc += 0.016;
  if (hudAcc > 0.12) {
    hudAcc = 0;
    const p = P.m1 * v1 + P.m2 * v2;
    const k = 0.5 * P.m1 * (v1 / SCALE) * (v1 / SCALE) + 0.5 * P.m2 * (v2 / SCALE) * (v2 / SCALE);
    setText('h-p', (p / SCALE).toFixed(2) + ' kg·m/s');
    setText('h-k', k.toFixed(2) + ' J');
    setText('h-n', String(hits));
    setText('h-dp', dp.toFixed(3));
    setText('h-fps', fps.toFixed(0) + ' FPS');
  }
  requestAnimationFrame(updateAndRender);
}
window.__simReset = reset;
setText('h-fps', '60 FPS');
requestAnimationFrame(updateAndRender);
"""

SCRIPT_GRAPHMOTION = r"""
const scene = makeCanvasPair();
const ctx = scene.ctx;
let W = scene.W, H = scene.H;

const P = { v0: 10, a: 2, tmax: 8 };
let tNow = 0;

function xOf(t) { return P.v0 * t + 0.5 * P.a * t * t; }
function vOf(t) { return P.v0 + P.a * t; }
function aOf(t) { return P.a; }

function reload() {
  const s = scene.resize();
  W = s.W; H = s.H;
  tNow = 0;
}
bindRange(0, val => { P.v0 = val; tNow = 0; }, 1);
bindRange(1, val => { P.a = val; tNow = 0; }, 1);
bindRange(2, val => { P.tmax = val; tNow = 0; }, 1);
window.addEventListener('resize', reload, { passive: true });
reload();

function panelRects() {
  const x0 = 40, x1 = W - 40;
  const y0 = 112, y1 = H - 136;
  const gap = 14;
  const totalW = x1 - x0;
  const lw = Math.round(totalW * 0.58);
  const rw = totalW - lw - gap;
  const rh = Math.round((y1 - y0 - gap) / 2);
  return [
    { x: x0, y: y0, w: lw, h: y1 - y0 },
    { x: x0 + lw + gap, y: y0, w: rw, h: rh },
    { x: x0 + lw + gap, y: y0 + rh + gap, w: rw, h: y1 - y0 - rh - gap },
  ];
}

function drawPanel(r, title, unit, color, fn, fill) {
  let lo = Infinity, hi = -Infinity;
  for (let k = 0; k <= 240; k++) {
    const v = fn(P.tmax * k / 240);
    if (v < lo) lo = v;
    if (v > hi) hi = v;
  }
  lo = Math.min(lo, 0);
  hi = Math.max(hi, 0);
  if (hi - lo < 1e-6) hi = lo + 1;
  const pad = (hi - lo) * 0.14;
  lo -= pad;
  hi += pad;

  const mapY = v => r.y + r.h - 20 - (v - lo) / (hi - lo) * (r.h - 40);
  const mapX = t => r.x + 52 + t / P.tmax * (r.w - 70);

  ctx.fillStyle = 'rgba(9,9,11,0.55)';
  ctx.strokeStyle = 'rgba(34,211,238,0.20)';
  ctx.lineWidth = 1;
  ctx.beginPath();
  if (ctx.roundRect) ctx.roundRect(r.x, r.y, r.w, r.h, 10); else ctx.rect(r.x, r.y, r.w, r.h);
  ctx.fill();
  ctx.stroke();

  ctx.fillStyle = color;
  ctx.font = 'bold 14px ui-monospace,monospace';
  ctx.fillText(title, r.x + 12, r.y + 16);
  ctx.fillStyle = 'rgba(168,168,178,0.85)';
  ctx.font = '12px ui-monospace,monospace';
  ctx.fillText(unit, r.x + 12 + ctx.measureText(title).width + 10, r.y + 16);

  const zeroY = mapY(0);
  ctx.strokeStyle = 'rgba(148,148,158,0.45)';
  ctx.setLineDash([4, 5]);
  ctx.beginPath();
  ctx.moveTo(r.x + 46, zeroY);
  ctx.lineTo(r.x + r.w - 12, zeroY);
  ctx.stroke();
  ctx.setLineDash([]);

  if (fill) {
    ctx.beginPath();
    ctx.moveTo(mapX(0), zeroY);
    for (let k = 0; k <= 240; k++) {
      const t = P.tmax * k / 240;
      ctx.lineTo(mapX(t), mapY(fn(t)));
    }
    ctx.lineTo(mapX(P.tmax), zeroY);
    ctx.closePath();
    ctx.fillStyle = color.replace(/[\d.]+\)$/, '0.13)');
    ctx.fill();
  }

  ctx.beginPath();
  for (let k = 0; k <= 240; k++) {
    const t = P.tmax * k / 240;
    const px = mapX(t), py = mapY(fn(t));
    if (k === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
  }
  ctx.strokeStyle = color;
  ctx.lineWidth = 2;
  ctx.lineJoin = 'round';
  ctx.stroke();

  ctx.fillStyle = 'rgba(200,200,210,0.95)';
  ctx.font = '12px ui-monospace,monospace';
  const ticks = [0, P.tmax / 2, P.tmax];
  for (const tk of ticks) {
    ctx.fillText(tk.toFixed(1) + 's', mapX(tk) - 8, r.y + r.h - 5);
  }
  ctx.fillText(hi.toFixed(1), r.x + 6, mapY(hi) + 12);
  ctx.fillText(lo.toFixed(1), r.x + 6, mapY(lo) + 4);

  const cx = mapX(tNow);
  const cv = fn(tNow);
  const cy = mapY(cv);
  ctx.strokeStyle = 'rgba(251,191,36,0.65)';
  ctx.lineWidth = 1.2;
  ctx.beginPath();
  ctx.moveTo(cx, r.y + 22);
  ctx.lineTo(cx, r.y + r.h - 16);
  ctx.stroke();

  ctx.fillStyle = '#0b0b0f';
  ctx.strokeStyle = 'rgba(251,191,36,1)';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.arc(cx, cy, 4.6, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();

  const label = cv.toFixed(2);
  ctx.fillStyle = 'rgba(251,191,36,0.95)';
  ctx.font = 'bold 13px ui-monospace,monospace';
  const lx = Math.min(cx + 10, r.x + r.w - 54);
  ctx.fillText(label, lx, Math.max(r.y + 34, cy - 8));
}

let hudAcc = 0;
function updateAndRender(now) {
  const dt = simDt(now);
  const fps = fpsTick(now);

  tNow += dt * 0.75;
  if (tNow > P.tmax) tNow = 0;

  ctx.fillStyle = '#09090b';
  ctx.fillRect(0, 0, W, H);
  gridBackground(ctx, W, H);

  const rs = panelRects();
  drawPanel(rs[0], 'v–t 速度图', '/ m·s⁻¹', 'rgba(168,85,247,0.98)', vOf, true);
  drawPanel(rs[1], 'x–t 位移图', '/ m', 'rgba(34,211,238,0.98)', xOf, false);
  drawPanel(rs[2], 'a–t 加速度图', '/ m·s⁻²', 'rgba(251,191,36,0.98)', aOf, true);

  ctx.fillStyle = 'rgba(208,208,218,0.95)';
  ctx.font = '12px ui-monospace,monospace';
  ctx.fillText('x–t 斜率 = 速度　|　v–t 斜率 = 加速度、面积 = 位移　|　a–t 面积 = 速度变化', 42, H - 106);

  hudAcc += 0.016;
  if (hudAcc > 0.1) {
    hudAcc = 0;
    setText('h-t', tNow.toFixed(2) + ' s');
    setText('h-x', xOf(tNow).toFixed(2) + ' m');
    setText('h-v', vOf(tNow).toFixed(2) + ' m/s');
    setText('h-a', P.a.toFixed(2) + ' m/s²');
    setText('h-fps', fps.toFixed(0) + ' FPS');
  }
  requestAnimationFrame(updateAndRender);
}
function reset() { tNow = 0; }
window.__simReset = reset;
setText('h-fps', '60 FPS');
requestAnimationFrame(updateAndRender);
"""

SCRIPT_GRAPHSHM = r"""
const scene = makeCanvasPair();
const ctx = scene.ctx;
let W = scene.W, H = scene.H;

const P = { A: 1.5, w: 1.6, phi: 0 };
let tNow = 0, tmaxNow = 8;

function xOf(t) { return P.A * Math.cos(P.w * t + P.phi); }
function vOf(t) { return -P.A * P.w * Math.sin(P.w * t + P.phi); }
function aOf(t) { return -P.A * P.w * P.w * Math.cos(P.w * t + P.phi); }

function reload() {
  const s = scene.resize();
  W = s.W; H = s.H;
  tNow = 0;
}
bindRange(0, val => { P.A = val; tNow = 0; }, 1);
bindRange(1, val => { P.w = val; tNow = 0; }, 2);
bindRange(2, val => { P.phi = val; tNow = 0; }, 2);
window.addEventListener('resize', reload, { passive: true });
reload();

function panelRects() {
  const x0 = 40, x1 = W - 40;
  const y0 = 112, y1 = H - 136;
  const gap = 14;
  const totalW = x1 - x0;
  const lw = Math.round(totalW * 0.58);
  const rw = totalW - lw - gap;
  const rh = Math.round((y1 - y0 - gap) / 2);
  return [
    { x: x0, y: y0, w: lw, h: y1 - y0 },
    { x: x0 + lw + gap, y: y0, w: rw, h: rh },
    { x: x0 + lw + gap, y: y0 + rh + gap, w: rw, h: y1 - y0 - rh - gap },
  ];
}

function drawPanel(r, title, unit, color, fn) {
  let lo = Infinity, hi = -Infinity;
  for (let k = 0; k <= 240; k++) {
    const v = fn(tmaxNow * k / 240);
    if (v < lo) lo = v;
    if (v > hi) hi = v;
  }
  lo = Math.min(lo, 0);
  hi = Math.max(hi, 0);
  if (hi - lo < 1e-6) hi = lo + 1;
  const pad = (hi - lo) * 0.16;
  lo -= pad;
  hi += pad;

  const mapY = v => r.y + r.h - 20 - (v - lo) / (hi - lo) * (r.h - 40);
  const mapX = t => r.x + 52 + t / tmaxNow * (r.w - 70);

  ctx.fillStyle = 'rgba(9,9,11,0.55)';
  ctx.strokeStyle = 'rgba(34,211,238,0.20)';
  ctx.lineWidth = 1;
  ctx.beginPath();
  if (ctx.roundRect) ctx.roundRect(r.x, r.y, r.w, r.h, 10); else ctx.rect(r.x, r.y, r.w, r.h);
  ctx.fill();
  ctx.stroke();

  ctx.fillStyle = color;
  ctx.font = 'bold 14px ui-monospace,monospace';
  ctx.fillText(title, r.x + 12, r.y + 16);
  ctx.fillStyle = 'rgba(168,168,178,0.85)';
  ctx.font = '12px ui-monospace,monospace';
  ctx.fillText(unit, r.x + 12 + ctx.measureText(title).width + 10, r.y + 16);

  const zeroY = mapY(0);
  ctx.strokeStyle = 'rgba(148,148,158,0.45)';
  ctx.setLineDash([4, 5]);
  ctx.beginPath();
  ctx.moveTo(r.x + 46, zeroY);
  ctx.lineTo(r.x + r.w - 12, zeroY);
  ctx.stroke();
  ctx.setLineDash([]);

  ctx.beginPath();
  for (let k = 0; k <= 320; k++) {
    const t = tmaxNow * k / 320;
    const px = mapX(t), py = mapY(fn(t));
    if (k === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
  }
  ctx.strokeStyle = color;
  ctx.lineWidth = 2;
  ctx.lineJoin = 'round';
  ctx.stroke();

  ctx.fillStyle = 'rgba(200,200,210,0.95)';
  ctx.font = '12px ui-monospace,monospace';
  for (let k = 0; k <= 4; k++) {
    const tk = tmaxNow * k / 4;
    ctx.fillText(tk.toFixed(1) + 's', mapX(tk) - 8, r.y + r.h - 5);
  }
  ctx.fillText(hi.toFixed(1), r.x + 6, mapY(hi) + 12);
  ctx.fillText(lo.toFixed(1), r.x + 6, mapY(lo) + 4);

  const cx = mapX(tNow);
  const cy = mapY(fn(tNow));
  ctx.strokeStyle = 'rgba(251,191,36,0.65)';
  ctx.lineWidth = 1.2;
  ctx.beginPath();
  ctx.moveTo(cx, r.y + 22);
  ctx.lineTo(cx, r.y + r.h - 16);
  ctx.stroke();

  ctx.fillStyle = '#0b0b0f';
  ctx.strokeStyle = 'rgba(251,191,36,1)';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.arc(cx, cy, 4.6, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();

  ctx.fillStyle = 'rgba(251,191,36,0.95)';
  ctx.font = 'bold 12.5px ui-monospace,monospace';
  ctx.fillText(fn(tNow).toFixed(2), Math.min(cx + 10, r.x + r.w - 54), Math.max(r.y + 34, cy - 8));
}

let hudAcc = 0;
function updateAndRender(now) {
  const dt = simDt(now);
  const fps = fpsTick(now);

  tmaxNow = 4 * Math.PI / Math.max(0.2, P.w);
  tNow += dt * 0.8;
  if (tNow > tmaxNow) tNow = 0;

  ctx.fillStyle = '#09090b';
  ctx.fillRect(0, 0, W, H);
  gridBackground(ctx, W, H);

  const rs = panelRects();
  drawPanel(rs[0], 'v–t 速度图', '/ m·s⁻¹', 'rgba(168,85,247,0.98)', vOf);
  drawPanel(rs[1], 'x–t 位移图', '/ m', 'rgba(34,211,238,0.98)', xOf);
  drawPanel(rs[2], 'a–t 加速度图', '/ m·s⁻²', 'rgba(251,191,36,0.98)', aOf);

  ctx.fillStyle = 'rgba(208,208,218,0.95)';
  ctx.font = '12px ui-monospace,monospace';
  ctx.fillText('v 比 x 超前 90°，a 与 x 始终反相　|　a = −ω²·x', 42, H - 106);

  hudAcc += 0.016;
  if (hudAcc > 0.1) {
    hudAcc = 0;
    setText('h-t', tNow.toFixed(2) + ' s');
    setText('h-x', xOf(tNow).toFixed(2) + ' m');
    setText('h-v', vOf(tNow).toFixed(2) + ' m/s');
    setText('h-a', aOf(tNow).toFixed(2) + ' m/s²');
    setText('h-tp', (2 * Math.PI / P.w).toFixed(2) + ' s');
    setText('h-fps', fps.toFixed(0) + ' FPS');
  }
  requestAnimationFrame(updateAndRender);
}
function reset() { tNow = 0; }
window.__simReset = reset;
setText('h-fps', '60 FPS');
requestAnimationFrame(updateAndRender);
"""

SCRIPT_FREEFALL = r"""
const scene = makeCanvasPair();
const ctx = scene.ctx;
let W = scene.W, H = scene.H;

const P = { g: 9.8, k: 0.15, h: 10.2, v0: 0 };
let SCALE = 42;
const RAD = 9;

let y = 428, v = 0, t = 0, aNow = 0;
let landed = false, holdT = 0, tEnd = 0, vEnd = 0;
const hist = [];

function groundY() { return H - 126; }
function fitScale() { SCALE = Math.max(8, Math.min(42, 520 / Math.max(1, P.h))); }
function ballX() { return safeX() + Math.min(112, (W - safeX()) * 0.16); }
function reset() {
  y = P.h * SCALE; v = P.v0 * SCALE; t = 0; aNow = P.g * SCALE;
  landed = false; holdT = 0; tEnd = 0; vEnd = 0;
  hist.length = 0;
}
function relayout() {
  const s = scene.resize();
  W = s.W; H = s.H;
  fitScale();
  reset();
}

bindRange(0, val => { P.g = val; reset(); }, 1);
bindRange(1, val => { P.k = val; }, 2);
bindRange(2, val => { P.h = val; fitScale(); reset(); }, 1);
bindRange(3, val => { P.v0 = val; reset(); }, 1);
window.addEventListener('resize', relayout, { passive: true });
relayout();

function step(dt) {
  if (landed) {
    holdT += dt;
    if (holdT > 1.2) reset();
    return;
  }
  aNow = P.g * SCALE - P.k * v;
  v += aNow * dt;
  if (v < 0) v = 0;
  y -= v * dt;
  t += dt;
  if (y <= 0) {
    y = 0; tEnd = t; vEnd = v; landed = true; v = 0;
  }
}

function drawRuler() {
  const gy = groundY();
  const rx = safeX() + 10;
  const topY = Math.max(78, gy - P.h * SCALE - 30);

  ctx.strokeStyle = 'rgba(34,211,238,0.22)';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(rx, topY);
  ctx.lineTo(rx, gy);
  ctx.stroke();

  ctx.font = '10.5px ui-monospace,monospace';
  for (let m = 0; m <= P.h + 0.01; m += 1) {
    const yy = gy - m * SCALE;
    const major = m % 2 === 0;
    ctx.strokeStyle = major ? 'rgba(34,211,238,0.45)' : 'rgba(34,211,238,0.18)';
    ctx.beginPath();
    ctx.moveTo(rx, yy);
    ctx.lineTo(rx + (major ? 13 : 7), yy);
    ctx.stroke();
    if (major) {
      ctx.fillStyle = 'rgba(212,212,222,0.96)';
      ctx.fillText(m + ' m', rx - 26, yy + 3);
    }
  }

  ctx.strokeStyle = 'rgba(34,211,238,0.85)';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(W * 0.10, gy);
  ctx.lineTo(W * 0.92, gy);
  ctx.stroke();
  ctx.fillStyle = 'rgba(34,211,238,0.22)';
  ctx.fillRect(W * 0.10, gy, W * 0.82, 9);

  ctx.strokeStyle = 'rgba(168,85,247,0.30)';
  ctx.setLineDash([5, 7]);
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(rx, gy - y);
  ctx.lineTo(ballX() + 40, gy - y);
  ctx.stroke();
  ctx.setLineDash([]);
  ctx.fillStyle = 'rgba(226,196,255,0.98)';
  ctx.fillText('h = ' + (y / SCALE).toFixed(2) + ' m', ballX() + 46, gy - y - 6);
}

function drawTrail() {
  for (let i = 0; i < hist.length; i++) {
    const yy = groundY() - hist[i];
    ctx.fillStyle = 'rgba(34,211,238,' + (0.06 + 0.22 * i / hist.length).toFixed(3) + ')';
    ctx.beginPath();
    ctx.arc(ballX(), yy, 2.4, 0, Math.PI * 2);
    ctx.fill();
  }
}

function drawBall() {
  const gx = ballX(), gy = groundY();
  const cy = gy - y;

  const rg = ctx.createRadialGradient(gx, cy, 0, gx, cy, 42);
  rg.addColorStop(0, 'rgba(34,211,238,0.40)');
  rg.addColorStop(1, 'rgba(34,211,238,0)');
  ctx.fillStyle = rg;
  ctx.beginPath();
  ctx.arc(gx, cy, 42, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = '#0b0b0f';
  ctx.strokeStyle = 'rgba(103,232,249,0.95)';
  ctx.lineWidth = 2.4;
  ctx.beginPath();
  ctx.arc(gx, cy, RAD, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();

  if (!landed && v > 6) {
    const len = Math.min(120, v * 0.32);
    const ex = gx, ey = cy + len;
    ctx.strokeStyle = 'rgba(251,191,36,0.9)';
    ctx.fillStyle = 'rgba(251,191,36,0.9)';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(gx, cy + RAD);
    ctx.lineTo(ex, ey);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(ex, ey);
    ctx.lineTo(ex - 6, ey - 8);
    ctx.lineTo(ex + 6, ey - 8);
    ctx.closePath();
    ctx.fill();
  }
}

function drawVT() {
  const gw = Math.min(480, Math.max(340, W * 0.36)), gh = 198;
  const gx = W - gw - 24, gy = H - gh - 214;
  if (gx < W * 0.54) return;
  ctx.fillStyle = 'rgba(20,20,27,0.94)';
  ctx.strokeStyle = 'rgba(34,211,238,0.38)';
  ctx.lineWidth = 1.2;
  ctx.beginPath();
  if (ctx.roundRect) ctx.roundRect(gx, gy, gw, gh, 12); else ctx.rect(gx, gy, gw, gh);
  ctx.fill();
  ctx.stroke();

  const padL = 30, padR = 20, padT = 50, padB = 34;
  const pw = gw - padL - padR, phh = gh - padT - padB;

  ctx.strokeStyle = 'rgba(160,160,172,0.55)';
  ctx.lineWidth = 1.2;
  ctx.beginPath();
  ctx.moveTo(gx + padL, gy + gh - padB);
  ctx.lineTo(gx + padL + pw, gy + gh - padB);
  ctx.moveTo(gx + padL, gy + padT);
  ctx.lineTo(gx + padL, gy + gh - padB);
  ctx.stroke();

  let vmax = 0.1;
  for (const s2 of hist) if (s2 > vmax) vmax = s2;
  vmax *= 1.15;

  ctx.beginPath();
  for (let i = 0; i < hist.length; i++) {
    const x = gx + padL + i / Math.max(1, hist.length - 1) * pw;
    const yy = gy + gh - padB - hist[i] / vmax * phh;
    if (i === 0) ctx.moveTo(x, yy); else ctx.lineTo(x, yy);
  }
  ctx.strokeStyle = 'rgba(251,191,36,1)';
  ctx.lineWidth = 2.6;
  ctx.stroke();

  ctx.fillStyle = 'rgba(251,191,36,1)';
  ctx.font = 'bold 14px ui-monospace,monospace';
  ctx.fillText('v–t 图像', gx + 16, gy + 24);
  ctx.fillStyle = 'rgba(214,214,224,0.96)';
  ctx.font = '12px ui-monospace,monospace';
  ctx.fillText('速度 v / m·s⁻¹', gx + 100, gy + 24);
  ctx.fillText('t →', gx + gw - 40, gy + gh - 10);
  ctx.fillText(vmax.toFixed(1), gx + 4, gy + padT + 12);
}

function drawBanner() {
  if (!landed) return;
  const text = '落地  t = ' + tEnd.toFixed(2) + ' s   v = ' + (vEnd / SCALE).toFixed(2) + ' m/s';
  ctx.fillStyle = 'rgba(251,191,36,0.92)';
  ctx.font = '12px ui-monospace,monospace';
  ctx.fillText(text, Math.min(ballX() - 60, W - 320), 88);
}

let hudAcc = 0, histT = 0;
function updateAndRender(now) {
  const dt = simDt(now);
  const fps = fpsTick(now);

  step(dt);
  histT += dt;
  if (histT > 0.024) {
    histT = 0;
    hist.push(v / SCALE);
    if (hist.length > 240) hist.shift();
  }

  ctx.fillStyle = '#09090b';
  ctx.fillRect(0, 0, W, H);
  gridBackground(ctx, W, H);
  drawRuler();
  drawTrail();
  drawBall();
  drawVT();
  drawBanner();

  hudAcc += 0.016;
  if (hudAcc > 0.12) {
    hudAcc = 0;
    setText('h-t', t.toFixed(2) + ' s');
    setText('h-v', (v / SCALE).toFixed(2) + ' m/s');
    setText('h-h', (y / SCALE).toFixed(2) + ' m');
    setText('h-a', (aNow / SCALE).toFixed(2) + ' m/s²');
    setText('h-fps', fps.toFixed(0) + ' FPS');
  }
  requestAnimationFrame(updateAndRender);
}
setText('h-fps', '60 FPS');
requestAnimationFrame(updateAndRender);
window.__simReset = reset;
"""

SCRIPT_PROJECTILE = r"""
const scene = makeCanvasPair();
const ctx = scene.ctx;
let W = scene.W, H = scene.H;

const P = { v0: 3.6, g: 9.8, h: 8.1 };
let SCALE = 42;
const RAD = 8.5;

let x = 0, y = 0, vy = 0, t = 0;
let landed = false, holdT = 0, tEnd = 0, xEnd = 0;
let pts = [];

function groundY() { return H - 132; }
function fitScale() { SCALE = Math.max(8, Math.min(42, (groundY() - 150) / Math.max(1, P.h))); }
function origin() {
  return { ox: safeX() + 44, oy: groundY() - P.h * SCALE };
}
function reset() {
  x = 0; y = 0; vy = 0; t = 0;
  landed = false; holdT = 0; tEnd = 0; xEnd = 0;
  pts = [];
}
function relayout() {
  const s = scene.resize();
  W = s.W; H = s.H;
  fitScale();
  reset();
}

bindRange(0, val => { P.v0 = val; reset(); }, 1);
bindRange(1, val => { P.g = val; reset(); }, 1);
bindRange(2, val => { P.h = val; fitScale(); reset(); }, 1);
window.addEventListener('resize', relayout, { passive: true });
relayout();

function step(dt) {
  if (landed) {
    holdT += dt;
    if (holdT > 1.2) reset();
    return;
  }
  vy += P.g * SCALE * dt;
  x += P.v0 * SCALE * dt;
  y += vy * dt;
  t += dt;
  if (y >= P.h * SCALE) {
    y = P.h; xEnd = x; tEnd = t; landed = true;
  }
}

function drawAxes() {
  const { ox, oy } = origin();
  const gy = groundY();

  ctx.strokeStyle = 'rgba(34,211,238,0.10)';
  ctx.lineWidth = 1;
  for (let i = 0; i * SCALE < P.h + 4; i++) {
    ctx.beginPath();
    ctx.moveTo(ox, oy + i * SCALE);
    ctx.lineTo(ox + Math.min(W * 0.72, 520), oy + i * SCALE);
    ctx.stroke();
  }

  ctx.strokeStyle = 'rgba(34,211,238,0.45)';
  ctx.lineWidth = 1.4;
  ctx.beginPath();
  ctx.moveTo(ox, oy);
  ctx.lineTo(ox + Math.min(W * 0.72, 520), oy);
  ctx.moveTo(ox, oy);
  ctx.lineTo(ox, gy + 12);
  ctx.stroke();

  ctx.font = '10.5px ui-monospace,monospace';
  for (let m = 0; m * SCALE <= P.h + 1; m += 2) {
    const yy = oy + m * SCALE;
    ctx.strokeStyle = 'rgba(34,211,238,0.30)';
    ctx.beginPath();
    ctx.moveTo(ox - 5, yy);
    ctx.lineTo(ox, yy);
    ctx.stroke();
    ctx.fillStyle = 'rgba(212,212,222,0.96)';
    ctx.fillText(m + ' m', ox - 34, yy + 3);
  }
  for (let m = 2; m * SCALE <= 520; m += 2) {
    const xx = ox + m * SCALE;
    if (xx > W - 20) break;
    ctx.strokeStyle = 'rgba(34,211,238,0.30)';
    ctx.beginPath();
    ctx.moveTo(xx, oy - 5);
    ctx.lineTo(xx, oy);
    ctx.stroke();
    ctx.fillStyle = 'rgba(208,208,218,0.95)';
    ctx.fillText(m + '', xx - 3, oy - 10);
  }

  ctx.fillStyle = 'rgba(34,211,238,0.88)';
  ctx.fillText('x / m', ox + 8, oy - 16);
  ctx.fillText('y / m', ox + 8, oy + 26);

  const rg = ctx.createRadialGradient(ox, oy, 0, ox, oy, 22);
  rg.addColorStop(0, 'rgba(34,211,238,0.85)');
  rg.addColorStop(1, 'rgba(34,211,238,0)');
  ctx.fillStyle = rg;
  ctx.beginPath();
  ctx.arc(ox, oy, 22, 0, Math.PI * 2);
  ctx.fill();

  ctx.strokeStyle = 'rgba(34,211,238,0.50)';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(W * 0.06, groundY());
  ctx.lineTo(W * 0.96, groundY());
  ctx.stroke();
}

function drawPrediction() {
  const { ox, oy } = origin();
  const tg = Math.sqrt(2 * P.h / P.g);
  ctx.save();
  ctx.setLineDash([5, 8]);
  ctx.strokeStyle = 'rgba(168,85,247,0.42)';
  ctx.lineWidth = 1.2;
  ctx.beginPath();
  for (let i = 0; i <= 60; i++) {
    const tt = tg * i / 60;
    const px = ox + P.v0 * SCALE * tt;
    const py = oy + 0.5 * P.g * SCALE * tt * tt;
    if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
  }
  ctx.stroke();
  ctx.restore();

  const ex = ox + P.v0 * SCALE * tg;
  const ey = oy + P.h * SCALE;
  ctx.strokeStyle = 'rgba(244,114,182,0.75)';
  ctx.lineWidth = 1.2;
  ctx.beginPath();
  ctx.moveTo(ex, ey - 26);
  ctx.lineTo(ex, ey + 8);
  ctx.stroke();
  ctx.fillStyle = 'rgba(244,114,182,0.85)';
  ctx.font = '10.5px ui-monospace,monospace';
  ctx.fillText('落点 ' + (P.v0 * tg).toFixed(1) + ' m', ex - 26, ey - 34);
}

function drawTrail() {
  const { ox, oy } = origin();
  if (pts.length > 1) {
    ctx.beginPath();
    for (let i = 0; i < pts.length; i++) {
      const px = ox + pts[i].x, py = oy + pts[i].y;
      if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
    }
    ctx.strokeStyle = 'rgba(103,232,249,0.85)';
    ctx.lineWidth = 2.2;
    ctx.stroke();
  }
}

function drawBall() {
  const { ox, oy } = origin();
  const sx = ox + x, sy = oy + y;

  const rg = ctx.createRadialGradient(sx, sy, 0, sx, sy, 34);
  rg.addColorStop(0, 'rgba(251,191,36,0.42)');
  rg.addColorStop(1, 'rgba(251,191,36,0)');
  ctx.fillStyle = rg;
  ctx.beginPath();
  ctx.arc(sx, sy, 34, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = '#0b0b0f';
  ctx.strokeStyle = 'rgba(251,191,36,0.95)';
  ctx.lineWidth = 2.2;
  ctx.beginPath();
  ctx.arc(sx, sy, RAD, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();

  const k = 0.22;
  arrow(sx, sy, sx + P.v0 * SCALE * k, sy, 'rgba(34,211,238,0.9)');
  arrow(sx, sy, sx, sy + vy * k, 'rgba(168,85,247,0.9)');
  arrow(sx, sy, sx + P.v0 * SCALE * k, sy + vy * k, 'rgba(251,191,36,0.95)');
}

function arrow(x1, y1, x2, y2, color) {
  if (Math.abs(x2 - x1) < 1 && Math.abs(y2 - y1) < 1) return;
  ctx.save();
  ctx.strokeStyle = color;
  ctx.fillStyle = color;
  ctx.lineWidth = 1.6;
  ctx.beginPath();
  ctx.moveTo(x1, y1);
  ctx.lineTo(x2, y2);
  ctx.stroke();
  const a = Math.atan2(y2 - y1, x2 - x1);
  ctx.beginPath();
  ctx.moveTo(x2, y2);
  ctx.lineTo(x2 - 7 * Math.cos(a - 0.4), y2 - 7 * Math.sin(a - 0.4));
  ctx.lineTo(x2 - 7 * Math.cos(a + 0.4), y2 - 7 * Math.sin(a + 0.4));
  ctx.closePath();
  ctx.fill();
  ctx.restore();
}

function drawBanner() {
  if (!landed) return;
  ctx.fillStyle = 'rgba(251,191,36,0.92)';
  ctx.font = '12px ui-monospace,monospace';
  ctx.fillText('落地  t = ' + tEnd.toFixed(2) + ' s   x = ' + (xEnd / SCALE).toFixed(2) + ' m', safeX() + 16, 30);
}

let hudAcc = 0;
function updateAndRender(now) {
  const dt = simDt(now);
  const fps = fpsTick(now);

  step(dt);
  const { ox, oy } = origin();
  const last = pts[pts.length - 1];
  if (!last || Math.hypot(last.x - x, last.y - y) > 1.5) {
    pts.push({ x: x, y: y });
    if (pts.length > 900) pts.shift();
  }

  ctx.fillStyle = '#09090b';
  ctx.fillRect(0, 0, W, H);
  gridBackground(ctx, W, H);
  drawAxes();
  drawPrediction();
  drawTrail();
  drawBall();
  drawBanner();
  void ox; void oy;

  hudAcc += 0.016;
  if (hudAcc > 0.12) {
    hudAcc = 0;
    const v = Math.hypot(P.v0 * SCALE, vy);
    setText('h-t', t.toFixed(2) + ' s');
    setText('h-x', (x / SCALE).toFixed(2) + ' m');
    setText('h-y', (y / SCALE).toFixed(2) + ' m');
    setText('h-vx', P.v0.toFixed(2));
    setText('h-vy', (vy / SCALE).toFixed(2));
    setText('h-v', (v / SCALE).toFixed(2) + ' m/s');
    setText('h-fps', fps.toFixed(0) + ' FPS');
  }
  requestAnimationFrame(updateAndRender);
}
setText('h-fps', '60 FPS');
requestAnimationFrame(updateAndRender);
window.__simReset = reset;
"""

SCRIPT_NEWTON = r"""
const scene = makeCanvasPair();
const ctx = scene.ctx;
let W = scene.W, H = scene.H;

const P = { F: 40, m: 6, mu: 0.15, g: 9.8 };
const SCALE = 40;
const BW = 66, BH = 66;

let xm = 0, v = 0, a = 0, f = 0, moving = false;
let histA = [], histV = [];

function groundY() { return H - 154; }
function originX() { return safeX() + 30; }
function reset() {
  xm = 0; v = 0; a = 0; f = 0; moving = false;
  histA = []; histV = [];
}
function relayout() {
  const s = scene.resize();
  W = s.W; H = s.H;
  reset();
}

bindRange(0, val => { P.F = val; }, 1);
bindRange(1, val => { P.m = val; reset(); }, 1);
bindRange(2, val => { P.mu = val; }, 2);
bindRange(3, val => { P.g = val; }, 1);
window.addEventListener('resize', relayout, { passive: true });
relayout();

function step(dt) {
  const N = P.m * P.g;
  const fmax = P.mu * N;
  if (v > 0.002) {
    f = -P.mu * N;
    moving = true;
  } else if (P.F > fmax) {
    f = -P.mu * N;
    moving = true;
  } else {
    f = -P.F;
    moving = false;
  }
  a = (P.F + f) / P.m;
  v += a * dt;
  if (v < 0) v = 0;
  xm += v * dt;

  histA.push(a);
  histV.push(v);
  if (histA.length > 220) { histA.shift(); histV.shift(); }

  const maxX = (W * 0.86 - originX() - BW) / SCALE;
  if (xm > maxX) reset();
}

function drawGround() {
  const gy = groundY();
  ctx.strokeStyle = 'rgba(34,211,238,0.45)';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(W * 0.06, gy);
  ctx.lineTo(W * 0.94, gy);
  ctx.stroke();

  ctx.strokeStyle = 'rgba(34,211,238,0.10)';
  ctx.lineWidth = 1;
  for (let i = -7; i <= 14; i++) {
    const xx = originX() + i * SCALE;
    ctx.beginPath();
    ctx.moveTo(xx, gy);
    ctx.lineTo(xx + 24, gy + 26);
    ctx.stroke();
  }
  for (let i = 1; i <= 12; i++) {
    const xx = originX() + i * SCALE;
    if (xx > W * 0.9) break;
    ctx.strokeStyle = 'rgba(34,211,238,0.22)';
    ctx.beginPath();
    ctx.moveTo(xx, gy);
    ctx.lineTo(xx, gy - 6);
    ctx.stroke();
    ctx.fillStyle = 'rgba(208,208,218,0.95)';
    ctx.font = '10.5px ui-monospace,monospace';
    ctx.fillText(i + '', xx - 3, gy + 20);
  }
}

function drawBlock() {
  const gy = groundY();
  const sx = originX() + xm * SCALE;
  const sy = gy - BH;

  ctx.fillStyle = 'rgba(34,211,238,0.10)';
  ctx.fillRect(sx - 8, gy, BW + 16, 6);

  ctx.fillStyle = '#101015';
  ctx.strokeStyle = 'rgba(34,211,238,0.85)';
  ctx.lineWidth = 2;
  ctx.beginPath();
  if (ctx.roundRect) ctx.roundRect(sx, sy, BW, BH, 7); else ctx.rect(sx, sy, BW, BH);
  ctx.fill();
  ctx.stroke();

  ctx.fillStyle = 'rgba(165,243,252,0.95)';
  ctx.font = 'bold 12px ui-monospace,monospace';
  ctx.fillText(P.m.toFixed(1) + ' kg', sx + 9, sy + 26);
  ctx.fillStyle = 'rgba(113,113,122,0.8)';
  ctx.font = '10.5px ui-monospace,monospace';
  ctx.fillText('BLOCK', sx + 12, sy + 44);

  const cx = sx + BW * 0.5, cy = sy + BH * 0.5;
  const N = P.m * P.g;
  const maxF = Math.max(1, P.F, Math.abs(f), N);
  const L = 62;

  forceArrow(cx + BW * 0.5, cy, cx + BW * 0.5 + (P.F / maxF) * L, cy, 'rgba(244,114,182,0.95)', 'F');
  forceArrow(cx - BW * 0.5, cy, cx - BW * 0.5 + (f / maxF) * L, cy, 'rgba(251,191,36,0.95)', 'f');
  forceArrow(cx, sy, cx, sy - (N / maxF) * L, 'rgba(74,222,128,0.9)', 'N');
  forceArrow(cx, gy, cx, gy + (N / maxF) * L, 'rgba(168,85,247,0.9)', 'G');

  if (v > 0.02) {
    forceArrow(cx, sy - 34, cx + Math.min(90, v * 12), sy - 34, 'rgba(103,232,249,0.9)', 'v');
  }
}

function forceArrow(x1, y1, x2, y2, color, label) {
  if (Math.abs(x2 - x1) < 2 && Math.abs(y2 - y1) < 2) return;
  ctx.save();
  ctx.strokeStyle = color;
  ctx.fillStyle = color;
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(x1, y1);
  ctx.lineTo(x2, y2);
  ctx.stroke();
  const ang = Math.atan2(y2 - y1, x2 - x1);
  ctx.beginPath();
  ctx.moveTo(x2, y2);
  ctx.lineTo(x2 - 8 * Math.cos(ang - 0.42), y2 - 8 * Math.sin(ang - 0.42));
  ctx.lineTo(x2 - 8 * Math.cos(ang + 0.42), y2 - 8 * Math.sin(ang + 0.42));
  ctx.closePath();
  ctx.fill();
  ctx.font = 'bold 11px ui-monospace,monospace';
  ctx.fillText(label, x2 + Math.cos(ang) * 8 - 4, y2 + Math.sin(ang) * 8 + 4);
  ctx.restore();
}

function drawChart() {
  const gw = Math.min(480, Math.max(340, W * 0.35)), gh = 198;
  const gx = W - gw - 22;
  const gy = Math.min(150, groundY() - BH - gh - 34);
  if (gx < W * 0.52) return;
  ctx.fillStyle = 'rgba(20,20,27,0.94)';
  ctx.strokeStyle = 'rgba(34,211,238,0.36)';
  ctx.lineWidth = 1.2;
  ctx.beginPath();
  if (ctx.roundRect) ctx.roundRect(gx, gy, gw, gh, 12); else ctx.rect(gx, gy, gw, gh);
  ctx.fill();
  ctx.stroke();

  const padL = 26, padR = 20, padT = 52, padB = 32;
  const pw = gw - padL - padR, phh = gh - padT - padB;

  ctx.strokeStyle = 'rgba(160,160,172,0.55)';
  ctx.lineWidth = 1.2;
  ctx.beginPath();
  ctx.moveTo(gx + padL, gy + gh - padB);
  ctx.lineTo(gx + padL + pw, gy + gh - padB);
  ctx.moveTo(gx + padL, gy + padT);
  ctx.lineTo(gx + padL, gy + gh - padB);
  ctx.stroke();

  let vmax = 0.5;
  for (const s2 of histV) if (Math.abs(s2) > vmax) vmax = Math.abs(s2);
  ctx.beginPath();
  for (let i = 0; i < histV.length; i++) {
    const px = gx + padL + i / Math.max(1, histV.length - 1) * pw;
    const py = gy + gh - padB - (histV[i] / vmax) * phh * 0.46;
    if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
  }
  ctx.strokeStyle = 'rgba(103,232,249,1)';
  ctx.lineWidth = 2.4;
  ctx.stroke();

  let amax = 0.5;
  for (const s2 of histA) if (Math.abs(s2) > amax) amax = Math.abs(s2);
  ctx.beginPath();
  for (let i = 0; i < histA.length; i++) {
    const px = gx + padL + i / Math.max(1, histA.length - 1) * pw;
    const py = gy + gh - padB - (histA[i] / amax) * phh * 0.46;
    if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
  }
  ctx.strokeStyle = 'rgba(251,191,36,0.95)';
  ctx.lineWidth = 2;
  ctx.stroke();

  ctx.font = 'bold 14px ui-monospace,monospace';
  ctx.fillStyle = 'rgba(103,232,249,1)';
  ctx.fillText('v–t 速度', gx + 16, gy + 24);
  ctx.fillStyle = 'rgba(251,191,36,1)';
  ctx.fillText('a–t 加速度', gx + 122, gy + 24);
  ctx.fillStyle = 'rgba(214,214,224,0.95)';
  ctx.font = '12px ui-monospace,monospace';
  ctx.fillText('t →', gx + gw - 40, gy + gh - 10);
}

function drawStatus() {
  const txt = moving
    ? '滑动状态：F_net = F − μmg → 匀加速'
    : (P.F > 0 ? '静止状态：拉力未超过最大静摩擦' : '静止状态：无外力');
  ctx.fillStyle = moving ? 'rgba(34,211,238,0.85)' : 'rgba(251,191,36,0.9)';
  ctx.font = '12px ui-monospace,monospace';
  ctx.fillText(txt, safeX() + 16, 30);
}

let hudAcc = 0;
function updateAndRender(now) {
  const dt = simDt(now);
  const fps = fpsTick(now);

  step(dt);

  ctx.fillStyle = '#09090b';
  ctx.fillRect(0, 0, W, H);
  gridBackground(ctx, W, H);
  drawGround();
  drawBlock();
  drawChart();
  drawStatus();

  hudAcc += 0.016;
  if (hudAcc > 0.12) {
    hudAcc = 0;
    setText('h-a', a.toFixed(2) + ' m/s²');
    setText('h-v', v.toFixed(2) + ' m/s');
    setText('h-x', xm.toFixed(2) + ' m');
    setText('h-f', f.toFixed(1) + ' N');
    setText('h-nf', (P.F + f).toFixed(1) + ' N');
    setText('h-fps', fps.toFixed(0) + ' FPS');
  }
  requestAnimationFrame(updateAndRender);
}
setText('h-fps', '60 FPS');
requestAnimationFrame(updateAndRender);
window.__simReset = reset;
"""

SCRIPT_CIRCULAR = r"""
const scene = makeCanvasPair();
const ctx = scene.ctx;
let W = scene.W, H = scene.H;

const P = { w: 1.4, r: 3.9, m: 1.5, th0: 0 };
let SCALE = 40;
const RAD = 11;

let th = 0;
let cx = 0, cy = 0;

function fitScale() {
  const room = Math.min(W - safeX() - 90, H - 190);
  SCALE = Math.max(3, Math.min(40, room * 0.42 / Math.max(0.2, P.r)));
}
function relayout() {
  const s = scene.resize();
  W = s.W; H = s.H;
  fitScale();
  cx = Math.max(W * 0.5, safeX() + P.r * SCALE + 24);
  cy = (H - 104) * 0.46;
}
bindRange(0, val => { P.w = val; }, 2);
bindRange(1, val => { P.r = val; fitScale(); cx = Math.max(W * 0.5, safeX() + P.r * SCALE + 24); }, 1);
bindRange(2, val => { P.m = val; }, 1);
bindRange(3, val => { P.th0 = val; th = val * Math.PI / 180; }, 0);
window.addEventListener('resize', relayout, { passive: true });
relayout();

function arrow(x1, y1, x2, y2, color, width) {
  if (Math.abs(x2 - x1) < 1.5 && Math.abs(y2 - y1) < 1.5) return;
  ctx.save();
  ctx.strokeStyle = color;
  ctx.fillStyle = color;
  ctx.lineWidth = width || 2;
  ctx.beginPath();
  ctx.moveTo(x1, y1);
  ctx.lineTo(x2, y2);
  ctx.stroke();
  const a = Math.atan2(y2 - y1, x2 - x1);
  ctx.beginPath();
  ctx.moveTo(x2, y2);
  ctx.lineTo(x2 - 9 * Math.cos(a - 0.4), y2 - 9 * Math.sin(a - 0.4));
  ctx.lineTo(x2 - 9 * Math.cos(a + 0.4), y2 - 9 * Math.sin(a + 0.4));
  ctx.closePath();
  ctx.fill();
  ctx.restore();
}

function drawOrbit() {
  ctx.save();
  ctx.setLineDash([4, 8]);
  ctx.strokeStyle = 'rgba(34,211,238,0.22)';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.arc(cx, cy, P.r * SCALE, 0, Math.PI * 2);
  ctx.stroke();
  ctx.restore();

  for (let k = 0; k < 12; k++) {
    const ang = k / 12 * Math.PI * 2;
    const x1 = cx + Math.cos(ang) * (P.r * SCALE - 4);
    const y1 = cy + Math.sin(ang) * (P.r * SCALE - 4);
    const x2 = cx + Math.cos(ang) * (P.r * SCALE + 4);
    const y2 = cy + Math.sin(ang) * (P.r * SCALE + 4);
    ctx.strokeStyle = 'rgba(34,211,238,0.18)';
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.stroke();
  }

  const rr = 34;
  ctx.strokeStyle = 'rgba(168,85,247,0.55)';
  ctx.lineWidth = 1.4;
  ctx.beginPath();
  ctx.arc(cx, cy, rr, 0, th % (Math.PI * 2));
  ctx.stroke();
  ctx.fillStyle = 'rgba(192,132,252,0.8)';
  ctx.font = '11.5px ui-monospace,monospace';
  ctx.fillText('θ', cx + rr + 6, cy + 4);
}

function drawCenter() {
  const rg = ctx.createRadialGradient(cx, cy, 0, cx, cy, 26);
  rg.addColorStop(0, 'rgba(226,232,240,0.85)');
  rg.addColorStop(1, 'rgba(226,232,240,0)');
  ctx.fillStyle = rg;
  ctx.beginPath();
  ctx.arc(cx, cy, 26, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = '#0b0b0f';
  ctx.strokeStyle = 'rgba(226,232,240,0.9)';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.arc(cx, cy, 6, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();
}

function drawBall() {
  const bx = cx + Math.cos(th) * P.r * SCALE;
  const by = cy + Math.sin(th) * P.r * SCALE;

  ctx.strokeStyle = 'rgba(178,190,205,0.68)';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(cx, cy);
  ctx.lineTo(bx, by);
  ctx.stroke();

  const rg = ctx.createRadialGradient(bx, by, 0, bx, by, 40);
  rg.addColorStop(0, 'rgba(103,232,249,0.45)');
  rg.addColorStop(1, 'rgba(103,232,249,0)');
  ctx.fillStyle = rg;
  ctx.beginPath();
  ctx.arc(bx, by, 40, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = '#0b0b0f';
  ctx.strokeStyle = 'rgba(103,232,249,0.95)';
  ctx.lineWidth = 2.4;
  ctx.beginPath();
  ctx.arc(bx, by, RAD, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();

  const vlen = Math.min(130, P.w * P.r * SCALE * 0.30);
  const tx = -Math.sin(th), ty = Math.cos(th);
  arrow(bx, by, bx + tx * vlen, by + ty * vlen, 'rgba(74,222,128,0.95)', 2.2);

  const alen = Math.min(120, P.w * P.w * P.r * SCALE * 0.24);
  const nx = -Math.cos(th), ny = -Math.sin(th);
  arrow(bx, by, bx + nx * alen, by + ny * alen, 'rgba(168,85,247,0.95)', 2.2);

  ctx.font = '11.5px ui-monospace,monospace';
  ctx.fillStyle = 'rgba(74,222,128,0.9)';
  ctx.fillText('v', bx + tx * vlen + 6, by + ty * vlen + 4);
  ctx.fillStyle = 'rgba(192,132,252,0.9)';
  ctx.fillText('a_c', bx + nx * alen + 6, by + ny * alen + 4);
}

let hudAcc = 0;
function updateAndRender(now) {
  const dt = simDt(now);
  const fps = fpsTick(now);

  th += P.w * dt;
  if (th > Math.PI * 200) th -= Math.PI * 200;

  ctx.fillStyle = '#09090b';
  ctx.fillRect(0, 0, W, H);
  gridBackground(ctx, W, H);
  drawOrbit();
  drawCenter();
  drawBall();

  ctx.fillStyle = 'rgba(34,211,238,0.88)';
  ctx.font = '12px ui-monospace,monospace';
  ctx.fillText('F = mω²r 指向圆心，速度始终沿切线', safeX() + 16, 30);

  hudAcc += 0.016;
  if (hudAcc > 0.12) {
    hudAcc = 0;
    const deg = (th % (Math.PI * 2)) * 180 / Math.PI;
    const v = P.w * P.r;
    const ac = P.w * P.w * P.r;
    setText('h-th', deg.toFixed(1) + '°');
    setText('h-v', v.toFixed(2) + ' m/s');
    setText('h-ac', ac.toFixed(2) + ' m/s²');
    setText('h-tp', (Math.PI * 2 / P.w).toFixed(2) + ' s');
    setText('h-f', (P.m * ac).toFixed(2) + ' N');
    setText('h-fps', fps.toFixed(0) + ' FPS');
  }
  requestAnimationFrame(updateAndRender);
}
setText('h-fps', '60 FPS');
requestAnimationFrame(updateAndRender);
function reset() { th = P.th0 * Math.PI / 180; }
window.__simReset = reset;
"""

SCRIPT_COULOMB = r"""
const scene = makeCanvasPair();
const ctx = scene.ctx;
let W = scene.W, H = scene.H;

const P = { q1: 10.0, q2: -6.0, d: 7.5 };
let SCALE = 22;
const RQ = 15;

let cx = 0, cy = 0, q1x = 0, q2x = 0;
let lines = [];
let dirty = true;

function fitScale() {
  SCALE = Math.max(2, Math.min(22, (W * 0.5 - safeX() - 70) / Math.max(0.5, P.d * 0.5)));
}
function relayout() {
  const s = scene.resize();
  W = s.W; H = s.H;
  fitScale();
  cx = W * 0.5;
  cy = (H - 104) * 0.50;
  dirty = true;
}
bindRange(0, val => { P.q1 = val; dirty = true; }, 1);
bindRange(1, val => { P.q2 = val; dirty = true; }, 1);
bindRange(2, val => { P.d = val; fitScale(); dirty = true; }, 1);
window.addEventListener('resize', relayout, { passive: true });
relayout();

function placeCharges() {
  const half = P.d * SCALE * 0.5;
  q1x = cx - half;
  q2x = cx + half;
}

function fieldAt(px, py) {
  let ex = 0, ey = 0;
  const dx1 = px - q1x, dy1 = py - cy;
  const r1 = dx1 * dx1 + dy1 * dy1;
  if (r1 > 60) {
    const m = P.q1 / (r1 * Math.sqrt(r1));
    ex += dx1 * m; ey += dy1 * m;
  }
  const dx2 = px - q2x, dy2 = py - cy;
  const r2 = dx2 * dx2 + dy2 * dy2;
  if (r2 > 60) {
    const m = P.q2 / (r2 * Math.sqrt(r2));
    ex += dx2 * m; ey += dy2 * m;
  }
  return { x: ex, y: ey };
}

function trace(sx, sy, dir) {
  const pts = [[sx, sy]];
  let x = sx, y = sy;
  for (let i = 0; i < 620; i++) {
    const e = fieldAt(x, y);
    const m = Math.hypot(e.x, e.y);
    if (!isFinite(m) || m < 1e-10) break;
    x += dir * e.x / m * 3.4;
    y += dir * e.y / m * 3.4;
    pts.push([x, y]);
    if (Math.hypot(x - q1x, y - cy) < RQ - 2) break;
    if (Math.hypot(x - q2x, y - cy) < RQ - 2) break;
    if (x < -70 || x > W + 70 || y < -70 || y > H + 70) break;
  }
  return pts;
}

function buildLines() {
  placeCharges();
  lines = [];
  const add = (sx, sy, dir, count) => {
    for (let i = 0; i < count; i++) {
      const ang = i / count * Math.PI * 2;
      lines.push(trace(sx + Math.cos(ang) * RQ, sy + Math.sin(ang) * RQ, dir));
    }
  };
  if (Math.abs(P.q1) > 0.05) {
    add(q1x, cy, P.q1 > 0 ? 1 : -1, Math.min(24, Math.max(5, Math.round(Math.abs(P.q1) * 5))));
  }
  if (Math.abs(P.q2) > 0.05) {
    add(q2x, cy, P.q2 > 0 ? 1 : -1, Math.min(24, Math.max(5, Math.round(Math.abs(P.q2) * 5))));
  }
}

function drawLines() {
  ctx.lineWidth = 1.1;
  for (const pts of lines) {
    if (pts.length < 2) continue;
    ctx.beginPath();
    ctx.moveTo(pts[0][0], pts[0][1]);
    for (let i = 1; i < pts.length; i++) ctx.lineTo(pts[i][0], pts[i][1]);
    ctx.strokeStyle = 'rgba(34,211,238,0.34)';
    ctx.stroke();

    for (let i = 26; i < pts.length - 2; i += 74) {
      const x1 = pts[i][0], y1 = pts[i][1];
      const x2 = pts[i + 2][0], y2 = pts[i + 2][1];
      const a = Math.atan2(y2 - y1, x2 - x1);
      ctx.fillStyle = 'rgba(34,211,238,0.85)';
      ctx.beginPath();
      ctx.moveTo(x2, y2);
      ctx.lineTo(x2 - 7 * Math.cos(a - 0.45), y2 - 7 * Math.sin(a - 0.45));
      ctx.lineTo(x2 - 7 * Math.cos(a + 0.45), y2 - 7 * Math.sin(a + 0.45));
      ctx.closePath();
      ctx.fill();
    }
  }
}

function drawCharge(x, y, q, color) {
  const rg = ctx.createRadialGradient(x, y, 0, x, y, 46);
  rg.addColorStop(0, color + '0.45)');
  rg.addColorStop(1, color + '0)');
  ctx.fillStyle = rg;
  ctx.beginPath();
  ctx.arc(x, y, 46, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = '#0b0b0f';
  ctx.strokeStyle = color + '0.95)';
  ctx.lineWidth = 2.4;
  ctx.beginPath();
  ctx.arc(x, y, RQ, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();

  ctx.strokeStyle = color + '1)';
  ctx.lineWidth = 2.6;
  ctx.beginPath();
  ctx.moveTo(x - 6, y);
  ctx.lineTo(x + 6, y);
  if (q > 0) { ctx.moveTo(x, y - 6); ctx.lineTo(x, y + 6); }
  ctx.stroke();

  ctx.fillStyle = color + '0.92)';
  ctx.font = '12px ui-monospace,monospace';
  ctx.fillText(q.toFixed(1) + ' μC', x - 18, y + RQ + 18);
}

function drawAxis() {
  ctx.save();
  ctx.setLineDash([4, 8]);
  ctx.strokeStyle = 'rgba(150,150,160,0.55)';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(q1x, cy);
  ctx.lineTo(q2x, cy);
  ctx.stroke();
  ctx.restore();

  const mx = (q1x + q2x) * 0.5;
  ctx.strokeStyle = 'rgba(168,85,247,0.55)';
  ctx.beginPath();
  ctx.moveTo(mx, cy - 10);
  ctx.lineTo(mx, cy + 10);
  ctx.stroke();
  ctx.fillStyle = 'rgba(192,132,252,0.8)';
  ctx.font = '10.5px ui-monospace,monospace';
  ctx.fillText('d = ' + P.d.toFixed(1) + ' cm', mx - 28, cy + 26);
}

function midField() {
  const half = Math.max(0.05, P.d * 0.5);
  const e1 = 9e7 * P.q1 / (half * half);
  const e2 = -9e7 * P.q2 / (half * half);
  return e1 + e2;
}

let hudAcc = 0;
function updateAndRender(now) {
  const dt = simDt(now);
  const fps = fpsTick(now);

  if (dirty) { buildLines(); dirty = false; }

  ctx.fillStyle = '#09090b';
  ctx.fillRect(0, 0, W, H);
  gridBackground(ctx, W, H);
  drawLines();
  drawAxis();
  placeCharges();
  drawCharge(q1x, cy, P.q1, 'rgba(244,114,182,');
  drawCharge(q2x, cy, P.q2, 'rgba(56,189,248,');

  ctx.fillStyle = 'rgba(34,211,238,0.88)';
  ctx.font = '12px ui-monospace,monospace';
  ctx.fillText('场线由正电荷发出、终止于负电荷；切线方向即电场方向', safeX() + 16, 30);

  hudAcc += 0.016;
  if (hudAcc > 0.12) {
    hudAcc = 0;
    const e = midField();
    const force = 90 * Math.abs(P.q1 * P.q2) / Math.max(0.05, P.d * P.d);
    const attract = (P.q1 * P.q2) < 0;
    setText('h-e', (e / 1e6).toFixed(2) + ' MV/m');
    setText('h-f', force.toFixed(0) + ' N · ' + (attract ? '吸引' : '排斥'));
    setText('h-d', P.d.toFixed(1) + ' cm');
    setText('h-fps', fps.toFixed(0) + ' FPS');
  }
  requestAnimationFrame(updateAndRender);
}
setText('h-fps', '60 FPS');
requestAnimationFrame(updateAndRender);
function reset() { dirty = true; }
window.__simReset = reset;
"""

SCRIPT_INDUCTION = r"""
const scene = makeCanvasPair();
const ctx = scene.ctx;
let W = scene.W, H = scene.H;

const SCALE = 40;
let LSCALE = 100;
const P = { B: 1.0, v: 3.0, L: 2.0 };
const RES = 1.0;

let barX = 0;
let left = 0, right = 0, trackTop = 0, phase = 0;

function fitScale() {
  LSCALE = Math.max(24, Math.min(100, (H - 200) / Math.max(0.1, P.L)));
}
function relayout() {
  const s = scene.resize();
  W = s.W; H = s.H;
  left = safeX() + 12;
  right = W * 0.93;
  fitScale();
  trackTop = (H - 104) * 0.5 - P.L * LSCALE * 0.5;
  barX = left + 40;
  phase = 0;
}
bindRange(0, val => { P.B = val; }, 2);
bindRange(1, val => { P.v = val; }, 1);
bindRange(2, val => {
  P.L = val;
  fitScale();
  trackTop = (H - 104) * 0.5 - P.L * LSCALE * 0.5;
}, 1);
window.addEventListener('resize', relayout, { passive: true });
relayout();

function emf() { return P.B * P.L * P.v; }
function current() { return emf() / RES; }
function ampere() { return P.B * current() * P.L; }

function drawField() {
  const y0 = trackTop, y1 = trackTop + P.L * LSCALE;
  ctx.strokeStyle = 'rgba(34,211,238,0.16)';
  ctx.lineWidth = 1;
  for (let y = y0 + 24; y < y1; y += 46) {
    for (let x = left + 24; x < right - 10; x += 46) {
      ctx.beginPath();
      ctx.arc(x, y, 5, 0, Math.PI * 2);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(x - 3, y - 3);
      ctx.lineTo(x + 3, y + 3);
      ctx.moveTo(x + 3, y - 3);
      ctx.lineTo(x - 3, y + 3);
      ctx.stroke();
    }
  }
  ctx.fillStyle = 'rgba(34,211,238,0.35)';
  ctx.font = '10.5px ui-monospace,monospace';
  ctx.fillText('B ⊗ 垂直纸面向内', left + 6, y0 - 12);
}

function drawRail() {
  const y0 = trackTop, y1 = trackTop + P.L * LSCALE;
  ctx.strokeStyle = 'rgba(148,163,184,0.55)';
  ctx.lineWidth = 3;
  ctx.lineCap = 'round';
  ctx.beginPath();
  ctx.moveTo(left, y0);
  ctx.lineTo(right, y0);
  ctx.moveTo(left, y1);
  ctx.lineTo(right, y1);
  ctx.stroke();

  ctx.strokeStyle = 'rgba(148,163,184,0.35)';
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.moveTo(left, y0);
  ctx.lineTo(left, y1);
  ctx.stroke();

  const rg = ctx.createLinearGradient(barX - 6, y0, barX + 6, y1);
  rg.addColorStop(0, 'rgba(34,211,238,0.95)');
  rg.addColorStop(1, 'rgba(168,85,247,0.95)');
  ctx.strokeStyle = rg;
  ctx.lineWidth = 6;
  ctx.shadowColor = 'rgba(34,211,238,0.9)';
  ctx.shadowBlur = 16;
  ctx.beginPath();
  ctx.moveTo(barX, y0 - 8);
  ctx.lineTo(barX, y1 + 8);
  ctx.stroke();
  ctx.shadowBlur = 0;

  ctx.fillStyle = 'rgba(103,232,249,0.9)';
  ctx.font = '11.5px ui-monospace,monospace';
  ctx.fillText('v →', barX + 10, trackTop - 14);

  ctx.strokeStyle = 'rgba(251,191,36,0.9)';
  ctx.fillStyle = 'rgba(251,191,36,0.9)';
  ctx.lineWidth = 2;
  const fy = (y0 + y1) * 0.5;
  const fx = barX - Math.min(120, ampere() * 10 + 18);
  ctx.beginPath();
  ctx.moveTo(barX - 4, fy);
  ctx.lineTo(fx, fy);
  ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(fx, fy);
  ctx.lineTo(fx + 10, fy - 6);
  ctx.lineTo(fx + 10, fy + 6);
  ctx.closePath();
  ctx.fill();
  ctx.font = '10.5px ui-monospace,monospace';
  ctx.fillText('F_A', fx - 6, fy - 10);
}

function drawCurrent() {
  const y0 = trackTop, y1 = trackTop + P.L * LSCALE;
  const on = current() > 0.02;

  ctx.strokeStyle = 'rgba(244,114,182,0.9)';
  ctx.fillStyle = 'rgba(244,114,182,0.9)';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(barX, y1);
  ctx.lineTo(barX, y0);
  ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(barX, y0);
  ctx.lineTo(barX - 6, y0 + 10);
  ctx.lineTo(barX + 6, y0 + 10);
  ctx.closePath();
  ctx.fill();

  if (!on) return;
  const segs = [
    { x1: barX, y1: y0, x2: left, y2: y0 },
    { x1: left, y1: y0, x2: left, y2: y1 },
    { x1: left, y1: y1, x2: barX, y2: y1 },
  ];
  phase += 0.012 * current();
  const dots = 9;
  for (const sg of segs) {
    for (let i = 0; i < dots; i++) {
      const t = ((i / dots) + phase) % 1;
      const x = sg.x1 + (sg.x2 - sg.x1) * t;
      const y = sg.y1 + (sg.y2 - sg.y1) * t;
      ctx.fillStyle = 'rgba(244,114,182,0.85)';
      ctx.beginPath();
      ctx.arc(x, y, 2.6, 0, Math.PI * 2);
      ctx.fill();
    }
  }
}

function drawInfo() {
  ctx.font = '12px ui-monospace,monospace';
  ctx.fillStyle = 'rgba(34,211,238,0.9)';
  ctx.fillText('ε = BLv ，感应电流方向由右手定则判定，安培力阻碍相对运动', safeX() + 16, 30);
}

let hudAcc = 0;
function updateAndRender(now) {
  const dt = simDt(now);
  const fps = fpsTick(now);

  barX += P.v * SCALE * dt;
  if (barX > right - 24) barX = left + 40;

  ctx.fillStyle = '#09090b';
  ctx.fillRect(0, 0, W, H);
  gridBackground(ctx, W, H);
  drawField();
  drawRail();
  drawCurrent();
  drawInfo();

  hudAcc += 0.016;
  if (hudAcc > 0.12) {
    hudAcc = 0;
    const e = emf(), i = current(), f = ampere();
    setText('h-emf', e.toFixed(2) + ' V');
    setText('h-i', i.toFixed(2) + ' A');
    setText('h-f', f.toFixed(2) + ' N');
    setText('h-p', (e * i).toFixed(2) + ' W');
    setText('h-fps', fps.toFixed(0) + ' FPS');
  }
  requestAnimationFrame(updateAndRender);
}
setText('h-fps', '60 FPS');
requestAnimationFrame(updateAndRender);
function reset() { barX = left + 40; phase = 0; }
window.__simReset = reset;
"""

SCRIPT_REFRACTION = r"""
const scene = makeCanvasPair();
const ctx = scene.ctx;
let W = scene.W, H = scene.H;

const P = { t: 42, n: 1.50, I: 1.0 };
let ox = 0, oy = 0;

function relayout() {
  const s = scene.resize();
  W = s.W; H = s.H;
  ox = Math.max(W * 0.50, safeX() + 210);
  oy = (H - 104) * 0.52;
}
bindRange(0, val => { P.t = val; }, 0);
bindRange(1, val => { P.n = val; }, 2);
bindRange(2, val => { P.I = val; }, 2);
window.addEventListener('resize', relayout, { passive: true });
relayout();

function ray(x1, y1, x2, y2, color, width) {
  ctx.save();
  ctx.strokeStyle = color;
  ctx.lineWidth = width;
  ctx.shadowColor = color;
  ctx.shadowBlur = 14 * P.I;
  ctx.beginPath();
  ctx.moveTo(x1, y1);
  ctx.lineTo(x2, y2);
  ctx.stroke();
  ctx.restore();

  const a = Math.atan2(y2 - y1, x2 - x1);
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.moveTo(x2, y2);
  ctx.lineTo(x2 - 12 * Math.cos(a - 0.36), y2 - 12 * Math.sin(a - 0.36));
  ctx.lineTo(x2 - 12 * Math.cos(a + 0.36), y2 - 12 * Math.sin(a + 0.36));
  ctx.closePath();
  ctx.fill();
}

function drawMedia() {
  ctx.fillStyle = 'rgba(34,211,238,0.035)';
  ctx.fillRect(0, 0, W, oy);
  ctx.fillStyle = 'rgba(168,85,247,0.055)';
  ctx.fillRect(0, oy, W, H - oy);

  ctx.strokeStyle = 'rgba(34,211,238,0.05)';
  ctx.lineWidth = 1;
  for (let y = oy + 22; y < H; y += 26) {
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(W, y);
    ctx.stroke();
  }

  ctx.strokeStyle = 'rgba(34,211,238,0.85)';
  ctx.lineWidth = 2;
  ctx.shadowColor = 'rgba(34,211,238,0.8)';
  ctx.shadowBlur = 12;
  ctx.beginPath();
  ctx.moveTo(0, oy);
  ctx.lineTo(W, oy);
  ctx.stroke();
  ctx.shadowBlur = 0;

  ctx.fillStyle = 'rgba(103,232,249,0.55)';
  ctx.font = '11.5px ui-monospace,monospace';
  ctx.fillText('空气  n₁ = 1.00', 24, oy - 16);
  ctx.fillText('玻璃  n₂ = ' + P.n.toFixed(2), 24, oy + 22);
}

function drawNormal() {
  ctx.save();
  ctx.setLineDash([6, 8]);
  ctx.strokeStyle = 'rgba(226,232,240,0.35)';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(ox, oy - Math.min(240, oy - 90));
  ctx.lineTo(ox, oy + Math.min(240, H - oy - 110));
  ctx.stroke();
  ctx.restore();
  ctx.fillStyle = 'rgba(226,232,240,0.4)';
  ctx.font = '10.5px ui-monospace,monospace';
  ctx.fillText('法线', ox + 6, oy - Math.min(232, oy - 98));
}

function drawAngles(radI, radR, tir) {
  const rr = 62;
  ctx.lineWidth = 1.4;

  ctx.strokeStyle = 'rgba(251,191,36,0.7)';
  ctx.beginPath();
  ctx.arc(ox, oy, rr, -Math.PI / 2 - radI, -Math.PI / 2);
  ctx.stroke();
  ctx.fillStyle = 'rgba(251,191,36,0.85)';
  ctx.fillText('θ₁=' + P.t.toFixed(0) + '°', ox - rr - 46, oy - rr + 6);

  ctx.strokeStyle = 'rgba(168,85,247,0.7)';
  ctx.beginPath();
  ctx.arc(ox, oy, rr, -Math.PI / 2, -Math.PI / 2 + radI);
  ctx.stroke();

  if (!tir) {
    ctx.strokeStyle = 'rgba(103,232,249,0.8)';
    ctx.beginPath();
    ctx.arc(ox, oy, rr - 14, Math.PI / 2 - radR, Math.PI / 2);
    ctx.stroke();
    ctx.fillStyle = 'rgba(103,232,249,0.9)';
    ctx.fillText('θ₂=' + (radR * 180 / Math.PI).toFixed(1) + '°', ox + rr - 4, oy + rr + 6);
  }
}

let hudAcc = 0;
function updateAndRender(now) {
  const dt = simDt(now);
  const fps = fpsTick(now);

  const radI = P.t * Math.PI / 180;
  const sinR = Math.sin(radI) / P.n;
  const tir = sinR >= 1;
  const radR = tir ? 0 : Math.asin(Math.min(1, sinR));
  const crit = Math.asin(Math.min(1, 1 / P.n));

  ctx.fillStyle = '#09090b';
  ctx.fillRect(0, 0, W, H);
  gridBackground(ctx, W, H);
  drawMedia();
  drawNormal();

  const L = Math.min(360, W * 0.34);
  const inX = ox - Math.sin(radI) * L;
  const inY = oy - Math.cos(radI) * L;
  const rfX = ox + Math.sin(radI) * L;
  const rfY = oy - Math.cos(radI) * L;
  const trX = ox + Math.sin(radR) * L;
  const trY = oy + Math.cos(radR) * L;

  ray(inX, inY, ox, oy, 'rgba(251,191,36,' + (0.55 + 0.4 * P.I) + ')', 2.2 * P.I);

  if (tir) {
    ray(ox, oy, rfX, rfY, 'rgba(244,114,182,0.98)', 3.4 * P.I);
  } else {
    ray(ox, oy, rfX, rfY, 'rgba(168,85,247,' + (0.30 + 0.25 * P.I) + ')', 1.8 * P.I);
    ray(ox, oy, trX, trY, 'rgba(103,232,249,0.95)', (2.4 + 1.2 * P.I) * P.I);
  }

  const rg = ctx.createRadialGradient(ox, oy, 0, ox, oy, 34);
  rg.addColorStop(0, 'rgba(255,255,255,0.75)');
  rg.addColorStop(1, 'rgba(255,255,255,0)');
  ctx.fillStyle = rg;
  ctx.beginPath();
  ctx.arc(ox, oy, 34, 0, Math.PI * 2);
  ctx.fill();

  drawAngles(radI, radR, tir);

  ctx.strokeStyle = 'rgba(251,191,36,0.45)';
  ctx.setLineDash([4, 6]);
  ctx.lineWidth = 1.2;
  ctx.beginPath();
  ctx.moveTo(ox, oy);
  ctx.lineTo(ox + Math.sin(crit) * 120, oy + Math.cos(crit) * 120);
  ctx.stroke();
  ctx.setLineDash([]);
  ctx.fillStyle = 'rgba(251,191,36,0.7)';
  ctx.fillText('θ_c=' + (crit * 180 / Math.PI).toFixed(1) + '°', ox + Math.sin(crit) * 124, oy + Math.cos(crit) * 124);

  if (tir) {
    const pulse = 0.6 + 0.4 * Math.sin(now / 160);
    ctx.fillStyle = 'rgba(244,114,182,' + pulse.toFixed(3) + ')';
    ctx.font = 'bold 15px ui-monospace,monospace';
    ctx.fillText('⚠ 全反射 · 无折射光', ox - 92, oy - 226);
    ctx.fillStyle = 'rgba(244,114,182,0.85)';
    ctx.font = '11.5px ui-monospace,monospace';
    ctx.fillText('θ₁ > θ_c → 光全部返回光密介质', ox - 110, oy - 206);
  }

  hudAcc += 0.016;
  if (hudAcc > 0.12) {
    hudAcc = 0;
    setText('h-i', P.t.toFixed(0) + '°');
    setText('h-r', tir ? '—' : (radR * 180 / Math.PI).toFixed(1) + '°');
    setText('h-c', (crit * 180 / Math.PI).toFixed(1) + '°');
    setText('h-mode', tir ? '全反射' : '折射 + 反射');
    setText('h-n', P.n.toFixed(2));
    setText('h-fps', fps.toFixed(0) + ' FPS');
  }
  requestAnimationFrame(updateAndRender);
}
setText('h-fps', '60 FPS');
requestAnimationFrame(updateAndRender);
function reset() { SIM.paused = false; }
window.__simReset = reset;
"""

SCRIPT_BOHR = r"""
const scene = makeCanvasPair();
const ctx = scene.ctx;
let W = scene.W, H = scene.H;

const P = { n: 3, nt: 1, speed: 1.0 };
const A0 = 18;

let cx = 0, cy = 0;
let th = 0;
let jState = 0, jT = 0, idleT = 0;
let photons = [];

function R(n) { return A0 * Math.pow(n, 1.5); }
function E(n) { return -13.6 / (n * n); }
function relayout() {
  const s = scene.resize();
  W = s.W; H = s.H;
  cx = Math.max(W * 0.44, safeX() + 275);
  cy = (H - 104) * 0.47;
}
bindRange(0, val => { P.n = val; jState = 0; jT = 0; idleT = 0; }, 0);
bindRange(1, val => { P.nt = val; jState = 0; jT = 0; idleT = 0; }, 0);
bindRange(2, val => { P.speed = val; }, 2);
window.addEventListener('resize', relayout, { passive: true });
relayout();

function drawOrbits() {
  for (let n = 1; n <= 6; n++) {
    const r = R(n);
    const active = n === P.n;
    const target = n === P.nt && P.nt !== P.n;
    ctx.strokeStyle = active
      ? 'rgba(34,211,238,0.42)'
      : target ? 'rgba(251,191,36,0.30)' : 'rgba(120,120,130,0.30)';
    ctx.lineWidth = active ? 1.5 : 1;
    ctx.beginPath();
    ctx.arc(cx, cy, r, 0, Math.PI * 2);
    ctx.stroke();

    ctx.fillStyle = active ? 'rgba(103,232,249,0.75)' : 'rgba(161,161,170,0.85)';
    ctx.font = '10.5px ui-monospace,monospace';
    ctx.fillText('n=' + n, cx + r + 4, cy + 3);
  }
}

function drawNucleus() {
  const rg = ctx.createRadialGradient(cx, cy, 0, cx, cy, 30);
  rg.addColorStop(0, 'rgba(251,191,36,0.85)');
  rg.addColorStop(0.35, 'rgba(244,114,182,0.35)');
  rg.addColorStop(1, 'rgba(244,114,182,0)');
  ctx.fillStyle = rg;
  ctx.beginPath();
  ctx.arc(cx, cy, 30, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = 'rgba(251,191,36,0.95)';
  ctx.beginPath();
  ctx.arc(cx, cy, 5, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = 'rgba(244,114,182,0.9)';
  ctx.beginPath();
  ctx.arc(cx + 5, cy - 3, 3.4, 0, Math.PI * 2);
  ctx.fill();
}

function electronRadius() {
  const rn = R(P.n);
  if (jState === 0) return rn;
  const rt = R(P.nt);
  if (jState === 1) return rn + (rt - rn) * jT;
  if (jState === 2) return rt;
  return rt + (rn - rt) * jT;
}

function drawElectron() {
  const r = electronRadius();
  const ex = cx + Math.cos(th) * r;
  const ey = cy + Math.sin(th) * r;

  ctx.strokeStyle = 'rgba(34,211,238,0.28)';
  ctx.lineWidth = 1.2;
  ctx.beginPath();
  ctx.moveTo(cx, cy);
  ctx.lineTo(ex, ey);
  ctx.stroke();

  const rg = ctx.createRadialGradient(ex, ey, 0, ex, ey, 22);
  rg.addColorStop(0, 'rgba(103,232,249,0.95)');
  rg.addColorStop(1, 'rgba(103,232,249,0)');
  ctx.fillStyle = rg;
  ctx.beginPath();
  ctx.arc(ex, ey, 22, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = '#0b0b0f';
  ctx.strokeStyle = 'rgba(103,232,249,0.98)';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.arc(ex, ey, 5.4, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();
}

function emitPhoton() {
  const dE = Math.abs(E(P.n) - E(P.nt));
  photons.push({ r: R(P.n), life: 1, dE: dE });
  if (photons.length > 6) photons.shift();
}

function drawPhotons(dt) {
  for (let i = photons.length - 1; i >= 0; i--) {
    const p = photons[i];
    p.r += 190 * dt;
    p.life -= dt * 0.85;
    if (p.life <= 0) { photons.splice(i, 1); continue; }
    const hue = p.dE > 10 ? '168,85,247' : p.dE > 2 ? '34,211,238' : '244,114,182';
    ctx.strokeStyle = 'rgba(' + hue + ',' + (p.life * 0.55).toFixed(3) + ')';
    ctx.lineWidth = 1.6;
    ctx.beginPath();
    ctx.arc(cx, cy, p.r, 0, Math.PI * 2);
    ctx.stroke();
  }
}

function drawLevels() {
  const gx = W - 214, gw = 178;
  if (gx < cx + 330) return;
  const gy1 = cy + 210;
  const scale = 13;

  ctx.fillStyle = 'rgba(9,9,11,0.60)';
  ctx.strokeStyle = 'rgba(34,211,238,0.18)';
  ctx.lineWidth = 1;
  ctx.beginPath();
  if (ctx.roundRect) ctx.roundRect(gx, cy - 186, gw, 416, 12); else ctx.rect(gx, cy - 186, gw, 416);
  ctx.fill();
  ctx.stroke();

  for (let n = 6; n >= 1; n--) {
    const y = gy1 + (E(n) + 13.6) * scale;
    const active = n === P.n || n === P.nt;
    ctx.strokeStyle = active ? 'rgba(34,211,238,0.85)' : 'rgba(150,150,160,0.55)';
    ctx.lineWidth = active ? 1.8 : 1;
    ctx.beginPath();
    ctx.moveTo(gx + 24, y);
    ctx.lineTo(gx + gw - 24, y);
    ctx.stroke();
    ctx.fillStyle = active ? 'rgba(103,232,249,0.9)' : 'rgba(168,168,178,0.88)';
    ctx.font = '10.5px ui-monospace,monospace';
    ctx.fillText('n=' + n, gx + 6, y + 3);
    ctx.fillText(E(n).toFixed(2) + ' eV', gx + gw - 66, y + 3);
  }

  if (P.n !== P.nt) {
    const ya = gy1 + (E(P.n) + 13.6) * scale;
    const yb = gy1 + (E(P.nt) + 13.6) * scale;
    ctx.strokeStyle = 'rgba(251,191,36,0.85)';
    ctx.lineWidth = 1.6;
    ctx.beginPath();
    ctx.moveTo(gx + gw * 0.5, ya);
    ctx.lineTo(gx + gw * 0.5, yb);
    ctx.stroke();
    const dir = yb > ya ? 1 : -1;
    ctx.fillStyle = 'rgba(251,191,36,0.9)';
    ctx.beginPath();
    ctx.moveTo(gx + gw * 0.5, yb);
    ctx.lineTo(gx + gw * 0.5 - 5, yb - 9 * dir);
    ctx.lineTo(gx + gw * 0.5 + 5, yb - 9 * dir);
    ctx.closePath();
    ctx.fill();
  }

  ctx.fillStyle = 'rgba(34,211,238,0.85)';
  ctx.font = '10.5px ui-monospace,monospace';
  ctx.fillText('ENERGY LEVELS  E_n = −13.6/n²', gx + 14, cy - 166);
}

let hudAcc = 0;
function updateAndRender(now) {
  const dt = simDt(now);
  const fps = fpsTick(now);

  const omega = 1.5 / P.n * P.speed;
  th += omega * dt;

  if (P.n !== P.nt) {
    if (jState === 0) {
      idleT += dt;
      if (idleT > 1.6) { jState = 1; jT = 0; idleT = 0; }
    } else if (jState === 1) {
      jT += dt / 0.30;
      if (jT >= 1) { jT = 1; jState = 2; jT = 0; emitPhoton(); }
    } else if (jState === 2) {
      jT += dt / 0.55;
      if (jT >= 1) { jState = 3; jT = 0; }
    } else {
      jT += dt / 0.30;
      if (jT >= 1) { jState = 0; jT = 0; idleT = 0; }
    }
  } else {
    jState = 0; jT = 0; idleT = 0;
  }

  ctx.fillStyle = '#09090b';
  ctx.fillRect(0, 0, W, H);
  gridBackground(ctx, W, H);
  drawOrbits();
  drawNucleus();
  drawPhotons(dt);
  drawElectron();
  drawLevels();

  ctx.fillStyle = 'rgba(34,211,238,0.88)';
  ctx.font = '12px ui-monospace,monospace';
  ctx.fillText('hν = E_n − E_n′ ：电子跃迁时发射或吸收一个光子', safeX() + 16, 30);

  hudAcc += 0.016;
  if (hudAcc > 0.12) {
    hudAcc = 0;
    const dE = Math.abs(E(P.n) - E(P.nt));
    const lam = dE > 0.01 ? 1240 / dE : 0;
    setText('h-n', String(P.n));
    setText('h-en', E(P.n).toFixed(2) + ' eV');
    setText('h-rn', (P.n * P.n * 0.529).toFixed(2) + ' Å');
    setText('h-vn', (2.19 / P.n).toFixed(2) + '×10⁶ m/s');
    setText('h-de', dE > 0.01 ? dE.toFixed(2) + ' eV' : '—');
    setText('h-lam', lam > 0 ? (lam > 1000 ? (lam / 1000).toFixed(2) + ' μm' : lam.toFixed(0) + ' nm') : '—');
    setText('h-fps', fps.toFixed(0) + ' FPS');
  }
  requestAnimationFrame(updateAndRender);
}
setText('h-fps', '60 FPS');
requestAnimationFrame(updateAndRender);
function reset() { th = 0; photons = []; jState = 0; jT = 0; idleT = 0; }
window.__simReset = reset;
"""

SCRIPT_WAVES = r"""
const scene = makeCanvasPair();
const ctx = scene.ctx;
let W = 0, H = 0;

const buf = document.createElement('canvas');
const bctx = buf.getContext('2d');
const LUT = new Float32Array(4096);
for (let i = 0; i < 4096; i++) LUT[i] = Math.sin(i * Math.PI * 2 / 4096);
const COL = new Uint8Array(256 * 3);
for (let i = 0; i < 256; i++) {
  const v = i / 255;
  COL[i * 3] = Math.round(6 + 118 * Math.pow(v, 2.8));
  COL[i * 3 + 1] = Math.round(12 + 236 * Math.pow(v, 0.92));
  COL[i * 3 + 2] = Math.round(28 + 198 * Math.pow(v, 1.15));
}

const P = { lam: 550, sep: 0.42, speed: 1.0 };
let BW = 320, BH = 175, img = null;
let idx1 = null, idx2 = null, wgt1 = null, wgt2 = null;
let wallX = 0, screenX = 0, slitA = 0, slitB = 0;
let phase = 0, dirty = false;

function buildField() {
  if (!idx1) return;
  const sc = BH / 190;
  const lam = Math.max(6, P.lam / 550 * 30 * sc);
  const sep = Math.max(4, Math.min(BH * 0.66, P.sep / 0.42 * 80 * sc));
  wallX = BW * 0.30;
  screenX = BW * 0.965;
  const cy = BH * 0.5;
  slitA = cy - sep * 0.5;
  slitB = cy + sep * 0.5;
  const K = 4096 / lam;
  for (let y = 0; y < BH; y++) {
    for (let x = 0; x < BW; x++) {
      const i = y * BW + x;
      const dx = x - wallX;
      const dy1 = y - slitA, dy2 = y - slitB;
      const r1 = Math.sqrt(dx * dx + dy1 * dy1) + 0.6;
      const r2 = Math.sqrt(dx * dx + dy2 * dy2) + 0.6;
      idx1[i] = r1 * K;
      idx2[i] = r2 * K;
      wgt1[i] = 1 / Math.sqrt(1 + r1 * 0.14);
      wgt2[i] = 1 / Math.sqrt(1 + r2 * 0.14);
    }
  }
}

function relayout() {
  const s = scene.resize();
  W = s.W; H = s.H;
  BW = 320;
  BH = Math.max(140, Math.round(BW * H / W));
  buf.width = BW;
  buf.height = BH;
  img = bctx.createImageData(BW, BH);
  const n = BW * BH;
  idx1 = new Float32Array(n);
  idx2 = new Float32Array(n);
  wgt1 = new Float32Array(n);
  wgt2 = new Float32Array(n);
  buildField();
}

bindRange(0, v => { P.lam = v; dirty = true; }, 0);
bindRange(1, v => { P.sep = v; dirty = true; }, 2);
bindRange(2, v => { P.speed = v; }, 2);
window.addEventListener('resize', relayout, { passive: true });
relayout();

function renderField(wt) {
  const d = img.data;
  const n = BW * BH;
  for (let i = 0, j = 0; i < n; i++, j += 4) {
    const a = LUT[((idx1[i] - wt) | 0) & 4095] * wgt1[i]
            + LUT[((idx2[i] - wt) | 0) & 4095] * wgt2[i];
    let q = (a * a * 94) | 0;
    if (q > 255) q = 255; else if (q < 0) q = 0;
    const c = q * 3;
    d[j] = COL[c]; d[j + 1] = COL[c + 1]; d[j + 2] = COL[c + 2]; d[j + 3] = 255;
  }
  bctx.putImageData(img, 0, 0);
  ctx.imageSmoothingEnabled = true;
  ctx.imageSmoothingQuality = 'low';
  ctx.drawImage(buf, 0, 0, W, H);
}

function drawOverlay(fps) {
  const SX = W / BW, SY = H / BH;
  const bx = wallX * SX;
  const yA = slitA * SY, yB = slitB * SY;
  const gap = 4;

  ctx.fillStyle = 'rgba(13,13,17,.97)';
  ctx.strokeStyle = 'rgba(34,211,238,.30)';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.rect(bx - 4, 0, 8, Math.max(0, yA - gap));
  ctx.rect(bx - 4, yA + gap, 8, Math.max(0, yB - yA - gap * 2));
  ctx.rect(bx - 4, yB + gap, 8, Math.max(0, H - yB - gap));
  ctx.fill();
  ctx.stroke();

  for (const yy of [yA, yB]) {
    const g = ctx.createRadialGradient(bx, yy, 0, bx, yy, 26);
    g.addColorStop(0, 'rgba(214,250,255,.95)');
    g.addColorStop(0.28, 'rgba(34,211,238,.55)');
    g.addColorStop(1, 'rgba(34,211,238,0)');
    ctx.fillStyle = g;
    ctx.beginPath();
    ctx.arc(bx, yy, 26, 0, Math.PI * 2);
    ctx.fill();
  }

  const sx = screenX * SX;
  ctx.save();
  ctx.setLineDash([7, 9]);
  ctx.strokeStyle = 'rgba(168,85,247,.42)';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(sx, 0);
  ctx.lineTo(sx, H);
  ctx.stroke();
  ctx.restore();
  ctx.fillStyle = 'rgba(192,132,252,.8)';
  ctx.font = '10.5px ui-monospace,monospace';
  ctx.fillText('SCREEN', Math.min(sx + 6, W - 60), 26);

  const midY = H * 0.5;
  ctx.save();
  ctx.strokeStyle = 'rgba(34,211,238,.30)';
  ctx.lineWidth = 1;
  for (let k = 1; k <= 3; k++) {
    const x = bx - 34 - k * 30;
    if (x < 8) break;
    ctx.globalAlpha = 0.9 - k * 0.22;
    ctx.beginPath();
    ctx.moveTo(x, midY - 34 + k * 3);
    ctx.lineTo(x, midY + 34 - k * 3);
    ctx.stroke();
  }
  ctx.globalAlpha = 1;
  ctx.fillStyle = 'rgba(34,211,238,.65)';
  ctx.beginPath();
  ctx.moveTo(bx - 14, midY);
  ctx.lineTo(bx - 26, midY - 5);
  ctx.lineTo(bx - 26, midY + 5);
  ctx.closePath();
  ctx.fill();
  ctx.font = '10.5px ui-monospace,monospace';
  ctx.fillText('PLANE WAVE', Math.max(8, bx - 118), midY - 12);
  ctx.restore();

  if (Math.abs(yB - yA) > 26) {
    const lx = bx - 20;
    ctx.strokeStyle = 'rgba(168,85,247,.55)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(lx, yA);
    ctx.lineTo(lx, yB);
    ctx.moveTo(lx - 3, yA + 6);
    ctx.lineTo(lx, yA);
    ctx.lineTo(lx + 3, yA + 6);
    ctx.moveTo(lx - 3, yB - 6);
    ctx.lineTo(lx, yB);
    ctx.lineTo(lx + 3, yB - 6);
    ctx.stroke();
    ctx.fillStyle = 'rgba(192,132,252,.85)';
    ctx.font = '11.5px ui-monospace,monospace';
    ctx.fillText('d', lx - 16, (yA + yB) * 0.5 + 3);
  }
}

let hudAcc = 0;
function updateAndRender(now) {
  const dt = simDt(now);
  const fps = fpsTick(now);
  if (dirty) { buildField(); dirty = false; }
  phase += dt * P.speed * 4.4;
  const wt = phase * (4096 / (Math.PI * 2));
  renderField(wt);
  drawOverlay(fps);
  hudAcc += 0.016;
  if (hudAcc > 0.12) {
    hudAcc = 0;
    updateHud(fps);
  }
  requestAnimationFrame(updateAndRender);
}

function updateHud(fps) {
  setText('h-lam', P.lam.toFixed(0) + ' nm');
  setText('h-sep', P.sep.toFixed(2) + ' mm');
  setText('h-dy', (P.lam / Math.max(0.01, P.sep) * 1e-3).toFixed(2) + ' mm');
  setText('h-phase', (phase % (Math.PI * 2)).toFixed(2) + ' rad');
  setText('h-fps', fps.toFixed(0) + ' FPS');
}
updateHud(60);
requestAnimationFrame(updateAndRender);
function reset() { phase = 0; }
window.__simReset = reset;
"""

SCRIPT_MECHANICS = r"""
const scene = makeCanvasPair();
const ctx = scene.ctx, fxc = scene.fxc;
let W = scene.W, H = scene.H;

const P = { g: 9.8, mu: 1.0, damp: 0.0 };
const S = [2.20, 0.0, 2.40, 0.0];
let cx = 0, cy = 0, sc = 100;
let lastX = 0, lastY = 0, hasTrail = false;

const k1 = [0, 0, 0, 0], k2 = [0, 0, 0, 0], k3 = [0, 0, 0, 0], k4 = [0, 0, 0, 0];
const tmp = [0, 0, 0, 0];

function deriv(s, o) {
  const t1 = s[0], w1 = s[1], t2 = s[2], w2 = s[3];
  const m1 = 1.0, m2 = P.mu, l1 = 1.0, l2 = 1.0, g = P.g;
  const dd = t1 - t2;
  const sd = Math.sin(dd), cd = Math.cos(dd);
  const den = 2 * m1 + m2 - m2 * Math.cos(2 * dd);
  o[0] = w1;
  o[1] = (-g * (2 * m1 + m2) * Math.sin(t1)
        - m2 * g * Math.sin(t1 - 2 * t2)
        - 2 * sd * m2 * (w2 * w2 * l2 + w1 * w1 * l1 * cd)) / (l1 * den);
  o[2] = w2;
  o[3] = (2 * sd * (w1 * w1 * l1 * (m1 + m2)
        + g * (m1 + m2) * Math.cos(t1)
        + w2 * w2 * l2 * m2 * cd)) / (l2 * den);
}

function rk4(h) {
  deriv(S, k1);
  for (let i = 0; i < 4; i++) tmp[i] = S[i] + k1[i] * h * 0.5;
  deriv(tmp, k2);
  for (let i = 0; i < 4; i++) tmp[i] = S[i] + k2[i] * h * 0.5;
  deriv(tmp, k3);
  for (let i = 0; i < 4; i++) tmp[i] = S[i] + k3[i] * h;
  deriv(tmp, k4);
  for (let i = 0; i < 4; i++) S[i] += (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) * h / 6;
  if (P.damp > 0) {
    const f = Math.max(0, 1 - P.damp * h);
    S[1] *= f;
    S[3] *= f;
  }
}

function normAngle(a) {
  const TAU = Math.PI * 2;
  return ((a % TAU) + TAU) % TAU;
}

function energy() {
  const t1 = S[0], w1 = S[1], t2 = S[2], w2 = S[3];
  const m1 = 1.0, m2 = P.mu;
  const T = 0.5 * (m1 + m2) * w1 * w1 + 0.5 * m2 * w2 * w2
          + m2 * w1 * w2 * Math.cos(t1 - t2);
  const V = -(m1 + m2) * P.g * Math.cos(t1) - m2 * P.g * Math.cos(t2);
  return { T: T, V: V, E: T + V };
}

function relayout() {
  const s = scene.resize();
  W = s.W; H = s.H;
  cx = Math.max(W * 0.38, safeX() + 130);
  cy = (H - 106) * 0.42;
  sc = Math.min(W * 0.24, (H - 170) * 0.34) * 0.5;
  hasTrail = false;
  fxc.clearRect(0, 0, W, H);
}

bindRange(0, v => { P.g = v; }, 1);
bindRange(1, v => { P.mu = v; }, 2);
bindRange(2, v => { P.damp = v; }, 3);
window.addEventListener('resize', relayout, { passive: true });
relayout();

const eHist = [];
for (let i = 0; i < 220; i++) eHist.push(0);

function pos(t1, t2, o) {
  o.x1 = cx + sc * Math.sin(t1);
  o.y1 = cy + sc * Math.cos(t1);
  o.x2 = o.x1 + sc * Math.sin(t2);
  o.y2 = o.y1 + sc * Math.cos(t2);
}

const pp = { x1: 0, y1: 0, x2: 0, y2: 0 };

function drawTrail() {
  pos(S[0], S[2], pp);
  fxc.globalCompositeOperation = 'destination-out';
  fxc.fillStyle = 'rgba(0,0,0,0.052)';
  fxc.fillRect(0, 0, W, H);
  fxc.globalCompositeOperation = 'lighter';
  if (hasTrail) {
    fxc.beginPath();
    fxc.moveTo(lastX, lastY);
    fxc.lineTo(pp.x2, pp.y2);
    fxc.strokeStyle = 'rgba(168,85,247,0.42)';
    fxc.lineWidth = 1.7;
    fxc.stroke();
  }
  lastX = pp.x2;
  lastY = pp.y2;
  hasTrail = true;
}

function drawBody() {
  pos(S[0], S[2], pp);
  const x1 = pp.x1, y1 = pp.y1, x2 = pp.x2, y2 = pp.y2;
  const r1 = 8 + 2 * Math.sqrt(1 / P.mu);
  const r2 = 8 + 5 * Math.min(2.4, P.mu);

  ctx.strokeStyle = 'rgba(178,190,205,0.68)';
  ctx.lineWidth = 3;
  ctx.lineCap = 'round';
  ctx.beginPath();
  ctx.moveTo(cx, cy);
  ctx.lineTo(x1, y1);
  ctx.stroke();

  const g = ctx.createLinearGradient(x1, y1, x2, y2);
  g.addColorStop(0, 'rgba(34,211,238,0.85)');
  g.addColorStop(1, 'rgba(168,85,247,0.85)');
  ctx.strokeStyle = g;
  ctx.lineWidth = 4;
  ctx.beginPath();
  ctx.moveTo(x1, y1);
  ctx.lineTo(x2, y2);
  ctx.stroke();

  for (const p of [{ x: cx, y: cy, r: 7, c: 'rgba(226,232,240,' }, { x: x1, y: y1, r: r1, c: 'rgba(34,211,238,' }, { x: x2, y: y2, r: r2, c: 'rgba(168,85,247,' }]) {
    const rg = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.r * 3.2);
    rg.addColorStop(0, p.c + '0.55)');
    rg.addColorStop(0.45, p.c + '0.14)');
    rg.addColorStop(1, p.c + '0)');
    ctx.fillStyle = rg;
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.r * 3.2, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = '#0b0b0f';
    ctx.strokeStyle = p.c + '0.95)';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
  }

  const vx = sc * (S[1] * Math.cos(S[0]) + S[3] * Math.cos(S[2]));
  const vy = -sc * (S[1] * Math.sin(S[0]) + S[3] * Math.sin(S[2]));
  const m = Math.sqrt(vx * vx + vy * vy);
  if (m > 4) {
    const k = Math.min(72, m) / m;
    arrow(x2, y2, x2 + vx * k, y2 + vy * k, 'rgba(34,211,238,0.85)');
  }
  arrow(cx, cy, x1, y1, 'rgba(148,163,184,0.30)', 0.5);
}

function arrow(x1, y1, x2, y2, color, alpha) {
  ctx.save();
  ctx.globalAlpha = alpha == null ? 1 : alpha;
  ctx.strokeStyle = color;
  ctx.fillStyle = color;
  ctx.lineWidth = 1.4;
  ctx.beginPath();
  ctx.moveTo(x1, y1);
  ctx.lineTo(x2, y2);
  ctx.stroke();
  const a = Math.atan2(y2 - y1, x2 - x1);
  ctx.beginPath();
  ctx.moveTo(x2, y2);
  ctx.lineTo(x2 - 7 * Math.cos(a - 0.42), y2 - 7 * Math.sin(a - 0.42));
  ctx.lineTo(x2 - 7 * Math.cos(a + 0.42), y2 - 7 * Math.sin(a + 0.42));
  ctx.closePath();
  ctx.fill();
  ctx.restore();
}

function drawEnergyPlot() {
  const gw = Math.min(460, Math.max(330, W * 0.32)), gh = 186;
  const gx = W - gw - 22, gy = H - gh - 208;
  if (gx < 300) return;
  ctx.fillStyle = 'rgba(20,20,27,0.94)';
  ctx.strokeStyle = 'rgba(34,211,238,0.36)';
  ctx.lineWidth = 1.2;
  ctx.beginPath();
  if (ctx.roundRect) ctx.roundRect(gx, gy, gw, gh, 12); else ctx.rect(gx, gy, gw, gh);
  ctx.fill();
  ctx.stroke();

  let lo = Infinity, hi = -Infinity;
  for (const v of eHist) { if (v < lo) lo = v; if (v > hi) hi = v; }
  const span = Math.max(1, hi - lo);
  const padL = 34, padR = 20, padT = 48, padB = 32;
  const pw = gw - padL - padR, phh = gh - padT - padB;

  ctx.strokeStyle = 'rgba(160,160,172,0.55)';
  ctx.lineWidth = 1.2;
  ctx.beginPath();
  ctx.moveTo(gx + padL, gy + gh - padB);
  ctx.lineTo(gx + padL + pw, gy + gh - padB);
  ctx.moveTo(gx + padL, gy + padT);
  ctx.lineTo(gx + padL, gy + gh - padB);
  ctx.stroke();

  ctx.beginPath();
  for (let i = 0; i < eHist.length; i++) {
    const x = gx + padL + i / (eHist.length - 1) * pw;
    const y = gy + gh - padB - (eHist[i] - lo) / span * phh;
    if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
  }
  ctx.strokeStyle = 'rgba(251,191,36,1)';
  ctx.lineWidth = 2.4;
  ctx.stroke();

  ctx.fillStyle = 'rgba(251,191,36,1)';
  ctx.font = 'bold 14px ui-monospace,monospace';
  ctx.fillText('能量守恒曲线', gx + 16, gy + 24);
  ctx.fillStyle = 'rgba(214,214,224,0.96)';
  ctx.font = '12px ui-monospace,monospace';
  ctx.fillText('E / J', gx + 130, gy + 24);
  ctx.fillText(hi.toFixed(1), gx + 4, gy + padT + 12);
  ctx.fillText(lo.toFixed(1), gx + 4, gy + gh - padB);
}

let hudAcc = 0, subSteps = 8;
function updateAndRender(now) {
  const dt = simDt(now);
  const fps = fpsTick(now);
  const h = Math.min(0.004, dt / subSteps);
  for (let i = 0; i < subSteps; i++) rk4(h);

  ctx.fillStyle = 'rgba(9,9,11,0.16)';
  ctx.fillRect(0, 0, W, H);
  for (let i = 0; i < 14; i++) {
    ctx.strokeStyle = 'rgba(34,211,238,0.035)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.arc(cx, cy, 34 + i * Math.min(W, H) * 0.033, 0, Math.PI * 2);
    ctx.stroke();
  }
  drawTrail();
  drawBody();
  drawEnergyPlot();

  const en = energy();
  eHist.push(Math.max(-400, Math.min(400, en.E)));
  if (eHist.length > 220) eHist.shift();

  hudAcc += 0.016;
  if (hudAcc > 0.1) {
    hudAcc = 0;
    setText('h-t1', normAngle(S[0]).toFixed(3));
    setText('h-t2', normAngle(S[2]).toFixed(3));
    setText('h-w1', S[1].toFixed(3));
    setText('h-w2', S[3].toFixed(3));
    setText('h-e', en.E.toFixed(3));
    setText('h-fps', fps.toFixed(0) + ' FPS');
  }
  requestAnimationFrame(updateAndRender);
}
setText('h-fps', '60 FPS');
requestAnimationFrame(updateAndRender);
function reset() {
  S[0] = 2.20; S[1] = 0; S[2] = 2.40; S[3] = 0;
  hasTrail = false; eHist.fill(0);
  fxc.clearRect(0, 0, W, H);
}
window.__simReset = reset;
"""

SCRIPT_EM = r"""
const scene = makeCanvasPair();
const ctx = scene.ctx, fxc = scene.fxc;
let W = scene.W, H = scene.H;

const SCALE = 40;
const P = { B: 1.0, q: 1.5, E: 0.0, num: 5 };
const parts = [];
const COLORS = ['#67e8f9', '#c084fc', '#fbbf24', '#f472b6', '#4ade80'];

function spawn(p, i) {
  p.x = safeX() + 232 + i * 7;
  p.y = (H - 110) * 0.5 + (i - (P.num - 1) * 0.5) * Math.min(26, (H - 190) / Math.max(1, P.num - 1));
  const sp = 118 + i * 26;
  p.vx = sp;
  p.vy = (i - 2) * 16;
  p.lx = p.x;
  p.ly = p.y;
  p.age = 0;
  p.c = COLORS[i % COLORS.length];
}

function resetAll() {
  parts.length = 0;
  for (let i = 0; i < P.num; i++) {
    const p = {};
    spawn(p, i);
    parts.push(p);
  }
  fxc.clearRect(0, 0, W, H);
}

function relayout() {
  const s = scene.resize();
  W = s.W; H = s.H;
  resetAll();
}

bindRange(0, v => { P.B = v; }, 2);
bindRange(1, v => { P.q = v; }, 1);
bindRange(2, v => { P.E = v; }, 1);
bindRange(3, v => { P.num = Math.max(1, Math.round(v)); resetAll(); }, 0);
window.addEventListener('resize', relayout, { passive: true });
relayout();

function drawFieldGrid() {
  const step = 78;
  const rows = Math.floor((H - 120) / step);
  const cols = Math.floor(W / step);
  for (let r = 0; r <= rows; r++) {
    for (let c = 0; c <= cols; c++) {
      const x = c * step + step * 0.5;
      const y = r * step + 60;
      if (y > H - 120) continue;
      ctx.strokeStyle = 'rgba(34,211,238,0.13)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.arc(x, y, 4.5, 0, Math.PI * 2);
      ctx.stroke();
      ctx.fillStyle = 'rgba(34,211,238,0.22)';
      ctx.beginPath();
      if (P.B >= 0) {
        ctx.arc(x, y, 1.5, 0, Math.PI * 2);
      } else {
        ctx.moveTo(x - 2.6, y - 2.6);
        ctx.lineTo(x + 2.6, y + 2.6);
        ctx.moveTo(x + 2.6, y - 2.6);
        ctx.lineTo(x - 2.6, y + 2.6);
      }
      ctx.fill();
    }
  }
  ctx.fillStyle = 'rgba(34,211,238,0.35)';
  ctx.font = '10.5px ui-monospace,monospace';
  ctx.fillText(P.B >= 0 ? 'B 垂直纸面向外 ⊙' : 'B 垂直纸面向内 ⊗', 20, H - 128);
}

function stepParticles(dt) {
  const omega = P.q * P.B * 1.7;
  const a = omega * dt;
  const ca = Math.cos(a), sa = Math.sin(a);
  const acc = P.q * P.E * 46;
  for (let i = 0; i < parts.length; i++) {
    const p = parts[i];
    p.lx = p.x; p.ly = p.y;
    p.vx += acc * dt * 0.5;
    const nvx = p.vx * ca + p.vy * sa;
    const nvy = -p.vx * sa + p.vy * ca;
    p.vx = nvx; p.vy = nvy;
    p.vx += acc * dt * 0.5;
    p.x += p.vx * dt;
    p.y += p.vy * dt;
    p.age += dt;
    if (p.age > 11 || !isFinite(p.x) || !isFinite(p.y) || p.x > W + 60 || p.x < -80 || p.y < -80 || p.y > H + 80) {
      spawn(p, i);
    }
  }
}

function drawTrails() {
  fxc.globalCompositeOperation = 'destination-out';
  fxc.fillStyle = 'rgba(0,0,0,0.030)';
  fxc.fillRect(0, 0, W, H);
  fxc.globalCompositeOperation = 'lighter';
  fxc.lineWidth = 1.4;
  for (const p of parts) {
    fxc.strokeStyle = p.c;
    fxc.globalAlpha = 0.55;
    fxc.beginPath();
    fxc.moveTo(p.lx, p.ly);
    fxc.lineTo(p.x, p.y);
    fxc.stroke();
  }
  fxc.globalAlpha = 1;
}

function arrow(x1, y1, x2, y2, color, width) {
  ctx.save();
  ctx.strokeStyle = color;
  ctx.fillStyle = color;
  ctx.lineWidth = width || 1.5;
  ctx.beginPath();
  ctx.moveTo(x1, y1);
  ctx.lineTo(x2, y2);
  ctx.stroke();
  const ang = Math.atan2(y2 - y1, x2 - x1);
  ctx.beginPath();
  ctx.moveTo(x2, y2);
  ctx.lineTo(x2 - 8 * Math.cos(ang - 0.4), y2 - 8 * Math.sin(ang - 0.4));
  ctx.lineTo(x2 - 8 * Math.cos(ang + 0.4), y2 - 8 * Math.sin(ang + 0.4));
  ctx.closePath();
  ctx.fill();
  ctx.restore();
}

function drawParticles() {
  for (const p of parts) {
    const sp = Math.sqrt(p.vx * p.vx + p.vy * p.vy);
    const rg = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, 20);
    rg.addColorStop(0, p.c);
    rg.addColorStop(0.22, p.c);
    rg.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.globalAlpha = 0.30;
    ctx.fillStyle = rg;
    ctx.beginPath();
    ctx.arc(p.x, p.y, 20, 0, Math.PI * 2);
    ctx.fill();
    ctx.globalAlpha = 1;
    ctx.fillStyle = '#0b0b0f';
    ctx.strokeStyle = p.c;
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(p.x, p.y, 5.2, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();

    if (sp > 1) {
      const k = 34 / sp;
      arrow(p.x, p.y, p.x + p.vx * k, p.y + p.vy * k, 'rgba(52,211,153,0.75)', 1.4);
      const fx = P.q * P.B * p.vy;
      const fy = -P.q * P.B * p.vx;
      const fm = Math.sqrt(fx * fx + fy * fy);
      if (fm > 1e-3) {
        const kf = 30 / fm;
        arrow(p.x, p.y, p.x + fx * kf, p.y + fy * kf, 'rgba(251,191,36,0.85)', 1.6);
      }
    }
  }
}

let hudAcc = 0;
function updateAndRender(now) {
  const dt = simDt(now);
  const fps = fpsTick(now);

  ctx.fillStyle = '#09090b';
  ctx.fillRect(0, 0, W, H);
  gridBackground(ctx, W, H);
  drawFieldGrid();
  stepParticles(dt);
  drawTrails();
  drawParticles();

  hudAcc += 0.016;
  if (hudAcc > 0.12) {
    hudAcc = 0;
    const p0 = parts[0];
    const sp = Math.sqrt(p0.vx * p0.vx + p0.vy * p0.vy);
    const omega = Math.abs(P.q * P.B * 1.7);
    const r = omega > 1e-4 ? sp / omega : Infinity;
    const T = omega > 1e-4 ? Math.PI * 2 / omega : Infinity;
    setText('h-b', P.B.toFixed(2) + ' T');
    setText('h-q', P.q.toFixed(1) + ' C');
    setText('h-e', P.E.toFixed(2) + ' V/m');
    setText('h-r', (isFinite(r) ? (r / SCALE).toFixed(2) : '∞') + ' m');
    setText('h-t', (isFinite(T) ? T.toFixed(2) : '∞') + ' s');
    setText('h-v', (sp / SCALE).toFixed(1) + ' m/s');
    setText('h-fps', fps.toFixed(0) + ' FPS');
  }
  requestAnimationFrame(updateAndRender);
}
setText('h-fps', '60 FPS');
requestAnimationFrame(updateAndRender);
window.__simReset = resetAll;
"""

SCRIPT_THERMAL = r"""
const scene = makeCanvasPair();
const ctx = scene.ctx, fxc = scene.fxc;
let W = scene.W, H = scene.H;

const SCALE = 40;
const P = { T: 1.0, N: 320, V: 1.0 };
const parts = [];
for (let i = 0; i < 1200; i++) parts.push({ x: 0, y: 0, vx: 0, vy: 0, k: 0, on: false });

let boxTop = 64, bot = H - 108, left = 200, rightEdge = W - 250, pistonX = 0;
const RAD = 3.0;

const SPRITES = [];
const GLOWS = ['rgba(56,189,248,', 'rgba(34,211,238,', 'rgba(103,232,249,', 'rgba(192,132,252,', 'rgba(251,191,36,', 'rgba(244,114,182,'];
for (const c of GLOWS) {
  const cv = document.createElement('canvas');
  cv.width = cv.height = 16;
  const g = cv.getContext('2d');
  const rg = g.createRadialGradient(8, 8, 0, 8, 8, 8);
  rg.addColorStop(0, c + '0.95)');
  rg.addColorStop(0.30, c + '0.40)');
  rg.addColorStop(1, c + '0)');
  g.fillStyle = rg;
  g.beginPath();
  g.arc(8, 8, 8, 0, Math.PI * 2);
  g.fill();
  SPRITES.push(cv);
}

function gauss() {
  let u = 0, v = 0;
  while (u === 0) u = Math.random();
  while (v === 0) v = Math.random();
  return Math.sqrt(-2 * Math.log(u)) * Math.cos(Math.PI * 2 * v);
}

function seed(p) {
  const vr = 96 * Math.sqrt(Math.max(0.1, P.T));
  p.x = left + RAD + Math.random() * Math.max(10, (rightEdge - left) * P.V - RAD * 2);
  p.y = boxTop + RAD + Math.random() * Math.max(10, bot - boxTop - RAD * 2);
  p.vx = gauss() * vr * 0.7;
  p.vy = gauss() * vr * 0.7;
  p.k = Math.min(5, Math.max(0, Math.round(Math.sqrt(p.vx * p.vx + p.vy * p.vy) / (vr * 1.6) * 5)));
  p.on = true;
}

function relayout() {
  const s = scene.resize();
  W = s.W; H = s.H;
  boxTop = 64;
  bot = H - 108;
  left = safeX() + 8;
  rightEdge = Math.max(left + 260, W - Math.min(300, Math.max(210, W * 0.22)));
  for (const p of parts) if (p.on) seed(p);
  fxc.clearRect(0, 0, W, H);
}

function applyCount() {
  const target = Math.round(P.N);
  for (let i = 0; i < parts.length; i++) {
    const p = parts[i];
    if (i < target) {
      if (!p.on) seed(p);
    } else if (p.on) {
      p.on = false;
    }
  }
}

bindRange(0, v => { P.T = v / 300; }, 0);
bindRange(1, v => { P.N = v; applyCount(); }, 0);
bindRange(2, v => { P.V = v; }, 2);
window.addEventListener('resize', relayout, { passive: true });
relayout();
applyCount();

let impulse = 0, pAvg = 0, collisions = 0, histAcc = 0;
let hist = new Float32Array(24);

function step(dt) {
  const vr = 96 * Math.sqrt(Math.max(0.1, P.T));
  const targetV2 = vr * vr * 2;
  let sum = 0, n = 0;
  for (const p of parts) {
    if (!p.on) continue;
    sum += p.vx * p.vx + p.vy * p.vy;
    n++;
  }
  let f = 1;
  if (n > 0 && sum > 1e-6) {
    f = 1 + (Math.sqrt(targetV2 * n / sum) - 1) * Math.min(1, dt * 3.2);
    f = Math.max(0.97, Math.min(1.03, f));
  }
  if (!isFinite(f)) f = 1;

  pistonX = left + (rightEdge - left) * P.V;
  let imp = 0, hits = 0;

  for (const p of parts) {
    if (!p.on) continue;
    p.vx *= f;
    p.vy *= f;
    p.x += p.vx * dt;
    p.y += p.vy * dt;

    if (p.x < left + RAD) {
      p.x = left + RAD;
      imp += 2 * Math.abs(p.vx);
      p.vx = Math.abs(p.vx);
      hits++;
    } else if (p.x > pistonX - RAD) {
      p.x = pistonX - RAD;
      imp += 2 * Math.abs(p.vx);
      p.vx = -Math.abs(p.vx);
      hits++;
    }
    if (p.y < boxTop + RAD) {
      p.y = boxTop + RAD;
      imp += 2 * Math.abs(p.vy);
      p.vy = Math.abs(p.vy);
      hits++;
    } else if (p.y > bot - RAD) {
      p.y = bot - RAD;
      imp += 2 * Math.abs(p.vy);
      p.vy = -Math.abs(p.vy);
      hits++;
    }
  }
  impulse += imp;
  collisions += hits;
  const perimeter = 2 * ((pistonX - left) + (bot - boxTop));
  const pNow = imp / Math.max(1e-4, dt * perimeter);
  pAvg = pAvg * 0.94 + pNow * 0.06;
  if (!isFinite(pAvg)) pAvg = 0;
}

function drawBox() {
  pistonX = left + (rightEdge - left) * P.V;
  ctx.fillStyle = 'rgba(34,211,238,0.030)';
  ctx.fillRect(left, boxTop, pistonX - left, bot - boxTop);
  ctx.strokeStyle = 'rgba(34,211,238,0.42)';
  ctx.lineWidth = 1.6;
  ctx.beginPath();
  ctx.moveTo(left, boxTop);
  ctx.lineTo(left, bot);
  ctx.moveTo(left, boxTop);
  ctx.lineTo(rightEdge, boxTop);
  ctx.moveTo(left, bot);
  ctx.lineTo(rightEdge, bot);
  ctx.stroke();

  ctx.save();
  ctx.strokeStyle = 'rgba(168,85,247,0.75)';
  ctx.lineWidth = 3;
  ctx.shadowColor = 'rgba(168,85,247,0.85)';
  ctx.shadowBlur = 14;
  ctx.beginPath();
  ctx.moveTo(pistonX, boxTop);
  ctx.lineTo(pistonX, bot);
  ctx.stroke();
  ctx.restore();

  ctx.fillStyle = 'rgba(192,132,252,0.65)';
  ctx.font = '10.5px ui-monospace,monospace';
  ctx.fillText('PISTON', Math.max(left + 4, pistonX - 44), boxTop - 8);
}

function drawParticles() {
  for (const p of parts) {
    if (!p.on) continue;
    const v = Math.sqrt(p.vx * p.vx + p.vy * p.vy);
    const k = Math.min(5, Math.max(0, Math.round(v / 160)));
    ctx.drawImage(SPRITES[k], p.x - 8, p.y - 8);
  }
}

function drawHistogram() {
  const gx = rightEdge + 26, gy = boxTop + 34;
  const gw = W - gx - 18, gh = bot - gy - 26;
  if (gw < 54 || gh < 60) return;

  ctx.fillStyle = 'rgba(9,9,11,0.55)';
  ctx.strokeStyle = 'rgba(34,211,238,0.20)';
  ctx.lineWidth = 1;
  ctx.beginPath();
  if (ctx.roundRect) ctx.roundRect(gx, gy, gw, gh, 10); else ctx.rect(gx, gy, gw, gh);
  ctx.fill();
  ctx.stroke();

  let vmax = 1;
  for (let i = 0; i < hist.length; i++) if (hist[i] > vmax) vmax = hist[i];
  const bw = gw / hist.length;
  for (let i = 0; i < hist.length; i++) {
    const h = (hist[i] / vmax) * (gh - 34);
    const x = gx + i * bw;
    ctx.fillStyle = 'rgba(34,211,238,0.85)';
    ctx.fillRect(x + 1, gy + gh - 12 - h, Math.max(1.5, bw - 3), h);
  }

  const vr = 96 * Math.sqrt(Math.max(0.1, P.T));
  const scaleV = 460;
  ctx.beginPath();
  for (let i = 0; i <= 80; i++) {
    const v = i / 80 * scaleV;
    const y = 2 * v / (vr * vr) * Math.exp(-(v * v) / (vr * vr));
    const x = gx + (v / scaleV) * gw;
    const py = gy + gh - 12 - y * (gh - 34) * 1.0;
    if (i === 0) ctx.moveTo(x, py); else ctx.lineTo(x, py);
  }
  ctx.strokeStyle = 'rgba(251,191,36,0.85)';
  ctx.lineWidth = 1.5;
  ctx.stroke();

  ctx.fillStyle = 'rgba(251,191,36,0.75)';
  ctx.font = '10.5px ui-monospace,monospace';
  ctx.fillText('麦克斯韦速率分布 f(v)', gx + 9, gy + 13);
  ctx.fillStyle = 'rgba(212,212,222,0.96)';
  ctx.fillText('v →', gx + gw - 24, gy + gh - 1);
}

let hudAcc = 0;
function updateAndRender(now) {
  const dt = simDt(now);
  const fps = fpsTick(now);

  ctx.fillStyle = '#09090b';
  ctx.fillRect(0, 0, W, H);
  gridBackground(ctx, W, H);
  drawBox();
  step(dt);
  drawParticles();
  drawHistogram();

  histAcc += dt;
  if (histAcc > 0.22) {
    histAcc = 0;
    hist = new Float32Array(24);
    const vr = 96 * Math.sqrt(Math.max(0.1, P.T));
    let sum = 0, n = 0;
    for (const p of parts) {
      if (!p.on) continue;
      const v = Math.sqrt(p.vx * p.vx + p.vy * p.vy);
      sum += v;
      n++;
      const i = Math.min(23, Math.floor(v / (vr * 2.2) * 24));
      hist[i] += 1;
    }
    window.__vAvg = n > 0 ? sum / n : 0;
  }

  hudAcc += 0.016;
  if (hudAcc > 0.14) {
    hudAcc = 0;
    let n = 0;
    for (const p of parts) if (p.on) n++;
    setText('h-t', (P.T * 300).toFixed(0) + ' K');
    setText('h-p', pAvg.toFixed(2) + ' kPa');
    setText('h-n', String(n));
    setText('h-v', ((window.__vAvg || 0) / SCALE).toFixed(2) + ' m/s');
    setText('h-c', String(collisions));
    setText('h-fps', fps.toFixed(0) + ' FPS');
  }
  requestAnimationFrame(updateAndRender);
}
setText('h-fps', '60 FPS');
requestAnimationFrame(updateAndRender);
function reset() {
  impulse = 0; pAvg = 0; collisions = 0; hist = new Float32Array(24);
  for (const p of parts) if (p.on) seed(p);
  fxc.clearRect(0, 0, W, H);
}
window.__simReset = reset;
"""

DANGEROUS_PATTERNS = [
    (r"\bfetch\s*\(", "网络请求 fetch"),
    (r"XMLHttpRequest", "网络请求 XMLHttpRequest"),
    (r"\bWebSocket\b", "WebSocket 连接"),
    (r"document\s*\.\s*cookie", "读取 Cookie"),
    (r"localStorage", "本地存储写入"),
    (r"sessionStorage", "会话存储写入"),
    (r"\beval\s*\(", "动态执行 eval"),
    (r"new\s+Function", "动态构造函数"),
    (r"window\s*\.\s*open", "弹窗 window.open"),
    (r"(?:top|parent)\s*\.\s*location", "父页面跳转"),
]

FALLBACK_CSS = (
    "<style>html,body{margin:0;padding:0;width:100%;height:100vh;"
    "overflow:hidden;background:#09090b;}canvas{display:block;"
    "max-width:100%;}#cv,#fx{width:100%;height:100%;}</style>"
)


def agent_compliance(raw: str, spec: Dict[str, Any]) -> Tuple[str, List[str], bool]:
    notes: List[str] = []
    src = (raw or "").strip()
    if not src:
        notes.append("输入为空，已回退本地物理引擎")
        return TEMPLATES[spec["engine"]](spec), notes, False

    src = re.sub(r"^\s*```[a-zA-Z0-9]*\s*", "", src)
    src = re.sub(r"\s*```\s*$", "", src)
    src = re.sub(r"```[a-zA-Z0-9]*", "", src)
    if "```" in raw:
        notes.append("已剔除 Markdown 代码块围栏")

    m = re.search(r"<!DOCTYPE html.*?</html\s*>", src, re.S | re.I)
    if not m:
        m = re.search(r"<html[\s>].*?</html\s*>", src, re.S | re.I)
    if not m:
        m = re.search(r"(<body[\s>].*?</body\s*>)", src, re.S | re.I)
        if not m:
            notes.append("未检出完整 HTML 文档，已回退本地物理引擎")
            return TEMPLATES[spec["engine"]](spec), notes, False
        src = m.group(1)
        notes.append("检测到 HTML 片段，已补全文档骨架")
    else:
        src = m.group(0)
        notes.append("已提取纯净 HTML 文档体")

    before = len(src)
    src = re.sub(r"<script[^>]*\bsrc\s*=\s*[^>]*>\s*</script\s*>", "", src, flags=re.I)
    src = re.sub(r"<link\b[^>]*>", "", src, flags=re.I)
    src = re.sub(r"<img\b[^>]*\bsrc\s*=\s*(['\"])https?://[^>]*>", "", src, flags=re.I)
    src = re.sub(r"@import\s+url\([^)]*\)\s*;?", "", src, flags=re.I)
    if len(src) != before:
        notes.append("已移除全部外部资源引用，确保零外部依赖")

    for pattern, label in DANGEROUS_PATTERNS:
        if re.search(pattern, src, re.I):
            notes.append("检测到高危行为：{}，已回退本地物理引擎".format(label))
            return TEMPLATES[spec["engine"]](spec), notes, False

    if 'name="viewport"' not in src.lower():
        src = re.sub(
            r"(<head[^>]*>)",
            r'\1<meta name="viewport" content="width=device-width,initial-scale=1">',
            src,
            count=1,
            flags=re.I,
        )
        notes.append("已注入 viewport 元信息，保证 iframe 内无缩放失真")

    if re.search(r"</head\s*>", src, re.I):
        src = re.sub(r"</head\s*>", FALLBACK_CSS + "</head>", src, count=1, flags=re.I)
    else:
        src = FALLBACK_CSS + src
    notes.append("已注入全屏防裁切样式层（100vh / overflow:hidden）")

    if "requestanimationframe" not in src.lower():
        notes.append("未检测到 requestAnimationFrame 实时渲染循环，已回退本地物理引擎")
        return TEMPLATES[spec["engine"]](spec), notes, False
    if 'type="range"' not in src and "type='range'" not in src:
        notes.append("未检测到可调滑块控件，已回退本地物理引擎")
        return TEMPLATES[spec["engine"]](spec), notes, False

    if len(src) < 420:
        notes.append("输出过短，无法构成可信仿真，已回退本地物理引擎")
        return TEMPLATES[spec["engine"]](spec), notes, False

    notes.append("安全检查通过，可以安全内嵌渲染")
    return src, notes, True


def agent_simulation(spec: Dict[str, Any]) -> str:
    return TEMPLATES[spec["engine"]](spec)


def card(title: str, desc: str, state: str) -> str:
    cls = "mp-card" + (" done" if state == "done" else " on" if state == "on" else "")
    return '<div class="{}"><div class="k">{}</div><div class="t">{}</div></div>'.format(
        cls, html_lib.escape(title), html_lib.escape(desc)
    )


def main() -> None:
    st.markdown(PAGE_CSS, unsafe_allow_html=True)
    st.markdown(
        '<div class="mp-hero"><h1>MatrixPhysics<span class="mp-tag">HIGH-SCHOOL PHYSICS SUITE</span></h1>'
        "<p>全套高中物理核心实验 · 纯前端实时物理引擎 · 12 个可交互动态仿真</p></div>",
        unsafe_allow_html=True,
    )

    if "exp_name" not in st.session_state:
        st.session_state.exp_name = DEFAULT_EXPERIMENT
    if "name_input" not in st.session_state:
        st.session_state.name_input = st.session_state.exp_name
    if "lab_module" not in st.session_state:
        st.session_state.lab_module = MODULE_OF.get(st.session_state.exp_name, "经典力学篇")
    if "run_seq" not in st.session_state:
        st.session_state.run_seq = 0
    if "mp_cache" not in st.session_state:
        st.session_state.mp_cache = {}

    def _pick_module() -> None:
        mod = st.session_state.lab_module
        first = MODULES[mod]["experiments"][0]
        st.session_state["lab_radio_" + mod] = first
        st.session_state.exp_name = first
        st.session_state.name_input = first
        st.session_state.run_seq += 1

    def _pick_lab() -> None:
        mod = st.session_state.get("lab_module")
        name = st.session_state.get("lab_radio_" + str(mod))
        if name and name != st.session_state.exp_name:
            st.session_state.exp_name = name
            st.session_state.name_input = name
            st.session_state.run_seq += 1

    def _on_name_change() -> None:
        txt = (st.session_state.name_input or "").strip()
        name = txt or DEFAULT_EXPERIMENT
        st.session_state.exp_name = name
        st.session_state.run_seq += 1
        eng = EXPERIMENT_INDEX.get(name) or classify(name)
        target = ENGINE_TO_EXPERIMENT.get(eng)
        if target:
            mod = MODULE_OF[target]
            st.session_state.lab_module = mod
            st.session_state["lab_radio_" + mod] = target

    def _use_preset(text: str) -> None:
        mod = MODULE_OF.get(text, "经典力学篇")
        st.session_state.lab_module = mod
        st.session_state["lab_radio_" + mod] = text
        st.session_state.exp_name = text
        st.session_state.name_input = text
        st.session_state.run_seq += 1

    with st.sidebar:
        st.markdown("### ◧ 实验模块导航")
        module = st.selectbox(
            "物理模块",
            list(MODULES.keys()),
            key="lab_module",
            on_change=_pick_module,
        )
        st.caption(MODULES[module]["desc"])
        exps = MODULES[module]["experiments"]
        current = st.session_state.exp_name
        idx = exps.index(current) if current in exps else 0
        radio_key = "lab_radio_" + module
        if st.session_state.get(radio_key) not in exps:
            st.session_state[radio_key] = exps[idx]
        st.radio(
            "核心实验",
            exps,
            key=radio_key,
            on_change=_pick_lab,
        )

        st.markdown("---")
        preview = agent_physics(st.session_state.exp_name)
        st.markdown(
            '<div class="mp-meta"><b>当前实验</b><br>{}<br><br><b>三项控制参数</b><br>{}</div>'.format(
                html_lib.escape(preview["title"]),
                "<br>".join(
                    "· {}：{} ~ {} {}".format(
                        html_lib.escape(p["label"]), p["min"], p["max"], html_lib.escape(p["unit"])
                    )
                    for p in preview["params"]
                ),
            ),
            unsafe_allow_html=True,
        )

        st.markdown("---")
        st.markdown(
            '<div class="mp-meta">'
            "<b>纯前端引擎</b><br>"
            "零 API 依赖 · 零外部 CDN<br>"
            "Canvas + requestAnimationFrame<br>"
            "渲染目标 <code>60 FPS</code>，视口 <code>100vh</code> 无裁切"
            "</div>",
            unsafe_allow_html=True,
        )
        if st.button("♻ 重载当前实验", use_container_width=True):
            st.session_state.mp_cache = {}
            st.session_state.run_seq += 1

    st.text_input(
        "物理实验名称（支持自定义关键词自动匹配）",
        key="name_input",
        on_change=_on_name_change,
        placeholder="例如：平抛运动 / 光的折射与全反射 / 导体棒切割磁感线",
    )

    cols = st.columns(4)
    for i, (short, full) in enumerate(PRESETS):
        cols[i].button(
            short,
            key="preset_btn_{}".format(i),
            use_container_width=True,
            on_click=_use_preset,
            args=(full,),
        )

    name = (st.session_state.exp_name or "").strip() or DEFAULT_EXPERIMENT
    spec = agent_physics(name)

    c_run, c_hint = st.columns([1, 3])
    if c_run.button("▶ 启动实时仿真", type="primary", use_container_width=True):
        st.session_state.run_seq += 1
    c_hint.markdown(
        '<div class="mp-meta" style="padding-top:10px">'
        "物理域：<b>{}</b> · 当前 3 项参数均可在仿真画面底部实时拖动，无需重新生成页面。"
        "</div>".format(html_lib.escape(spec["domain"])),
        unsafe_allow_html=True,
    )

    if name in st.session_state.mp_cache:
        html_doc, report = st.session_state.mp_cache[name]
    else:
        with st.spinner("物理引擎装配中：解析物理模型 → 生成实时渲染管线 → 静态合规自检 …"):
            html_doc, report, _ok = agent_compliance(agent_simulation(spec), spec)
            st.session_state.mp_cache[name] = (html_doc, report)

    st.markdown(
        '<div class="mp-pipe">'
        + card("AGENT 01", "物理原理与参数拆解", "done")
        + card("AGENT 02", "高性能仿真引擎架构", "done")
        + card("AGENT 03", "代码安全与渲染合规", "done")
        + "</div>",
        unsafe_allow_html=True,
    )

    st.markdown('<div class="mp-updateAndRender">', unsafe_allow_html=True)
    components.html(html_doc, height=720, scrolling=False)
    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2 = st.columns([1.45, 1])
    with c1:
        st.markdown('<div class="mp-meta"><b>核心公式</b></div>', unsafe_allow_html=True)
        st.latex(spec["latex"])
    with c2:
        st.markdown(
            '<div class="mp-meta"><b>初始状态量</b><br>{}</div>'.format(
                "<br>".join("· " + html_lib.escape(x) for x in spec["initial"])
            ),
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="mp-meta" style="margin-top:10px"><b>引擎</b><br>{}<br>'
            '<b>依赖</b><br>无外部 API / 无 CDN</div>'.format(html_lib.escape(spec["domain"])),
            unsafe_allow_html=True,
        )

    exam = spec["exam"]
    with st.expander("🎯 考点卡片 · 易错点 · 典型例题", expanded=False):
        ex1, ex2 = st.columns(2)
        with ex1:
            st.markdown("**考纲要点**")
            for item in exam["points"]:
                st.markdown("- " + item)
        with ex2:
            st.markdown("**易错点**")
            for item in exam["pitfalls"]:
                st.markdown("- " + item)
        st.markdown("**典型例题**")
        st.info(exam["example"])
        with st.expander("查看答案与解析"):
            st.success(exam["answer"])

    with st.expander("🔍 参数拆解 · 物理定律 · 合规自检报告", expanded=False):
        st.markdown("**三项核心可调控制参数**")
        st.table(
            [
                {
                    "参数": p["label"],
                    "取值范围": "{} ~ {}".format(p["min"], p["max"]),
                    "默认值": p["value"],
                    "单位": p["unit"],
                    "物理含义": p["hint"],
                }
                for p in spec["params"]
            ]
        )
        st.markdown("**适用物理定律**：" + "，".join(spec["laws"]))
        st.markdown("**合规自检**")
        for note in report:
            st.markdown("- " + note)


main()
