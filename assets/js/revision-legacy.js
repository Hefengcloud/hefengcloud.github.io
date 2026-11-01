'use strict';
(() => {
 const query=new URLSearchParams(location.search),category=query.get('category')||'',base=document.body.dataset.base||'';
 let path='/revision/mid/';
 if(query.get('group')==='oral'||category.startsWith('口语'))path='/revision/mid/oral/';
 else if(['期中能力自查','PEP · 复习要求','语法专项'].includes(category))path='/revision/mid/guide/';
 else if(category==='背诵与 Passage')path='/revision/mid/written/mid-1/';
 else if(category==='阅读理解')path='/revision/mid/written/';
 else if(category||query.get('track')==='pep')path='/revision/mid/written/mid-2/';
 query.delete('group');const suffix=query.toString();location.replace(base+path+(suffix?'?'+suffix:'')+location.hash);
})();
