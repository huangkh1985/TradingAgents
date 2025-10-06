# 🚀 Streamlit Cloud 部署前验证清单

## ✅ 本地验证步骤（部署前必做）

### 第 1 步：验证 streamlit_app.py（最重要！）

**这是 Streamlit Cloud 将使用的入口文件**

```bash
# 在项目根目录运行
streamlit run streamlit_app.py
```

**预期结果：**
- ✅ 浏览器自动打开 http://localhost:8501
- ✅ 页面正常加载，没有 ModuleNotFoundError
- ✅ 侧边栏显示正常
- ✅ 可以看到输入表单

**如果失败：**
- ❌ 不要推送到 GitHub
- ❌ 先解决错误再继续

---

### 第 2 步：测试核心功能

不需要完整测试（可能需要 API 密钥），但要确认：

- [ ] 页面布局正确
- [ ] 没有导入错误
- [ ] 静态内容显示正常
- [ ] 表单可以输入

---

### 第 3 步：检查敏感文件

```bash
# 运行检查
git status
```

**确认以下文件不会被提交：**
- ❌ `.streamlit/secrets.toml`
- ❌ `.env`
- ❌ 任何包含 API 密钥的文件

**检查 .gitignore：**
```bash
# 查看 .gitignore 内容
cat .gitignore | grep secrets
```

应该看到：
```
.streamlit/secrets.toml
```

---

### 第 4 步：验证部署文件存在

```bash
# 检查关键文件
ls streamlit_app.py
ls .streamlit/config.toml
ls .streamlit/secrets.toml.example
ls requirements.txt
ls pyproject.toml
```

全部应该存在。

---

## 📋 部署流程总结

### ✅ 本地验证通过后

1. **推送到 GitHub**
   ```bash
   python push_to_github_adapted.py
   ```
   
   或手动：
   ```bash
   git add .
   git commit -m "添加 Streamlit Cloud 部署配置"
   git push origin main
   ```

2. **登录 Streamlit Cloud**
   - 访问: https://share.streamlit.io/
   - 使用 GitHub 账号登录

3. **创建应用**
   - Repository: `你的用户名/TradingAgents-CN`
   - Branch: `main`
   - Main file path: `streamlit_app.py` ⭐ 关键！
   - 点击 Deploy

4. **配置 Secrets**
   - 等待部署完成（3-5分钟）
   - Settings → Secrets
   - 复制 `.streamlit/secrets.toml.example` 内容
   - 填入真实 API 密钥
   - Save

5. **测试访问**
   - 桌面浏览器测试
   - 手机浏览器测试

---

## 🔧 快速命令参考

### 本地测试（选择其一）

```bash
# 方法 1：测试云部署入口（推荐）
streamlit run streamlit_app.py

# 方法 2：直接测试 web/app.py
cd web && streamlit run app.py

# 方法 3：使用启动脚本
python run_local.py
```

### 诊断问题

```bash
# 检查 Git 状态
git status

# 检查敏感文件
python diagnose_git_issue.py

# 查看详细日志
streamlit run streamlit_app.py --logger.level=debug
```

---

## ⚠️ 常见错误和解决

### 错误 1：ModuleNotFoundError: No module named 'components'

**原因：** 工作目录或 Python 路径不正确

**解决：**
```bash
# 确保在项目根目录
cd D:\user_data\Deeplearn\TradingAgents-CN

# 运行正确的入口
streamlit run streamlit_app.py
```

### 错误 2：API 密钥未配置

**本地测试时：**
- 创建 `.streamlit/secrets.toml`（参考 example 文件）
- 或使用 `.env` 文件

**Streamlit Cloud：**
- 在 Settings → Secrets 中配置

### 错误 3：依赖安装失败

**本地：**
```bash
pip install -r requirements.txt
# 或
pip install -e .
```

**Streamlit Cloud：**
- 检查 `requirements.txt` 或 `pyproject.toml`
- 查看部署日志找到具体错误

---

## 📊 验证检查表

部署前确认：

- [ ] ✅ `streamlit run streamlit_app.py` 本地运行成功
- [ ] ✅ 没有 ModuleNotFoundError 或 ImportError
- [ ] ✅ 页面可以正常加载和显示
- [ ] ✅ `.gitignore` 包含 `secrets.toml`
- [ ] ✅ 没有敏感信息在代码中
- [ ] ✅ GitHub 仓库已创建（Public）
- [ ] ✅ 代码已推送到 GitHub
- [ ] ✅ 准备好 API 密钥用于配置 Secrets

全部勾选后，可以开始部署！

---

## 🎯 部署成功标志

### Streamlit Cloud 界面

- 状态显示 "Running" 🟢
- 有一个公开 URL（https://xxx.streamlit.app）
- 日志没有红色错误

### 应用访问

- 桌面浏览器可以打开
- 手机浏览器可以打开
- 页面布局正常
- 功能可以使用（输入 API 密钥后）

---

## 📚 相关文档

- [快速指南](STREAMLIT_DEPLOY_简明指南.md) - 5分钟快速部署
- [详细指南](STREAMLIT_CLOUD_DEPLOY.md) - 完整部署文档
- [检查清单](DEPLOY_CHECKLIST.md) - 部署检查清单
- [部署总结](DEPLOYMENT_SUMMARY.md) - 部署准备总结

---

## 💡 专业提示

1. **本地必须测试 streamlit_app.py**
   - 这是 Streamlit Cloud 使用的文件
   - 本地不测试 = 云上大概率失败

2. **保护好 API 密钥**
   - 永远不要提交 secrets.toml
   - 使用 Streamlit Cloud 的 Secrets 管理

3. **分步骤部署**
   - 先本地验证
   - 再推送 GitHub
   - 最后部署 Cloud
   - 每步都确认成功

4. **查看日志**
   - Streamlit Cloud 有详细日志
   - Manage app → Logs
   - 错误信息在这里找

---

**准备好了吗？开始验证！** 🚀

```bash
streamlit run streamlit_app.py
```

