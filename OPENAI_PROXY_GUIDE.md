# 🌐 OpenAI 代理配置指南

## 📖 概述

如果您在国内无法直接访问 OpenAI API，可以通过配置 `OPENAI_API_BASE` 使用代理服务。

---

## ⚡ 快速配置

在 Streamlit Cloud 的 **Settings → Secrets** 中添加：

```toml
[llm]
# OpenAI API 密钥
OPENAI_API_KEY = "sk-你的OpenAI密钥"

# OpenAI API 代理地址（重要！）
OPENAI_API_BASE = "https://your-proxy-url.com/v1"
```

**⚠️ 注意**：
- `OPENAI_API_BASE` 必须以 `/v1` 结尾
- 不同代理服务的 URL 格式可能不同
- 确保代理服务稳定可靠

---

## 🔗 常见代理服务

### 1. OpenAI-SB（国内常用）
```toml
[llm]
OPENAI_API_KEY = "你的OpenAI-SB密钥"
OPENAI_API_BASE = "https://api.openai-sb.com/v1"
```
- 🔗 官网: https://openai-sb.com/
- 💰 费用: 按使用量计费
- 🇨🇳 特点: 国内访问稳定

### 2. API2D（商业代理）
```toml
[llm]
OPENAI_API_KEY = "你的API2D密钥"
OPENAI_API_BASE = "https://openai.api2d.net/v1"
```
- 🔗 官网: https://api2d.com/
- 💰 费用: 充值使用
- 🇨🇳 特点: 支持支付宝

### 3. CloseAI（亚洲优化）
```toml
[llm]
OPENAI_API_KEY = "你的CloseAI密钥"
OPENAI_API_BASE = "https://api.closeai-asia.com/v1"
```
- 🔗 官网: https://console.closeai-asia.com/
- 💰 费用: 按使用量计费
- 🌏 特点: 亚洲节点，速度快

---

## 🔧 配置步骤

### 方式 1：使用 OpenAI 官方密钥 + 代理

1. **获取 OpenAI 官方密钥**
   - 访问 https://platform.openai.com/
   - 创建 API Key

2. **选择代理服务**
   - 选择上面列出的任一代理服务

3. **配置 Secrets**
   ```toml
   [llm]
   OPENAI_API_KEY = "sk-官方密钥"
   OPENAI_API_BASE = "代理URL"
   ```

### 方式 2：使用代理服务的密钥

某些代理服务提供自己的密钥系统：

1. **注册代理服务**
   - 在代理服务网站注册账号
   - 充值/购买额度

2. **获取代理密钥**
   - 在代理服务控制台创建密钥

3. **配置 Secrets**
   ```toml
   [llm]
   OPENAI_API_KEY = "代理服务的密钥"
   OPENAI_API_BASE = "代理服务的URL"
   ```

---

## ✅ 测试配置

配置完成后，测试是否正常工作：

1. **重启应用**
   - 保存 Secrets 后重启

2. **登录应用**
   - 使用测试账号：`admin` / `admin123`

3. **测试分析**
   - 输入股票代码：`AAPL` 或 `000001`
   - 点击"开始分析"
   - 查看是否能正常调用 LLM

4. **检查日志**
   - 如果出错，查看应用日志
   - 确认 API 调用是否成功

---

## 🐛 常见问题

### Q1: 配置后仍然报错 "Connection timeout"

**原因**：代理 URL 配置错误或代理服务不可用

**解决**：
1. 检查 `OPENAI_API_BASE` 格式是否正确（必须包含 `/v1`）
2. 确认代理服务是否正常运行
3. 尝试更换其他代理服务

### Q2: 报错 "Invalid API key"

**原因**：密钥配置错误

**解决**：
1. 确认使用的是代理服务的密钥（不是 OpenAI 官方密钥）
2. 检查密钥是否复制完整
3. 确认密钥是否已过期或被禁用

### Q3: 分析速度很慢

**原因**：代理服务网络延迟高

**解决**：
1. 选择离您更近的代理节点
2. 更换响应更快的代理服务
3. 或直接使用国内 LLM（阿里云、DeepSeek）

### Q4: 代理服务需要付费吗？

**回答**：
- 大多数代理服务需要付费
- 费用通常比 OpenAI 官方稍高（包含代理成本）
- 建议对比多个服务，选择性价比最高的

---

## 🔄 替代方案

如果不想使用代理，可以考虑：

### 方案 1：使用国内 LLM（推荐）⭐

**阿里云通义千问**：
```toml
[llm]
DASHSCOPE_API_KEY = "sk-你的dashscope密钥"
```
- ✅ 无需科学上网
- ✅ 中文理解好
- ✅ 新用户有免费额度
- 🔗 https://dashscope.aliyun.com/

**DeepSeek**：
```toml
[llm]
DEEPSEEK_API_KEY = "sk-你的deepseek密钥"
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
```
- ✅ 性价比极高
- ✅ 性能接近 GPT-4
- ✅ 价格便宜 10 倍
- 🔗 https://platform.deepseek.com/

### 方案 2：自建代理

如果您有海外服务器，可以自建 OpenAI 代理：
- 使用 Nginx 反向代理
- 使用 Cloudflare Workers
- 详细教程请搜索 "OpenAI 反向代理搭建"

---

## 💡 最佳实践

### 1. 多备份方案
配置多个 LLM 提供商，防止单点故障：

```toml
[llm]
# 主力：OpenAI 代理
OPENAI_API_KEY = "sk-代理密钥"
OPENAI_API_BASE = "https://proxy.com/v1"

# 备用：国内 LLM
DASHSCOPE_API_KEY = "sk-dashscope密钥"
DEEPSEEK_API_KEY = "sk-deepseek密钥"
```

### 2. 监控使用量
- 定期检查 API 使用量
- 设置预算提醒
- 避免超额扣费

### 3. 安全性
- 定期更换 API 密钥
- 不要在公开场合分享密钥
- 使用 Streamlit Secrets 存储密钥

---

## 📞 获取帮助

如果遇到配置问题：

1. **查看应用日志**
   - Streamlit Cloud → Manage app → Logs
   - 查找具体的错误信息

2. **测试代理连接**
   - 使用 curl 测试代理是否可访问
   ```bash
   curl https://your-proxy-url.com/v1/models \
     -H "Authorization: Bearer your-api-key"
   ```

3. **咨询代理服务商**
   - 联系代理服务的客服
   - 确认配置是否正确

4. **切换到国内 LLM**
   - 如果代理问题无法解决
   - 建议直接使用阿里云或 DeepSeek

---

**更新时间**: 2025-10-06  
**适用版本**: TradingAgents-CN v1.0+  
**状态**: ✅ 已验证可用

