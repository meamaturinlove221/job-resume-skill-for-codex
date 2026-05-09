# 🎯 Job Resume Skill — Claude Code 自动化求职工作流

> 💼 基于 Claude Code 的求职助手：Boss直聘搜岗 → Excel 管理 → 智能生成自我介绍 + 定制简历 PDF
>
> 从刷 JD 到投递，把重复劳动交给 AI。

---

## 🤔 为什么需要这个工作流？

求职最耗时的从来不是面试——是 **重复刷岗、手动筛 JD、逐个改简历**。

```
传统求职流程 ❌                          本工作流 ✅
───────────────                          ───────────────
刷Boss直聘 2 小时 ──► 筛出 20 个岗       自动抓取 + Excel 整理
每个岗手动复制 JD ──► 改一版简历 30 分钟  AI 根据 JD 定制简历
投了 30 家海投 ──► HR 一眼看出           每个岗位独立定制，ATS 优化
打招呼想半天 ──► 要么套话要么空白         自动生成匹配的 100 字自我介绍
```

---

## ✨ Skill 亮点

| 能力 | 说明 |
|------|------|
| 🔍 **模板化搜岗** | 预设城市/岗位/薪资/规模/行业组合，支持多模板批量搜索 |
| 📊 **Excel 可视管理** | 岗位信息自动写入 Excel，一目了然，勾选即筛选 |
| 💬 **智能自我介绍** | 根据 JD 自动生成 100-150 字 Boss 打招呼话术，口语化不生硬 |
| 📄 **定制简历 PDF** | 基于 JD 关键词重写工作经历，ATS 优化，Chrome 直接出 PDF |
| 🎯 **真实可信赖** | 只改表述顺序和措辞，**不编造经历**，保留所有量化数据 |
| 🔄 **去重** | 自动去重、跨天排重 |

---

## 📦 包含的技能

| 技能 | 说明 |
|------|------|
| `/resume` | 传入 JD 文本或链接，直接生成针对性简历 + 匹配度评估 + 面试建议 |
| `/job-hunt search` | 自动搜索 Boss直聘岗位，去重后写入 Excel |
| `/job-hunt apply` | 读取 Excel 勾选，批量生成自我介绍 + 定制简历 PDF |

---

## 🚀 快速开始

### 1. 安装技能文件

将 `skills/` 下的文件复制到 Claude Code commands 目录：

```bash
# 方法1：复制到全局 commands
mkdir -p ~/.claude/commands/求职工具
cp skills/resume.md skills/job-hunt.md ~/.claude/commands/求职工具/

# 方法2：复制到项目级 commands
cp -r skills/ .claude/commands/求职工具/
```

### 2. 配置模板文件

```bash
mkdir -p ~/Desktop/job-search/resumes
cp templates/resume_template.html ~/Desktop/job-search/
cp templates/job_templates.json ~/Desktop/job-search/
```

### 3. 填写个人信息

编辑 skill 文件中的占位符：

| 占位符 | 替换为 |
|--------|--------|
| `{{YOUR_NAME}}` | 你的姓名 |
| `{{YOUR_EMAIL}}` | 邮箱 |
| `{{YOUR_PHONE}}` | 电话 |
| 工作经历、教育背景、技能等 | 你的真实经历 |

### 4. 创建用户档案

基于 `examples/profile_template.md` 创建你的完整技能档案：

```bash
cp examples/profile_template.md ~/.claude/projects/-YOUR_PATH/memory/user_profile.md
# 编辑填写你的信息
```

