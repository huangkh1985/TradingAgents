# DeepSeek 双模型支持

## ✅ 已完成的功能

成功为 DeepSeek 添加了双模型支持，现在用户可以在以下两个模型之间选择：

### 1. DeepSeek Chat（deepseek-chat）
- 💬 **类型**：通用对话模型
- 🎯 **适用场景**：股票分析、日常对话、快速响应
- ⚡ **特点**：响应速度快，成本较低

### 2. DeepSeek Reasoner（deepseek-reasoner）
- 🧠 **类型**：推理模型
- 🎯 **适用场景**：深度思考、复杂分析、推理任务
- 💡 **特点**：推理能力强，适合需要深度分析的场景

---

## 🔧 修改的文件

### 1. `web/components/sidebar.py`
**修改内容**：
- 在侧边栏添加了 DeepSeek 双模型选择器
- 用户可以在 `deepseek-chat` 和 `deepseek-reasoner` 之间选择

**代码变更**：
```python
deepseek_options = ["deepseek-chat", "deepseek-reasoner"]

llm_model = st.selectbox(
    "选择DeepSeek模型",
    options=deepseek_options,
    index=current_index,
    format_func=lambda x: {
        "deepseek-chat": "DeepSeek Chat - 💬 通用对话模型，适合股票分析",
        "deepseek-reasoner": "DeepSeek Reasoner - 🧠 推理模型，深度思考分析"
    }[x],
    help="选择用于分析的DeepSeek模型",
    key="deepseek_model_select"
)
```

### 2. `web/utils/analysis_runner.py`
**修改内容**：
- 移除了硬编码的 `deepseek-chat`
- 所有研究深度（1-5级）现在都使用用户选择的模型
- 支持动态切换 `deepseek-chat` 和 `deepseek-reasoner`

**代码变更**：
```python
# 修改前（所有深度都硬编码）
elif llm_provider == "deepseek":
    config["quick_think_llm"] = "deepseek-chat"  # ❌ 硬编码
    config["deep_think_llm"] = "deepseek-chat"

# 修改后（使用用户选择的模型）
elif llm_provider == "deepseek":
    config["quick_think_llm"] = llm_model  # ✅ 动态选择
    config["deep_think_llm"] = llm_model
```

---

## 📋 如何使用

### 配置 DeepSeek API 密钥

在 Streamlit Cloud Secrets 中配置：

```toml
[llm]
DEEPSEEK_API_KEY = "sk-your-deepseek-api-key"
```

### 在应用中选择模型

1. **侧边栏** → **LLM提供商** → 选择 **🚀 DeepSeek V3**
2. **选择DeepSeek模型**：
   - **DeepSeek Chat** - 💬 通用对话模型，适合股票分析
   - **DeepSeek Reasoner** - 🧠 推理模型，深度思考分析
3. 开始分析！

---

## 🎯 使用建议

### 何时使用 DeepSeek Chat
- ✅ 日常股票分析
- ✅ 快速获取分析结果
- ✅ 需要控制成本时
- ✅ 研究深度 1-2 级

### 何时使用 DeepSeek Reasoner
- ✅ 复杂的股票分析
- ✅ 需要深度推理
- ✅ 多因素综合分析
- ✅ 研究深度 3-5 级

---

## 🔍 技术细节

### 模型支持范围

| 研究深度 | Quick Think LLM | Deep Think LLM | 说明 |
|---------|-----------------|----------------|------|
| 1级 快速 | 用户选择的模型 | 用户选择的模型 | 快速分析 |
| 2级 基础 | 用户选择的模型 | 用户选择的模型 | 基础分析 |
| 3级 标准 | 用户选择的模型 | 用户选择的模型 | 标准分析 |
| 4级 深度 | 用户选择的模型 | 用户选择的模型 | 深度分析 |
| 5级 全面 | 用户选择的模型 | 用户选择的模型 | 全面分析 |

### DeepSeek 适配器

DeepSeek 使用自定义适配器（`tradingagents/llm_adapters/deepseek_adapter.py`）：
- ✅ 支持 Token 使用统计
- ✅ 支持 `deepseek-chat` 和 `deepseek-reasoner`
- ✅ 自动从环境变量读取 API 密钥
- ✅ 支持 Streamlit Cloud Secrets

---

## ✨ 优势

### 灵活性
- ✅ 用户可以根据需求选择合适的模型
- ✅ 无需修改代码即可切换模型

### 成本控制
- ✅ 简单任务使用 DeepSeek Chat（成本低）
- ✅ 复杂任务使用 DeepSeek Reasoner（效果好）

### 性能优化
- ✅ Chat 模型响应快，适合快速分析
- ✅ Reasoner 模型推理强，适合深度分析

---

## 📝 示例配置

### 最小配置（仅 DeepSeek）

```toml
[llm]
DEEPSEEK_API_KEY = "sk-your-deepseek-api-key"
```

### 完整配置（包含多个提供商）

```toml
[llm]
# DeepSeek（推荐用于复杂分析）
DEEPSEEK_API_KEY = "sk-your-deepseek-api-key"

# OpenAI（备用）
OPENAI_API_KEY = "sk-your-openai-api-key"

# 其他可选...
```

---

## 🚀 提交记录

```
ea7e6a3 feat: add DeepSeek dual model support (deepseek-chat and deepseek-reasoner)
```

**修改内容**：
- 在侧边栏添加 DeepSeek 双模型选择
- 修复所有硬编码的 `deepseek-chat`
- 支持用户动态选择模型
- 所有研究深度都支持双模型

---

## 🎉 总结

DeepSeek 现在支持两个模型：
- **DeepSeek Chat** - 快速、经济、适合日常分析
- **DeepSeek Reasoner** - 强大、深度、适合复杂推理

用户可以根据具体需求灵活选择，在性能和成本之间取得最佳平衡！

---

**更新日期**: 2025-10-06  
**状态**: ✅ 已完成并部署

