# Optional free Render demonstration

This additive deployment profile preserves the normal Next.js/Express/FastAPI/worker Compose architecture. It exports the same Next.js client UI and serves it from Express on the same HTTPS origin. This keeps refresh cookies first-party and reduces memory use. FastAPI, BullMQ and private Mailpit run as supervised child processes in the same container.

Only the web service, a dedicated Postgres instance and a dedicated Key Value instance use Render's explicit `free` plans. No persistent disk, paid worker, paid scaling or paid database is requested. The web service sleeps on idle, so background work also pauses. Redis and the private Mailpit inbox are ephemeral. The PostgreSQL outbox is authoritative for pending delivery, but the free database expires after 30 days. This is a synthetic demonstration, not an always-on production deployment or completion of the durable cloud assessment.

The API key remains in the ignored local `.env` as `RENDER_API_KEY`. Unique cloud database credentials, JWT/MFA/internal/webhook secrets and `RENDER_DEMO_PASSWORD` are stored there with `RENDER_` prefixes and copied only into protected Render environment variables. The Render API key is never copied into the deployed application. Database and Redis external IP allow lists remain empty. Only the HTTPS application port is public; internal analytics, worker health and Mailpit are bound to loopback.

Startup is explicitly gated by `FINCORE_HOSTED_DEMO=true`, `PAYMENT_PROVIDER=local`, production mode and strong generated demo credentials. The bootstrap creates a restricted application database role, applies the original migrations and initializes synthetic users without resetting existing records. Owner database credentials are removed from the API and worker child environments. Production activation of simulated MFA remains disabled by the existing security rule. Stripe/Twilio and external Stripe refund delivery remain unverified.

Files: `infrastructure/render/Demo.Dockerfile`, `start-demo.mjs`, `scripts/render-bootstrap.ts`, `services/financial-analytics/requirements.runtime.txt`, and the optional export in `apps/web/next.config.mjs`. `FINCORE_SERVE_WEB=true` activates static serving; its content security policy hashes the generated inline scripts instead of allowing arbitrary inline JavaScript.

Official limits: https://render.com/docs/free. Credentials/API setup: https://render.com/docs/api. Actual deployment and browser evidence must be captured before claiming a live URL; configuration alone is not deployment evidence. The original hosted image-security gate and independent-review requirements are retained.

## Current deployment and manual continuation

The root `render.yaml` provides an easier **Deploy to Render** option: it references the dedicated private datastores and generates strong application/demo secrets inside Render. No API key or secret is embedded in the Blueprint. The entrypoint derives the restricted application's connection string from the owner connection and generated role password. After deployment, the management API can synchronize the generated credentials into the ignored local `.env` without displaying them.

On 26 November 2026, API authentication succeeded and the dedicated `fincore-demo-db` and `fincore-demo-redis` instances were created on explicit free plans in Singapore with empty external IP allow lists. The database expires at 2026-12-25T19:00:32Z (26 December, 00:30 IST). Automatic approval review rejected creation of the web service with only "blocked by policy" as its reason. The web application has not been deployed and no public application URL is verified.

The same-origin production-mode UI/API profile passed eight local browser checks, including CSP hydration, secure HttpOnly refresh cookies after reload, denied private-file/staff access, customer funding and Mailpit delivery. The separate [container verification run](https://github.com/nitinsharma2005900-ai/FinCore-Digital-Wallet-Platform-Deployment/actions/runs/45683317516) also passed all eight browser tests against the complete container with a 512 MiB memory limit, exercising bootstrap, restricted-role migrations, FastAPI, BullMQ and private Mailpit. Neither run substitutes for verification of the actual public Render service. The user subsequently reported creating a web service, but the current API key does not show a FinCore service; its actual URL is required to verify that deployment.

To finish the authorized free demo manually:

1. In https://dashboard.render.com choose New > Web Service > Public Git repository and enter `https://github.com/nitinsharma2005900-ai/FinCore-Digital-Wallet-Platform-Deployment`.
2. Select branch `deployment/render-free-demo`, runtime Docker, name `fincore-wallet-demo-nitinsharma`, region Singapore and the **Free** instance type.
3. In Advanced settings set Dockerfile Path to `infrastructure/render/Demo.Dockerfile`, Docker Build Context to `.`, and Health Check Path to `/ready`. Keep automatic deploys off while the image-security/independent-review gates are unresolved.
4. Use Environment > Add from .env and paste the contents of the local ignored `.env.render` file. This generated file contains only this demo's runtime settings, not the Render management API key. Never commit or send this file through chat. Leave the existing PostgreSQL and Redis instances on Free.
5. Create the web service. Its entrypoint applies migrations and initializes synthetic accounts; free one-off jobs/shell access are not required. If any paid plan, paid build option or upgrade is required, stop.
6. After Render reports Live, copy the actual HTTPS URL and verify `/health`, `/ready` and the hosted browser suite against that URL. Until then, deployment remains incomplete. The cloud demo login is `customer@fincore.test` with the password stored as `RENDER_DEMO_PASSWORD` in the local `.env`.
