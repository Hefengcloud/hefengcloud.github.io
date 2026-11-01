"""Import G4S1 sources; requires pypdf and ffmpeg/ffprobe. No network required."""
from pathlib import Path
import argparse, hashlib, json, shutil, subprocess, zipfile, xml.etree.ElementTree as ET
from collections import Counter
from pypdf import PdfReader
from content_tracks import track_for
parser=argparse.ArgumentParser();parser.add_argument('source',type=Path);parser.add_argument('english',type=Path);args=parser.parse_args()
ROOT=Path(__file__).resolve().parents[1]; dest=ROOT/'assets/learning';dest.mkdir(parents=True,exist_ok=True)
def save(name,data): (dest/name).write_text(json.dumps(data,ensure_ascii=False,indent=2))
stories=json.loads((args.english/'data/kids_stories/grade_4_term_1.json').read_text())['stories']; bysha={s['source_sha256']:s for s in stories}
joy=json.loads((args.english/'data/joy_books/grade_4_term_1.json').read_text())
overrides_path=dest/'document-overrides.json'
overrides=json.loads(overrides_path.read_text()) if overrides_path.exists() else {}
items=[]; seen={}; manifest=[]
for p in sorted(args.source.rglob('*')):
 if not p.is_file():continue
 rel=str(p.relative_to(args.source))
 if p.name.startswith('.'):manifest.append({'source':rel,'status':'ignored metadata'});continue
 sha=hashlib.sha256(p.read_bytes()).hexdigest()
 if sha in seen:
  seen[sha]['sources'].append(rel);manifest.append({'source':rel,'id':seen[sha]['id'],'status':'duplicate'});continue
 ext=p.suffix.lower(); ident=sha[:16]; target=dest/(ident+('.mp3' if ext=='.wma' else ext))
 item={'id':ident,'title':p.stem,'sources':[rel],'sha256':sha,'url':'/assets/learning/'+target.name,'kind':'audio' if ext in ('.mp3','.wma') else 'document','category':'resources'}
 if ext=='.wma':
  if not target.exists():subprocess.run(['ffmpeg','-v','error','-y','-i',str(p),'-codec:a','libmp3lame','-q:a','4',str(target)],check=True)
 else:shutil.copyfile(p,target)
 if item['kind']=='audio':
  item['duration']=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(target)]))
  if sha in bysha:
   s=bysha[sha];item.update(title=s['title'],category='stories',text=s['content'],segments=[{'text':x['text'],'start':x['start_time'],'end':x['end_time']} for x in s['alignments']],order=s['sort_index'])
  elif sha==joy['source_sha256']:item.update(title='The Wind and the Sun',category='dialogues',text=joy['books'][0]['content'])
  elif 'aunt picky' in rel.lower():item.update(title='Aunt Picky',category='chants',text='''Aunt Picky wants a pumpkin.
“Oh, which one will I buy?
The big one? The small one?
The fat one? The tall one?
I just can’t decide!”
“Is this one as good as that one?
It’s better than the fat one.
It’s bigger than the next one.
Oh, which one is the best one?!”
She looks and thinks… And thinks and looks…
And there in front of her eyes,
She sees the best of all the pumpkins
To put into her pie!
“Look, lady, which one do you want?”
Asks the pumpkin man.
“I need to go home as soon as I can.”
Aunt Picky frowns and cries a lot.
“I’m sorry,” she says, “but I forgot.”''')
  elif 'chant' in rel.lower():item['category']='chants'
  elif 'talk' in rel.lower() or 'dialogue' in rel.lower():item['category']='dialogues'
  elif 'spell' in rel.lower():item['category']='phonics'
  elif 'learn' in rel.lower():item['category']='words'
  elif 'read' in rel.lower():item['category']='reading'
  elif 'revision' in rel.lower() or 'review' in rel.lower():item['category']='revision'
  item['series']='Our World 练习册' if 'OW 练习册' in rel else 'Our World' if '/OW/' in rel else 'PEP' if '/PEP/' in rel else '英语作业本' if '作业本' in rel else 'KIDS’ STORIES' if "KIDS' STORIES" in rel else '背诵内容'
 elif ext=='.pdf':
  pdf=PdfReader(p); item['pages']=len(pdf.pages);item['text']='\n\n'.join(x.extract_text() or '' for x in pdf.pages)
 elif ext=='.docx':
  with zipfile.ZipFile(p) as z:
   tree=ET.fromstring(z.read('word/document.xml')); ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
   item['text']='\n'.join(''.join(t.text or '' for t in para.findall('.//w:t',ns)) for para in tree.findall('.//w:p',ns))
 elif ext=='.png': item['text']='Aunt Picky 歌谣教材照片；文字已整理至歌谣页面。'
 if sha in overrides: item.update(overrides[sha])
 seen[sha]=item;items.append(item);manifest.append({'source':rel,'id':ident,'status':'imported'})
