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

**重要**：每次操作前务必执行 `agent-browser snapshot -i` 获取最新的 refs。

按照以下顺序填写表单字段：

| 字段 | 值/操作 |
|------|---------|
| **搜索類型** | 选择「現有上市」（保持默认） |
| **證券 股份代號/股份名稱** | 输入股票代码（如 `00700`），等待自动补全出现（检测 `<tbody>` 是否有子元素），然后执行命令确认：<br>`agent-browser eval "(async () => { while (true) { const tbody = document.querySelector('#autocomplete-list-0 tbody'); if (tbody && tbody.children.length > 0) { const firstRow = tbody.querySelector('tr'); firstRow?.click(); return 'Autocomplete found and clicked'; } await new Promise(r => setTimeout(r, 1000)); } })()"` |
| **標題類別及文件類別** | 1. snapshot 后点击第一个「所有」下拉框<br>2. 选择「標題類別」<br>3. 重新 snapshot，点击第二个「所有」下拉框<br>4. 选择「財務報表/環境、社會及管治資料」<br>5. 选择子菜单中的「年報」 |
| **開始日期** | 使用默认值，无需修改 |
| **完結日期** | 使用当前日期（格式：YYYY/MM/DD），默认已填充 |
| **訊息標題** | 留空，不输入任何内容 |

### 步骤 3：执行搜尋

点击「搜尋」按钮，等待页面加载结果。

等待约 5 秒让搜索结果完全加载。

### 步骤 4：获取 PDF 链接并下载

搜索结果页面会显示历年年报列表。

**推荐方式：使用 JavaScript 提取链接 + curl 下载**

首先获取最近 5 年的 PDF 链接（动态计算年份，只匹配年份即可）：
```bash
agent-browser eval "(async () => { const currentYear = new Date().getFullYear(); const links = {}; for (let i = 0; i < 5; i++) { const year = currentYear - i; const a = Array.from(document.querySelectorAll('a')).find(el => el.textContent.includes(year.toString())); if (a) links[year] = a.href; } return links; })()"
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

# 2. 获取页面 refs 并填写股票代码
agent-browser snapshot -i
agent-browser fill @<股份代号输入框ref> "00700"

# 3. 等待并确认自动补全（检测 tbody 是否有子元素，然后点击第一行）
agent-browser eval "(async () => { while (true) { const tbody = document.querySelector('#autocomplete-list-0 tbody'); if (tbody && tbody.children.length > 0) { const firstRow = tbody.querySelector('tr'); firstRow?.click(); return 'Autocomplete found and clicked'; } await new Promise(r => setTimeout(r, 1000)); } })()"

# 4. 设置标题类别 - 每步都需要重新 snapshot
agent-browser snapshot -i
agent-browser click @<第一个"所有"ref>        # 点击第一个下拉框
agent-browser snapshot -i
agent-browser click @<"標題類別"ref>          # 选择標題類別
agent-browser snapshot -i
agent-browser click @<第二个"所有"ref>        # 点击第二个下拉框
agent-browser snapshot -i
agent-browser click @<"財務報表"ref>          # 选择財務報表
agent-browser snapshot -i
agent-browser click @<"年報"ref>              # 选择年報

# 5. 执行搜尋
agent-browser snapshot -i
agent-browser click @<搜尋按钮ref>           # 点击"搜尋"按钮

# 6. 等待结果并获取 PDF 链接（动态计算最近 5 年，只匹配年份）
agent-browser wait 5000
agent-browser eval "(async () => { const currentYear = new Date().getFullYear(); const links = {}; for (let i = 0; i < 5; i++) { const year = currentYear - i; const a = Array.from(document.querySelectorAll('a')).find(el => el.textContent.includes(year.toString())); if (a) links[year] = a.href; } return links; })()"

# 7. 使用 curl 下载（根据上一步返回的链接，逐个下载以便处理错误）
curl -o "00700_${year}_年报.pdf" "<PDF_URL>"  # 替换 ${year} 和 <PDF_URL> 为实际值
# ... 继续下载其他年份

# 8. 关闭浏览器
agent-browser close
```

## 注意事项

- 确保网络连接正常，能够访问港交所网站
- **refs（如 @e16, @e18）每次页面加载都会变化**，务必在每次操作前执行 `agent-browser snapshot -i` 获取最新的 refs
- **年份匹配**：由于搜索时已设置"年报"类别，结果中包含年份（如 "2024"）的就一定是年报，无需额外匹配"年報"或"年度報告"
- **自动补全确认**：通过检测 `#autocomplete-list-0 tbody` 是否有子元素来判断补全是否完成，然后自动点击第一行。如需选择特定结果，可修改 `tbody.querySelector('tr')` 为 `tbody.children[index]`（从 0 开始）
- 搜索结果可能包含多个版本的年报（如英文版、中文版），默认获取中文版本（链接包含 `_c.pdf`）
- 如果股票代码无效，系统会显示无结果，需要提示用户确认
- 下载的文件用于投资分析，请遵守港交所的使用条款
- URL 需要用引号包裹，避免 shell 解析错误
- **网络不稳定时**：curl 可能返回 SSL 连接错误或下载缓慢，重新执行失败的下载命令即可
