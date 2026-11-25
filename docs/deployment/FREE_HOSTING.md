# Free hosting decision and manual steps

Verified against official provider documentation on 25 November 2026. No paid resource has been created.

## Render decision

[Render's free-instance documentation](https://render.com/docs/free) lists web services, Postgres, Key Value and static sites as free options; other service types are excluded. Free web instances sleep after inactivity, share a monthly instance-hour allowance, and free Postgres expires after 30 days. The separate continuously running BullMQ [background worker](https://render.com/docs/background-workers) therefore cannot be represented as a complete, durable free Render deployment of this architecture. Do not deploy a paid worker to make the assessment appear complete.

Your Render account can host the frontend on a free onrender.com subdomain, with the API/analytics/worker and authoritative database hosted elsewhere. `infrastructure/render/frontend.render.yaml` is an optional frontend-only configuration, not a claim that the full platform is deployed. Set a zero spend limit where available and do not attach/enable paid overage resources. Review current quotas in your Dashboard before enabling builds.

Update, 26 November 2026: an optional shared-process **free demo** is now live at https://fincore-wallet-demo-nitinsharma.onrender.com and passed eight public browser tests. Its worker runs only while the web service is awake; its private free database expires on 26 December 2026 (IST). This avoids claiming a separate always-on free worker and preserves the original architecture for a suitable VM. See `RENDER_DEMO.md` and `evidence/render-deployment-status.json`.

## Suitable full-stack alternative

[Oracle Always Free](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm) currently includes an eligible Ampere A1 allocation equivalent to 2 OCPUs and 12 GB RAM for Always Free tenancies. This is a reasonable candidate for the existing Docker Compose architecture. Capacity may be unavailable and idle instances may be reclaimed; it is not a paid production reliability guarantee. Use only resources labeled Always Free eligible and do not upgrade to paid shapes or exceed the displayed quotas.

1. Create/sign in to an OCI account and verify current Always Free eligibility in your home region. Identity/payment-method verification may be required by the provider; do not send those details to this project.
2. Provision an Always Free eligible Ubuntu VM within the documented CPU/RAM/storage limits. If no free capacity exists, stop and report that blocker rather than purchasing capacity.
3. Generate an SSH key locally, upload only its public key during provisioning, and keep the private key in your protected local environment. Allow HTTPS and controlled SSH only. Keep database/cache ports unpublished.
4. Install open-source Docker Engine and Compose using [official Ubuntu instructions](https://docs.docker.com/engine/install/ubuntu/). Clone the private GitHub repository using a restricted deploy credential. Copy a newly generated `.env` to the VM over SSH; do not reuse demo passwords publicly.
5. To obtain a free HTTPS hostname without buying a domain, register an available subdomain with [DuckDNS](https://www.duckdns.org/) and point it to the VM's public IP. Keep any DNS update token server-side. Alternatively, host the frontend on Render's free supplied hostname and configure an HTTPS API hostname separately.
6. Configure the existing HTTPS reverse proxy with that actual hostname and a free certificate. Set `WEB_ORIGIN` to the actual frontend HTTPS origin and build `NEXT_PUBLIC_API_URL` with the actual HTTPS API URL.
7. Start the production-like Compose override, run migrations, create non-default synthetic demo users securely, verify dependency readiness, execute a restore drill and test browser flows. No live Stripe key is allowed.
8. Add GitHub staging/production environment secrets from docs/deployment/DEPLOYMENT.md and require production approval. Capture real deployment/HTTPS/CI evidence before marking assessment 14 complete.

Needed from you: a provisioned eligible free VM (or another explicitly selected free equivalent), SSH access and a selected free hostname. No cloud target is provisioned yet. All credentials remain in `.env`, the host's protected configuration, or GitHub environment secrets; no credentials belong in the submission ZIP.
