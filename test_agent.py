import os
import traceback
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 导入投研函数
from agents import run_ashare_research


def test_ashare_research():
    """测试 A 股投研分析功能"""
    
    print("=" * 80)
    print("📊 中国 A 股投资研究智能体 - 测试")
    print("=" * 80)
    print()
    
    # 测试股票代码：贵州茅台
    stock_code = "600519"
    
    print(f"🎯 测试标的：{stock_code} (贵州茅台)")
    print()
    
    try:
        # 调用投研分析函数
        print("🔄 正在运行投研分析...")
        print("-" * 80)
        
        report_text = run_ashare_research(stock_code)
        
        print("✅ 投研分析完成！")
        print()
        print("=" * 80)
        print("📄 投资研究报告")
        print("=" * 80)
        print()
        
        # 直接打印 Markdown 报告
        print(report_text)
        
        print()
        print("=" * 80)
        print("✅ 测试成功完成！")
        print("=" * 80)
        
    except Exception as e:
        print()
        print("❌ 测试失败！")
        print("=" * 80)
        print()
        print("错误信息：")
        print("-" * 80)
        print(f"类型：{type(e).__name__}")
        print(f"描述：{str(e)}")
        print()
        print("完整错误堆栈：")
        print("-" * 80)
        traceback.print_exc()
        print()
        print("=" * 80)


if __name__ == "__main__":
    test_ashare_research()
