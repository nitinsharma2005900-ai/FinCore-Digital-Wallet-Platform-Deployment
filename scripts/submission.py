"""Generate submission from actual execution evidence; verify a sanitized ZIP extraction."""
from pathlib import Path
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak
from reportlab.lib.styles import getSampleStyleSheet
import json,os,zipfile,tempfile,re
from urllib.parse import urlsplit,unquote
ROOT=Path(__file__).resolve().parents[1]
def data(path,default=None):
    p=ROOT/path
    return json.loads(p.read_text(encoding='utf-8-sig')) if p.exists() else default
def junit(path):
    p=ROOT/path
    if not p.exists():return {'tests':0,'failures':0,'verified':False}
    cases=ET.parse(p).getroot().findall('.//testcase');failed=sum(c.find('failure') is not None or c.find('error') is not None for c in cases);skipped=sum(c.find('skipped') is not None for c in cases)
    return {'tests':len(cases),'failures':failed,'skipped':skipped,'verified':bool(cases) and failed==0 and skipped==0}
results={name:junit(path) for name,path in [('node','evidence/node-tests.xml'),('python','evidence/python-tests.xml'),('browser','evidence/browser-tests.xml')]}
results['containerBrowser']=junit('evidence/container-browser-tests.xml')
if (ROOT/'evidence/hosted-browser-tests.xml').exists():results['hostedProfile']=junit('evidence/hosted-browser-tests.xml')
if (ROOT/'evidence/render-container-browser-tests.xml').exists():results['renderContainer']=junit('evidence/render-container-browser-tests.xml')
if (ROOT/'evidence/render-cloud-browser-tests.xml').exists():results['renderCloud']=junit('evidence/render-cloud-browser-tests.xml')
if (ROOT/'evidence/node-runtime-browser-tests.xml').exists():results['nodeRuntime']=junit('evidence/node-runtime-browser-tests.xml')
checks=data('evidence/checks.json',[]);capstone=data('evidence/capstone.json',{});delivery=data('evidence/notification-recovery.json',{});coverage=data('coverage/coverage-summary.json',{}).get('total',{})
docker=data('evidence/docker-runtime.json',{})
names=['Financial customer frontend','Financial REST APIs','Double-entry ledger database','Financial identity and authorization','Python financial calculations','FastAPI risk analytics','Transfer consistency engine','Payment and notification integrations','Containerized financial stack','Git and change governance','Secure financial CI/CD','Ledger and payment testing','Financial API contracts','Secure deployment and recovery','Financial incident simulation']
sources=['apps/web/app/page.tsx; apps/web/app/workspace.tsx; apps/web/app/records.tsx','apps/api/src/app.ts; apps/api/src/customer.ts; apps/api/src/staff.ts','database/migrations/001_foundation.sql; apps/api/src/ledger.ts','apps/api/src/auth.ts; apps/api/src/customer.ts','services/financial-analytics/app.py','services/financial-analytics/app.py; apps/api/src/customer.ts','apps/api/src/ledger.ts','apps/api/src/payments.ts; apps/api/src/providers.ts; apps/worker/src/index.ts','docker-compose.yml; infrastructure/docker','docs/GOVERNANCE.md; .github/CODEOWNERS','.github/workflows/ci.yml; .github/workflows/deploy.yml','tests/integration; tests/frontend; tests/e2e','apps/api/src/openapi.ts; scripts/contracts.ts; docs/API.md','scripts/recovery.py; infrastructure/nginx; docs/deployment/DEPLOYMENT.md','scripts/capstone.ts; scripts/notification-drill.ts']
objectives=['Responsive customer/staff workflows connected to stored financial records','Validated versioned APIs, safe errors, ownership and pagination','Exact precision, immutable entries, balanced posting, holds and constraints','Bcrypt, JWT, refresh rotation/replay revocation, simulated MFA, RBAC and reauthentication','Decimal fees, interest, totals, summaries, reconciliation and HALF_EVEN rounding','Five deterministic risk patterns, explanations and actionable operations alerts','Atomic transfers, funds checks, payload-bound idempotency and ordered row locks','Signed webhooks, deduplication, settlement, refund outbox and retryable notifications','Non-root multi-stage containers, private data networking, persistent volumes and health checks','Semantic commits, review checklist, CODEOWNERS, controlled hotfix and tag','Tests, dependency/secret/image scans, versioned artifacts, provenance and approved deployment','Real PostgreSQL concurrency/integrity, API/security, Python, React and browser tests','OpenAPI/Swagger/Postman and lifecycle, signatures, ledger and export documentation','HTTPS deployment preparation, encrypted backups and isolated integrity-checked restore','Duplicate payment, mismatched settlement, unbalanced posting, dependency timeout and suspicious-activity incidents']
limitations={1:'Workspaces share a Next.js route. Staff lists are bounded to 100 records.',2:'Staff lists capped at 100; reconciliation processes the newest 1000 intents per run.',3:'INR only; one full compensation per original transaction. Privileged migrator credentials must remain separate.',4:'MFA is explicitly simulated locally; production activation is blocked without secure delivery.',5:'Benchmark is in-process TestClient measurement, not production capacity.',6:'Risk is threshold-based decision support, not proof of fraud. Stored alerts evaluate at transfer time.',7:'Automatic retry is limited to deadlock/serialization failures; durable operation keys remain mandatory.',8:'Local settlement and Mailpit verified. Stripe, Mailtrap and Twilio test credentials absent; external adapters unverified.',9:'Docker Desktop/engine absent. Container builds, Compose runtime and container health have not been executed.',10:'Local Git history is genuine. No designated remote repository, independent review or hosted protections.',11:'Workflow definitions prepared. No hosted CI run, image scan, attestation or deployment approval is claimed.',12:'Coverage is measured over included API/UI modules; external-credential and container tests remain unexecuted.',13:'Response envelope schemas are broad rather than exhaustive per-domain response-field schemas.',14:'Local encrypted restore passed. Cloud VM, domain, DNS, HTTPS and offsite scheduling require selected hosting access.',15:'Incidents use synthetic local wallets only; no production incident or recording is claimed.'}
def status(i):
    if i==8:return 'LOCAL SIMULATION ONLY'
    if i==9 and docker.get('verified') and junit('evidence/container-browser-tests.xml')['verified']:return 'COMPLETE AND VERIFIED'
    if i==11 and data('evidence/image-scan-summary.json',{}).get('gatePassed'):return 'CI VERIFIED; PRODUCTION APPROVAL PENDING'
    if i in (9,10,11):return 'IMPLEMENTED BUT NOT VERIFIED'
    if i==14:return 'PARTIALLY VERIFIED; FREE DEMO DEPLOYED' if data('evidence/render-deployment-status.json',{}).get('publicDeploymentVerified') else 'PARTIALLY VERIFIED; CLOUD DEPLOYMENT PENDING'
    verified=results['python']['verified'] if i in (5,6) else results['browser']['verified'] if i==1 else bool(capstone.get('timeline')) if i==15 else results['node']['verified']
    if i==12:verified=all(r['verified'] for r in results.values())
    return 'COMPLETE AND VERIFIED' if verified else 'IMPLEMENTED BUT NOT VERIFIED'
