# 📊 中国 A 股投资研究智能体

一个基于 LangChain + Streamlit + Baostock 的智能 A 股投资研究系统。

## ✨ 功能特点

- 🤖 **AI 驱动分析**：使用 DeepSeek 大模型进行专业投资分析
- 📈 **实时数据**：通过 Baostock 获取真实 A 股行情和财务数据
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
OPENAI_API_KEY=your-real-deepseek-api-key-here
OPENAI_API_BASE=https://api.deepseek.com
MODEL_NAME=deepseek-v4-flash
```

**支持的 DeepSeek 模型**：
- `deepseek-v4-flash`（默认，速度快）
- `deepseek-v4-pro`（能力强，适合复杂分析）

### 3. 运行应用

```bash
streamlit run app.py
```

然后在浏览器中打开 `http://localhost:8501`

## 📝 使用说明

1. 在侧边栏选择模型（默认 deepseek-v4-flash）
2. 在主界面输入 A 股股票代码（如 600519）
3. 点击"开始分析"按钮
4. 等待智能体完成数据收集和分析
5. 查看生成的投资研究报告

## 📋 报告结构

生成的投资研究报告包含以下部分：

| 部分 | 说明 |
|------|------|
| **投资观点** | 投资建议（四选一） |
| **核心观察** | 关键分析点 |
| **支撑证据** | 数据与分析依据 |
| **主要风险** | 风险警示 |
| **不确定性边界** | 边界条件说明 |

### 投资观点选项

- 🟣 **强烈推荐买入**
- 🟠 **谨慎看多**
- 🔵 **中性观望**
- 🟡 **建议规避**

## 🎨 UI 布局

- **顶部**：突出的投资观点卡片（渐变色）
- **左侧**：财务与行情数据
- **右侧**：核心观察与支撑证据
- **中间**：主要风险（红色）、不确定性边界（蓝色）
- **底部**：新闻舆情（可折叠展开）

## 🛠️ 技术栈

- **Streamlit**：Web 应用框架
- **LangChain**：AI 应用开发框架
- **Baostock**：A 股数据接口（稳定免费）
- **AkShare**：A 股备用数据接口
- **DuckDuckGo Search**：新闻搜索
- **DeepSeek**：大语言模型

## 📌 支持的股票市场

- 🏢 沪市主板（600xxx, 601xxx, 603xxx, 605xxx）
- 🏭 深市主板（000xxx, 001xxx）
- 🚀 创业板（300xxx, 301xxx）

## ⚠️ 免责声明

本工具仅供学习和研究使用，不构成任何投资建议。股市有风险，投资需谨慎。

## 📄 License

MIT License
