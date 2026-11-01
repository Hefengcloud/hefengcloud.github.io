const {chromium}=require(process.env.PLAYWRIGHT_PATH||'playwright');
const assert=require('node:assert/strict');
(async()=>{const browser=await chromium.launch({headless:true,args:['--use-fake-ui-for-media-stream','--use-fake-device-for-media-stream']});try{
 const root=process.env.SITE_URL||'http://127.0.0.1:4100';const context=await browser.newContext({permissions:['microphone','clipboard-read','clipboard-write']});const page=await context.newPage();page.setDefaultTimeout(15000);const errors=[];page.on('pageerror',e=>errors.push(e.message));
 for(const category of ['stories','dialogues','chants']){
  await page.goto(root+'/'+category+'/');const link=page.locator('[data-listening-link]').first();await link.waitFor();if(category==='stories')assert.equal(await page.locator('[data-listening-link]').count(),13);const href=await link.getAttribute('href');await link.click();await page.waitForURL(root+href);
  assert.equal(await page.locator('section.inline-player').count(),1);assert.equal(await page.locator('dialog').count(),0);
  await page.waitForFunction(()=>document.querySelector('#audio').readyState>=1);
  assert((await page.locator('#transcript').textContent()).length>100);
  if(category==='stories'){assert(await page.locator('.sentence').count()>5);await page.locator('.sentence').nth(1).click();await page.waitForFunction(()=>!document.querySelector('#audio').paused);await page.click('#stop-range');}
  await page.selectOption('#speed','0.8');assert.equal(await page.locator('#audio').evaluate(a=>a.playbackRate),.8);
  await page.selectOption('#mode','shadow');await page.fill('#point-a','0');await page.fill('#point-b','0.5');await page.click('#play-range');await page.waitForFunction(()=>document.querySelector('#player-status').textContent.includes('轮到你'));await page.click('#stop-range');
  await page.click('#record');await page.waitForFunction(()=>document.querySelector('#record').textContent.includes('停止录音'));await page.waitForTimeout(600);await page.click('#record');await page.waitForSelector('#recording:not([hidden])');
  await page.click('#complete-audio');await page.click('#share-reading');assert.equal(await page.evaluate(()=>navigator.clipboard.readText()),root+href);
  await page.reload();await page.waitForFunction(()=>document.querySelector('#audio').readyState>=1);assert((await page.locator('#complete-audio').textContent()).includes('已完成'));
  await page.setViewportSize({width:390,height:844});assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  await page.locator('.reading-back').click();await page.locator('[data-listening-link]').first().waitFor();assert((await page.locator('.resource-row').first().textContent()).includes('已完成'));
  const visitor=await browser.newContext();const shared=await visitor.newPage();await shared.goto(root+href);await shared.waitForFunction(()=>document.querySelector('#audio').readyState>=1);assert.equal(await shared.locator('#recording').isVisible(),false);await visitor.close();
 }
 assert.deepEqual(errors,[]);console.log('PASS: stories/dialogues/chants navigation, direct URLs, inline audio, shadow reading, recording, share, persistence, mobile.');
}finally{await browser.close();}})().catch(e=>{console.error(e);process.exit(1)});
