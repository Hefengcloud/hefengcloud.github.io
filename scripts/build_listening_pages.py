"""Generate shareable main-course story/chant/dialogue routes from the imported catalog."""
from pathlib import Path
import json,re
root=Path(__file__).resolve().parents[1]
items=[x for x in json.loads((root/'assets/learning/catalog.json').read_text()) if x['track']=='main' and x['category'] in ('stories','chants','dialogues')]
for item in items:
 item['slug']=re.sub('[^a-z0-9]+','-',item['title'].lower()).strip('-') or item['id']
 folder=root/'_pages'/item['category'];folder.mkdir(exist_ok=True)
 title=json.dumps(item['title'],ensure_ascii=False)
 (folder/(item['slug']+'.html')).write_text(f'---\nlayout: listening_detail\ntitle: {title}\ndescription: "听原音、调语速、选段跟读，录下自己的声音。"\npermalink: /{item["category"]}/{item["slug"]}/\nsection: {item["category"]}\naudio_id: {item["id"]}\n---\n')
(root/'_data/listening.json').write_text(json.dumps(items,ensure_ascii=False,indent=2))
print(f'Generated {len(items)} listening pages')
