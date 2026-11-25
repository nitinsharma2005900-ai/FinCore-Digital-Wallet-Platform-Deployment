# Identity, authorization and operations

| Role | Permission |
|---|---|
| CUSTOMER | Own accounts, wallets, beneficiaries, transfers, intents, statements, disputes, profile and notifications |
| SUPPORT | Dispute queue, self-assignment, investigation and closure |
| OPERATIONS | Risk alerts and provider reconciliation investigation |
| FINANCE | Ledger/settlement reports and authorized compensation requests |
| ADMIN | Users, roles, settings, failed-job recovery, system health and audits |

Staff permissions do not imply permission to spend customer funds. All protected endpoints authenticate server-side and verify either ownership or the endpoint role. Sensitive mutations require password reauthentication. Passwords are salted bcrypt hashes at cost 12. Refresh tokens are random values stored as keyed hashes; rotated tokens remain as revoked records so replay is detected. Access JWTs are issuer/audience checked and tied to an active server-side session. Logs use request IDs and do not include authorization headers, cookies, passwords or raw request bodies.

Helmet applies HTTP security headers. CORS permits the configured frontend origin only. Refresh cookies are HttpOnly, SameSite=Strict and Secure in production. Cookie-based refresh requires trusted Origin; protected business actions use memory-held Bearer tokens. Server schemas reject unexpected sensitive fields and validate untrusted values. Tagged database queries are parameterized. React escapes text. CSV exports neutralize formula cells. Payment webhooks verify exact raw bytes before parsing.

MFA is explicitly simulated locally; use of production MFA is blocked without secure delivery. Stripe live keys/events are rejected. Twilio uses test credentials with magic test numbers and never represents a delivered real SMS. Local credentials and generated secrets remain in ignored .env/.runtime; source exports and ZIPs exclude them.

Security tests are in tests/integration/platform.test.ts and tests/integration/ledger.test.ts. Dependency reports are genuine local npm audit and pip-audit outputs under evidence/. A passing dependency scan is limited to known advisories at execution time, not a security certification. The free Render demo's public browser checks verify HTTPS, first-party secure-cookie refresh, CSP hydration, role restrictions and private-file denial. Its database/cache are private-only; the management API key is absent from the app. Strict Node/Render image gates now pass on both push and pull_request with zero captured HIGH/CRITICAL findings; see docs/incidents/IMAGE_SECURITY.md. Independent production governance and external sandbox execution remain incomplete. See docs/deployment/RENDER_DEMO.md.

Local Gitleaks scans the committed history. Its only allowlist is the exact static synthetic CI fixture values in the CI workflow; it does not exempt general credentials, directories or private key formats. Downloaded scanner binaries are checksum verified. The report is evidence/gitleaks.json. Real .env/.runtime secrets are not committed or packaged.
