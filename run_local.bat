@echo off
REM 本地运行 TradingAgents-CN 的批处理脚本
REM Windows 用户双击即可运行

echo ================================================================================
echo 启动 TradingAgents-CN Web 应用
echo ================================================================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python
    echo 请确保 Python 已安装并添加到 PATH
    pause
    exit /b 1
)

REM 检查 Streamlit
python -m streamlit --version >nul 2>&1
if errorlevel 1 (
    echo [错误] Streamlit 未安装
    echo 正在安装 Streamlit...
    pip install streamlit
)

echo [启动] 正在启动应用...
echo 浏览器将自动打开 http://localhost:8501
echo.
echo 按 Ctrl+C 停止服务器
echo ================================================================================
echo.

REM 运行应用（方法1：使用 Python 脚本）
python run_local.py

REM 或者直接运行（方法2，取消注释下面两行）
REM cd web
REM streamlit run app.py

pause

