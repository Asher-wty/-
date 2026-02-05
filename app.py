import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from production_model import MixingOptimizer
from construction_model import LogisticsOptimizer

# 设置字体以支持中文展示（Streamlit默认环境可能需配置，这里做基本兼容）
matplotlib.rcParams['font.sans-serif'] = ['SimHei'] 
matplotlib.rcParams['axes.unicode_minus'] = False

# --- 页面配置 ---
st.set_page_config(
    page_title="新疆石油低温能耗优化系统",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- 自定义 CSS 样式 (精美大方、工业风) ---
st.markdown("""
    <style>
    /* 全局背景 */
    .stApp {
        background-color: #F0F2F6;
    }
    /* 自定义卡片样式 */
    .metric-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-top: 5px solid #004595;
        margin-bottom: 20px;
    }
    .status-ok { color: #28a745; font-weight: bold; }
    .status-warn { color: #dc3545; font-weight: bold; }
    h1, h2, h3 { color: #004595; }
    </style>
    """, unsafe_allow_html=True)

# --- 侧边栏：控制面板 ---
st.sidebar.image("https://img.icons8.com/fluency/96/oil-industry.png", width=80)
st.sidebar.title("🎛️ 现场中控台")

with st.sidebar:
    st.markdown("### 1. 生产端实时工况")
    temp = st.slider("环境温度 (°C)", -40, 0, -25, help="新疆冬季实测环境气温")
    viscosity = st.number_input("原油实时黏度 (mPa.s)", 500, 8000, 2500)
    
    st.markdown("---")
    st.markdown("### 2. 施工端现场记录")
    dist = st.number_input("运输半径 (km)", 0.0, 30.0, 8.0)
    starts = st.slider("今日设备启停次数", 0, 10, 3)
    is_pre = st.radio("设备预热状态", ["已预热", "未预热"], index=1)
    gap = st.number_input("工序衔接间隔 (min)", 0, 120, 45)

# --- 核心逻辑计算 ---
prod_opt = MixingOptimizer(temp)
log_opt = LogisticsOptimizer()

# 生产端方案
res_p = prod_opt.optimize_process(viscosity)
# 施工端方案
res_t = log_opt.calculate_transport_impact(dist)
res_s_val, res_s_msg = log_opt.calculate_startup_impact(starts, (is_pre == "已预热"))
res_g = log_opt.calculate_process_gap(gap)

# --- 主界面布局 ---
st.title("🛢️ 新疆石油低温能耗全链条优化系统")
st.markdown("##### 融合 CN207478358U 专利技术 · 极寒环境生产效能监测看板")

tabs = st.tabs(["📊 生产优化方案", "🚧 施工诊断报告", "💡 综合经济效益"])

# --- Tab 1: 生产优化 ---
with tabs[0]:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.subheader("🎯 分温区自适应指令")
        m1, m2, m3 = st.columns(3)
        m1.metric("推荐转速", f"{res_p['智能调整后转速(r/min)']} r/min")
        m2.metric("温区状态", res_p['工况温区'])
        m3.metric("传动系统", "齿轮传动 (1:3)")
        
        st.write("**技术建议：** 采用变频调速模块，实现黏度-转速联动补偿控制。")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 配比图表
        st.write("### 🧪 物料配比明细")
        ratios = res_p['建议物料配比']
        df_r = pd.DataFrame(list(ratios.items()), columns=['成分', '占比'])
        st.bar_chart(df_r.set_index('成分'))

    with col2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.subheader("⚙️ 硬件适配")
        st.write("✅ **传动**：专利齿轮传动")
        st.write("✅ **润滑**：SHC 630 低温脂")
        st.write("✅ **保温**：铝箔+10cm岩棉")
        st.markdown("</div>", unsafe_allow_html=True)

# --- Tab 2: 施工诊断 ---
with tabs[1]:
    st.subheader("🔍 现场作业能耗诊断")
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown(f"""<div class='metric-card'>
            <h4>🚛 运输分析</h4>
            <p>状态：<span class='{"status-ok" if res_t["状态"]=="达标" else "status-warn"}'>{res_t["状态"]}</span></p>
            <p>{res_t["诊断"]}</p>
            <hr>
            <small><b>建议工况：</b>半径 ≤ 5.0km</small>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(f"""<div class='metric-card'>
            <h4>🔄 启停监测</h4>
            <p>状态：<span class='{"status-ok" if res_s_val==0 else "status-warn"}'>{res_s_msg}</span></p>
            <p>量化损耗：{int(res_s_val*100)}%</p>
            <hr>
            <small><b>建议工况：</b>次数 ≤ 2，预热 > 30min</small>
        </div>""", unsafe_allow_html=True)

    with c3:
        st.markdown(f"""<div class='metric-card'>
            <h4>⏱️ 工序衔接</h4>
            <p>状态：<span class='{"status-ok" if res_g["状态"]=="高效" else "status-warn"}'>{res_g["状态"]}</span></p>
            <p>{res_g["诊断"]}</p>
            <hr>
            <small><b>建议工况：</b>间隔 ≤ 20min</small>
        </div>""", unsafe_allow_html=True)

# --- Tab 3: 经济效益 ---
with tabs[2]:
    st.subheader("💰 综合节能减排预测")
    base_cost = 2000
    savings = prod_opt.calculate_savings(base_cost)
    
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        st.info(f"预计每日节省运行成本：¥ {savings}")
        st.success(f"能耗修正系数优化：由 1.48 降至 {res_p.get('能耗修正系数', 1.25)}")
    
    with col_e2:
        st.warning("🍀 碳减排贡献：预计每月减少二氧化碳排放 0.85 吨")

st.divider()
st.caption("© 2026 中国石油大学（北京）- 极寒之星技术团队 | 三创赛演示 Demo")