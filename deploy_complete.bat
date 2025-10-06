@echo off
REM 部署完整应用到 Streamlit Cloud

echo ========================================
echo 部署完整应用到 Streamlit Cloud
echo ========================================
echo.

echo 📝 添加文件到 Git...
git add streamlit_app.py
git add web/__init__.py
git add cloud_setup.py
git add CLOUD_DEPLOYMENT_GUIDE.md
git add deploy_complete.bat

echo.
echo 💾 提交更改...
git commit -m "feat: Add complete application with cloud compatibility

- Update streamlit_app.py to load full web application
- Add proper error handling and fallback mode
- Create cloud setup check script
- Add comprehensive deployment guide
- Ensure web module is properly importable"

echo.
echo 🚀 推送到 GitHub...
git push origin main

echo.
echo ========================================
echo ✅ 完整应用已推送！
echo ========================================
echo.
echo 📋 接下来请：
echo.
echo 1. 等待 Streamlit Cloud 重新部署 (3-5分钟)
echo 2. 配置 API 密钥:
echo    - 访问 Streamlit Cloud 控制台
echo    - Settings -^> Secrets
echo    - 添加至少一个 LLM 提供商的密钥
echo.
echo 3. 验证功能:
echo    - 登录功能
echo    - 股票分析功能
echo    - 查看分析结果
echo.
echo 详细说明请查看: CLOUD_DEPLOYMENT_GUIDE.md
echo.

pause

