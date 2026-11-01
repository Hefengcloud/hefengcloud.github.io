"""Build the complete mid-term review from the imported PDFs and curated source mappings."""
from pathlib import Path
import json,re
root=Path(__file__).resolve().parents[1]
catalog=json.loads((root/'assets/learning/catalog.json').read_text())
bytitle={x['title'].strip():x for x in catalog}
mid1=bytitle['Mid 1'];mid2=bytitle['Mid 2'];mid3=bytitle['Mid-3 Reading']
oral=next(x for x in catalog if 'oral review questions' in x['title'] and 'Suggested' not in x['title'])
answers=next(x for x in catalog if 'oral review questions' in x['title'] and 'Suggested' in x['title'])
summary=bytitle['G4S1英语期中知识点汇编']
items=[]
def add(id,title,category,prompt,answer='',source=mid2,track='main',note='',link='',map=False,answer_label='本站整理参考答案',check='先独立口述，再展开参考内容核对。'):
 assert not any(x['id']==id for x in items),id
 items.append(dict(id=id,title=title,category=category,track=track,prompt=prompt,answer=answer,source=source['title'],source_url=source['url'],answer_label=answer_label,note=note,link=link,map=map,check=check))
# Oral short answers a–q. Missing fields are filled only from the supplied suggested answers.
short=[
('How can you describe someone who everyone likes?','They are popular.'),
('How can you describe someone who is always happy to help people?','They are helpful.'),
('How can you describe someone who is intelligent?','They are clever.'),
('I work in a hospital and help doctors. What is my job?','You are a nurse.'),
('I am an engineer who designs buildings. What is my job?','You are an architect.'),
('I work in a hospital and am good at medicine. What is my job?','You are a doctor.'),
('I work in a hospital and am good at helping people. What is my job?','You are a nurse.'),
('I work in a school and play a lot of sport. What is my job?','You are a PE teacher.'),
('I like sport and I’m good with children. What job should I have?','You should be a PE teacher.'),
('I like painting and I am good at art. What is my job?','You should be an artist.')]
for i,(question,answer) in enumerate(short):
 letter=chr(97+i);add('oral-short-'+letter,'简答 '+letter.upper()+' · '+question,'口语 · 简答',question,answer,oral,note='原题此处留空；问题按配套参考答案补全。' if i in [6,7] else '',answer_label='配套参考答案（统一标点）')
places=[('bakery','Go up Forest Street and take the first right onto Second Avenue. Go past the café and the bakery is on your left.'),('square','Go up Forest Street and take the second right onto Main Street. Go past the Chinese restaurant and the square is on your right.'),('theatre','Go up Forest Street and take the second right onto Main Street. The theatre is on your left, opposite the Chinese restaurant.'),('police station','Go up Forest Street and take the second right onto Main Street. Go straight on, cross Pine Street and go past the park. The police station is on your left.'),('cinema','Go up Forest Street and take the first right onto Second Avenue. Go to the end of the road and turn left onto Pine Street. Take the first right and go along Oak Street. Go past the park and the cinema is on your right.'),('fire department','Go up Forest Street and take the second right onto Main Street. Go straight on and cross Pine Street. The fire department is on your left, opposite the park.'),('jewellery store','Go up Forest Street and take the second left onto Main Street. Go past the Italian restaurant and turn right onto Hill Avenue. Go up the road and the jewellery store is on your right.')]
for i,(place,answer) in enumerate(places):
 letter=chr(107+i);add('oral-map-'+letter,'指路 '+letter.upper()+' · '+place,'口语 · 看图指路',f'Look at the map. How can I get to the {place}?\n从红色 Start 出发，按顺序说出道路、转弯和目的地位置。',answer,oral,note=('原题目的地留空，按配套参考答案补全。' if i>=4 else '')+'地图来自题目 PDF 第 2 页。',map=True,answer_label='按配套答案整理（补齐冠词、统一表达）')
