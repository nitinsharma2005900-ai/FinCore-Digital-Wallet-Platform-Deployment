# FinCore verified free HTTPS demo

Existing implementation extended without resetting databases or replacing the architecture. Native services, a separate isolated Compose stack, real PostgreSQL concurrency/integrity checks, local payment/notification simulation, Python Decimal/risk service, customer and staff workflows, API contracts, encrypted recovery evidence and vector architecture diagrams are included.

Live demo: https://fincore-wallet-demo-nitinsharma.onrender.com . The new public deployment repository includes an optional first-party UI/API export, restricted database role, supervised FastAPI/BullMQ/private Mailpit and validated all-Free Render Blueprint. Database/cache external access is disabled. Cloud credentials remain private.

Separate execution reports record 19 Node/API/frontend tests, 14 native Chrome tests, 8 local production-profile Chrome tests, 8 complete demo-container Chrome tests and 8 Chrome tests against the actual public HTTPS service. Earlier evidence records 8 Python and 6 original Compose browser tests. Health/readiness and public Swagger UI passed. Both complete push and pull-request workflows now pass verification, strict Node/Render image scans and provenance. The runtime remediation reduces captured HIGH/CRITICAL findings from 55 to zero without security suppressions. Six additional browser checks pass on the separate Next.js/API/worker runtime. The updated Render service passed all eight public browser checks again. Independent production deployment approval is not claimed.

Stripe Test Mode and Twilio execution still require the user's sandbox credentials. Mailpit needs no API key. The free demo sleeps after inactivity, pauses its worker and has an ephemeral Redis/Mailpit inbox. Its database expires on 26 December 2026 (IST); always-on production and scheduled offsite recovery remain incomplete. No paid resource or LLM API was used.

This prerelease is an educational simulation and does not process real money. The full 15-assessment status and limitations are in ASSESSMENT_MATRIX.md and the PDF. The ZIP excludes .env, runtime data, dependencies, caches and secrets.
