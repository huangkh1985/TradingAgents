"""
Git 上传问题诊断工具
帮助快速定位 GitHub 推送失败的原因
"""

import subprocess
import os
import sys

def run_cmd(cmd, silent=False):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        if not silent:
            if result.stdout:
                print(result.stdout.strip())
            if result.stderr:
                print(result.stderr.strip())
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

print("="*80)
print("🔍 Git 上传问题诊断工具")
print("="*80)
print()

# 1. 检查 Git 安装
print("1️⃣ 检查 Git 安装...")
success, stdout, stderr = run_cmd("git --version", silent=True)
if success:
    print(f"   ✅ Git 已安装: {stdout.strip()}")
else:
    print("   ❌ Git 未安装或无法访问")
    print("   请访问 https://git-scm.com/download/win 下载安装")
    sys.exit(1)

# 2. 检查 Git 配置
print("\n2️⃣ 检查 Git 配置...")
success1, username, _ = run_cmd("git config --global user.name", silent=True)
success2, email, _ = run_cmd("git config --global user.email", silent=True)

if success1 and username.strip():
    print(f"   ✅ 用户名: {username.strip()}")
else:
    print("   ❌ 未配置用户名")
    print("   运行: git config --global user.name \"你的用户名\"")

if success2 and email.strip():
    print(f"   ✅ 邮箱: {email.strip()}")
else:
    print("   ❌ 未配置邮箱")
    print("   运行: git config --global user.email \"你的邮箱\"")

# 3. 检查是否在 Git 仓库中
print("\n3️⃣ 检查当前目录...")
if os.path.exists('.git'):
    print("   ✅ 当前目录是 Git 仓库")
    
    # 检查仓库状态
    success, stdout, stderr = run_cmd("git status", silent=True)
    if success:
        print("   ✅ Git 仓库状态正常")
    else:
        print("   ❌ Git 仓库可能损坏")
        print(f"   错误: {stderr}")
else:
    print("   ❌ 当前目录不是 Git 仓库")
    print("   请先运行: git init")

# 4. 检查远程仓库配置
print("\n4️⃣ 检查远程仓库...")
success, stdout, stderr = run_cmd("git remote -v", silent=True)
if success and stdout.strip():
    print("   ✅ 远程仓库已配置:")
    for line in stdout.strip().split('\n'):
        print(f"      {line}")
else:
    print("   ❌ 未配置远程仓库")
    print("   运行: git remote add origin <你的仓库URL>")

# 5. 检查暂存区
print("\n5️⃣ 检查暂存区...")
success, stdout, stderr = run_cmd("git status --short", silent=True)
if success:
    if stdout.strip():
        lines = stdout.strip().split('\n')
        print(f"   ⚠️  有 {len(lines)} 个文件未提交")
        print("   前10个文件:")
        for line in lines[:10]:
            print(f"      {line}")
    else:
        print("   ✅ 工作区干净，所有文件已提交")
else:
    print("   ❌ 无法检查状态")

# 6. 检查提交历史
print("\n6️⃣ 检查提交历史...")
success, stdout, stderr = run_cmd("git log --oneline -n 3", silent=True)
if success and stdout.strip():
    print("   ✅ 最近的提交:")
    for line in stdout.strip().split('\n'):
        print(f"      {line}")
else:
    print("   ⚠️  没有提交记录（新仓库）")

# 7. 测试网络连接
print("\n7️⃣ 测试 GitHub 连接...")
success, stdout, stderr = run_cmd("ping github.com -n 2", silent=True)
if success or "bytes=" in stdout:
    print("   ✅ 可以连接到 GitHub")
else:
    print("   ⚠️  无法连接到 GitHub，请检查网络")
    print("   如果在中国大陆，可能需要配置代理")

# 8. 检查大文件
print("\n8️⃣ 检查大文件（>50MB）...")
large_files = []
for root, dirs, files in os.walk('.'):
    # 跳过 .git 目录
    if '.git' in root:
        continue
    for file in files:
        filepath = os.path.join(root, file)
        try:
            size = os.path.getsize(filepath)
            if size > 50 * 1024 * 1024:  # 50MB
                large_files.append((filepath, size / (1024*1024)))
        except:
            pass

if large_files:
    print(f"   ⚠️  发现 {len(large_files)} 个大文件:")
    for filepath, size in large_files[:5]:
        print(f"      {filepath}: {size:.1f}MB")
    print()
    print("   注意: GitHub 限制单个文件不超过 100MB")
    print("   建议: 将大文件添加到 .gitignore")
else:
    print("   ✅ 没有超过 50MB 的大文件")

# 9. 检查敏感文件
print("\n9️⃣ 检查敏感文件...")
sensitive_files = [
    '.env',
    '.env.local',
    '.streamlit/secrets.toml',
    'secrets.toml',
]

found_sensitive = []
for file in sensitive_files:
    if os.path.exists(file):
        found_sensitive.append(file)

if found_sensitive:
    print(f"   ⚠️⚠️⚠️  发现敏感文件:")
    for file in found_sensitive:
        print(f"      {file}")
    print()
    print("   请确认这些文件已在 .gitignore 中！")
    print("   运行: git status 查看是否会被提交")
else:
    print("   ✅ 没有发现明显的敏感文件")

# 10. 尝试推送（模拟）
print("\n🔟 尝试连接远程仓库...")
success, stdout, stderr = run_cmd("git ls-remote --heads origin", silent=True)
if success:
    print("   ✅ 可以连接到远程仓库")
    if stdout.strip():
        print("   远程分支:")
        for line in stdout.strip().split('\n')[:5]:
            if line.strip():
                print(f"      {line.split('/')[-1]}")
else:
    print("   ❌ 无法连接到远程仓库")
    if "fatal: Authentication failed" in stderr:
        print("   错误: 认证失败")
        print("   解决方案:")
        print("      1. 确认使用 Personal Access Token（不是密码）")
        print("      2. 访问: https://github.com/settings/tokens")
        print("      3. 生成新 token，勾选 'repo' 权限")
        print("      4. 推送时使用 token 作为密码")
    elif "fatal: repository" in stderr:
        print("   错误: 仓库不存在或 URL 错误")
        print("   解决方案:")
        print("      1. 检查远程仓库 URL 是否正确")
        print("      2. 运行: git remote -v")
        print("      3. 如需修改: git remote set-url origin <新URL>")
    else:
        print(f"   错误信息: {stderr[:200]}")

print("\n" + "="*80)
print("📋 诊断总结")
print("="*80)
print()

# 给出建议
print("🔧 常见问题解决方案:")
print()
print("1. 认证失败:")
print("   git config --global credential.helper store")
print("   git push origin main")
print("   (然后输入用户名和 Personal Access Token)")
print()
print("2. 分支冲突:")
print("   git pull origin main --rebase")
print("   git push origin main")
print()
print("3. 重新配置远程:")
print("   git remote remove origin")
print("   git remote add origin <你的仓库URL>")
print("   git push -u origin main")
print()
print("4. 强制推送（谨慎使用）:")
print("   git push -f origin main")
print()

print("💡 需要详细日志？运行:")
print("   git push origin main 2>&1 | tee push_log.txt")
print()

