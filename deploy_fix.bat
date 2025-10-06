@echo off
REM Streamlit Cloud 部署修复脚本

echo ========================================
echo Streamlit Cloud 部署修复
echo ========================================
echo.

echo 📝 准备提交修复...
git add .streamlit/config.toml
git add packages.txt
git add .gitignore
git add .streamlit/README.md
git add STREAMLIT_CLOUD_FIX.md

echo.
echo 💾 提交修复...
git commit -m "fix: Update Streamlit Cloud configuration for deployment

- Fix config.toml for cloud compatibility (headless, CORS, XSRF)
- Add system packages (pandoc, build-essential) to packages.txt
- Update .gitignore to exclude local config
- Add comprehensive documentation"

echo.
echo 🚀 推送到 GitHub...
git push origin main

echo.
echo ========================================
echo ✅ 部署修复已推送！
echo ========================================
echo.
echo 接下来请：
echo 1. 访问 Streamlit Cloud 控制台
echo 2. 等待 3-5 分钟让应用重新部署
echo 3. 检查日志确认应用启动成功
echo 4. 如需 API 功能，在 Settings -^> Secrets 中配置密钥
echo.
echo 详细说明请查看: STREAMLIT_CLOUD_FIX.md
echo.

pause

