# Remaining limitations and external prerequisites

- Assessment 08: Local settlement and Mailpit verified. Stripe, Mailtrap and Twilio test credentials absent; external adapters unverified.
- Assessment 09: Isolated fincore-verify Compose stack verified in Ubuntu WSL; native database/data preserved. Cloud container execution remains separate.
- Assessment 10: Public repository published at github.com/nitinsharma2005900-ai/FinCore-Digital-Wallet-Platform with user authorization. See evidence/github-protection-response.json for actual protection setup result; no independent review is fabricated.
- Assessment 11: Hosted verify job passed, but the image-security gate has unresolved OS advisories. Real run status is in evidence/github-status.json and raw findings in evidence/image-scan.json. No successful overall pipeline is claimed.
- Assessment 14: Free HTTPS demonstration live at https://fincore-wallet-demo-nitinsharma.onrender.com; /health, /ready and eight public Chrome tests passed. Dedicated free PostgreSQL/Redis are private-only; runtime role is restricted. The service/worker sleep, Redis/Mailpit are ephemeral and the database expires 26 December 2026 (IST). Always-on production architecture, scheduled offsite recovery and complete deployment governance are not verified. No paid resource was requested.

No real-money operation, live key, hosted CI, cloud URL or delivered external SMS is represented as completed.
