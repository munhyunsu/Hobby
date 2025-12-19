import { PrismaBetterSqlite3 } from '@prisma/adapter-better-sqlite3';
import { PrismaClient } from '@/generated/prisma/client';
import { LogLevel, LogDefinition } from '@/generated/prisma/internal/prismaNamespace';

const adapter = new PrismaBetterSqlite3({
  url: process.env.DATABASE_URL,
});

function getPrismaLog() {
  if (process.env.PRISMA_LOG_LEVELS) {
    return process.env.PRISMA_LOG_LEVELS.split(',').map((x) => x.trim());
  }
  if (process.env.NODE_ENV !== 'production') {
    return ['query', 'error', 'warn'];
  }
  return ['error'];
}

export const prisma = new PrismaClient({
  adapter: adapter,
  log: getPrismaLog() as (LogLevel | LogDefinition)[],
});
