import streamlit as st
from dotenv import load_dotenv
import os
import concurrent.futures

# 加载环境变量
load_dotenv()

st.set_page_config(page_title="金融投资研究智能体", page_icon="📈", layout="wide")

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
        st.error("❌ 配置不完整，请检查 .env 文件", icon="⚠️")
    
    st.markdown("---")
    st.markdown("### 📖 使用说明")
    st.markdown("""
    1. 输入 A 股股票代码（如 600519）
    2. 点击开始分析
    3. 等待智能体生成研究报告
    """)
    
    st.markdown("---")
    st.markdown("### 🔐 安全提示")
    st.info("API Key 从本地 .env 文件读取，不会在界面上显示")

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

if start_button and stock_code:
    # 检查配置
    api_key = os.getenv("OPENAI_API_KEY", "")
    api_base = os.getenv("OPENAI_API_BASE", "")
    
    if not api_key or not api_base:
        st.error("❌ 配置不完整，请检查 .env 文件")
    else:
        # 设置环境变量
        os.environ["OPENAI_API_KEY"] = api_key
        os.environ["OPENAI_API_BASE"] = api_base
        os.environ["MODEL_NAME"] = model_name
        
        st.markdown(f"### 📌 正在分析：{stock_code}")
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
                    return get_ashare_financials_and_price.invoke({"stock_code": stock_code})
                
                def fetch_news_data():
                    return search_ashare_market_news.invoke({"stock_code": stock_code})
                
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
                report_text = run_ashare_research(stock_code, financial_data, news_data)
                st.write("✅ 投资研究报告生成完成")
                research_status.update(label="✅ 投资报告生成完成", state="complete", expanded=False)
            
            # 显示原始数据（可选折叠）
            with st.expander("📊 查看原始数据"):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.subheader("财务与行情数据")
                    st.text(financial_data)
                with col_b:
                    st.subheader("新闻与舆情")
                    st.text(news_data)
            
            st.markdown("---")
            st.markdown(f"## 📄 {stock_code} 投资研究报告")
            
            # 直接显示 Markdown 报告
            st.markdown(report_text)
            
            # 添加下载按钮
            st.markdown("---")
            st.download_button(
                "📥 下载完整报告 (Markdown)",
                data=report_text,
                file_name=f"{stock_code}_investment_report.md",
                mime="text/markdown"
            )
            
        except Exception as e:
            st.error(f"❌ 分析过程中出错：{str(e)}")
            st.info("💡 请检查：1. .env 配置是否正确 2. 股票代码是否有效 3. 网络连接是否正常")

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
