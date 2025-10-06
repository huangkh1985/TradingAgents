# Streamlit Cloud UnboundLocalError 修复报告

## 问题描述

在 Streamlit Cloud 上运行应用时出现以下错误：

```
UnboundLocalError: cannot access local variable 'save_model_selection' where it is not associated with a value
```

错误发生在 `web/components/sidebar.py` 第 492 行。

## 根本原因

在 `render_sidebar()` 函数中存在一个**变量作用域冲突**问题：

1. 文件顶部（第 15 行）已经导入了 `save_model_selection`：
   ```python
   from web.utils.persistence import load_model_selection, save_model_selection
   ```

2. 但在函数内部的条件块中（第 225 行）又有一个重复的导入：
   ```python
   from ..utils.persistence import save_model_selection
   ```

3. 当 Python 解析器看到函数内部有对 `save_model_selection` 的导入时，它会将该变量标记为**局部变量**。

4. 如果条件判断为 False（即 `dashscope_key` 存在），第 225 行的导入不会执行，`save_model_selection` 就没有被赋值。

5. 当后续代码（如第 492 行）尝试使用 `save_model_selection` 时，就会抛出 `UnboundLocalError`，因为局部变量未被初始化。

## 解决方案

删除函数内部的重复导入语句（第 225 行），直接使用模块级别已导入的函数：

### 修改前：
```python
if not dashscope_key:
    logger.warning("⚠️ [自动修复] 检测到 dashscope 未配置，自动切换到 openai")
    st.session_state.llm_provider = 'openai'
    st.session_state.model_category = 'openai'
    # 保存更新后的配置
    from ..utils.persistence import save_model_selection  # ❌ 问题所在
    save_model_selection('openai', 'openai', st.session_state.llm_model)
```

### 修改后：
```python
if not dashscope_key:
    logger.warning("⚠️ [自动修复] 检测到 dashscope 未配置，自动切换到 openai")
    st.session_state.llm_provider = 'openai'
    st.session_state.model_category = 'openai'
    # 保存更新后的配置 (使用已在模块顶部导入的函数)
    save_model_selection('openai', 'openai', st.session_state.llm_model)  # ✅ 修复
```

## 技术说明

这是一个经典的 Python 作用域问题：

- **全局作用域导入**：在模块顶部导入的变量在整个模块中都可用
- **局部作用域导入**：在函数内部导入会创建局部变量
- **冲突问题**：当两者混用时，局部导入会"遮蔽"全局导入
- **条件导入风险**：如果局部导入在条件块中，可能导致变量未初始化

## 验证

修复后代码已通过 linter 检查，无任何错误。

## 预期效果

修复后，应用应该能在 Streamlit Cloud 上正常运行，不会再出现 `UnboundLocalError` 错误。

## 建议

为避免类似问题：
1. ✅ 在模块顶部集中管理所有导入
2. ❌ 避免在函数内部重复导入已在模块级别导入的内容
3. ❌ 避免在条件块中导入常用函数
4. ✅ 如果确实需要条件导入，确保在所有代码路径中都能访问到该变量

## 修改文件

- `web/components/sidebar.py` - 第 225 行

---
**修复日期**: 2025-10-06
**状态**: ✅ 已完成

