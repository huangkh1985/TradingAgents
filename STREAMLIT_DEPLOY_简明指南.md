# 📱 Streamlit Cloud 移动端部署 - 5分钟快速指南

## 🎯 目标
将你的 TradingAgents 项目部署到 Streamlit Cloud，实现手机/平板访问

---

## 📋 准备工作（已完成✅）

我已经为你创建了以下文件：

1. ✅ **streamlit_app.py** - 云部署入口文件
2. ✅ **.streamlit/config.toml** - Streamlit 配置（已更新）
3. ✅ **.streamlit/secrets.toml.example** - API密钥配置示例
4. ✅ **packages.txt** - 系统依赖（按需使用）
5. ✅ **.gitignore** - 已添加 secrets.toml（保护密钥）

---

## 🚀 部署步骤（5步完成）

### 步骤 1: 推送代码到 GitHub

```bash
# 在项目目录打开终端，执行：
git add .
git commit -m "添加 Streamlit Cloud 部署配置"
git push origin main
```

### 步骤 2: 登录 Streamlit Cloud

1. 打开浏览器访问: https://share.streamlit.io/
2. 点击 **"Sign up"** 或 **"Sign in"**
3. 选择 **"Continue with GitHub"**
4. 授权 Streamlit Cloud 访问你的仓库

### 步骤 3: 创建新应用

1. 点击右上角 **"New app"** 按钮

2. 填写配置信息：
   - **Repository**: 选择 `你的用户名/TradingAgents-CN`
   - **Branch**: `main` (或 `master`)
   - **Main file path**: `streamlit_app.py`

3. （可选）点击 **"Advanced settings"**：
   - **Python version**: 选择 `3.10` 或 `3.11`

4. 点击 **"Deploy!"** 开始部署

### 步骤 4: 配置 API 密钥

等待 3-5 分钟部署完成后：

1. 点击右下角 **"Manage app"**
2. 选择左侧 **"Settings"** 
3. 点击 **"Secrets"**
4. 复制以下内容并填入你的真实密钥：

```toml
# 必需配置（至少配置一个 LLM）
[llm]
OPENAI_API_KEY = "sk-你的OpenAI密钥"

# 或者使用国产大模型（二选一）
DASHSCOPE_API_KEY = "你的通义千问密钥"
# GOOGLE_API_KEY = "你的Google密钥"

# 如果需要分析 A股（可选）
[data_sources]
TUSHARE_TOKEN = "你的Tushare令牌"
```

5. 点击 **"Save"**，应用会自动重启

### 步骤 5: 测试访问

1. 部署成功后，你会看到一个 URL：
   ```
   https://你的应用名.streamlit.app
   ```

2. 在电脑浏览器测试是否正常打开

3. 在手机浏览器输入相同 URL 测试

---

## 📱 添加到手机主屏幕

### iPhone / iPad (iOS)

1. 在 **Safari** 浏览器打开应用
2. 点击底部 **分享** 按钮 (正方形向上箭头)
3. 向下滚动找到 **"添加到主屏幕"**
4. 点击 **"添加"**
5. 现在可以像原生 App 一样使用！

### Android 手机

1. 在 **Chrome** 浏览器打开应用
2. 点击右上角 **菜单** (三个点)
3. 选择 **"添加到主屏幕"** 或 **"安装应用"**
4. 点击 **"添加"**
5. 主屏幕会出现应用图标

---

## ⚡ 常见问题

### Q1: 部署失败怎么办？

**A**: 检查以下几点：
1. GitHub 仓库是否公开（Private 仓库需要授权）
2. `streamlit_app.py` 文件是否在根目录
3. 查看 Streamlit Cloud 的日志，找到具体错误

### Q2: 应用显示 "Secrets not found"

**A**: 
1. 进入应用设置 → Secrets
2. 按照步骤 4 添加 API 密钥配置
3. 保存后等待应用重启（约 30 秒）

### Q3: 依赖安装超时

**A**: 项目依赖较多，可能需要 5-10 分钟：
- 耐心等待完成
- 如果超过 15 分钟仍失败，查看日志
- 可以尝试简化 `requirements.txt`

### Q4: 移动端布局显示不正常

**A**: 
1. 刷新页面
2. 清除浏览器缓存
3. 尝试横屏/竖屏切换

### Q5: 应用多久会休眠？

**A**: Streamlit Cloud 免费版：
- 7 天未访问会休眠
- 首次访问会自动唤醒（需要 1-2 分钟）
- 升级付费版可保持永久在线

---

## 🎯 验证清单

部署成功的标志：

- [ ] 能在电脑浏览器打开应用
- [ ] 能在手机浏览器打开应用
- [ ] 可以选择股票代码
- [ ] 可以提交分析请求
- [ ] 能看到分析结果
- [ ] 移动端界面显示正常

全部勾选 = 部署成功！🎉

---

## 📚 完整文档

需要更详细的信息？查看：

- **详细部署指南**: `STREAMLIT_CLOUD_DEPLOY.md`
- **快速检查清单**: `DEPLOY_CHECKLIST.md`
- **Streamlit 官方文档**: https://docs.streamlit.io/

---

## 🆘 需要帮助？

1. 查看应用日志：Streamlit Cloud → Manage app → Logs
2. 检查 GitHub Issues: https://github.com/你的用户名/TradingAgents-CN/issues
3. Streamlit 社区: https://discuss.streamlit.io/

---

## ✨ 恭喜！

完成这 5 个步骤后，你的股票分析应用就可以：

- ✅ 随时随地访问（手机、平板、电脑）
- ✅ 自动更新（推送代码即自动部署）
- ✅ 免费托管（Streamlit Cloud 免费版）
- ✅ 无需服务器维护
- ✅ HTTPS 安全连接

**开始你的移动端 AI 交易分析之旅吧！** 📈📱

