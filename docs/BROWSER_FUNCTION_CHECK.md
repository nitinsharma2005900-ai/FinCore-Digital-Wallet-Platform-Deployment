# Browser function verification

Verification date: 26 November 2026 (Asia/Calcutta). Application: http://127.0.0.1:3000. Chrome ran through Playwright in headless mode; this does not claim a visible desktop browser was opened. The existing implementation and database were retained.

## Executed checks

The complete browser suite has 14 tests. Seven extended tests exercise connected customer and staff actions; seven existing tests cover workspace access, reservations, statements and mobile navigation. The authoritative result, timestamps and durations are in `evidence/browser-tests.xml`. No skipped test counts as verified.

| Area | Actions exercised in the browser |
|---|---|
| Registration and sign-in | Register two disposable customers; sign out; sign in again; log in with each staff role |
| Navigation | Customer/staff menus, collapsed navigation, dark mode, 390 x 844 mobile navigation |
| Wallets and accounts | Create a wallet and account; rename, freeze and reactivate a wallet |
| Funding | Successful and failed local simulated settlement |
| Beneficiaries | Look up a disposable recipient by email, save and remove the recipient |
| Transfers | Six stored transfers; reject an insufficient-funds transfer with a visible error |
| Transactions | Server search returns six matching transfers; type/date controls; expand record details; select a transaction |
| Statements | Download CSV and PDF; verify filename, nonempty contents and CSV header/PDF signature |
| Reservations | Create a hold and release it through each of the two available release forms |
| Notifications | Mark a notification read; recover an explicitly failed notification through the admin UI; wait for worker status SENT |
| Profile | Save a new customer name |
| Security | Enable simulated MFA, complete its challenge, disable it, revoke another session, change password and log in with the new password |
| Support | Investigate and resolve the customer dispute created in this run |
| Operations | Review the generated velocity alert; run reconciliation; record investigation of the failed simulated settlement |
| Finance | Reverse one posted transfer and refund another; verify a balanced journal |
| Administration | Disable/reactivate only the disposable customer; update support email; view audit and system status |
| Customer overview | Return after staff compensation and assert the exact available balance: INR 196.00 after funding 200, six transfers of 1, reversal 1 and refund 1 |

All customer mutations use disposable synthetic accounts. Staff actions use the existing local demo accounts. The failed-notification recovery check seeds one explicitly FAILED notification for the disposable customer through Prisma, then uses the browser recovery form and the running worker/Mailpit delivery path. It does not claim an actual SMTP outage occurred in this browser run.

## Defects corrected

1. Successful authentication and password-confirmation requests consumed the failed-authentication allowance. The limiter now counts failed requests, exempts anonymous refresh checks without a cookie, and retains failed-attempt limits. An API regression performs 45 successful refreshes and 45 anonymous page-load refresh checks, then verifies failed authentication is still limited.
2. Signing out after registration retained the registration screen. Sign-out now resets the authentication screen, MFA challenge, selected view and pending payment state.
3. Returning to the customer overview after a staff refund could show a cached balance. Returning to Overview now refreshes the dashboard; the browser verifies the resulting balance.

One earlier run encountered a transient bounded analytics timeout. The transfer was rejected before posting funds. The duplicate Docker verification stack was stopped to reduce local resource load; native PostgreSQL, Redis, API, analytics, worker, Mailpit and web services remained in use. The final full browser run is captured separately from those earlier failures.

## Evidence and limits

- Browser source: `tests/e2e/full-workflows.spec.ts`, `management.spec.ts`, `platform.spec.ts`.
- Machine-readable results: `evidence/browser-tests.xml`, `evidence/node-tests.xml`, `evidence/health.json`.
- Screenshots: `evidence/full-customer-browser.png`, `evidence/full-admin-browser.png` and the existing role screenshots.
- Reproduce with the native services running: `npm run test:e2e`. Local demo credentials are read from `.runtime/demo-credentials.json`, never embedded in the test source or submission archive.

This report describes the listed native workflows, not every input/device/failure combination. A later free HTTPS demo separately passed eight browser checks; see `evidence/render-cloud-browser-tests.xml` and `docs/deployment/RENDER_DEMO.md`. Stripe Test Mode browser/webhook execution, Twilio test requests, external Stripe refund delivery, always-on production deployment and the hosted image-security gate remain incomplete. Payment processing is explicitly simulated; MFA is simulated locally and its production activation is blocked; email testing uses private Mailpit. No paid service was used. All assessment limitations remain in `ASSESSMENT_MATRIX.md` and `docs/KNOWN_LIMITATIONS.md`.
