# Image scan failure and verified remediation

Both `Financial quality gates / images` checks failed on commit `642707117b7cb3fc405a05944cce1b912fff4a8d`. The [push run](https://github.com/nitinsharma2005900-ai/FinCore-Digital-Wallet-Platform-Deployment/actions/runs/45687229469) and [pull-request run](https://github.com/nitinsharma2005900-ai/FinCore-Digital-Wallet-Platform-Deployment/actions/runs/45687241336) each reported 55 HIGH findings in Debian 13 runtime packages, with no fixed versions listed. This was a genuine security-gate failure. The original report is retained as `evidence/image-scan-before-remediation.json`.

## Changes

- Use the supported official `node:22.23.5-alpine3.24` runtime, apply current APK updates and install the required PostgreSQL client/OpenSSL packages. The Node major version, application code and database schema/migrations are preserved.
- Generate Prisma's supported musl/OpenSSL 3 engines for x64 and ARM64 alongside the native build target. No database migration or data reset is needed.
- Prune development dependencies from runtime images. Remove unused npm/npx/Yarn; after Python dependencies are installed, remove pip and its bundled ensurepip installer. The expanded Render scan had identified five additional HIGH findings in unused Python packaging components; the vulnerable files are absent from the final runtime.
- Update Trivy to v0.76.2 and scan both the separate Node runtime and the actual Render image. Keep CRITICAL/HIGH, failure exit code 1, secret scanning, provenance and branch protection. No ignore file, blanket suppression, ignore-unfixed, severity reduction or continue-on-error bypass was introduced.

## Actual verification

Commit `b4ecdaef272b94db5bd7fc6b858f85f8bfb8c3c5` passed the complete [push workflow](https://github.com/nitinsharma2005900-ai/FinCore-Digital-Wallet-Platform-Deployment/actions/runs/45689845258) and [pull-request workflow](https://github.com/nitinsharma2005900-ai/FinCore-Digital-Wallet-Platform-Deployment/actions/runs/45689856389), including image scans and provenance. All four image reports contain zero HIGH/CRITICAL vulnerabilities and zero secret findings. `evidence/image-remediation.json` records commits, run IDs and report paths.

The [runtime compatibility run](https://github.com/nitinsharma2005900-ai/FinCore-Digital-Wallet-Platform-Deployment/actions/runs/45689845163) passed eight browser tests against the complete 512 MiB Render demo and six against the separate Next.js server/API/worker stack. It verifies Prisma, PostgreSQL migrations, Python analytics, startup without runtime package managers, funding, statements and role workspaces. Verification jobs also passed 19 API/frontend tests, eight Python tests and 14 native browser tests.

Render was updated to that tested application commit without resetting the database or replacing its secrets. The live HTTPS application then passed readiness and all eight public browser tests again. Deployment/browser evidence is in `evidence/render-deployment-status.json` and `evidence/render-cloud-browser-tests.xml`.

Windows had a Prisma DLL in use by the running local app. Client generation was verified in clean Linux CI rather than stopping that app to replace the DLL.

Passing these scans establishes the captured results, not a permanent security certification. Independent review, production approval, external Stripe/Twilio execution and always-on hosting requirements remain separate.
