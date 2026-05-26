import akshare as ak
from ddgs import DDGS
from langchain_core.tools import tool
from typing import Optional
from datetime import datetime, timedelta
import baostock as bs


# A股股票代码到名称的映射表（常用股票）
STOCK_NAME_MAPPING = {
    "600519": "贵州茅台",
    "000001": "平安银行",
    "000002": "万科A",
    "601318": "中国平安",
    "600036": "招商银行",
    "000858": "五粮液",
    "002594": "比亚迪",
    "300750": "宁德时代",
    "601899": "紫金矿业",
    "600900": "长江电力",
    "600276": "恒瑞医药",
    "000333": "美的集团",
    "601888": "中国中免",
    "000651": "格力电器",
    "601328": "交通银行",
}


# 模拟的股票基本数据（用于网络不可用时的备选方案）
MOCK_STOCK_DATA = {
    "600519": {
        "股票代码": "600519",
        "股票简称": "贵州茅台",
        "行业": "食品饮料",
        "最新价": "1788.00",
        "涨跌幅": "-1.25%",
        "市盈率-动态": "28.50",
        "市净率": "9.80",
        "总市值": "22420.00亿",
        "流通市值": "22420.00亿",
    },
    "000001": {
        "股票代码": "000001",
        "股票简称": "平安银行",
        "行业": "银行",
        "最新价": "11.85",
        "涨跌幅": "+0.50%",
        "市盈率-动态": "6.80",
        "市净率": "0.55",
        "总市值": "2280.00亿",
        "流通市值": "2280.00亿",
    },
}


def get_stock_name(stock_code: str) -> Optional[str]:
    """
    获取股票名称，先查映射表
    
    Args:
        stock_code: 股票代码
    
    Returns:
        股票名称或None
    """
    return STOCK_NAME_MAPPING.get(stock_code)


def get_mock_stock_data(stock_code: str) -> str:
    """
    获取模拟的股票数据（用于网络不可用时）
    
    Args:
        stock_code: 股票代码
    
    Returns:
        格式化的股票数据字符串
    """
    result = []
    result.append("📊 【股票基本信息】")
    
    stock_name = get_stock_name(stock_code)
    if stock_name:
        result.append(f"- 股票简称：{stock_name}")
    
    if stock_code in MOCK_STOCK_DATA:
        data = MOCK_STOCK_DATA[stock_code]
        for key, value in data.items():
            result.append(f"- {key}：{value}")
    else:
        result.append("- 股票代码：" + stock_code)
        result.append("- 行业：未知")
        result.append("- 最新价：--")
        result.append("- 涨跌幅：--")
    
    result.append("\n")
    result.append("📈 【实时行情信息】")
    
    if stock_code in MOCK_STOCK_DATA:
        data = MOCK_STOCK_DATA[stock_code]
        result.append(f"- 股票名称：{data.get('股票简称', stock_name or stock_code)}")
        result.append(f"- 最新价：{data.get('最新价', '--')}")
        result.append(f"- 涨跌幅：{data.get('涨跌幅', '--')}")
        result.append(f"- 市盈率(PE)：{data.get('市盈率-动态', '--')}")
        result.append(f"- 市净率(PB)：{data.get('市净率', '--')}")
        result.append(f"- 总市值：{data.get('总市值', '--')}")
    else:
        result.append(f"- 股票名称：{stock_name or stock_code}")
        result.append("- 最新价：--")
        result.append("- 涨跌幅：--")
        result.append("- 市盈率(PE)：--")
        result.append("- 市净率(PB)：--")
    
    result.append("\n⚠️ 注：由于数据源连接问题，当前展示的是示例数据")
    
    return "\n".join(result)


def get_baostock_data(stock_code: str) -> Optional[str]:
    """
    使用 Baostock 获取股票数据
    
    Args:
        stock_code: 股票代码
    
    Returns:
        格式化的股票数据字符串，失败返回None
    """
    try:
        # 登录系统
        lg = bs.login()
        if lg.error_code != '0':
            return None
        
        # 构建股票代码（Baostock需要前缀）
        if stock_code.startswith('6'):
            bs_code = f"sh.{stock_code}"
        else:
            bs_code = f"sz.{stock_code}"
        
        # 计算日期范围：最近20天（减少数据量）
        end_date = datetime.now()
        start_date = end_date - timedelta(days=20)
        
        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")
        
        # 获取K线数据（只获取必要字段）
        rs = bs.query_history_k_data_plus(
            bs_code,
            "date,open,high,low,close,volume,amount,turn,pctChg",
            start_date=start_date_str,
            end_date=end_date_str,
            frequency="d",
            adjustflag="3"
        )
        
        if rs.error_code != '0':
            bs.logout()
            return None
        
        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        
        if not data_list:
            bs.logout()
            return None
        
        # 获取最新数据
        latest_data = data_list[-1]
        
        result = []
        result.append("📊 【股票基本信息】")
        result.append(f"- 股票代码：{stock_code}")
        
        stock_name = get_stock_name(stock_code)
        if stock_name:
            result.append(f"- 股票简称：{stock_name}")
            if stock_code in MOCK_STOCK_DATA:
                result.append(f"- 行业：{MOCK_STOCK_DATA[stock_code].get('行业', '--')}")
        
        result.append("\n")
        result.append("📈 【行情信息】")
        result.append(f"- 数据日期：{latest_data[0]}")
        result.append(f"- 最新价：{latest_data[4]}")
        result.append(f"- 涨跌幅：{latest_data[8]}%")
        result.append(f"- 开盘价：{latest_data[1]}")
        result.append(f"- 最高价：{latest_data[2]}")
        result.append(f"- 最低价：{latest_data[3]}")
        result.append(f"- 成交量：{latest_data[5]}")
        result.append(f"- 成交额：{latest_data[6]}")
        result.append(f"- 换手率：{latest_data[7]}%")
        
        # 登出系统
        bs.logout()
        
        return "\n".join(result)
        
    except Exception:
        try:
            bs.logout()
        except Exception:
            pass
        return None