ask=[('teacher','Your teacher’s plan for the weekend.',['What are you doing at the weekend?','Are you coming to school at the weekend?','Where are you going at the weekend?']),('friend','Your friend’s plan for next week.',['What is Tommy doing next week?','Is Tommy coming to school next week?','How is Tommy coming to school next week?']),('family','Your family’s plan for the winter holiday.',['What are your family doing in the winter holiday?','When are you going to your hometown this winter holiday?','Why aren’t you visiting your grandparents in the winter holiday?'])]
for group,task,examples in ask:
 for i,example in enumerate(examples):add(f'oral-ask-{group}-{i+1}',f'主动提问 · {task} {chr(65+i)}','口语 · 主动提问',task+'\n用 be + verb-ing + time 提出一个问题。本组练习尝试不同问法。',example,oral,answer_label='配套答案示例（答案不唯一）',check='句子有问号；be 动词与主语一致；时间与题目一致。')
jobs=[('I like working with children and I’m good at sport. What job can I have?','You can be a PE teacher.','原题 a 与参考答案 a 的场景不同：这里保留原题，答案按原题整理。参考答案另举 animals + sport → polo player。'),('I like painting and I’m good at working hard. What job can I have?','You can be a painter and decorator.','原题 b 留空；按参考答案补全。参考答案 pointer and decorator 更正为 painter and decorator。'),('I like working with children and I’m good with numbers. What job can I have?','You can be a maths teacher.','原题 c 留空；按参考答案补全。'),('I like dinosaurs and I’m good at science. What job can I have?','You can be a palaeontologist.','原题 d 留空；按参考答案补全。'),('I like computer games and I’m good at design. What job can I have?','You can be a computer games designer.','原题 e 留空；按参考答案补全。')]
for i,(q,a,note) in enumerate(jobs):add(f'oral-ask-job-{i+1}','职业问答 '+chr(65+i),'口语 · 主动提问',q+'\n先用 I like… / I’m good at… 提问，再请同伴推荐职业。',a,oral,note=note,answer_label='按题目与配套答案整理的示例')
topics=[('classmates','What are you and your classmates doing next week? What aren’t you doing?',[
'I’m going to tell you about what my classmates and I are doing next week.','We are all students, so next week we are all coming to school and doing our homework every day.','On Monday, I am also going to dance class.','I often go to art class on Tuesday, but next week I am going on Wednesday.','My classmate Tommy isn’t going to art class on Wednesday.','He is going on Thursday because he doesn’t have time on Wednesday.','Another classmate, Judy, is taking part in a swimming competition on Friday.','She is very good at swimming.','These are the plans for my classmates and me next week.']),
('family','What are you and your family doing at the weekend? What aren’t you doing?',[
'Here are my family’s plans for this weekend.','I am finishing my homework on Saturday morning.','Then I’m going to the park with my brother.','My mum is going to her tennis class on Saturday morning.','My dad is cooking lunch for us.','On Sunday, we are all going to the museum together.','We aren’t going shopping on Sunday.','I want to see the dinosaurs there.','These are my family’s plans for this weekend.']),
('after-school','What are you and your friends doing after school? What aren’t you doing?',[
'Here are the plans for my friends and me after school.','We are all doing our homework.','We are not going to the park after school.','After I finish my homework, I’m having dinner.','Then I’m watching TV until I go to bed.','One of my friends, Sally, is going to her football club after school.','She plays football every week.','These are the plans for my friends and me after school.'])]
for slug,q,lines in topics:add('oral-topic-'+slug,'话题表达 · '+q,'口语 · 话题表达',q+'\n至少 8 句：开头 1 句 + 内容 6–8 句 + 结尾 1 句。包含要做和不做的事。','\n'.join(f'{i+1}. {s}' for i,s in enumerate(lines)),oral,note='根据配套参考答案整理：更正 me and… 的主语形式及 every day 拼写；家庭话题补充否定计划；课后话题结尾更正为朋友和课后的计划。可按真实情况改写。',answer_label='整理后的示范回答（不是原件逐字抄录）',check='切题；至少 8 句；有开头结尾；有肯定与否定计划；be + ing + 时间；语音语调自然。')
# Mid 1: all three recitation texts, including the previously missing farm passage.
for slug,title,begin,end,link in [('wind-sun','The Wind and the Sun','Dialogue\n','\nChant','/dialogues/the-wind-and-the-sun/'),('aunt-picky','Aunt Picky','Chant\n','\nPassage','/chants/aunt-picky/'),('indoor-farm','On this farm… · 室内农场','Passage\n',None,'')]:
 text=mid1['text'].split(begin,1)[1];text=text.split(end,1)[0] if end else text
 if slug=='indoor-farm':answer='1. What do farmers grow? They grow lettuce.\n2. How high can the shelves be? Up to 15 levels high.\n3. What helps the lettuce grow faster? Special LED lights.\n4. What is another advantage? Indoor farms use much less water than outdoor farms.'
 else:answer='先逐句读准，再注意重音、比较级和人物语气；最后遮住原文尝试背诵。'
 add('recite-'+slug,'背诵 · '+title,'背诵与 Passage',text.strip(),answer,mid1,link=link,note='Mid 1 的 Aunt Picky 印为 better(bigger)，跟读页按教材照片使用 better。' if slug=='aunt-picky' else '',answer_label='本站练习与核对提示',check='读准每一句；理解意思；遮住原文复述或背诵。')