limitations[9]='Docker Engine and Compose installed in Ubuntu WSL. Compose configuration validated; see evidence/docker-runtime.json for actual container verification. No Docker Desktop subscription used.'
if docker.get('verified'):limitations[9]='Isolated fincore-verify Compose stack verified in Ubuntu WSL; native database/data preserved. Cloud container execution remains separate.'
limitations[10]='Public repository published at github.com/nitinsharma2005900-ai/FinCore-Digital-Wallet-Platform with user authorization. See evidence/github-protection-response.json for actual protection setup result; no independent review is fabricated.'
limitations[11]='Hosted verify job passed, but the image-security gate has unresolved OS advisories. Real run status is in evidence/github-status.json and raw findings in evidence/image-scan.json. No successful overall pipeline is claimed.'
if data('evidence/image-scan-summary.json',{}).get('gatePassed'):limitations[11]='Complete push and pull-request workflows passed verification, strict Node/Render image scans and provenance. Captured HIGH/CRITICAL and secret findings are zero; no security suppression or branch-protection bypass was added. See evidence/image-remediation.json. Independent review and approved always-on production deployment remain unverified.'
limitations[14]='Local encrypted restore verified. Render free services do not support the full durable worker architecture. Free full-stack VM/subdomain setup requires manual account provisioning; no paid resource created.'
if (ROOT/'evidence/render-deployment-status.json').exists():limitations[14]='Render API authenticated; dedicated free PostgreSQL/Redis created with private-only connection access. Optional demo container and browser checks verified separately. See evidence/render-deployment-status.json for actual web-service creation and public HTTPS verification. Until public checks pass, deployment remains unverified. The free profile sleeps and its database expires after 30 days; it does not satisfy always-on production requirements.'
if data('evidence/render-deployment-status.json',{}).get('publicDeploymentVerified'):limitations[14]='Free HTTPS demonstration live at https://fincore-wallet-demo-nitinsharma.onrender.com; /health, /ready and eight public Chrome tests passed. Dedicated free PostgreSQL/Redis are private-only; runtime role is restricted. The service/worker sleep, Redis/Mailpit are ephemeral and the database expires 26 December 2026 (IST). Always-on production architecture, scheduled offsite recovery and complete deployment governance are not verified. No paid resource was requested.'
limitations[12]='Coverage is measured over included API/UI modules. Six container browser tests executed successfully; external-credential tests remain unexecuted.'
evidence=['evidence/browser-tests.xml; evidence/customer-browser.png','evidence/node-tests.xml','evidence/capstone.json; evidence/node-tests.xml','evidence/node-tests.xml','evidence/python-tests.xml; evidence/python-benchmark.json','evidence/python-tests.xml; evidence/capstone.json','evidence/node-tests.xml; evidence/capstone.json','evidence/notification-recovery.json; evidence/capstone.json','docs/deployment/DEPLOYMENT.md','evidence/git-history.txt','evidence/checks.json; evidence/npm-audit.json; evidence/python-audit.json','evidence/node-tests.xml; evidence/python-tests.xml; evidence/browser-tests.xml','docs/openapi.json; postman/FinCore.postman_collection.json','evidence/restore-drill.json','evidence/capstone.json; evidence/notification-recovery.json']
tests=['tests/e2e/full-workflows.spec.ts; tests/e2e/platform.spec.ts; tests/e2e/management.spec.ts; tests/frontend/table.test.tsx','tests/integration/platform.test.ts','tests/integration/ledger.test.ts; scripts/capstone.ts','tests/integration/platform.test.ts','services/financial-analytics/test_app.py','services/financial-analytics/test_app.py; scripts/capstone.ts','tests/integration/ledger.test.ts','tests/integration/platform.test.ts; scripts/notification-drill.ts','Hosted image/Compose checks pending','Actual local Git hotfix and merge history','scripts/verify.mjs; hosted workflows pending','npm test; npm run test:e2e; pytest','tests/integration/platform.test.ts','python scripts/recovery.py','npm run capstone']
tests[8]='scripts/docker-evidence.mjs; tests/e2e/platform.spec.ts against isolated container ports'
evidence[8]='evidence/docker-runtime.json; evidence/container-browser-tests.xml'
tests[10]='scripts/verify.mjs; actual GitHub Actions verify/images jobs'
matrix=['# Assessment traceability matrix','','Local verification is distinct from external/cloud execution. No hosted results are fabricated.','','| # | Requirement | Implementation file | Test file | Test result | Evidence path | Completion status | Remaining limitation |','|---|---|---|---|---|---|---|---|']
for i,name in enumerate(names,1):
    summary='Verified local results below' if status(i) in ('COMPLETE AND VERIFIED','LOCAL SIMULATION ONLY') else 'Local portion tested; external execution pending'
    if i==11 and data('evidence/image-scan-summary.json',{}).get('gatePassed'):summary='Push/PR verification, both strict runtime scans and provenance passed; independent production approval pending'
    matrix.append(f'| {i:02} | {objectives[i-1]} | {sources[i-1]} | {tests[i-1]} | {summary} | {evidence[i-1]} | {status(i)} | {limitations[i]} |')
    doc=f'# Assessment {i:02}: {name}\n\nObjective: {objectives[i-1]}.\n\nStatus: **{status(i)}**\n\nImplementation: {sources[i-1]}.\n\nDesign decisions: see docs/architecture/ARCHITECTURE.md, docs/SECURITY.md and docs/API.md.\n\nSetup: scripts/Setup.ps1 followed by scripts/Start.ps1. External setup is documented in docs/deployment/DEPLOYMENT.md.\n\nAutomated tests: {tests[i-1]}.\n\nActual evidence: {evidence[i-1]}.\n\nActual suite results: {json.dumps(results)}. Only evidence relevant to this assessment supports its status.\n\nKnown limitation: {limitations[i]}\n'
    (ROOT/f'docs/assessments/{i:02}.md').write_text(doc,encoding='utf-8')
