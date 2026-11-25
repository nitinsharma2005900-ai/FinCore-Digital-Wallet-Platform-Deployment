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
ARG NEXT_PUBLIC_API_URL=http://127.0.0.1:4000/api/v1
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
ARG NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=
ENV NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=$NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY
RUN npm run db:generate && npm run build
RUN npm prune --omit=dev --ignore-scripts
FROM node:22.23.5-alpine3.24 AS runtime
RUN apk upgrade --no-cache && apk add --no-cache openssl ca-certificates postgresql17-client
# The runtime invokes Node directly; package managers are build-time tools.
RUN rm -rf /usr/local/lib/node_modules/npm /usr/local/bin/npm /usr/local/bin/npx /opt/yarn-* /usr/local/bin/yarn /usr/local/bin/yarnpkg
WORKDIR /app
COPY --from=build --chown=node:node /app /app
RUN mkdir -p /app/.runtime && chown node:node /app/.runtime
USER node
ENV NODE_ENV=production HOST=0.0.0.0 PSQL_BIN=psql
EXPOSE 3000 4000
CMD ["node","dist/apps/api/src/server.js"]
