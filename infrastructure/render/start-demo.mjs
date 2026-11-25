import {spawn} from 'node:child_process';
import {createHash} from 'node:crypto';
const env={...process.env,NODE_ENV:'production',FASTAPI_SERVICE_URL:'http://127.0.0.1:8001',SMTP_HOST:'127.0.0.1',SMTP_PORT:'1025',SMTP_SECURE:'false',SMS_PROVIDER:'local',EMAIL_PROVIDER:'mailpit',WEB_ORIGIN:process.env.RENDER_EXTERNAL_URL||process.env.WEB_ORIGIN};
if(env.FINCORE_HOSTED_DEMO!=='true'||env.PAYMENT_PROVIDER!=='local'||!env.WEB_ORIGIN)throw Error('An explicit local-payment hosted demo and canonical origin are required');
if(env.RENDER_DATABASE_PASSWORD&&!/^[A-Za-z0-9_-]{32,128}$/.test(env.RENDER_DATABASE_PASSWORD))env.RENDER_DATABASE_PASSWORD=createHash('sha256').update(env.RENDER_DATABASE_PASSWORD).digest('hex');
if(!env.DATABASE_URL&&env.MIGRATION_DATABASE_URL&&env.RENDER_DATABASE_PASSWORD){const uri=new URL(env.MIGRATION_DATABASE_URL);uri.username='fincore_app';uri.password=env.RENDER_DATABASE_PASSWORD;uri.searchParams.set('connection_limit','3');uri.searchParams.set('pool_timeout','15');env.DATABASE_URL=uri.href;}
const children=[];let stopping=false;
function stop(code){if(stopping)return;stopping=true;for(const child of children)child.kill('SIGTERM');setTimeout(()=>process.exit(code),1500);}
function launch(name,args,childEnv=env){const child=spawn(args[0],args.slice(1),{env:childEnv,stdio:'inherit'});children.push(child);child.on('error',()=>{console.error(name+' could not start');stop(1);});child.on('exit',code=>{if(!stopping){console.error(name+' exited ('+code+')');stop(1);}});return child;}
async function ready(url){const deadline=Date.now()+60000;while(Date.now()<deadline){try{if((await fetch(url,{signal:AbortSignal.timeout(1500)})).ok)return;}catch{/* Wait for the owned child to bind its local port. */}await new Promise(r=>setTimeout(r,250));}throw Error('An internal demo dependency did not become ready');}
for(const signal of ['SIGTERM','SIGINT'])process.on(signal,()=>stop(0));
try{
 const bootstrap=spawn(process.execPath,['dist/scripts/render-bootstrap.js'],{env,stdio:'inherit'});
 await new Promise((resolve,reject)=>{bootstrap.on('error',reject);bootstrap.on('exit',code=>code===0?resolve():reject(Error('Hosted demo bootstrap failed')));});
 launch('Mailpit',['/usr/local/bin/mailpit','--listen','127.0.0.1:8025','--smtp','127.0.0.1:1025']);
 launch('Analytics',['/opt/analytics/bin/python','-m','uvicorn','app:app','--app-dir','services/financial-analytics','--host','127.0.0.1','--port','8001','--no-access-log']);
 await ready('http://127.0.0.1:8001/health');await ready('http://127.0.0.1:8025/api/v1/info');
 const runtimeEnv={...env,NODE_OPTIONS:'--max-old-space-size=128'};delete runtimeEnv.MIGRATION_DATABASE_URL;delete runtimeEnv.RENDER_DATABASE_PASSWORD;delete runtimeEnv.RENDER_DEMO_PASSWORD;delete runtimeEnv.RENDER_API_KEY;
 launch('Worker',[process.execPath,'dist/apps/worker/src/index.js'],runtimeEnv);await ready('http://127.0.0.1:8081');
 launch('API and frontend',[process.execPath,'dist/apps/api/src/server.js'],runtimeEnv);
 console.log('Free hosted simulation: worker sleeps with this service; email stays in private Mailpit; free database expiry applies.');
}catch(error){console.error(error.message);stop(1);}