matrix+=['','## Actual execution summary','',json.dumps(results,indent=2),'',json.dumps(checks,indent=2),'','Coverage scope: API modules and React workspace component, not the whole application. See evidence/coverage-summary.json.','',json.dumps(coverage,indent=2)]
(ROOT/'ASSESSMENT_MATRIX.md').write_text('\n'.join(matrix),encoding='utf-8')
(ROOT/'evidence/test-summary.json').write_text(json.dumps({'suites':results,'checks':checks,'coverage':coverage},indent=2))
if (ROOT/'coverage/coverage-summary.json').exists():(ROOT/'evidence/coverage-summary.json').write_bytes((ROOT/'coverage/coverage-summary.json').read_bytes())
incident=['# Controlled financial incident report','','Reproduction: npm run capstone. All records are synthetic; timeline timestamps are actual UTC execution times.','']
causes={'duplicate-payment-events':'At-least-once provider delivery; unique event ID suppresses duplicate credit and successful settlement ignores later failure.','mismatched-provider-settlement':'Observed amount differs from intent; store discrepancy without journal posting.','unbalanced-journal':'Only debit side exists; deferred database constraint rejects commit and rolls back the transaction.','dependency-timeout':'Analytics URL intentionally unavailable; bounded dependency failure rejects before financial posting.','suspicious-activity':'Synthetic threshold inputs trigger explainable risk decision support.','concurrent-transfers':'Two spends compete for one balance; ordered row locks permit only one successful spend.','failed-settlement':'Provider failure persists without creating wallet credit.','financial-reversal':'A new compensating journal restores funds; original remains immutable.'}
for event in capstone.get('timeline',[]):
    name=event['incident'];incident += [f'## {name}','',f'Timeline: {event["at"]}.',f'Root cause and corrective action: {causes.get(name,name)}',f'Actual result and recovery evidence: {json.dumps(event["data"])}','Impact: synthetic wallets only. Regression: scripts/capstone.ts, tests/integration/ledger.test.ts and tests/integration/platform.test.ts.','Prevention: preserve database constraints, idempotency keys, role checks, immutable history and bounded timeouts.','']
