import {PrismaClient} from '@prisma/client';
import bcrypt from 'bcryptjs';
import {spawnSync} from 'node:child_process';
const ownerUrl=process.env.MIGRATION_DATABASE_URL;
if(process.env.FINCORE_HOSTED_DEMO!=='true'||process.env.NODE_ENV!=='production'||process.env.PAYMENT_PROVIDER!=='local'||!ownerUrl)throw Error('Bootstrap is limited to the explicitly enabled hosted simulation');
const password=process.env.RENDER_DEMO_PASSWORD||'';
const rolePassword=process.env.RENDER_DATABASE_PASSWORD||'';
if(!/^[A-Za-z0-9_-]{32,128}$/.test(rolePassword)||password.length<24)throw Error('Unique strong hosted demo credentials are required');
const owner=new PrismaClient({datasourceUrl:ownerUrl});
async function main(){
 const exists=await owner.$queryRaw<{rolname:string}[]>`SELECT rolname FROM pg_roles WHERE rolname='fincore_app'`;
 if(!exists.length)await owner.$executeRawUnsafe("CREATE ROLE fincore_app LOGIN PASSWORD '"+rolePassword+"' NOSUPERUSER NOCREATEDB NOCREATEROLE");
 const migrated=spawnSync(process.execPath,['dist/scripts/migrate.js'],{env:process.env,stdio:'inherit'});if(migrated.status!==0)throw Error('Hosted migration failed');
 const {db}=await import('../apps/api/src/core');const {post}=await import('../apps/api/src/ledger');
 try{
  const treasury=await db.wallet.upsert({where:{id:'treasury'},create:{id:'treasury',name:'Simulation treasury',type:'TREASURY'},update:{}});
  const hash=await bcrypt.hash(password,12);
  for(const [role,email,name] of [['CUSTOMER','customer@fincore.test','Hosted Demo Customer'],['CUSTOMER','recipient@fincore.test','Hosted Demo Recipient'],['SUPPORT','support@fincore.test','Hosted Support'],['OPERATIONS','operations@fincore.test','Hosted Operations'],['FINANCE','finance@fincore.test','Hosted Finance'],['ADMIN','admin@fincore.test','Hosted Administrator']]){
   const user=await db.user.upsert({where:{email},create:{email,name,role,passwordHash:hash},update:{}});
   if(role==='CUSTOMER'){
    let wallet=await db.wallet.findFirst({where:{userId:user.id}});if(!wallet)wallet=await db.wallet.create({data:{userId:user.id,name:'Everyday wallet'}});
    await db.account.upsert({where:{reference:'FC-HOSTED-'+user.id},create:{reference:'FC-HOSTED-'+user.id,label:'Demo account',userId:user.id},update:{}});
    await post({fromWalletId:treasury.id,toWalletId:wallet.id,amount:'25000.00',currency:'INR',kind:'FUNDING',description:'Hosted synthetic opening funds',userId:user.id,key:user.id,scope:'hosted-demo-seed'});
   }
  }
  console.log('Hosted synthetic accounts ready. Credentials stay in the protected local/cloud environment.');
 }finally{await db.$disconnect();}
}
main().finally(()=>owner.$disconnect()).catch(error=>{console.error(error.message);process.exitCode=1;});
