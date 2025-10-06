# TradingAgents-CN 快速启动脚本 (PowerShell)
# 使用方法: .\start_app.ps1

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "  🚀 启动 TradingAgents-CN Web 应用" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

# 切换到 web 目录
Set-Location -Path "web"

Write-Host "✅ 工作目录: $(Get-Location)" -ForegroundColor Green
Write-Host "🌐 启动 Streamlit 服务器..." -ForegroundColor Yellow
Write-Host "   浏览器将自动打开 http://localhost:8501" -ForegroundColor Yellow
Write-Host ""
Write-Host "💡 提示：按 Ctrl+C 停止服务器" -ForegroundColor Gray
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

# 启动 Streamlit
streamlit run app.py

# 返回项目根目录
Set-Location -Path ".."

