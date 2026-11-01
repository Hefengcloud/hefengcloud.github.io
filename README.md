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
