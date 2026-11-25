# Assessment traceability matrix

Local verification is distinct from external/cloud execution. No hosted results are fabricated.

| # | Requirement | Implementation file | Test file | Test result | Evidence path | Completion status | Remaining limitation |
|---|---|---|---|---|---|---|---|
| 01 | Responsive customer/staff workflows connected to stored financial records | apps/web/app/page.tsx; apps/web/app/workspace.tsx; apps/web/app/records.tsx | tests/e2e/full-workflows.spec.ts; tests/e2e/platform.spec.ts; tests/e2e/management.spec.ts; tests/frontend/table.test.tsx | Verified local results below | evidence/browser-tests.xml; evidence/customer-browser.png | COMPLETE AND VERIFIED | Workspaces share a Next.js route. Staff lists are bounded to 100 records. |
| 02 | Validated versioned APIs, safe errors, ownership and pagination | apps/api/src/app.ts; apps/api/src/customer.ts; apps/api/src/staff.ts | tests/integration/platform.test.ts | Verified local results below | evidence/node-tests.xml | COMPLETE AND VERIFIED | Staff lists capped at 100; reconciliation processes the newest 1000 intents per run. |
| 03 | Exact precision, immutable entries, balanced posting, holds and constraints | database/migrations/001_foundation.sql; apps/api/src/ledger.ts | tests/integration/ledger.test.ts; scripts/capstone.ts | Verified local results below | evidence/capstone.json; evidence/node-tests.xml | COMPLETE AND VERIFIED | INR only; one full compensation per original transaction. Privileged migrator credentials must remain separate. |
| 04 | Bcrypt, JWT, refresh rotation/replay revocation, simulated MFA, RBAC and reauthentication | apps/api/src/auth.ts; apps/api/src/customer.ts | tests/integration/platform.test.ts | Verified local results below | evidence/node-tests.xml | COMPLETE AND VERIFIED | MFA is explicitly simulated locally; production activation is blocked without secure delivery. |
| 05 | Decimal fees, interest, totals, summaries, reconciliation and HALF_EVEN rounding | services/financial-analytics/app.py | services/financial-analytics/test_app.py | Verified local results below | evidence/python-tests.xml; evidence/python-benchmark.json | COMPLETE AND VERIFIED | Benchmark is in-process TestClient measurement, not production capacity. |
| 06 | Five deterministic risk patterns, explanations and actionable operations alerts | services/financial-analytics/app.py; apps/api/src/customer.ts | services/financial-analytics/test_app.py; scripts/capstone.ts | Verified local results below | evidence/python-tests.xml; evidence/capstone.json | COMPLETE AND VERIFIED | Risk is threshold-based decision support, not proof of fraud. Stored alerts evaluate at transfer time. |
| 07 | Atomic transfers, funds checks, payload-bound idempotency and ordered row locks | apps/api/src/ledger.ts | tests/integration/ledger.test.ts | Verified local results below | evidence/node-tests.xml; evidence/capstone.json | COMPLETE AND VERIFIED | Automatic retry is limited to deadlock/serialization failures; durable operation keys remain mandatory. |
| 08 | Signed webhooks, deduplication, settlement, refund outbox and retryable notifications | apps/api/src/payments.ts; apps/api/src/providers.ts; apps/worker/src/index.ts | tests/integration/platform.test.ts; scripts/notification-drill.ts | Verified local results below | evidence/notification-recovery.json; evidence/capstone.json | LOCAL SIMULATION ONLY | Local settlement and Mailpit verified. Stripe, Mailtrap and Twilio test credentials absent; external adapters unverified. |
| 09 | Non-root multi-stage containers, private data networking, persistent volumes and health checks | docker-compose.yml; infrastructure/docker | scripts/docker-evidence.mjs; tests/e2e/platform.spec.ts against isolated container ports | Verified local results below | evidence/docker-runtime.json; evidence/container-browser-tests.xml | COMPLETE AND VERIFIED | Isolated fincore-verify Compose stack verified in Ubuntu WSL; native database/data preserved. Cloud container execution remains separate. |
| 10 | Semantic commits, review checklist, CODEOWNERS, controlled hotfix and tag | docs/GOVERNANCE.md; .github/CODEOWNERS | Actual local Git hotfix and merge history | Local portion tested; external execution pending | evidence/git-history.txt | IMPLEMENTED BUT NOT VERIFIED | Public repository published at github.com/nitinsharma2005900-ai/FinCore-Digital-Wallet-Platform with user authorization. See evidence/github-protection-response.json for actual protection setup result; no independent review is fabricated. |
| 11 | Tests, dependency/secret/image scans, versioned artifacts, provenance and approved deployment | .github/workflows/ci.yml; .github/workflows/deploy.yml | scripts/verify.mjs; actual GitHub Actions verify/images jobs | Push/PR verification, both strict runtime scans and provenance passed; independent production approval pending | evidence/checks.json; evidence/npm-audit.json; evidence/python-audit.json | CI VERIFIED; PRODUCTION APPROVAL PENDING | Complete push and pull-request workflows passed verification, strict Node/Render image scans and provenance. Captured HIGH/CRITICAL and secret findings are zero; no security suppression or branch-protection bypass was added. See evidence/image-remediation.json. Independent review and approved always-on production deployment remain unverified. |
| 12 | Real PostgreSQL concurrency/integrity, API/security, Python, React and browser tests | tests/integration; tests/frontend; tests/e2e | npm test; npm run test:e2e; pytest | Verified local results below | evidence/node-tests.xml; evidence/python-tests.xml; evidence/browser-tests.xml | COMPLETE AND VERIFIED | Coverage is measured over included API/UI modules. Six container browser tests executed successfully; external-credential tests remain unexecuted. |
| 13 | OpenAPI/Swagger/Postman and lifecycle, signatures, ledger and export documentation | apps/api/src/openapi.ts; scripts/contracts.ts; docs/API.md | tests/integration/platform.test.ts | Verified local results below | docs/openapi.json; postman/FinCore.postman_collection.json | COMPLETE AND VERIFIED | Response envelope schemas are broad rather than exhaustive per-domain response-field schemas. |
| 14 | HTTPS deployment preparation, encrypted backups and isolated integrity-checked restore | scripts/recovery.py; infrastructure/nginx; docs/deployment/DEPLOYMENT.md | python scripts/recovery.py | Local portion tested; external execution pending | evidence/restore-drill.json | PARTIALLY VERIFIED; FREE DEMO DEPLOYED | Free HTTPS demonstration live at https://fincore-wallet-demo-nitinsharma.onrender.com; /health, /ready and eight public Chrome tests passed. Dedicated free PostgreSQL/Redis are private-only; runtime role is restricted. The service/worker sleep, Redis/Mailpit are ephemeral and the database expires 26 December 2026 (IST). Always-on production architecture, scheduled offsite recovery and complete deployment governance are not verified. No paid resource was requested. |
| 15 | Duplicate payment, mismatched settlement, unbalanced posting, dependency timeout and suspicious-activity incidents | scripts/capstone.ts; scripts/notification-drill.ts | npm run capstone | Verified local results below | evidence/capstone.json; evidence/notification-recovery.json | COMPLETE AND VERIFIED | Incidents use synthetic local wallets only; no production incident or recording is claimed. |

