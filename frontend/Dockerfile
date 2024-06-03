^FROM node:slim AS base

# Install pnpm
RUN npm install -g pnpm


WORKDIR /app
COPY package.json ./
RUN pnpm install

# dev server
CMD pnpm install && pnpm run dev --host
