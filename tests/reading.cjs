const {chromium}=require(process.env.PLAYWRIGHT_PATH||'playwright');
const assert=require('node:assert/strict');
(async()=>{
 const browser=await chromium.launch({headless:true});
 try{
 const root=process.env.SITE_URL||'http://127.0.0.1:4100';
 const context=await browser.newContext({permissions:['clipboard-read','clipboard-write']});const page=await context.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(root+'/reading/');assert.equal(await page.locator('.reading-link').count(),8);assert.equal(await page.locator('textarea,.reading-body').count(),0);
 const links=await page.locator('.reading-link').evaluateAll(nodes=>nodes.map(n=>n.href));
 for(const link of links){await page.goto(link);assert.equal(await page.locator('.reading-body').count(),1);assert((await page.locator('.reading-body').textContent()).length>500);assert((await page.title()).includes(await page.locator('#app h1').textContent()));}
 await page.goto(links[0]);await page.fill('#reading-answer','My private answer.');await page.click('[data-done]');await page.reload();assert.equal(await page.inputValue('#reading-answer'),'My private answer.');assert.equal(await page.locator('[data-done]').getAttribute('aria-pressed'),'true');
 await page.click('#share-reading');assert.equal(await page.evaluate(()=>navigator.clipboard.readText()),links[0]);
 await page.locator('.reading-back').click();assert((await page.locator('[data-reading-status="reading-0"]').textContent()).includes('已完成'));
 await page.goto(links[1]);assert.equal(await page.inputValue('#reading-answer'),'');
 const visitor=await browser.newContext();const shared=await visitor.newPage();await shared.goto(links[0]);assert.equal(await shared.inputValue('#reading-answer'),'');
 await page.goto(links[0]);await page.evaluate(()=>Object.defineProperty(navigator,'clipboard',{value:{writeText:()=>Promise.reject(new Error('denied'))},configurable:true}));await page.click('#share-reading');await page.waitForSelector('#share-link:visible');assert.equal(await page.inputValue('#share-link'),links[0]);
 await page.setViewportSize({width:390,height:844});for(const link of [root+'/reading/',links[0]]){await page.goto(link);assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));}
 const noJS=await browser.newContext({javaScriptEnabled:false});const staticPage=await noJS.newPage();await staticPage.goto(links[0]);assert((await staticPage.locator('.reading-body').textContent()).includes('Jack'));
 assert.deepEqual(errors,[]);console.log('PASS: 8 direct routes, reading list, static content, share copy/fallback, private drafts, completion, mobile.');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