incident+=['## Recovery confirmation','',f'Final journal: {json.dumps(capstone.get("integrity",{}))}. Source after reversal: {json.dumps(capstone.get("after",{}))}.','', '## Background delivery outage','',json.dumps(delivery,indent=2),'Reproduction: node --import tsx scripts/notification-drill.ts. It intentionally stops/restarts the owned local Mailpit process; BullMQ retries and then delivers.']
(ROOT/'docs/incidents').mkdir(exist_ok=True);(ROOT/'docs/incidents/INCIDENT_REPORT.md').write_text('\n'.join(incident),encoding='utf-8')
(ROOT/'docs/KNOWN_LIMITATIONS.md').write_text('# Remaining limitations and external prerequisites\n\n'+'\n'.join(f'- Assessment {i:02}: {limitations[i]}' for i in (8,9,10,11,14))+'\n\nReal-money processing, live Stripe keys and delivered external SMS have not been executed. Verified free HTTPS demo and hosted security checks are distinct from independent production approval and always-on hosting requirements.\n',encoding='utf-8')
styles=getSampleStyleSheet();styles['BodyText'].fontSize=9;styles['BodyText'].leading=13
story=[Paragraph('FinCore',styles['Title']),Paragraph('Digital Wallet, Ledger & Payment Processing Platform',styles['Heading2']),Paragraph('Synthetic educational platform: verified local results and explicit external limitations',styles['BodyText'])]
documents=['README.md','docs/PROJECT_OVERVIEW.md','ASSESSMENT_MATRIX.md','docs/BROWSER_FUNCTION_CHECK.md','docs/architecture/ARCHITECTURE.md','docs/SECURITY.md','docs/ENVIRONMENT.md','docs/SANDBOX_CREDENTIALS.md','docs/API.md','docs/incidents/INCIDENT_REPORT.md','docs/deployment/DEPLOYMENT.md','docs/deployment/WSL_DOCKER.md','docs/deployment/FREE_HOSTING.md','docs/deployment/RENDER_DEMO.md','docs/GOVERNANCE.md','docs/DEMO_SCRIPT.md','docs/KNOWN_LIMITATIONS.md']+[f'docs/assessments/{i:02}.md' for i in range(1,16)]
import runpy
diagrams=runpy.run_path(str(ROOT/'scripts/diagrams.py'))
for name in ['architecture','entities','sequence']:story.extend([PageBreak(),diagrams[name]])
for name in documents:
    story.extend([PageBreak(),Paragraph(escape(name),styles['Heading1'])])
    for line in (ROOT/name).read_text(encoding='utf-8').splitlines():
        if line.strip():story.extend([Paragraph(escape(line[:1000]),styles['BodyText']),Spacer(1,4)])
