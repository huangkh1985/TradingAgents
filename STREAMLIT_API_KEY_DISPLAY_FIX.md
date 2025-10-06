# Streamlit Cloud API密钥显示修复

## 问题描述

在Streamlit Cloud上运行时，即使用户选择了OpenAI作为LLM提供商，系统仍然在"必需配置"中显示"❌ 阿里百炼: 未配置"的错误提示，这会误导用户。

## 问题根源

`web/components/sidebar.py` 文件中的API密钥状态检查逻辑将"阿里百炼"和"FinnHub"硬编码为"必需配置"，没有根据用户选择的LLM提供商动态调整。

原有逻辑：
```python
# 必需的API密钥
st.markdown("*必需配置:*")

# 阿里百炼 - 硬编码为必需
dashscope_key = get_api_key("DASHSCOPE_API_KEY", "llm")
status, level = validate_api_key(dashscope_key, "dashscope")
if level == "success":
    st.success(f"✅ 阿里百炼: {status}")
# ...
else:
    st.error("❌ 阿里百炼: 未配置")
```

## 修复方案

### 1. 动态必需配置显示

修改后的逻辑根据 `llm_provider` 变量动态显示必需配置：

```python
# 根据选择的LLM提供商动态显示必需配置
st.markdown("*必需配置:*")

# 显示当前选择的LLM提供商的API密钥状态
if llm_provider == "dashscope":
    # 阿里百炼
    dashscope_key = get_api_key("DASHSCOPE_API_KEY", "llm")
    # ...检查并显示状态
elif llm_provider == "openai" or llm_provider == "custom_openai":
    # OpenAI
    openai_key = get_api_key("OPENAI_API_KEY", "llm")
    # ...检查并显示状态
elif llm_provider == "deepseek":
    # DeepSeek
    # ...
# ... 其他提供商
```

### 2. 支持的LLM提供商

修复后支持以下LLM提供商的动态检查：

- ✅ **阿里百炼 (dashscope)** - 当选择时显示为必需配置
- ✅ **OpenAI (openai/custom_openai)** - 当选择时显示为必需配置  
- ✅ **DeepSeek (deepseek)** - 当选择时显示为必需配置
- ✅ **Google AI (google)** - 当选择时显示为必需配置
- ✅ **Anthropic (anthropic)** - 当选择时显示为必需配置
- ✅ **OpenRouter (openrouter)** - 当选择时显示为必需配置
- ✅ **硅基流动 (siliconflow)** - 当选择时显示为必需配置
- ✅ **千帆 (qianfan)** - 当选择时显示为必需配置（需要AK和SK）

### 3. 优化可选配置显示

修改后的"可选配置"部分只显示未被选择为主LLM的提供商：

```python
# 可选的API密钥 - 只显示未被选择为主LLM的提供商
st.markdown("*可选配置:*")

# 阿里百炼 (仅当不是当前选择的LLM时显示)
if llm_provider != "dashscope":
    dashscope_key = get_api_key("DASHSCOPE_API_KEY", "llm")
    # ...检查并显示状态（使用 st.info 而非 st.error）
```

## 修复效果

### 修复前
```
必需配置:
❌ 阿里百炼: 未配置  ← 即使选择了OpenAI也显示此错误
❌ FinnHub: 未配置

可选配置:
✅ OpenAI: sk-proj...  ← OpenAI在可选配置中
```

### 修复后（选择OpenAI时）
```
必需配置:
✅ OpenAI: sk-proj...  ← 当前选择的LLM显示在必需配置
❌ FinnHub: 未配置

可选配置:
ℹ️ 阿里百炼: 未配置  ← 其他LLM显示在可选配置，使用info样式
ℹ️ DeepSeek: 未配置
ℹ️ Google AI: 未配置
```

### 修复后（选择阿里百炼时）
```
必需配置:
✅ 阿里百炼: sk-xxx...  ← 当前选择的LLM显示在必需配置
❌ FinnHub: 未配置

可选配置:
ℹ️ OpenAI: 未配置  ← 其他LLM显示在可选配置
ℹ️ DeepSeek: 未配置
ℹ️ Google AI: 未配置
```

## 测试建议

1. **本地测试**：
   ```bash
   streamlit run streamlit_app.py
   ```

2. **测试场景**：
   - ✅ 选择OpenAI，检查OpenAI是否显示在"必需配置"
   - ✅ 选择阿里百炼，检查阿里百炼是否显示在"必需配置"
   - ✅ 选择DeepSeek，检查DeepSeek是否显示在"必需配置"
   - ✅ 选择Google AI，检查Google AI是否显示在"必需配置"
   - ✅ 检查未选择的提供商是否正确显示在"可选配置"
   - ✅ 确认FinnHub始终显示在"必需配置"（数据源）

3. **Streamlit Cloud部署**：
   - 在Streamlit Cloud Secrets中配置相应的API密钥
   - 确认选择不同的LLM提供商时，必需配置正确切换

## 相关文件

- `web/components/sidebar.py` - API密钥状态显示逻辑（已修复）

## 注意事项

1. **FinnHub** 作为数据源API密钥，无论选择哪个LLM提供商，都会显示在"必需配置"中
2. **Tushare** 作为可选的数据源，总是显示在"可选配置"中
3. 未配置的可选API密钥使用 `st.info()` 样式（蓝色信息图标），而不是 `st.error()` 样式（红色错误图标）
4. 对于某些LLM提供商（如千帆），可能需要多个密钥（AK和SK），修复逻辑已支持这种情况

## 部署到Streamlit Cloud

修复后，请重新部署到Streamlit Cloud：

1. 提交代码更改：
   ```bash
   git add web/components/sidebar.py
   git commit -m "fix: 修复API密钥显示逻辑，根据选择的LLM提供商动态显示必需配置"
   git push
   ```

2. Streamlit Cloud会自动检测到更改并重新部署

3. 验证修复效果：
   - 访问部署的应用
   - 切换不同的LLM提供商
   - 确认"必需配置"和"可选配置"正确显示

## 总结

此修复解决了Streamlit Cloud上API密钥状态显示的混淆问题，使用户能够清楚地了解：
- ✅ 当前选择的LLM提供商需要哪些API密钥
- ✅ 哪些API密钥是必需的
- ✅ 哪些API密钥是可选的
- ✅ 避免了不必要的错误提示

