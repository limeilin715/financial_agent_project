import streamlit as st
from dotenv import load_dotenv
import os
import concurrent.futures
import re

# 加载环境变量
load_dotenv()

st.set_page_config(page_title="金融投资研究智能体", page_icon="📈", layout="wide")

# 自定义CSS样式
st.markdown("""
<style>
    .view-card-buy {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
    }
    .view-card-watch {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(245, 87, 108, 0.4);
    }
    .view-card-neutral {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(79, 172, 254, 0.4);
    }
    .view-card-avoid {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: #333;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(250, 112, 154, 0.4);
    }
    .view-title {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .view-subtitle {
        font-size: 1.2rem;
        opacity: 0.95;
    }
    .data-card {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4facfe;
    }
    .section-header-1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 10px;
        font-size: 1.4rem;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .section-header-2 {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 10px;
        font-size: 1.4rem;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .section-header-3 {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 10px;
        font-size: 1.4rem;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .subsection-title {
        font-size: 1.1rem;
        font-weight: bold;
        color: #333;
        margin: 15px 0 10px 0;
    }
    .news-content {
        font-size: 1rem;
        line-height: 1.6;
    }
    .news-link {
        color: #667eea;
        text-decoration: none;
        font-size: 0.9rem;
    }
    .news-link:hover {
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 中国A股投资研究智能体")
st.markdown("---")

# 侧边栏 - 仅显示非敏感配置
with st.sidebar:
    st.header("⚙️ 配置")
    
    model_name = st.selectbox(
        "选择模型",
        ["deepseek-v4-flash", "deepseek-v4-pro"],
        index=0,
        help="Flash: 更快响应，Pro: 更强大能力"
    )
    
    # 检查配置是否完整
    api_key = os.getenv("OPENAI_API_KEY", "")
    api_base = os.getenv("OPENAI_API_BASE", "")
    
    if api_key and api_base:
        st.success("✅ 配置已就绪", icon="🔒")
    else:
        st.error("❌ 配置不完整，请检查环境变量设置", icon="⚠️")
        st.info("💡 本地：检查 .env 文件 | 云端：检查应用 Secrets 配置")
    
    st.markdown("---")
    st.markdown("### 📖 使用说明")
    st.markdown("""
    1. 输入 A 股股票代码（如 600519）
    2. 点击开始分析
    3. 等待智能体生成研究报告
    """)

# 主界面
col1, col2 = st.columns([3, 1])
with col1:
    stock_code = st.text_input(
        "请输入股票代码",
        placeholder="例如：600519 贵州茅台, 000001 平安银行, 300750 宁德时代"
    )
with col2:
    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
    start_button = st.button("开始分析", type="primary", use_container_width=True)

def is_valid_stock_code(code: str) -> bool:
    """验证是否为有效的A股代码格式"""
    code = code.strip()
    if not code.isdigit():
        return False
    if len(code) != 6:
        return False
    # 检查是否为A股代码段
    if code.startswith(('600', '601', '603', '605', '000', '001', '300', '301')):
        return True
    return False

def parse_report_sections(report_text: str):
    """解析报告各个章节"""
    sections = {}
    
    # 尝试按标题分割
    lines = report_text.split('\n')
    
    current_section = ""
    current_content = []
    
    for line in lines:
        if line.startswith('###'):
            if current_section:
                sections[current_section] = '\n'.join(current_content)
            current_section = line.strip()
            current_content = []
        else:
            if current_section:
                current_content.append(line)
    
    if current_section:
        sections[current_section] = '\n'.join(current_content)
    
    return sections

def parse_and_display_news(news_data: str):
    """解析并美化显示新闻，提取链接"""
    lines = news_data.split('\n')
    
    st.markdown('<div class="news-content">', unsafe_allow_html=True)
    
    current_title = ""
    current_body = ""
    current_link = ""
    
    for line in lines:
        if line.startswith('📰 标题：'):
            if current_title:
                st.markdown(f"**{current_title}**")
                st.markdown(current_body)
                if current_link:
                    st.markdown(f'<a href="{current_link}" target="_blank" class="news-link">🔗 查看原文</a>', unsafe_allow_html=True)
                st.markdown("---")
            current_title = line.replace('📰 标题：', '').strip()
            current_body = ""
            current_link = ""
        elif line.startswith('📝 内容：'):
            current_body = line.replace('📝 内容：', '').strip()
        elif line.startswith('🔗 链接：'):
            current_link = line.replace('🔗 链接：', '').strip()
        elif line == '---':
            continue
        elif line.strip() and not line.startswith('🔍 【'):
            if current_body:
                current_body += " " + line.strip()
            else:
                st.markdown(line)
    
    if current_title:
        st.markdown(f"**{current_title}**")
        st.markdown(current_body)
        if current_link:
            st.markdown(f'<a href="{current_link}" target="_blank" class="news-link">🔗 查看原文</a>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def parse_and_display_report(report_text: str, stock_code: str, financial_data: str, news_data: str):
    """解析并美化显示研究报告"""
    
    # 显示股票标题
    st.markdown(f"## 📄 {stock_code} 投资研究报告")
    st.markdown("---")
    
    # 从报告中提取投资观点
    view_text = ""
    view_type = "neutral"
    
    # 简单解析，找到投资观点部分
    if "**强烈推荐买入**" in report_text:
        view_text = "强烈推荐买入"
        view_type = "buy"
    elif "**谨慎看多**" in report_text:
        view_text = "谨慎看多"
        view_type = "watch"
    elif "**建议规避**" in report_text:
        view_text = "建议规避"
        view_type = "avoid"
    elif "**中性观望**" in report_text:
        view_text = "中性观望"
        view_type = "neutral"
    
    # 解析报告章节
    sections = parse_report_sections(report_text)
    
    # --- 第一大板块 ---
    st.markdown('<div class="section-header-1">🎯 第一大板块：投资观点及依据</div>', unsafe_allow_html=True)
    
    # 显示突出的投资观点卡片
    if view_text:
        card_class = {
            "buy": "view-card-buy",
            "watch": "view-card-watch",
            "neutral": "view-card-neutral",
            "avoid": "view-card-avoid"
        }[view_type]
        
        st.markdown(f"""
            <div class="{card_class}">
                <div class="view-subtitle">💡 投资观点</div>
                <div class="view-title">{view_text}</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("")
    
    # 左右两栏布局
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        # 左侧：1. 财务与行情数据
        st.markdown('<div class="subsection-title">1️⃣ 财务与行情数据</div>', unsafe_allow_html=True)
        st.markdown('<div class="data-card">', unsafe_allow_html=True)
        st.text(financial_data)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_right:
        # 右侧：2. 核心观察，3. 支撑依据
        for title, content in sections.items():
            if "核心观察" in title:
                st.markdown('<div class="subsection-title">2️⃣ 核心观察</div>', unsafe_allow_html=True)
                st.markdown(content)
        
        for title, content in sections.items():
            if "支撑证据" in title:
                st.markdown('<div class="subsection-title">3️⃣ 支撑依据</div>', unsafe_allow_html=True)
                st.markdown(content)
    
    st.markdown("---")
    
    # --- 第二大板块 ---
    st.markdown('<div class="section-header-2">⚠️ 第二大板块：主要风险</div>', unsafe_allow_html=True)
    
    for title, content in sections.items():
        if "主要风险" in title:
            st.markdown(content)
    
    st.markdown("---")
    
    # --- 第三大板块 ---
    st.markdown('<div class="section-header-3">🔮 第三大板块：未来展望</div>', unsafe_allow_html=True)
    
    for title, content in sections.items():
        if "未来展望" in title:
            st.markdown(content)
    
    st.markdown("---")
    
    # 底部：新闻舆情（可折叠）
    with st.expander("📰 查看新闻与舆情（点击展开）", expanded=False):
        parse_and_display_news(news_data)

if start_button and stock_code:
    # 先验证股票代码格式
    stock_code_clean = stock_code.strip()
    if not is_valid_stock_code(stock_code_clean):
        st.warning("🔔 请输入有效的A股代码（6位数字，如600519）")
        st.info("支持的格式：\n- 沪市：600xxx, 601xxx, 603xxx, 605xxx\n- 深市：000xxx, 001xxx\n- 创业板：300xxx, 301xxx")
    else:
        # 检查配置
        api_key = os.getenv("OPENAI_API_KEY", "")
        api_base = os.getenv("OPENAI_API_BASE", "")
        
        if not api_key or not api_base:
            st.error("❌ 配置不完整，请检查环境变量设置")
            st.info("💡 本地：检查 .env 文件 | 云端：检查应用 Secrets 配置")
        else:
            # 设置环境变量
            os.environ["OPENAI_API_KEY"] = api_key
            os.environ["OPENAI_API_BASE"] = api_base
            os.environ["MODEL_NAME"] = model_name
            
            st.markdown(f"### 📌 正在分析：{stock_code_clean}")
            st.markdown("---")
            
            # 导入模块
            from agents import run_ashare_research
            from tools import get_ashare_financials_and_price, search_ashare_market_news
            
            try:
                financial_data = None
                news_data = None
                
                # 优化：并行获取股票数据和新闻数据，大幅提升速度！
                with st.status("🚀 正在收集数据...", expanded=True) as data_status:
                    st.write("正在并行获取股票数据和市场新闻...")
                    
                    # 定义并行执行的函数
                    def fetch_financial_data():
                        return get_ashare_financials_and_price.invoke({"stock_code": stock_code_clean})
                    
                    def fetch_news_data():
                        return search_ashare_market_news.invoke({"stock_code": stock_code_clean})
                    
                    # 使用线程池并行执行
                    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                        future_financial = executor.submit(fetch_financial_data)
                        future_news = executor.submit(fetch_news_data)
                        
                        # 获取结果
                        financial_data = future_financial.result()
                        news_data = future_news.result()
                    
                    st.write("✅ 股票数据获取完成")
                    st.write("✅ 市场新闻获取完成")
                    data_status.update(label="✅ 数据收集完成", state="complete", expanded=False)
                
                # 阶段2：大模型深度推理
                with st.status("🤖 Research Agent 正在深度推理...", expanded=True) as research_status:
                    st.write("正在调用大模型分析数据...")
                    report_text = run_ashare_research(stock_code_clean, financial_data, news_data)
                    st.write("✅ 投资研究报告生成完成")
                    research_status.update(label="✅ 投资报告生成完成", state="complete", expanded=False)
                
                st.markdown("---")
                
                # 美化显示报告
                parse_and_display_report(report_text, stock_code_clean, financial_data, news_data)
                
                # 添加下载按钮
                st.markdown("---")
                st.download_button(
                    "📥 下载完整报告 (Markdown)",
                    data=report_text,
                    file_name=f"{stock_code_clean}_investment_report.md",
                    mime="text/markdown"
                )
                
            except Exception as e:
                st.error("❌ 分析过程中出错，请稍后再试")
                st.info("💡 可能的原因：股票代码不存在、网络问题或API配置错误")

else:
    # 欢迎界面
    st.info("👋 欢迎使用中国 A 股投资研究智能体！请输入股票代码开始分析。")
    
    st.markdown("---")
    st.subheader("📌 支持的股票市场")
    col_market1, col_market2, col_market3 = st.columns(3)
    with col_market1:
        st.markdown("**🏢 沪市主板**")
        st.markdown("600xxx, 601xxx, 603xxx, 605xxx")
    with col_market2:
        st.markdown("**🏭 深市主板**")
        st.markdown("000xxx, 001xxx")
    with col_market3:
        st.markdown("**🚀 创业板**")
        st.markdown("300xxx, 301xxx")
