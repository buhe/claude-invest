---
name: hkex-fetcher
description: 从香港交易所披露易网站获取并下载上市公司年报。使用 agent-browser 访问 https://www1.hkexnews.hk/search/titlesearch.xhtml?lang=zh，填写搜索表单（现有上市、股票代码、标题类别、年报），搜尋并下载最近 5 年的财报 PDF 文件。当用户需要以下操作时使用：(1) 下载港股上市公司年报，(2) 获取港交所披露的财务报告，(3) 搜索香港上市公司公告文件
---

# Hkex Fetcher

## Overview

使用 agent-browser 自动化访问香港交易所披露易网站，搜索指定股票的年报并下载最近 5 年的财报 PDF 文件。

## 工作流程
所有文字使用繁体字
This skill works with the **agent-browser** skill to perform web automation:
### 步骤 1：访问披露易搜索页面

使用 agent-browser cli 访问：
```
https://www1.hkexnews.hk/search/titlesearch.xhtml?lang=zh
```

### 步骤 2：填写搜索表单

按照以下顺序填写表单字段：

| 字段 | 值/操作 |
|------|---------|
| **搜索類型** | 选择「現有上市」（保持默认） |
| **證券 股份代號/股份名稱** | 输入股票代码（如 `00700` 或 `騰訊控股`），等待自动补全，然后执行以下命令确认：<br>`agent-browser eval "Array.from(document.querySelectorAll('span')).find(s => s.textContent.includes('騰訊'))?.click()"` |
| **標題類別及文件類別** | 1. 点击第一个「所有」下拉框<br>2. 选择「標題類別」<br>3. 点击第二个「所有」下拉框<br>4. 选择「財務報表/環境、社會及管治資料」<br>5. 选择子菜单中的「年報」 |
| **開始日期** | 使用默认值（2007/06/25），无需修改 |
| **完結日期** | 使用当前日期（格式：YYYY/MM/DD），默认已填充 |
| **訊息標題** | 留空，不输入任何内容 |

### 步骤 3：执行搜尋

点击「搜尋」按钮，等待页面加载结果。

等待约 5 秒让搜索结果完全加载。

### 步骤 4：获取 PDF 链接并下载

搜索结果页面会显示历年年报列表。

**推荐方式：使用 JavaScript 提取链接 + curl 下载**

首先获取最近 5 年的 PDF 链接（注意年份文本格式可能不同，建议根据实际网页内容调整）：
```bash
agent-browser eval "(async () => { const links = {}; ['2024年報', '2023年度報告', '2022年度報告', '2021年度報告', '二零二零年度報告'].forEach(text => { const a = Array.from(document.querySelectorAll('a')).find(el => el.textContent.includes(text)); if (a) links[text] = a.href; }); return links; })()"
```

然后使用 curl 下载（建议逐个下载，遇到网络错误可重试）：
```bash
# 根据上一步返回的链接下载（示例）
curl -o "00700_2024_年报.pdf" "<PDF_URL_2024>"
curl -o "00700_2023_年报.pdf" "<PDF_URL_2023>"
# ... 继续下载其他年份
```

**如遇网络错误**：curl 可能返回 SSL 连接错误，重新执行失败的下载命令即可。

**替代方式：点击链接下载**
- 使用 `agent-browser click` 点击年报链接
- PDF 会在新标签页打开，使用 `agent-browser tab` 切换
- 使用浏览器下载功能保存（此方式较慢，不推荐）

## 使用示例

**用户请求示例：**
- "帮我下载腾讯控股最近 5 年的年报"
- "下载 00700 的财报"
- "获取小米集团的年报"

**完整命令示例（下载腾讯年报）：**
```bash
# 1. 打开搜索页面
agent-browser open "https://www1.hkexnews.hk/search/titlesearch.xhtml?lang=zh"

# 2. 填写股票代码
agent-browser fill @e16 "00700"

# 3. 确认自动补全
agent-browser eval "Array.from(document.querySelectorAll('span')).find(s => s.textContent.includes('騰訊'))?.click()"

# 4. 设置标题类别（假设 snapshot 后 refs 为 e18-e26）
agent-browser click @e18        # 点击第一个"所有"
agent-browser click @e20        # 选择"標題類別"
agent-browser click @e19        # 点击第二个"所有"
agent-browser click @e24        # 选择"財務報表/環境、社會及管治資料"
agent-browser click @e26        # 选择"年報"

# 5. 执行搜尋（重新获取 snapshot，找到搜尋按钮的 ref）
agent-browser snapshot -i
agent-browser click @<搜尋按钮的ref>        # 点击"搜尋"按钮

# 6. 等待结果并获取 PDF 链接
agent-browser wait 5000
agent-browser eval "(async () => { const links = {}; ['2024年報', '2023年度報告', '2022年度報告', '2021年度報告', '二零二零年度報告'].forEach(text => { const a = Array.from(document.querySelectorAll('a')).find(el => el.textContent.includes(text)); if (a) links[text] = a.href; }); return links; })()"

# 7. 使用 curl 下载（根据上一步返回的链接，逐个下载以便处理错误）
curl -o "00700_2024_年报.pdf" "<PDF_URL_2024>"
# ... 下载其他年份

# 8. 关闭浏览器
agent-browser close
```

## 注意事项

- 确保网络连接正常，能够访问港交所网站
- **refs（如 @e16, @e18）可能随页面变化**，每次操作前务必执行 `agent-browser snapshot -i` 获取最新的 refs
- 搜索结果可能包含多个版本的年报（如英文版、中文版），根据用户偏好选择
- 如果股票代码无效，系统会显示无结果，需要提示用户确认
- 下载的文件用于投资分析，请遵守港交所的使用条款
- URL 需要用引号包裹，避免 shell 解析错误
- **网络不稳定时**：curl 可能返回 SSL 连接错误 (SSL_ERROR_SYSCALL)，重新执行失败的下载命令即可
- **年份文本格式不统一**：网页上年份可能显示为「2024年報」、「2023年度報告」或「二零二零年度報告」，JS 代码需要根据实际情况调整