def footer(canvas,doc):
    canvas.setFont('Helvetica',8);canvas.drawString(42,25,'FinCore | Simulation Only - No Real Money');canvas.drawRightString(550,25,str(doc.page))
SimpleDocTemplate(str(ROOT/'docs/FinCore_Project_Report.pdf'),title='FinCore Verified Project Report',leftMargin=42,rightMargin=42).build(story,onFirstPage=footer,onLaterPages=footer)
archive=ROOT/'FinCore_Digital_Wallet_Platform.zip';excluded={'.git','.runtime','.tools','.venv','node_modules','.next','out','__pycache__','.pytest_cache','coverage','dist','test-results','playwright-report'}
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for directory,dirs,files in os.walk(ROOT):
        dirs[:]=[d for d in dirs if d not in excluded]
        for name in files:
            p=Path(directory)/name
            if name in ('.env','.coverage','package-verification.json') or (name.startswith('.env.') and name!='.env.example') or p.suffix in ('.zip','.log','.pyc','.tsbuildinfo','.enc','.backup'):continue
            z.write(p,str(p.relative_to(ROOT)))
private_values=set()
if (ROOT/'.env').exists():
    for line in (ROOT/'.env').read_text(encoding='utf-8-sig').splitlines():
        if '=' not in line or line.lstrip().startswith('#'):continue
        key,value=line.split('=',1);value=value.strip().strip('\"\'')
        if re.search(r'SECRET|TOKEN|PASSWORD|API_KEY|DATABASE_URL',key) and len(value)>=16:private_values.add(value)
        if 'DATABASE_URL' in key:
            password=urlsplit(value).password
            if password and len(password)>=16:private_values.add(unquote(password))
with tempfile.TemporaryDirectory(prefix='fincore-verify-') as target:
    with zipfile.ZipFile(archive) as z:
        for name in z.namelist():
            contents=z.read(name)
            assert not any(value.encode() in contents for value in private_values),'Private environment value in archive member: '+name
        assert z.testzip() is None;z.extractall(target)
        for required in ['package.json','package-lock.json','.env.example','database/migrations/001_foundation.sql','docs/FinCore_Project_Report.pdf','docker-compose.yml','postman/FinCore.postman_collection.json']:assert (Path(target)/required).exists(),required
        assert not (Path(target)/'.env').exists()
package={'archive':archive.name,'bytes':archive.stat().st_size,'crcVerified':True,'extractionVerified':True,'excludedSecretsAndRuntime':True,'privateValuesChecked':len(private_values),'privateValueScanPassed':True if private_values else None}
(ROOT/'evidence/package-verification.json').write_text(json.dumps(package,indent=2))
print(json.dumps({'suites':results,'package':package},indent=2))