# Complete spelling and recognition lists: each word/phrase is independently reviewable.
pep='farmer|nurse|doctor|office worker|teacher|police officer|factory worker|look after|sweep the floor|cook together|tall and strong|short hair|kind|long hair|short and thin|quiet|read books|help me with Chinese|play games|play football|hospital|park|shop|bus stop|toilets|library|playground|gym|supermarket|go shopping|take a walk|do sports|see a doctor|museum|together|similarities|differences'.split('|')
compare='big-bigger|small-smaller|old-older|young-younger|tall-taller|short-shorter|fast-faster|slow-slower|strong-stronger|cute-cuter|smart-smarter|friendly-friendlier|ugly-uglier|much-more|good-better|bad-worse|beautiful-more beautiful'.split('|')
ow='glasses|wavy hair|blond hair|straight hair|curly hair|pumpkin|lettuce|cucumber|cabbage|hot peppers|onion|eggplant|green beans|zucchini|tomato|dig|plant|water|weed|pick|three times a week|once a month|twice a month|every day|on Fridays|fresh food|relatives|different'.split('|')
read='special|get along|shell|share|his|her|lawn|mane|awoke|nap|shout|forget|repay|pitied|sobbed|sharp|sneered at|frightened|family traits|shape|inherit|combination|earlobes|attached|unattached|inherited|fold|thumb|live with|England|get up|make breakfast|take me to school|pasta sauce|help me with math|go to the library/cinema|go to a concert|boring|think of|reason|important|hero-heroes|building|catch on fire|put out fires|be trapped in|burning|save people|accident|get sick|help people|drive a truck|siren|black|duck|helpful|job|chores|busy|tired|make a gift|clean the room|water the plants|feed the pet|community|do the dishes|neighbor|favourite'.split('|')
for category,words,track,prefix in [('PEP · 拼写词汇',pep,'pep','pep-spell'),('OW · 比较级',compare,'main','ow-compare'),('OW · 拼写词汇',ow,'main','ow-spell'),('认读词汇与短语',read,'main','read-word')]:
 for i,word in enumerate(words):
  iscomp=prefix=='ow-compare';spell=prefix!='read-word';prompt=('说出 '+word.split('-',1)[0]+' 的比较级，再用 than 造句。' if iscomp else f'请朗读“{word}”，说出它在课文中的意思，再造一句话。'+('然后遮住单词默写。' if spell else ''))
  add(f'{prefix}-{i+1:02}',word,category,prompt,word,track=track,answer_label='原资料词形 / 拼写',check='能读准、结合语境理解'+('、正确默写' if spell else '')+'，并在句子中运用。',note='原资料的连写 be trapped in burning 按词组 be trapped in 与单词 burning 分开练习。' if word in ['be trapped in','burning'] else '')
