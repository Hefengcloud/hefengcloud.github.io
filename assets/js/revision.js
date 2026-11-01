'use strict';
(() => {
 const $=s=>document.querySelector(s),key='hefeng-mid-revision-v1',list=$('[data-review-list]'),detail=$('[data-review-detail]');
 let state={items:{},drafts:{},last:{}};
 try{const saved=JSON.parse(localStorage.getItem(key)||'{}');for(const k of ['items','drafts','last'])if(saved[k]&&typeof saved[k]==='object'&&!Array.isArray(saved[k]))state[k]=saved[k];}catch{}
 // Reuse stable item IDs and the original storage key so existing drafts remain available.
 try{const old=JSON.parse(localStorage.getItem('hefeng-english-v1')||'{}');for(const [id,checked] of Object.entries(old.reviewChecks||{})){if(checked&&!state.items['requirement-'+id])state.items['requirement-'+id]='mastered';}}catch{}
 function save(){try{localStorage.setItem(key,JSON.stringify(state));return true;}catch{return false;}}
 const labels={new:'未复习',learning:'需要再练',mastered:'已掌握'};
 const itemState=id=>labels[state.items[id]]?state.items[id]:'new';
 if(list){
  const entries=[...document.querySelectorAll('.review-entry')],track=$('#review-track'),category=$('#review-category'),status=$('#review-status'),search=$('#review-search');
  const query=new URLSearchParams(location.search);track.value=query.get('track')==='pep'&&[...track.options].some(o=>o.value==='pep')?'pep':'main';
  function categories(){category.replaceChildren(new Option('全部类别',''));[...new Set(entries.filter(e=>e.dataset.track===track.value).map(e=>e.dataset.category))].forEach(c=>category.add(new Option(c,c)));}
  categories();const requested=query.get('group')==='oral'?'oral':query.get('category');if([...category.options].some(o=>o.value===requested))category.value=requested;
  function render(){
   const pool=entries.filter(e=>e.dataset.track===track.value),mastered=pool.filter(e=>itemState(e.dataset.id)==='mastered').length,learning=pool.filter(e=>itemState(e.dataset.id)==='learning').length;
   $('#review-progress').textContent=`${track.value==='pep'?'PEP 基础':'主线'}：已掌握 ${mastered} / ${pool.length} 项 · 需要再练 ${learning} 项`;
   $('#review-progress-bar').max=pool.length;$('#review-progress-bar').value=mastered;
   let visible=[];for(const el of entries){const current=itemState(el.dataset.id),matches=el.dataset.track===track.value&&(!category.value||(category.value==='oral'?el.dataset.category.startsWith('口语'):el.dataset.category===category.value))&&(!status.value||(status.value==='pending'?current!=='mastered':current===status.value))&&el.textContent.toLowerCase().includes(search.value.trim().toLowerCase());el.hidden=!matches;if(matches)visible.push(el);el.querySelector('.review-entry-status').textContent=labels[current]+' →';}
   $('#review-results').textContent=`当前显示 ${visible.length} 项`;$('#review-empty').hidden=visible.length>0;
   const pending=visible.filter(e=>itemState(e.dataset.id)!=='mastered'),resume=pending.find(e=>e.dataset.id===(state.last[list.dataset.reviewScope+':'+track.value]||state.last[track.value]))||pending[0]||visible[0];
   $('#resume-review').hidden=!resume;if(resume){$('#resume-review').href=resume.href;$('#resume-review').textContent=pending.length?'继续逐项复习 →':'回顾已掌握内容 →';}
  }
  track.onchange=()=>{categories();render();};for(const el of [category,status,search])el.addEventListener('input',render);render();window.addEventListener('pageshow',event=>{if(event.persisted)location.reload();});
 }
 if(!detail)return;
 const id=detail.dataset.reviewDetail,track=detail.dataset.reviewTrack;state.last[detail.dataset.reviewScope+':'+track]=id;save();
 $('#review-draft').value=state.drafts[id]||'';$('#review-draft').oninput=e=>{state.drafts[id]=e.target.value;$('#review-draft-status').textContent=save()?'回答已保存到本机。':'无法保存，请复制回答自行保留。';};
 function mark(){document.querySelectorAll('[data-review-mark]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.reviewMark===itemState(id))));}
 document.querySelectorAll('[data-review-mark]').forEach(b=>b.onclick=()=>{state.items[id]=b.dataset.reviewMark;$('#review-mark-status').textContent=save()?'已记录：'+labels[b.dataset.reviewMark]:'无法保存掌握状态，请自行记录。';mark();});mark();
 $('[data-share-review]').onclick=async()=>{const link=location.origin+location.pathname;try{await navigator.clipboard.writeText(link);$('#review-share-status').textContent='链接已复制，不包含你的回答与录音。';}catch{const field=$('#review-share-url');field.hidden=false;field.value=link;field.focus();field.select();$('#review-share-status').textContent='请复制下面的链接。';}};
 let recorder=null,stream=null,recordURL=null,pending=false,session=0,active=true;
 function clear(){const audio=$('#review-recording');audio.pause();audio.removeAttribute('src');audio.hidden=true;$('#review-record-download').hidden=true;if(recordURL)URL.revokeObjectURL(recordURL);recordURL=null;}
 function stop(){if(recorder?.state==='recording')recorder.stop();if(stream)stream.getTracks().forEach(t=>t.stop());stream=null;$('#review-record').textContent='● 开始录音';}
 $('#review-record').onclick=async()=>{
  if(recorder?.state==='recording'){stop();return;}if(pending)return;
  if(!navigator.mediaDevices?.getUserMedia||!window.MediaRecorder){$('#review-record-status').textContent='此浏览器不支持录音，请使用支持录音的浏览器，并通过 HTTPS 或 localhost 打开。';return;}
  clear();pending=true;$('#review-record').disabled=true;const token=++session;
  try{const acquired=await navigator.mediaDevices.getUserMedia({audio:true});if(!active||token!==session){acquired.getTracks().forEach(t=>t.stop());return;}stream=acquired;const recording=new MediaRecorder(stream),chunks=[];recorder=recording;
   recording.ondataavailable=e=>{if(e.data.size)chunks.push(e.data);};recording.onstop=()=>{acquired.getTracks().forEach(t=>t.stop());if(!active||token!==session)return;recordURL=URL.createObjectURL(new Blob(chunks,{type:recording.mimeType}));$('#review-recording').src=recordURL;$('#review-recording').hidden=false;const link=$('#review-record-download');link.href=recordURL;link.download=id+(recording.mimeType.includes('mp4')?'.m4a':'.webm');link.hidden=false;$('#review-record-status').textContent='录音完成，可以回放或下载。';};recording.start();$('#review-record').textContent='■ 停止录音';$('#review-record-status').textContent='正在录音…';
  }catch{stop();$('#review-record-status').textContent='无法使用麦克风，请检查录音权限。仍可口述、填写答案并记录复习状态。';}
  finally{pending=false;$('#review-record').disabled=false;}
 };
 window.addEventListener('pagehide',()=>{active=false;session++;stop();clear();});window.addEventListener('pageshow',event=>{if(event.persisted)location.reload();});
})();
