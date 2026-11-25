import {test,expect} from '@playwright/test';
import {readFileSync} from 'node:fs';
const password=process.env.DEMO_PASSWORD||JSON.parse(readFileSync('.runtime/demo-credentials.json','utf8')).password;
test('same-origin exported UI hydrates under CSP, refresh cookie survives reload, private files stay inaccessible',async({page,context})=>{
 const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));const response=await page.goto('/');const csp=response!.headers()['content-security-policy'];expect(csp.split(';').find(d=>d.trim().startsWith('script-src'))).toContain('sha256-');expect(csp.split(';').find(d=>d.trim().startsWith('script-src'))).not.toContain('unsafe-inline');
 await page.getByLabel('Email address').fill('customer@fincore.test');await page.getByLabel('Password',{exact:true}).fill(password);await page.getByRole('button',{name:'Sign in securely'}).click();await expect(page.getByRole('button',{name:'Sign out'})).toBeVisible();
 const cookie=(await context.cookies()).find(c=>c.name==='fincore_refresh');expect(cookie?.httpOnly).toBe(true);expect(cookie?.secure).toBe(true);expect(cookie?.sameSite).toBe('Strict');await page.reload();await expect(page.getByRole('button',{name:'Sign out'})).toBeVisible();
 expect((await page.request.get('/.env')).status()).toBe(404);expect((await page.request.get('/services/financial-analytics/docs')).status()).toBe(404);expect(errors).toEqual([]);
});
test('hosted simulation funds a disposable customer, denies staff access and delivers to private Mailpit',async({page})=>{
 await page.goto('/');await page.getByRole('button',{name:'Create your account',exact:true}).click();await page.getByLabel('Full name').fill('Hosted Synthetic Browser');await page.getByLabel('Email address').fill('hosted-'+Date.now()+'@fincore.test');await page.getByLabel('Password',{exact:true}).fill('SyntheticHostedBrowser2026!');
 const pending=page.waitForResponse(r=>r.url().endsWith('/auth/register')&&r.request().method()==='POST');await page.getByRole('button',{name:'Create account',exact:true}).click();const registration=await pending;expect(registration.status()).toBe(201);const {accessToken}= (await registration.json()).data;
 await expect(page.getByText('Total available balance')).toBeVisible();expect((await page.request.get('/api/v1/admin/users',{headers:{Authorization:'Bearer '+accessToken}})).status()).toBe(403);
 await page.getByRole('button',{name:'Funding',exact:true}).click();await page.getByLabel('Amount (INR)').fill('12.00');await page.getByRole('button',{name:'Confirm',exact:true}).click();await expect(page.getByRole('status')).toContainText('successfully');
 await expect.poll(async()=>{const response=await page.request.get('/api/v1/notifications',{headers:{Authorization:'Bearer '+accessToken}});const records=(await response.json()).data;return records.some((r:any)=>r.deliveryStatus==='SENT');},{timeout:45000}).toBe(true);
 await page.getByRole('button',{name:'Overview',exact:true}).click();await expect(page.locator('.balance .amount')).toHaveText('₹12.00');await page.screenshot({path:process.env.FINCORE_HOSTED_SCREENSHOT||'evidence/hosted-demo-browser.png',fullPage:true});
});