for item in items: item['track']=track_for(item)
save('catalog.json',items);save('manifest.json',manifest)
report=['# G4S1 内容分析','',f'共 {len(manifest)} 个文件；有效文件 {sum(x["status"]!="ignored metadata" for x in manifest)} 个；去重后 {len(items)} 项。',str(Counter(x['status'] for x in manifest)),str(Counter(x['category'] for x in items)),'','## 知识分类','- W2：人物外貌、性格、is/has、频率副词、第三人称单数。','- W2 同名 (1) 文件与 W3 作业：现在进行时表示未来安排、否定句、特殊疑问句。','- W4：职业、like / be good at / prefer、家人职业介绍。','- W6：人物、计划与职业综合复习。','- W7/W8：社区地点、方位介词、there is/are、问路指路。','- Mid 1：风与太阳对话、Aunt Picky、室内农场短文。','- Mid 2：PEP U1–3、Our World U1–2、故事 S3–5；比较级、家务、种植、频率、口语话题。','- Mid 3：8 篇阅读，家庭劳动、友谊、社区、菜园、遗传特征、消防员、助老、情绪。','- PEP U3 PDF：社区、ck 拼读、阅读与项目任务。','- Notetaking：记录词汇、语法、发音、例句，强调、分类、解释用途。','- IMG_5757.PNG：Aunt Picky 清晰歌词照片，作为歌谣文字依据。','- PEP U1–6、作业本 U1–6/Review/Revision、OW 学生用书和练习册：全部音频入库，按文件可识别知识类别分类。仅编号 OW 音轨保留编号，不推测标题。','','## 学习分区','- PEP 教材、PEP PDF 与配套英语作业本进入独立 PEP 基础专区；主线列表、推荐和统计排除这些资料。','- Mid 2 含 PEP 与 Our World/故事综合内容，原件仅在 PEP 专区的综合资料栏保留，主线知识卡继续使用其中的进阶知识。','- ck 拼读卡与练习移入基础专区；保留原有学习记录。','','## 质量与来源','- 13 篇故事按源文件 SHA-256 匹配 LMS 转写及时间轴，WMA 转 MP3 供浏览器播放。转写为机器生成，可能存在识别误差。','- 风与太阳按 SHA-256 匹配 LMS 对话文字；歌谣按照片和 Mid 1 整理。无已核对时间轴时提供手动 A–B 跟读。','- 重复录音按 SHA-256 合并，catalog 保留全部源路径；macOS ._* 元数据忽略并记录。','- W2 文件混入 Grade 5 足球拓展页，保留原件但不当作四上核心知识。W3/W4/W7 作业内部周次与文件名不一致，按主题归类。','- 原文练习与参考答案保留；网站新增练习标为本站练习。个人进度、错题与笔记仅保存在当前浏览器。','- LMS 参考：词汇熟练度、语法/表达分类、故事时间轴、拼读练习、错题和复习；静态站不需要 Django 服务。','','## 全量文件清单','']
report += [f'- [{x["status"]}] {x["source"]}'+(f' → {x["id"]}' if 'id' in x else '') for x in manifest]
(ROOT/'docs/content-analysis.md').write_text('\n'.join(report));print('\n'.join(report[:6]))
