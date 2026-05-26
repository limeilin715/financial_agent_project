# 📊 中国 A 股投资研究智能体

一个基于 LangChain + Streamlit + AkShare 的智能 A 股投资研究系统。

## ✨ 功能特点

- 🤖 **AI 驱动分析**：支持 DeepSeek、GPT-4o 等多种大模型进行专业投资分析
- 📈 **实时数据**：通过 AkShare 获取真实 A 股行情和财务数据
- 📰 **新闻舆情**：使用 DuckDuckGo 搜索相关市场新闻
- 📋 **结构化报告**：生成标准化的投资研究报告
- 🎨 **友好界面**：基于 Streamlit 的交互式 Web 应用

## 📦 项目结构

```
financial_agent_project/
├── app.py              # Streamlit 前端应用
├── agents.py           # 智能体核心逻辑
├── tools.py            # LangChain 工具函数
├── requirements.txt    # Python 依赖
├── .env               # 环境变量配置（含真实密钥，不提交到 Git）
├── .env.example       # 环境变量模板（不含密钥，可安全提交）
├── .gitignore         # Git 忽略配置
└── README.md          # 项目文档
```

## 🔒 安全说明

- **`.env`** - 包含真实 API 密钥，已加入 `.gitignore`，**永远不会被提交到 Git**
- **`.env.example`** - 只包含配置模板，不含密钥，可以安全提交

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env`，并填入你的真实 API Key：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
OPENAI_API_KEY=your-real-api-key-here
OPENAI_API_BASE=https://api.deepseek.com/v1
MODEL_NAME=deepseek-chat
```

**支持的模型**：
- `deepseek-chat`（默认，DeepSeek）
- `gpt-4o`（OpenAI）
- `gpt-4-turbo`（OpenAI）
- `gpt-3.5-turbo`（OpenAI）

### 3. 运行应用

```bash
streamlit run app.py
```

然后在浏览器中打开 `http://localhost:8501`

## 📝 使用说明

1. 在侧边栏输入 OpenAI API Key
2. 选择模型（默认 gpt-4o）
3. 在主界面输入 A 股股票代码（如 600519）
4. 点击"开始分析"按钮
5. 等待智能体完成数据收集和分析
6. 查看生成的投资研究报告

## 📋 报告结构

生成的投资研究报告包含以下字段：

| 字段 | 说明 |
|------|------|
| `research_question` | 研究问题 |
| `key_observations` | 核心观察点（至少 3 条）|
| `supporting_evidence` | 支持性证据 |
| `investment_view` | 投资观点（四选一）|
| `major_risks` | 主要风险考量 |
| `uncertainty_boundaries` | 不确定性边界 |

### 投资观点选项

- 🟢 **强烈推荐买入**
- 🟡 **谨慎看多**
- ⚪ **中性观望**
- 🔴 **建议规避**

## 🛠️ 技术栈

- **Streamlit**：Web 应用框架
- **LangChain**：AI 应用开发框架
- **AkShare**：A 股数据接口
- **DuckDuckGo Search**：新闻搜索
- **DeepSeek / OpenAI GPT**：大语言模型
- **Pydantic**：数据验证

## 📌 支持的股票市场

- 🏢 沪市主板（600xxx, 601xxx, 603xxx, 605xxx）
- 🏭 深市主板（000xxx, 001xxx）
- 🚀 创业板（300xxx, 301xxx）

## ⚠️ 免责声明

本工具仅供学习和研究使用，不构成任何投资建议。股市有风险，投资需谨慎。

## 📄 License

MIT License
