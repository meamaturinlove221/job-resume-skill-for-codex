# Boss直聘求职助手

## 使用方法
- `/job-hunt search` — 搜索Boss直聘岗位，写入Excel
- `/job-hunt apply` — 根据用户勾选，生成自我介绍和简历

## 项目路径
- **项目根目录**: `~/Desktop/job-search/`
- **搜索模板**: Excel Sheet2（岗位模版）或 `~/Desktop/job-search/job_templates.json`
- **Excel输出**: `~/Desktop/job-search/jobs_YYYY-MM-DD.xlsx`
- **简历模板**: `~/Desktop/job-search/resume_template.html`
- **简历输出**: `~/Desktop/job-search/resumes/`
- **用户档案**: `~/.claude/projects/-YOUR_PATH/memory/user_profile.md`

## 用户信息

**姓名**：{{YOUR_NAME}}
**邮箱**：{{YOUR_EMAIL}}
**电话**：{{YOUR_PHONE}}

---

## 子命令：search

### 前置条件
- 确认 browser-act 可用
- 确认用户已登录 Boss直聘（zhipin.com），如未登录提示用户先在浏览器中登录

### 执行步骤

**Step 1: 读取搜索模板**
- 优先从 Excel 模板的 Sheet2（"岗位模版"）读取：`~/Desktop/job-search/jobs_template.xlsx`
- Sheet2 列：城市(A)、岗位名称(B)、薪资待遇(C)、公司规模(D)、公司行业(E)
- 同时同步更新 `job_templates.json` 作为备份
- 展示所有模板名称列表（如"杭州-内容运营"），让用户选择（可多选）
- 也支持用户直接手动输入搜索条件（城市、关键词、薪资、规模、行业）
- 经验要求：默认覆盖 1-3年 和 3-5年（都会搜索，不限制）

**Step 2: browser-act 抓取岗位**
对每个选中的模板，使用 browser-act 执行以下操作：

1. 打开 Boss直聘搜索页面：`https://www.zhipin.com/web/geek/job?query={keywords}&city={city_code}&experience={exp_code}`
2. 如果页面提示登录，暂停并通知用户先登录
3. 在搜索结果页面：
   - 设置筛选条件：经验要求、薪资范围、公司规模、公司行业
   - 通过页面上的筛选下拉菜单设置公司规模和公司行业
   - 按推荐排序
   - 滚动页面加载更多结果
   - 提取每个岗位卡片的信息：
     - 公司名称
     - 岗位名称
     - 工作城市（Base地）
     - 岗位链接（href）
4. 对每个岗位：
   - 点击进入岗位详情页
   - 提取完整 JD 内容（岗位职责 + 任职要求）
   - 记录 JD 全文到内存缓存（以岗位链接为 key）
5. 返回搜索结果列表继续提取下一个

**Boss直聘城市代码参考：**
- 上海: 101020100
- 北京: 101010100
- 深圳: 101280600
- 广州: 101280100
- 杭州: 101210100
- 成都: 101270100

**经验代码参考：**
- 1-3年: 104
- 3-5年: 105
- 5-10年: 106

**公司规模代码参考：**
- 0-20人: 0
- 20-99人: 1
- 100-499人: 2
- 500-999人: 3
- 1000-9999人: 4
- 10000人以上: 5

**公司行业参考：**
- 通过页面筛选菜单选择，常见：互联网、电子商务、游戏等

**Step 3: 去重**
- 按岗位链接去重
- 去除已存在于之前 Excel 中的岗位（检查最近7天的Excel文件）

**Step 4: 写入 Excel**
使用 `/xlsx` skill 创建 Excel 文件：
- 文件名：`~/Desktop/job-search/jobs_YYYY-MM-DD.xlsx`（YYYY-MM-DD 为当天日期）
- 表头：
  - A1: 公司
  - B1: 岗位
  - C1: Base
  - D1: 链接
  - E1: 感兴趣?
  - F1: 自我介绍
  - G1: 需新简历?
  - H1: 业务模块（个人介绍中的职业技能关键词）
  - I1: 修改后的工作经历
  - J1: 简历路径
- 填入 A-D 列数据
- E列和G列留空（供用户打勾）
- D列设置超链接格式
- E列和G列设置数据验证（下拉：Y / 空）
- 适当调整列宽：A=15, B=20, C=8, D=35, E=8, F=40, G=8, H=30, I=50, J=30

**Step 5: JD缓存**
- 将所有岗位的 JD 全文缓存到一个临时文件：`~/Desktop/job-search/.jd_cache_YYYY-MM-DD.json`
- 格式：`{"岗位链接": "JD全文", ...}`
- 此文件对用户不可见（点开头），apply 阶段读取

