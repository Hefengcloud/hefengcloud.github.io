const { chromium } = require(process.env.PLAYWRIGHT_PATH || 'playwright');
const assert=require('node:assert/strict');
(async()=>{
 const browser=await chromium.launch({headless:true,args:['--use-fake-ui-for-media-stream','--use-fake-device-for-media-stream']});
 const context=await browser.newContext({viewport:{width:1440,height:1100},permissions:['microphone']});
 const page=await context.newPage(); page.setDefaultTimeout(15000); const errors=[];page.on('pageerror',e=>errors.push(e.message));
 const root=process.env.SITE_URL||'http://127.0.0.1:4100';
 for(const section of ['','words/','grammar/','pep/','expressions/','stories/','chants/','dialogues/','reading/','revision/','resources/','notebook/']){
  await page.goto(root+'/'+section);await page.waitForSelector('#app h1');assert(!await page.getByText('学习资料暂时没有加载成功').count());assert.equal(await page.locator('nav a').count(),12);
 }
 const catalog=await (await context.request.get(root+'/assets/learning/catalog.json')).json();
 const pepIds=catalog.filter(x=>x.track!=='main').map(x=>x.id);
 for(const route of ['words','grammar','chants','dialogues','reading','revision','resources']){
  await page.goto(root+'/'+route+'/');await page.waitForSelector('#app h1');
  const ids=await page.locator('[data-play],[data-doc]').evaluateAll(nodes=>nodes.map(n=>n.dataset.play||n.dataset.doc));
  assert(!ids.some(id=>pepIds.includes(id)),route+' mixes PEP resources');
 }
 await page.goto(root+'/pep/');await page.waitForSelector('#media-list .resource-row');
 assert.equal(await page.locator('#media-list .resource-row').count(),110);
 await page.selectOption('#series','英语作业本');await page.selectOption('#unit','3');
 assert(await page.locator('#media-list .resource-row').count()>0);
 assert((await page.locator('#media-list').textContent()).includes('Unit 3'));
 await page.locator('#media-list [data-play]').first().click();await page.waitForFunction(()=>document.querySelector('#audio').readyState>=1);
 await page.click('#complete-audio');await page.click('#close-player');
 await page.goto(root);await page.waitForSelector('.hero');
 assert.equal(await page.locator('.stats strong').first().textContent(),'0');
 assert(!pepIds.includes(await page.locator('.hero [data-play]').getAttribute('data-play')));
 await page.goto(root+'/phonics/');assert(await page.locator('a.button[href$="/pep/"]').count());
 await page.goto(root);await page.waitForSelector('.hero');await page.screenshot({path:'/tmp/hefeng-english-desktop.png',fullPage:true});
 console.log('routes passed; testing story');await page.goto(root+'/stories/');await page.locator('[data-play]').first().click();await page.waitForFunction(()=>document.querySelector('#audio').readyState>=1);assert(await page.locator('.sentence').count()>5);
 await page.locator('.sentence').nth(1).click();await page.waitForTimeout(300);assert(await page.locator('#audio').evaluate(a=>!a.paused));
 await page.selectOption('#speed','0.8');assert.equal(await page.locator('#audio').evaluate(a=>a.playbackRate),.8);
 console.log('play and speed passed; testing shadow');await page.selectOption('#mode','shadow');await page.fill('#point-a','1');await page.fill('#point-b','1.6');await page.click('#play-range');await page.waitForFunction(()=>document.querySelector('#player-status').textContent.includes('轮到你')).catch(async e=>{console.log(await page.evaluate(()=>({status:document.querySelector('#player-status').textContent,paused:document.querySelector('#audio').paused,time:document.querySelector('#audio').currentTime,ready:document.querySelector('#audio').readyState,network:document.querySelector('#audio').networkState,seeking:document.querySelector('#audio').seeking,error:document.querySelector('#audio').error})));throw e});await page.waitForFunction(()=>document.querySelector('#player-status').textContent.includes('接着跟读'));
 await page.click('#stop-range');await page.waitForTimeout(1200);assert(await page.locator('#audio').evaluate(a=>a.paused));
 await page.selectOption('#mode','loop');await page.click('#play-range');await page.waitForFunction(()=>document.querySelector('#player-status').textContent.includes('准备重复'));await page.click('#stop-range');
 await page.fill('#point-b','0');await page.click('#play-range');assert((await page.locator('#player-status').textContent()).includes('有效区间'));
 console.log('record test');await page.click('#record');await page.waitForFunction(()=>document.querySelector('#record').textContent.includes('停止录音'));await page.waitForTimeout(600);await page.click('#record');await page.waitForSelector('#recording:not([hidden])');assert((await page.locator('#recording').getAttribute('src')).startsWith('blob:'));
 await page.click('#complete-audio');await page.keyboard.press('Escape');assert(!await page.locator('#player-dialog').evaluate(d=>d.open));assert(await page.locator('#audio').evaluate(a=>a.paused));
 for(const path of ['chants','dialogues']){console.log('Testing',path);await page.goto(root+'/'+path+'/');await page.locator('[data-play]').first().click();await page.waitForFunction(()=>document.querySelector('#audio').readyState>=1);await page.selectOption('#mode','shadow');await page.fill('#point-a','0');await page.fill('#point-b','0.5');await page.click('#play-range');await page.waitForFunction(()=>document.querySelector('#player-status').textContent.includes('轮到你')).catch(async e=>{console.log(await page.evaluate(()=>({status:document.querySelector('#player-status').textContent,paused:document.querySelector('#audio').paused,time:document.querySelector('#audio').currentTime,duration:document.querySelector('#audio').duration,error:document.querySelector('#audio').error})));throw e});await page.click('#close-player');}
 await page.goto(root+'/resources/');await page.fill('#search','Notetaking');assert.equal(await page.locator('.resource-row').count(),1);await page.click('[data-doc]');assert((await page.locator('.document-text').textContent()).includes('notes'));
 await page.goto(root+'/revision/');await page.locator('[data-choice="0"]').click();await page.reload();await page.click('#wrong-quiz');assert((await page.locator('#quiz h3').textContent()).includes('long hair'));await page.click('[data-choice="1"]');await page.click('#next');assert((await page.locator('#quiz').textContent()).includes('0 道'));
 await page.goto(root+'/words/');await page.locator('[data-done]').first().click();await page.reload();await page.waitForSelector('[data-done][aria-pressed="true"]');
 await page.goto(root+'/notebook/');await page.fill('textarea','Test note: helpful — She is helpful.');await page.reload();await page.waitForSelector('textarea');assert((await page.inputValue('textarea')).includes('Test note'));
 await page.setViewportSize({width:390,height:844});for(const section of ['','pep/','resources/','reading/','words/','stories/']){await page.goto(root+'/'+section);await page.waitForSelector('#app h1');assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),section+' overflow');}await page.goto(root);await page.waitForSelector('.hero');await page.screenshot({path:'/tmp/hefeng-english-mobile.png',fullPage:true});
 assert.deepEqual(errors,[]);console.log('PASS: 12 routes, responsive layouts, audio playback, speed, sentence seeking, A–B loop, shadow pause/resume, recording, cleanup, search, documents, quiz, persistence.');await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