@tool
def get_ashare_financials_and_price(stock_code: str) -> str:
    """
    获取中国A股股票的财务数据和实时行情信息。
    
    Args:
        stock_code: 股票代码，支持纯数字格式（如"600519")
    
    Returns:
        结构化的中文文本，包含股票基本信息、实时行情和财务指标
    """
    try:
        if not stock_code:
            return "错误：股票代码不能为空"
        
        # 方案1：优先使用 Baostock（完全免费，稳定！）
        try:
            baostock_result = get_baostock_data(stock_code)
            if baostock_result:
                return baostock_result
        except Exception:
            pass
        
        # 方案2：使用 akshare 历史行情接口
        try:
            result = []
            real_data_success = False
            
            end_date = datetime.now()
            start_date = end_date - timedelta(days=20)
            
            start_date_str = start_date.strftime("%Y%m%d")
            end_date_str = end_date.strftime("%Y%m%d")
            
            hist_data = ak.stock_zh_a_hist(
                symbol=stock_code,
                period="daily",
                start_date=start_date_str,
                end_date=end_date_str,
                adjust="qfq"
            )
            
            if not hist_data.empty:
                latest_data = hist_data.iloc[-1]
                prev_data = hist_data.iloc[-2] if len(hist_data) > 1 else latest_data
                price_change = ((latest_data['收盘'] - prev_data['收盘']) / prev_data['收盘']) * 100
                
                result.append("📊 【股票基本信息】")
                result.append(f"- 股票代码：{stock_code}")
                
                stock_name = get_stock_name(stock_code)
                if stock_name:
                    result.append(f"- 股票简称：{stock_name}")
                    if stock_code in MOCK_STOCK_DATA:
                        result.append(f"- 行业：{MOCK_STOCK_DATA[stock_code].get('行业', '--')}")
                
                result.append("\n")
                result.append("📈 【行情信息】")
                result.append(f"- 数据日期：{latest_data['日期']}")
                result.append(f"- 最新价：{latest_data['收盘']}")
                result.append(f"- 涨跌幅：{price_change:.2f}%")
                result.append(f"- 开盘价：{latest_data['开盘']}")
                result.append(f"- 最高价：{latest_data['最高']}")
                result.append(f"- 最低价：{latest_data['最低']}")
                result.append(f"- 成交量：{latest_data['成交量']}")
                result.append(f"- 成交额：{latest_data['成交额']}")
                result.append(f"- 振幅：{latest_data['振幅']}%")
                result.append(f"- 换手率：{latest_data['换手率']}%")
                
                real_data_success = True
            
            if real_data_success and result:
                return "\n".join(result)
        except Exception:
            pass
        
        # 如果获取真实数据失败，返回模拟数据
        return get_mock_stock_data(stock_code)
        
    except Exception as e:
        return f"❌ 获取股票数据时发生错误：{str(e)}"


@tool
def search_ashare_market_news(stock_code: str) -> str:
    """
    搜索中国A股相关的市场新闻和舆情信息。
    
    Args:
        stock_code: 股票代码，支持纯数字格式（如"600519")
    
    Returns:
        近期前3条核心财经新闻文本（含链接）
    """
    try:
        if not stock_code:
            return "错误：股票代码不能为空"
        
        # 获取股票名称
        stock_name = get_stock_name(stock_code)
        
        # 优化：减少关键词数量，提高速度
        search_keywords = []
        
        if stock_name:
            search_keywords = [f"{stock_name} 最新消息", f"{stock_name} 股票"]
        else:
            search_keywords = [f"{stock_code} 股票"]
        
        news_results = []
        
        with DDGS() as ddgs:
            for keyword in search_keywords:
                try:
                    # 减少返回结果数量
                    results = ddgs.text(
                        query=keyword,
                        region="cn-zh",
                        safesearch="moderate",
                        max_results=2
                    )
                    
                    for r in results:
                        title = r.get('title', '')
                        body = r.get('body', '')
                        url = r.get('href', '')
                        
                        news_item = f"📰 标题：{title}\n📝 内容：{body}\n🔗 链接：{url}\n---"
                        news_results.append(news_item)
                        
                        # 提前退出，减少搜索时间
                        if len(news_results) >= 3:
                            break
                        
                except Exception:
                    continue
                
                if len(news_results) >= 3:
                    break
        
        # 去重并取前3条
        unique_news = []
        seen = set()
        
        for news in news_results:
            if news not in seen:
                seen.add(news)
                unique_news.append(news)
                if len(unique_news) >= 3:
                    break
        
        # 构建返回结果
        display_name = f"{stock_name} ({stock_code})" if stock_name else stock_code
        
        if unique_news:
            return f"🔍 【{display_name} 相关新闻资讯】\n\n" + "\n\n".join(unique_news)
        else:
            return f"⚠️ 未找到 {display_name} 的相关新闻"
            
    except Exception as e:
        return f"❌ 搜索新闻时发生错误：{str(e)}"


if __name__ == "__main__":
    # 简单测试
    print("测试 get_ashare_financials_and_price()...")
    try:
        print(get_ashare_financials_and_price.invoke("600519"))
    except Exception as e:
        print(f"测试失败：{e}")
    
    print("\n" + "="*50 + "\n")
    
    print("测试 search_ashare_market_news()...")
    try:
        print(search_ashare_market_news.invoke("600519"))
    except Exception as e:
        print(f"测试失败：{e}")