# All 15 language patterns.
patterns=[('Who is your best friend?','My best friend is John.'),('What’s your friend’s name?','His name is Zhang Peng.'),('What does he look like?','He is tall and thin.'),('What’s his personality?','He is kind.'),('What do you often do together?','We often read books together.'),('用比较级说一句关于你和朋友的话。','My best friend is bigger than I am.'),('Who is faster?','The girl is faster than the boy.'),('Which is smaller, the dog or the cat?','The cat is smaller than the dog.'),('How often do you have to water the garden?','I have to water the garden three times a week.'),('What do you have to do tonight?','I have to …'),('What does she/he have to do?','She/He has to …'),('What would you like for lunch?','I’d like a bowl of vegetable soup.'),('What would you like to do on weekends?','I’d like to play games on weekends.'),('What’s your father’s job?','He’s a factory worker.'),("What’s in the community?",'There is a … / There are …')]
for i,(q,a) in enumerate(patterns):add(f'pattern-{i+1:02}','句型 '+str(i+1)+' · '+q,'句型逐项练习',q,a,track='pep' if i in [0,1,2,3,4,13,14] else 'main',answer_label='Mid 2 原句型示例',note='这些朋友、职业、社区基础句型在 PEP 分组练习。' if i in [0,1,2,3,4,13,14] else '')
for i,(q,a) in enumerate([
('Introduce your friend from different aspects: name, appearance, hobbies and abilities.','I have a good/special friend.\nHe/She is …\nHe/She has …\nHe/She often …\nWe are friends because …'),
('Use comparatives to compare people around you.','… and I are different.\nI am … than …\nI have a … but …\nI inherited it from …'),
('Talk about your dream job. Give three reasons.','I want to be a/an … because …\nI like to do/doing …'),
('Talk about one of your special days: special events and how you felt.','开头：交代哪一天。\n内容：按顺序描述事件。\n结尾：表达感受。讲已发生的事件注意过去时。'),
('Introduce a story we learned this term, for example The Lion and the Mouse.','Today I want to tell you the story “…”\nAbout the story: …\nFrom the story, I learn “…”')]):
 add(f'mid2-topic-{i+1}','Topic '+str(i+1)+' · '+q,'话题说写',q,a,answer_label='原资料表达框架' if i!=3 else '本站补充表达框架',check='切题、有开头结尾；第三个话题需给出三个理由；根据内容选用正确时态。')
# Read-and-answer passage from Mid 2.
special=mid2['text'].split('A special school day',1)[1].strip()
add('reading-special-school-day','A Special School Day','阅读理解',special,'1. Nina went to the zoo.\n2. She sang songs with her friends on the school bus.\n3. She saw hippos, birds and a baby elephant.（至少说出两种。）',note='原文 when she got school 应为 when she got to school；正文按原件保留，朗读时使用完整表达。')
reading_answers=[
'1. He made breakfast, helped his mom clean the room and watered the plants.\n2. They cooked dinner together and made pasta with tomato sauce.\n3. He cleaned the room, watered the plants, did the dishes and fed his dog.（至少两项。）',
'1. Lily is tall and thin. She has long hair and big eyes.\n2. They often read books together and play games after school.\n3. Lily is friendlier and smarter; the writer is faster.（至少两点。）',
'1. They went to the park and the library.\n2. She read books about animals.\n3. There is a park, a library, a supermarket and a gym.（至少两处。）',
'1. They planted tomatoes, cucumbers and green beans.\n2. They water the garden three times a week.\n3. They picked tomatoes and lettuce.',
'示例：Who is taller, Mike or Amy? — Mike is taller.\nWho did Amy inherit her wavy hair from? — Her mother.\nCan Amy fold her tongue? — No, she can’t.',
'示例：Where does Uncle Ben work? — In the fire station.\nWhat do firefighters do? — They put out fires and save people.\nWhat did he teach at school? — How to be safe in a fire.',
'示例：Where did the students go? — To the old people’s home.\nWhat did the boys do? — They watered the flowers.\nHow did the students feel? — They were tired but happy.',
'示例：Why was Tom sleepy? — He went to bed late.\nWhere was his schoolbag? — Under the desk.\nWho helped Tom? — His friend Jack.']
for r,a in zip(json.loads((root/'_data/readings.json').read_text()),reading_answers):add('reading-'+r['slug'],r['title'],'阅读理解',r['text'],a,mid3,link='/reading/'+r['slug']+'/',answer_label='本站参考答案 / 提问示例（原件无答案）',check='先朗读与独立作答，再在文中找证据。后四篇要求自己提出三个问题。')
for i,moral in enumerate(['Little friends prove great friends.','A friend in need is a friend indeed.']):add(f'moral-{i+1}',moral,'故事寓意',moral+'\n结合 A Lion and a Mouse 解释这句话。','小小的朋友也能给予很大的帮助。朋友遇到困难时伸出援手，才体现真正的友谊。',link='/stories/a-lion-and-a-mouse/')
# All requirements from the newly supplied compilation (19 checks), linked to relevant practice.
requirements=json.loads((root/'assets/learning/midterm.json').read_text())
for track in ['main','pep']:
 for group in requirements[track]:
  for id,text,link in group['items']:add('requirement-'+id,text,'PEP · 复习要求' if track=='pep' else '期中能力自查',group['title']+'\n'+group['subtitle']+'\n'+text,'对照要求完成相关练习；能独立完成后再标记“已掌握”。',summary,track=track,link=link,answer_label='自查方法',check=text)
