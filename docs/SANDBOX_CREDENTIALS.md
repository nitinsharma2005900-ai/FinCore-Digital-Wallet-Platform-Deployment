# Free sandbox credentials and activation

No Gemini or other AI API is needed. Keep your Gemini key outside this project. All values below belong in ignored root `.env`, never in chat, source code, screenshots or a ZIP. Keep existing database/JWT/backup secrets unchanged. The local payment simulator, Mailpit and local SMS mode need no external account or key.

## Stripe Test Mode

Official websites: [Stripe](https://stripe.com), [Dashboard API keys](https://dashboard.stripe.com/apikeys), [official key documentation](https://docs.stripe.com/keys), [Stripe CLI](https://docs.stripe.com/cli).

1. Sign in or create your Stripe account. Select a sandbox or Test mode in the account/environment picker; ensure you are not in live mode.
2. Open Developers/Workbench → API keys for that sandbox. Copy the test secret (`sk_test_…`) and publishable (`pk_test_…`) keys. This integration deliberately rejects live secret keys.
3. Install the free Stripe CLI using the official installation instructions. Run `stripe login` and authorize only your sandbox. Some accounts require an administrator to enable CLI access under Team and security → MCP and CLI access.
4. Run `stripe listen --forward-to http://127.0.0.1:4001/api/v1/webhooks/payments`. Copy its `whsec_…` signing secret to `.env`. Keep this terminal open. A Dashboard endpoint secret and a CLI forwarding secret are different; use the one actually signing the incoming events.
5. Configure:

```dotenv
PAYMENT_PROVIDER=stripe
STRIPE_SECRET_KEY=sk_test_REPLACE_LOCALLY
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_REPLACE_LOCALLY
STRIPE_WEBHOOK_SECRET=whsec_REPLACE_LOCALLY
```

6. Restart the owned API, worker and Next.js processes so server configuration and public build-time configuration refresh. Sign in, open Funding, create an INR test intent and use Stripe's documented test payment method, never real card data. Only the signed success webhook credits the wallet. The simulator confirmation endpoint is disabled for Stripe intents.
7. Finance can request a full refund. The worker reserves funds, calls Stripe with a stable idempotency key, and posts the compensation only after a succeeded refund status. Pending/failed refunds retain their reservation for retry/investigation. Verify actual Stripe request/webhook/refund evidence before calling assessment 08 externally complete.

Sandbox testing does not move real funds. Account availability/onboarding depends on Stripe and your country. If you cannot obtain a sandbox account, keep `PAYMENT_PROVIDER=local`; that is explicitly a local simulation, not a verified Stripe integration.

## Mailpit: free local email capture

Official project: [Mailpit](https://github.com/axllent/mailpit). It is already part of the native setup. No account/API key is needed. Open http://127.0.0.1:8025.

```dotenv
EMAIL_PROVIDER=mailpit
SMTP_HOST=127.0.0.1
SMTP_PORT=1025
SMTP_USER=
SMTP_PASSWORD=
SMTP_SECURE=false
```

## Optional Mailtrap Email Sandbox

Official websites: [Mailtrap](https://mailtrap.io), [sandbox setup](https://docs.mailtrap.io/email-sandbox/setup/sandbox-smtp-integration).

1. Create/sign in to a free account and select Email Sandbox rather than live Email Sending.
2. Open your sandbox inbox → Integration → SMTP. Copy that inbox's host, port, username and password.
3. Set `EMAIL_PROVIDER=mailtrap`, `SMTP_HOST=sandbox.smtp.mailtrap.io`, and set `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD` to the exact displayed values. Set `SMTP_SECURE` according to that SMTP port's instructions. Do not purchase sending credits; remain within free sandbox limits or continue using Mailpit.
4. Restart the worker, trigger a synthetic notification and verify it appears in the sandbox inbox. Mailtrap credentials are not required when Mailpit is used.

## Twilio test credentials: no real SMS or charge

Official websites: [Twilio Console](https://console.twilio.com), [test credentials and magic inputs](https://www.twilio.com/docs/iam/test-credentials).

1. Sign in/create an account. Go to Admin → Account management → API keys & tokens.
2. Find Test credentials, and copy the **test** Account SID and Auth Token. Do not use production credentials or buy a telephone number for this test.
3. Set:

```dotenv
SMS_PROVIDER=twilio
TWILIO_TEST_MODE=true
TWILIO_ACCOUNT_SID=REPLACE_WITH_TEST_ACCOUNT_SID
TWILIO_AUTH_TOKEN=REPLACE_WITH_TEST_AUTH_TOKEN
TWILIO_FROM_NUMBER=+15005550006
```

4. Restart the worker and set a synthetic customer's phone field. The adapter sends only magic-number test requests. Twilio test credentials validate API behavior but do not deliver SMS, trigger status callbacks or represent a real recipient delivery.
5. Until test credentials are configured and a response is verified, retain `SMS_PROVIDER=local`. No external SMS integration is claimed complete.

## Deployment and Docker prerequisites

The public source/deployment repositories, Docker/WSL verification and free HTTPS demo now have execution evidence. No paid resource was requested. The optional Render profile and its sleeping/expiry limits are in docs/deployment/RENDER_DEMO.md. Full production/SSH deployment remains separate. Keep all credentials outside source control and submission archives.

## Render management and demo credentials

Official API instructions: https://render.com/docs/api. Open https://dashboard.render.com/u/settings, choose Create API key, give it a name such as `FinCore Deployment`, select the intended workspace and required resource permissions, and generate it. Save the value only in the ignored local `.env` as `RENDER_API_KEY`. Never paste it into chat or deploy it as an application variable.

The root `render.yaml` uses explicit Free plans and generates application secrets in protected Render environment variables. After deployment, those values were synchronized into the local `.env` with `RENDER_` prefixes. The actual demo login is `customer@fincore.test`; its password is `RENDER_DEMO_PASSWORD`. Management access uses `RENDER_SERVICE_ID` and `RENDER_WEB_ORIGIN`. The optional `.env.render` export contains only runtime settings and excludes `RENDER_API_KEY`; it is Git-ignored and excluded from the ZIP. Local and cloud demo passwords are distinct. No Gemini key is used.