### 5. 前置依赖

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI
- [browser-act](https://github.com/nicepkg/browser-act) — Boss直聘页面自动化（`/job-hunt search` 需要）
- Google Chrome — 简历 HTML → PDF 渲染
- `xlsx` skill — Excel 读写

---

## 📐 工作流程

### `/resume` — 从 JD 直接生成简历

```
/JD 文本或链接
     │
     ▼
📖 获取 JD 内容（webReader）
     │
     ▼
🔍 关键词分级（P1必须/P2重要/P3加分）
     │
     ▼
🎯 匹配分析（技能档案 vs JD要求）
     │
     ▼
📝 生成简历 Markdown
     │
     ▼
💡 输出：简历 + 匹配度评估 + 面试建议
```

### `/job-hunt` — 批量搜岗 + 批量出简历

```
/job-hunt search                         /job-hunt apply
     │                                         │
     ▼                                         ▼
 📋 选择搜索模板                            📖 读取勾选 + JD 缓存
     │                                         │
     ▼                                         ▼
 🌐 browser-act 自动抓岗                    💬 生成自我介绍（E列 ✓）
     │                                         │
     ▼                                         ▼
 🔄 去重                                     📄 定制简历 PDF（G列 ✓）
     │                                         │
     ▼                                         ▼
 📊 写入 Excel + 缓存 JD                    💾 保存 Excel + 清理缓存
     │
     ▼
 ✋ 暂停 — 等你打勾
```

**两步搞定：**

```bash
# 📌 Step 1：搜索岗位，写入 Excel
/job-hunt search

# 👆 在 Excel 中勾选感兴趣的岗位和需要新简历的岗位

# 📌 Step 2：批量生成自我介绍 + 定制简历
/job-hunt apply
```

---

## 📁 文件结构

```
job-resume-skill/
├── README.md                          # 🫵 你正在看的这个文件
├── LICENSE                            # 📜 MIT License
├── .gitignore
├── skills/
│   ├── resume.md                      # 📝 /resume 技能
│   └── job-hunt.md                    # 📝 /job-hunt 技能
├── templates/
│   ├── resume_template.html           # 📄 HTML 简历模板
│   └── job_templates.json             # 🔧 搜索条件模板
└── examples/
    └── profile_template.md            # 👤 用户技能档案模板
```

---

## 📊 Excel 结构（job-hunt 生成）

| 列 | 表头 | 阶段 | 说明 |
|:--:|------|------|------|
| A | 公司 | search | 公司名称 |
| B | 岗位 | search | 岗位名称 |
| C | Base | search | 工作城市 |
| D | 链接 | search | Boss直聘岗位链接（超链接） |
| E | 感兴趣? | 👤 用户勾选 | 打勾 → 生成自我介绍 |
| F | 自我介绍 | apply | 100-150 字匹配话术 |
| G | 需新简历? | 👤 用户勾选 | 打勾 → 生成定制简历 |
| H | 业务模块 | apply | 职业技能关键词（可手动修改） |
| I | 修改后的工作经历 | apply | 3 段经历针对 JD 的修改版 |
| J | 简历路径 | apply | 生成的 PDF 路径 |

---

## 🎨 简历生成原理

```
resume_template.html（模板）
         │
         ▼  替换 <!-- WORK_EXPERIENCE --> 占位符
    定制 HTML（临时文件）
         │
         ▼  Chrome headless --print-to-pdf
    单页 A4 PDF（中文宋体/黑体排版）
```

- 模板排版：22pt 姓名居中 + 深蓝板块标题 + 宋体正文
- 工作经历：只改表述和顺序，保留所有量化数据
- ATS 友好：使用 JD 原文关键词

---

## ⚠️ 注意事项

- 🔐 **首次搜索需要登录** — 第一次运行 `search` 前，在浏览器中登录 Boss直聘
- ✅ **真实性优先** — 所有简历内容基于真实经历，不编造
- 📏 **单页控制** — 简历内容控制在一页 A4 以内
- 🌐 **中文支持** — HTML 模板使用 PingFang SC / Songti SC 系统字体

---

## 🛠 技术栈

- **Claude Code Skill** — 工作流编排
- **browser-act** — Boss直聘页面自动化
- **xlsx skill** — Excel 读写
- **Chrome headless** — HTML → PDF 渲染
- **HTML/CSS** — 简历模板排版

---

## 📄 License

MIT
