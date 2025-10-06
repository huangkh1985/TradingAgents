# ⚡ 快速配置指南

## 🎯 最简配置（2分钟搞定）

### 配置内容

在 Streamlit Cloud 的 **Settings → Secrets** 中添加：

```toml
[llm]
# OpenAI API 密钥
OPENAI_API_KEY = "sk-你的真实OpenAI密钥"

[data_sources]
# AKShare 完全免费，无需配置！
# 已内置支持，无需任何 token
```

**就这么简单！** 只需要一个 OpenAI 密钥即可。

---

## 📝 OpenAI API 密钥获取步骤

### 1. 注册 OpenAI 账号
- 🔗 访问: https://platform.openai.com/
- 📧 使用邮箱注册
- ⚠️ 需要绑定信用卡（国内双币卡或虚拟卡）

### 2. 创建 API 密钥
1. 登录后，点击右上角头像
2. 选择 **API keys**
3. 点击 **Create new secret key**
4. 给密钥起个名字（如 "TradingAgents"）
5. 点击 **Create secret key**
6. **立即复制密钥**（只显示一次！）

### 3. 配置到 Streamlit Cloud
1. 打开您的应用管理页面
2. 点击 **Settings** → **Secrets**
3. 粘贴上面的配置模板
4. 将 `"sk-你的真实OpenAI密钥"` 替换为刚才复制的密钥
5. 点击 **Save**
6. 重启应用

---

## 💰 费用说明

### OpenAI
- **按使用量计费**
- 新用户通常有 $5-18 免费额度
- GPT-3.5-turbo: 约 $0.002/1K tokens（非常便宜）
- GPT-4: 约 $0.03/1K tokens
- 💡 一次股票分析约消耗 0.5-2 美分

### AKShare
- **完全免费！**
- 无需注册
- 无需 API 密钥
- 支持 A股、港股、美股、期货、基金等
- 数据实时更新

---

## ✅ 测试配置

配置完成后：

1. 等待应用重启（约 30 秒）
2. 访问应用，使用测试账号登录：
   - 管理员：`admin` / `admin123`
3. 输入股票代码测试：
   - A股示例：`000001` (平安银行)
   - 美股示例：`AAPL` (苹果)
4. 点击"开始分析"

如果看到分析进度，说明配置成功！🎉

---

## 🔄 其他 LLM 选项

如果不想用 OpenAI，也可以选择：

### 阿里云通义千问
```toml
[llm]
DASHSCOPE_API_KEY = "sk-你的dashscope密钥"
```
- 🔗 https://dashscope.aliyun.com/
- 🇨🇳 中文友好，国内访问快
- 💰 新用户有免费额度

### DeepSeek
```toml
[llm]
DEEPSEEK_API_KEY = "sk-你的deepseek密钥"
```
- 🔗 https://platform.deepseek.com/
- 💎 性价比极高
- 💰 价格比 OpenAI 便宜 10 倍

---

## ❓ 常见问题

**Q: 我没有信用卡，怎么办？**
A: 可以使用阿里云通义千问或 DeepSeek，支持支付宝付款。

**Q: OpenAI 在国内能用吗？**
A: 需要科学上网，或使用国内的 LLM 服务商。

**Q: 免费额度用完了怎么办？**
A: OpenAI 需要充值继续使用，或切换到其他免费额度更多的服务商。

**Q: 配置后还是报错？**
A: 
1. 检查密钥是否复制完整（包括 `sk-` 前缀）
2. 确认密钥没有过期
3. 查看 Streamlit Cloud 日志获取详细错误信息

---

## 🎉 完成！

配置完成后，您就可以：
- 分析任意股票（A股、港股、美股）
- 获取 AI 智能分析报告
- 查看历史分析记录
- 导出分析结果

开始您的智能投资之旅吧！📈