## Actual execution summary

{
  "node": {
    "tests": 19,
    "failures": 0,
    "skipped": 0,
    "verified": true
  },
  "python": {
    "tests": 8,
    "failures": 0,
    "skipped": 0,
    "verified": true
  },
  "browser": {
    "tests": 14,
    "failures": 0,
    "skipped": 0,
    "verified": true
  },
  "containerBrowser": {
    "tests": 6,
    "failures": 0,
    "skipped": 0,
    "verified": true
  },
  "hostedProfile": {
    "tests": 8,
    "failures": 0,
    "skipped": 0,
    "verified": true
  },
  "renderContainer": {
    "tests": 8,
    "failures": 0,
    "skipped": 0,
    "verified": true
  },
  "renderCloud": {
    "tests": 8,
    "failures": 0,
    "skipped": 0,
    "verified": true
  },
  "nodeRuntime": {
    "tests": 6,
    "failures": 0,
    "skipped": 0,
    "verified": true
  }
}

[
  {
    "name": "test",
    "exitCode": 0,
    "passed": true,
    "elapsedSeconds": 40.921,
    "completedAt": "2026-11-25T17:15:42.888Z"
  },
  {
    "name": "docs",
    "exitCode": 0,
    "passed": true,
    "elapsedSeconds": 8.106,
    "completedAt": "2026-11-25T17:16:32.484Z"
  },
  {
    "name": "build",
    "exitCode": 0,
    "passed": true,
    "elapsedSeconds": 28.138,
    "completedAt": "2026-11-25T18:38:43.556Z"
  },
  {
    "name": "lint",
    "exitCode": 0,
    "passed": true,
    "elapsedSeconds": 8.268,
    "completedAt": "2026-11-25T19:23:50.052Z"
  },
  {
    "name": "typecheck",
    "exitCode": 0,
    "passed": true,
    "elapsedSeconds": 19.29,
    "completedAt": "2026-11-25T19:24:09.344Z"
  }
]

Coverage scope: API modules and React workspace component, not the whole application. See evidence/coverage-summary.json.

{
  "lines": {
    "total": 433,
    "covered": 345,
    "skipped": 0,
    "pct": 79.67
  },
  "statements": {
    "total": 886,
    "covered": 565,
    "skipped": 0,
    "pct": 63.76
  },
  "functions": {
    "total": 185,
    "covered": 101,
    "skipped": 0,
    "pct": 54.59
  },
  "branches": {
    "total": 511,
    "covered": 259,
    "skipped": 0,
    "pct": 50.68
  },
  "branchesTrue": {
    "total": 0,
    "covered": 0,
    "skipped": 0,
    "pct": 100
  }
}