# All five synthesis requirements have explicit explanations on existing grammar pages.
lessons=json.loads((root/'assets/learning/lessons.json').read_text())
for l in lessons['grammar']:
 add('grammar-'+l[0],l[1],'语法专项',l[3]+'\n\n练习：'+l[5],l[4],summary,link='/grammar/',note='根据汇编要求整理的本站知识讲解和示例。',answer_label='本站示例与句型')
# Canonical architecture: revision -> period -> assessment -> source paper -> item.
for item in items:
 item['period']='mid'
 if item['source']==oral['title']:
  item['assessment']='oral';item['paper']='oral';item['list_url']='/revision/mid/oral/'
 elif item['source']==summary['title']:
  item['assessment']='guide';item['paper']='guide';item['list_url']='/revision/mid/guide/'
 else:
  item['assessment']='written';item['paper']={mid1['title']:'mid-1',mid2['title']:'mid-2',mid3['title']:'mid-3'}[item['source']]
  item['list_url']='/revision/mid/written/'+item['paper']+'/'
 item['url']=item['list_url']+item['id']+'/'
for item in items:
 peers=[x for x in items if x['list_url']==item['list_url'] and x['category']==item['category'] and x['track']==item['track']];index=peers.index(item)
 item['previous_url']=peers[index-1]['url'] if index else None;item['next_url']=peers[index+1]['url'] if index+1<len(peers) else None
 folder=root/'_pages/revision/items';folder.mkdir(parents=True,exist_ok=True)
 (folder/(item['id']+'.html')).write_text('---\nlayout: revision_detail\ntitle: '+json.dumps(item['title'],ensure_ascii=False)+'\nsection: revision\nreview_id: '+item['id']+'\npermalink: '+item['url']+'\n---\n')
 legacy=root/'_pages/mid-revision';legacy.mkdir(exist_ok=True)
 (legacy/(item['id']+'.html')).write_text('---\nlayout: revision_redirect\ntitle: 复习内容已迁移\npermalink: /mid-revision/'+item['id']+'/\nredirect_to: '+item['url']+'\nsitemap: false\n---\n')
papers=[]
for n in range(1,6):
 paper_id='mid-'+str(n);source={1:mid1,2:mid2,3:mid3}.get(n);selected=[x for x in items if x['paper']==paper_id]
 papers.append({'id':paper_id,'title':'Mid-Revision '+str(n),'description':{1:'Recitation · 对话、歌谣与 Passage',2:'词汇、比较级、句型、话题与阅读',3:'Reading and Answering · 八篇阅读理解'}.get(n,'资料待补充'),'available':source is not None,'url':'/revision/mid/written/'+paper_id+'/','source_url':source['url'] if source else None,'count':len(selected),'main_count':sum(x['track']=='main' for x in selected),'pep_count':sum(x['track']=='pep' for x in selected)})
data={'sources':[{'title':x['title'],'url':x['url']} for x in [mid1,mid2,mid3,oral,answers,summary]],'items':items,'papers':papers,'counts':{group:sum(x['assessment']==group for x in items) for group in ['oral','written','guide']}}
(root/'_data/revision.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print('Review items:',len(items),data['counts'])
