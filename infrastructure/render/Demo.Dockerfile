# Optional free hosted demonstration. The original Compose deployment is unchanged.
FROM node:22-bookworm-slim AS build
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends openssl ca-certificates && rm -rf /var/lib/apt/lists/*
COPY package*.json ./
COPY apps/web/package.json apps/web/package.json
COPY apps/api/package.json apps/api/package.json
COPY apps/worker/package.json apps/worker/package.json
COPY packages/shared/package.json packages/shared/package.json
RUN npm ci
COPY tsconfig*.json ./
COPY apps ./apps
COPY packages ./packages
COPY database ./database
COPY scripts ./scripts
ENV DATABASE_URL=postgresql://build:build@localhost:5432/build
ENV FINCORE_STATIC_EXPORT=true NEXT_PUBLIC_API_URL=/api/v1
RUN npm run db:generate && npm run build
RUN npm prune --omit=dev --ignore-scripts

FROM axllent/mailpit:v1.34.0 AS mailpit
FROM node:22.23.5-alpine3.24 AS runtime
RUN apk upgrade --no-cache && apk add --no-cache openssl ca-certificates postgresql17-client python3
WORKDIR /app
COPY services/financial-analytics/requirements.runtime.txt /tmp/requirements.txt
RUN python3 -m venv /opt/analytics && /opt/analytics/bin/pip install --no-cache-dir -r /tmp/requirements.txt
COPY --from=build --chown=node:node /app /app
COPY --from=mailpit /mailpit /usr/local/bin/mailpit
COPY --chown=node:node services/financial-analytics/app.py /app/services/financial-analytics/app.py
COPY --chown=node:node infrastructure/render/start-demo.mjs /app/infrastructure/render/start-demo.mjs
RUN mkdir -p /app/.runtime && chown node:node /app/.runtime && rm -rf /usr/local/lib/node_modules/npm /usr/local/bin/npm /usr/local/bin/npx /opt/yarn-* /usr/local/bin/yarn /usr/local/bin/yarnpkg
USER node
ENV NODE_ENV=production FINCORE_HOSTED_DEMO=true FINCORE_SERVE_WEB=true HOST=0.0.0.0 PORT=10000 PSQL_BIN=psql
EXPOSE 10000
CMD ["node","infrastructure/render/start-demo.mjs"]
