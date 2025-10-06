# Streamlit Cloud 部署问题修复

## 问题诊断

从日志中发现的关键错误：
```
❗️ The service has encountered an error while checking the health of the Streamlit app: 
Get "http://localhost:8501/healthz": dial tcp 127.0.0.1:8501: connect: connection refused
```

**原因分析**：应用无法启动，健康检查失败。主要问题是 `.streamlit/config.toml` 配置文件包含了本地开发的设置，与 Streamlit Cloud 环境不兼容。

## 已修复的问题

### 1. `.streamlit/config.toml` 配置修复

**问题配置（本地开发用）：**
```toml
[server]
address = "localhost"      # ❌ 会导致云端绑定失败
headless = false           # ❌ 云端必须使用 headless 模式
enableCORS = false         # ❌ 云端需要启用 CORS
enableXsrfProtection = false  # ❌ 安全问题

[browser]
serverAddress = "localhost"  # ❌ 云端不应指定
serverPort = 8501           # ❌ 云端自动分配端口
```

**修复后配置（云端兼容）：**
```toml
[server]
headless = true            # ✅ 云端无头模式
enableCORS = true          # ✅ 启用跨域
enableXsrfProtection = true  # ✅ 启用安全保护
fileWatcherType = "none"   # ✅ 云端禁用文件监控

[browser]
gatherUsageStats = false

[client]
showErrorDetails = true    # ✅ 开启以便调试
```

### 2. `packages.txt` 系统依赖添加

**之前**：空文件

**现在**：
```
build-essential
pandoc
```

这些系统包是某些 Python 依赖所需的：
- `pandoc`：pypandoc 包需要
- `build-essential`：编译某些包的 C 扩展

## 部署步骤

### 1. 推送修复到 GitHub

```bash
git add .streamlit/config.toml packages.txt
git commit -m "fix: Update Streamlit Cloud configuration for deployment"
git push origin main
```

### 2. Streamlit Cloud 会自动检测更新并重新部署

等待几分钟，查看日志确认应用启动成功。

### 3. 成功标志

看到以下日志表示成功：
```
[时间] 🎉 Server is running!
```

健康检查应该返回 200 OK 而不是 connection refused。

## 其他建议

### 配置 Secrets（必需的 API 密钥）

如果应用需要 API 密钥，在 Streamlit Cloud 中：

1. 进入应用设置 → **Secrets**
2. 参考 `.streamlit/secrets.toml.example` 
3. 添加必需的密钥（至少配置一个 LLM 提供商）：

```toml
[llm]
# 至少配置以下之一
OPENAI_API_KEY = "sk-your-key"
# 或
DASHSCOPE_API_KEY = "sk-your-key"
# 或  
DEEPSEEK_API_KEY = "sk-your-key"

[data_sources]
# 可选：配置数据源
TUSHARE_TOKEN = "your-token"
```

### 监控应用日志

在 Streamlit Cloud 控制台：
- 点击 **Manage app** → **Logs**
- 查看实时日志输出
- 如有错误会显示完整堆栈跟踪

### 本地测试

如果想在推送前本地测试：

```bash
# 创建云端兼容的配置
cp .streamlit/config.toml .streamlit/config.toml.local
# 使用修复后的配置运行
streamlit run streamlit_app.py
```

## 常见问题

### Q: 如何切换本地开发和云端配置？

**A**: 可以创建两个配置文件：

```bash
# 本地开发配置
.streamlit/config.local.toml  (不提交到 Git)

# 云端配置
.streamlit/config.toml  (提交到 Git)
```

在 `.gitignore` 中添加：
```
.streamlit/config.local.toml
.streamlit/secrets.toml
```

### Q: 应用启动后显示 "Please login"？

**A**: 这是正常的，应用有认证系统。使用测试账号：
- 管理员：`admin` / `admin123`
- 普通用户：`user` / `user123`

### Q: 提示缺少 API 密钥？

**A**: 在 Streamlit Cloud Secrets 中配置至少一个 LLM 提供商的密钥。

## 预期结果

修复后，部署日志应该显示：

```
[时间] 🚀 Starting up repository: 'tradingagents', branch: 'main', main module: 'streamlit_app.py'
[时间] 🐙 Cloning repository...
[时间] 🐙 Cloned repository!
[时间] 📦 Processing dependencies...
[时间] 📦 Processed dependencies!
[时间] 🎉 App is running!  ← 关键成功标志
```

然后可以通过浏览器访问应用。

## 技术细节

### 为什么 `address = "localhost"` 会导致问题？

Streamlit Cloud 运行在容器环境中，应用需要绑定到 `0.0.0.0` 以接受外部连接。指定 `localhost` 会让应用只监听本地回环接口，导致健康检查和外部访问失败。

### 为什么需要 `headless = true`？

Streamlit 在云端运行时不需要（也不能）打开浏览器窗口。`headless = true` 告诉 Streamlit 以无头模式运行，只提供 web 服务。

## 支持

如果问题仍然存在：

1. 检查 Streamlit Cloud 日志中的详细错误信息
2. 确认所有依赖都成功安装
3. 验证 `streamlit_app.py` 文件存在且无语法错误
4. 查看项目 README.md 获取更多帮助

---

**修复日期**：2025-10-06
**修复项**：Streamlit Cloud 配置兼容性
**状态**：✅ 已修复，等待部署验证

