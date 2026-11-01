# 和风英语 · Little English Club

小学英语静态学习站，以 G4S1 为当前课程。保留 Jekyll / GitHub Pages 部署方式，无需 Django 或外部 API。

## 本地预览

```sh
bundle install
bundle exec jekyll serve --host 127.0.0.1 --port 4100
```

## 内容与来源

- 12 个页面：首页、词汇、语法、表达、故事、歌谣、对话、阅读、复习、资料库、PEP 基础专区、学习本。
- 348 个有效源文件按 SHA-256 去重，得到 287 项资料（268 段音频、19 份文档/图片）。10 个 macOS 元数据文件只记入清单。
- 完整分类、源文件清单和已知原文问题见 `docs/content-analysis.md`。
- `assets/learning/catalog.json` 保留原始文件路径和哈希；`manifest.json` 记录逐文件导入结果。
- 故事文字/时间轴来自指定 LMS 的四上数据，按源音频 SHA-256 匹配。机器转写可能有识别误差。原始 WMA 使用 ffmpeg 转为 MP3。
- 风与太阳使用 LMS 转写；Aunt Picky 文字根据教材照片整理。没有可靠时间轴的音频提供手动 A–B 选段，不伪造句子边界。
- 教学卡片、练习为根据材料整理的学习内容；原 PDF/DOCX 保留供核对图片和排版。阅读作答与口语任务不做自动判分。

## 跟读与学习记录

音频支持 0.6–1.2 倍速、逐句点读（有时间轴时）、A–B 循环、留白模仿、麦克风录音回放与下载。留白时长与选段播放时长一致，至少 1 秒。停止、关闭弹窗或离开页面会停止循环并释放麦克风。录音需 HTTPS/localhost 及浏览器授权；不支持时仍可播放与跟读。录音不上传，关闭弹窗会释放录音。

掌握状态、错题、阅读回答和笔记只存于当前浏览器 localStorage，没有账户同步或语音评分。

## 再次导入

需要 Python `pypdf` 及 `ffmpeg` / `ffprobe`：

```sh
python3 scripts/import_content.py /path/to/G4S1 /path/to/django_backend/english
```

课程卡片位于 `assets/learning/lessons.json`，练习位于 `quiz.json`。导入脚本不会覆盖这两个文件。

## 验证

```sh
bundle exec jekyll build
python3 scripts/check_site.py
# 安装 playwright 后，在本地预览服务运行时执行：
node tests/browser.cjs
```

可使用 `PLAYWRIGHT_PATH` 指向现有 playwright 模块，`SITE_URL` 指定其他预览地址。浏览器测试使用模拟麦克风，不录制真实声音。覆盖页面、响应式布局、音频、循环与留白、录音、关闭清理、搜索、原文、练习和本机保存。

推送 main 将触发现有 GitHub Pages 工作流；本次改版未自动提交或推送。

## PEP 分区

PEP 教材与配套作业本 110 项资料在 `/pep/` 单独学习，可按单元、教材和类型筛选。主线保留 176 项进阶资料。Mid 2 原件包含多教材内容，在基础专区的综合资料栏单独保存。主线不显示 PEP 音轨、拼读卡片或 ck 练习，也不计入 PEP 完成数；原有学习状态保留。旧 `/phonics/` 路径提供前往基础专区的入口。导入分类规则在 `scripts/content_tracks.py`，重新导入不会恢复混排。

## 独立分享页面

`/reading/` 展示阅读列表，单篇路径为 `/reading/<slug>/`。`/stories/`、`/dialogues/` 和 `/chants/` 的“听读”链接进入独立页面，页面内直接提供播放器、选段跟读、录音和复制分享链接。PEP 仍在基础专区。音频页由 `python3 scripts/build_listening_pages.py` 根据已导入目录生成。阅读、听读页面的专项浏览器验证分别为 `tests/reading.cjs`、`tests/listening.cjs`。

## 期中知识点汇编

新增 `G4S1英语期中知识点汇编.pdf` 后共有 288 项资料（268 段音频、20 份文档/图片）。扫描件已人工核对转录。`midterm.json` 保存复习路线：主线 14 项、PEP 5 项，自查状态仅保存在本机。语法、表达、词汇与 S3–S5 故事页已补充对应要求、复述和练笔入口；题库新增 8 道练习，旧题 ID 不变。原件与来源详情见 `docs/content-analysis.md`。

## 复习信息架构

```text
/revision/                         复习中心
├── mid/                           期中复习
│   ├── oral/                      口试：Oral test review questions（34 项）
│   │   └── <item-id>/             逐项练习
│   ├── written/                   笔试：Mid-Revision 1–5
│   │   ├── mid-1/<item-id>/        3 项背诵与 Passage
│   │   ├── mid-2/<item-id>/        173 项词汇、句型、话题与阅读
│   │   ├── mid-3/<item-id>/        8 篇阅读题
│   │   ├── mid-4/                 原件待补充
│   │   └── mid-5/                 原件待补充
│   └── guide/                     共用范围、能力自查与语法说明（27 项）
├── final/                         期末复习
│   ├── oral/                      期末口试资料待补充
│   └── written/                   期末笔试资料待补充
└── practice/                      本站补充练习与错题
```

侧栏只保留“复习中心”。口试和笔试按资料来源分开；Mid 2 中的说写题仍属于笔试资料册，不因题型名称挪到 Oral test review。PEP 基础作为各册/共用范围内的独立筛选，不与主线进度混合。当前 G4S1 目录只提供 Mid 1–3，不把知识点汇编冒充 Mid 4/5，也不复用期中题作为期末题。

数据与详情页由 `python3 scripts/build_mid_revision.py` 生成，当前结构位于 `_data/revision.json`。245 个稳定条目 ID 不变，保留 `hefeng-mid-revision-v1` 本机存储，旧回答与掌握状态继续可用；继续学习的记录按资料册、课程分组隔离。旧自查勾选也会迁入对应条目。旧 `/mid-revision/` 入口和全部详情链接跳转到对应新位置。

录音回放/下载、草稿、分享、状态筛选仍可使用。浏览器验证：`node tests/revision-architecture.cjs`（可设置 `PLAYWRIGHT_PATH` / `SITE_URL`）。