**Step 6: 通知用户**
- 告知用户抓取了多少个岗位
- 提示打开 Excel 文件勾选：
  - E列（感兴趣?）打勾的岗位会生成自我介绍
  - G列（需新简历?）打勾的岗位会生成定制简历
- 告知用户勾选完成后运行 `/job-hunt apply`

---

## 子命令：apply

### 前置条件
- 当天的 Excel 文件存在且用户已勾选
- JD缓存文件存在

### 执行步骤

**Step 1: 读取 Excel 和 JD缓存**
- 读取当天 Excel：`~/Desktop/job-search/jobs_YYYY-MM-DD.xlsx`
- 读取 JD缓存：`~/Desktop/job-search/.jd_cache_YYYY-MM-DD.json`
- 识别 E列（感兴趣?）有值的行
- 识别 G列（需新简历?）有值的行
- 如无勾选行，提示用户先勾选并保存 Excel

**Step 2: 读取用户技能档案**
- 读取 `~/.claude/projects/-YOUR_PATH/memory/user_profile.md` 获取完整技能信息

**Step 3: 生成自我介绍（对每个感兴趣的岗位）**
对 E列有值的每个岗位：
1. 从 JD 缓存读取该岗位的 JD 全文
2. 分析 JD 核心要求，提取关键匹配点
3. 生成 100-150字自我介绍：
   - 第1句：你是谁+核心背景
   - 第2-3句：与JD最匹配的2-3个经历/能力（引用具体数据）
   - 第4句：表达兴趣+期待沟通
4. 自然口语化，不堆砌关键词
5. 语气：专业但亲和，适合Boss直聘打招呼场景
6. 将自我介绍写入对应行的 F列

**Step 4: 生成业务模块 + 修改工作经历 + 生成简历（对每个需新简历的岗位）**
对 G列有值的每个岗位：
1. 从 JD 缓存读取该岗位的 JD 全文
2. 根据 JD 生成个人介绍中的业务模块关键词（如"内容运营/创作者生态/整合营销/AI工具"），写入 H列
   - 从JD提取核心业务方向，用"/"分隔
3. 基于 JD 重写工作经历：
   - 只改表述顺序和措辞，不编造经历
   - 优先排列与JD最匹配的 bullet point
   - 使用JD中的关键词（ATS优化）
   - 保留所有量化数据
   - 每段4-6个bullet point
4. 将修改后的工作经历写入 I列
5. 生成简历 PDF：
   a. 读取 `~/Desktop/job-search/resume_template.html`
   b. 将 H列的业务模块替换 `<!-- BUSINESS_MODULES -->` 占位符
   c. 将修改后的工作经历替换 `<!-- WORK_EXPERIENCE -->` 占位符
   d. 将替换后的 HTML 写入临时文件
   e. 用 Chrome headless 生成 PDF：
      ```bash
      "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
        --headless --disable-gpu --no-pdf-header-footer \
        --print-to-pdf="$HOME/Desktop/job-search/resumes/YYYY-MM-DD_公司_岗位.pdf" \
        "/tmp/resume_公司_岗位.html"
      ```
   f. 命名格式：`YYYY-MM-DD_公司_岗位.pdf`（公司和岗位去除特殊字符）
6. 将 PDF 路径写入 J列

**工作经历 HTML 替换格式：**
每个工作经历条目替换为以下 HTML 结构：

```html
<div class="work-item">
  <div class="work-row">
    <span class="work-company">公司名 - 岗位名</span>
    <span class="work-date">时间段</span>
  </div>
  <ul class="work-bullets">
    <li>bullet point 1</li>
    <li>bullet point 2</li>
    ...
  </ul>
</div>
```

**Step 5: 保存 Excel**
- 使用 xlsx skill 保存更新后的 Excel
- 告知用户完成情况：
  - 生成了 X 份自我介绍
  - 生成了 Y 份简历
  - 简历保存在 `~/Desktop/job-search/resumes/`

**Step 6: 清理**
- 删除 JD 缓存文件和临时 HTML 文件

---

## 注意事项

1. **真实性**：所有简历内容必须基于真实经历，不编造
2. **数据保留**：修改工作经历时保留所有量化数据
3. **ATS优化**：使用JD中的原文关键词
4. **中文支持**：HTML模板使用系统字体（PingFang SC / Songti SC），确保中文正常渲染
5. **单页控制**：简历内容控制在一页A4以内
6. **浏览器登录**：首次 search 需要用户在浏览器中登录Boss直聘
