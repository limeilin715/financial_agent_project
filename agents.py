import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from tools import get_ashare_financials_and_price, search_ashare_market_news


# 加载环境变量
load_dotenv()


# 定义系统提示词
SYSTEM_PROMPT = """你是一位**资深 A 股新财富白金分析师 + 严谨的公募基金风控总监**。

你的职责是基于提供的工具获取的真实数据，撰写专业、客观、严谨的 A 股投资研究报告。

【工作原则】
1. **数据驱动，严禁造假**：所有分析必须严格基于提供的真实数据，包括最新股价、PE、PB、市值、新闻等。绝对不允许凭空捏造 A 股价格和财报指标。
2. **Markdown 格式输出**：你必须直接输出精确的 Markdown 格式投研报告，报告中必须包含以下标题，顺序非常重要：
   - ### 1. 投资观点（这一项必须在最前面！）
   - ### 2. 核心观察
   - ### 3. 支撑证据
   - ### 4. 主要风险
   - ### 5. 不确定性边界
3. **风险敏感**：作为风控总监，你必须敏锐捕捉企业在 A 股环境下的潜在暴雷点。
4. **客观中立**：避免过度乐观或悲观，基于数据给出理性判断。
5. **投资观点选择**：投资观点必须从以下四个选项中选择一个，且单独一行显示，加粗：
   - **强烈推荐买入**
   - **谨慎看多**
   - **中性观望**
   - **建议规避**

现在，请基于提供的真实数据，撰写指定 A 股股票的投资研究报告。**记住：投资观点必须放在最前面！**"""


def run_ashare_research(stock_code: str, financial_data: str = None, news_data: str = None) -> str:
    """
    运行 A 股投研分析的主入口函数
    
    Args:
        stock_code: 股票代码（如 "600519")
        financial_data: 可选，已获取的财务数据
        news_data: 可选，已获取的新闻数据
    
    Returns:
        str: Markdown 格式的投资研究报告
    """
    
    try:
        # 如果没有提供数据，则获取数据
        if financial_data is None:
            print(f"正在获取 {stock_code} 的财务与行情数据...")
            financial_data = get_ashare_financials_and_price.invoke({"stock_code": stock_code})
        
        if news_data is None:
            print(f"正在获取 {stock_code} 的新闻与舆情...")
            news_data = search_ashare_market_news.invoke({"stock_code": stock_code})
        
        # 获取环境变量并打印调试信息
        model_name = os.getenv("MODEL_NAME", "deepseek-v4-flash")
        api_key = os.getenv("OPENAI_API_KEY")
        api_base = os.getenv("OPENAI_API_BASE", "https://api.deepseek.com")
        
        print(f"调试信息 - 模型: {model_name}")
        print(f"调试信息 - API Base: {api_base}")
        print(f"调试信息 - API Key 已配置: {api_key is not None and len(api_key) > 0}")
        
        # 初始化大模型
        llm = ChatOpenAI(
            model=model_name,
            temperature=0.7,
            api_key=api_key,
            base_url=api_base
        )
        
        # 构建分析提示词
        analysis_prompt = f"""{SYSTEM_PROMPT}

【分析标的】
股票代码：{stock_code}

【真实财务与行情数据】
{financial_data}

【最新新闻与舆情】
{news_data}

请基于以上真实数据，撰写一份专业、严谨的投资研究报告。确保所有分析都有数据支撑，严禁捏造任何信息。

注意：你必须直接输出 Markdown 格式的报告内容，不要包含任何额外的说明文字！"""
        
        # 调用大模型生成报告
        print("正在调用大模型生成投资研究报告...")
        response = llm.invoke(analysis_prompt)
        
        # 返回纯文本内容
        report_text = response.content if hasattr(response, 'content') else str(response)
        
        return report_text
        
    except Exception as e:
        import traceback
        error_msg = f"投研分析失败：{str(e)}\n\n详细堆栈：\n{traceback.format_exc()}"
        print(error_msg)
        raise Exception(error_msg)


if __name__ == "__main__":
    # 简单测试
    print("Testing A-share research agent module...")
    print("="*50)
    
    try:
        print("Testing imports...")
        print("✅ run_ashare_research function loaded")
        print("\nModule is ready to use!")
        print("\nPlease configure your .env file with OPENAI_API_KEY before running.")
        
    except Exception as e:
        print(f"Test failed: {e}")
