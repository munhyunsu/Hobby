# Next.js 16.1 + Prisma 7 + SQLite3 + BetterAuth

## 회원가입, 로그인, 로그아웃 처리

(2025-12-26) Next.js 서버 컴포넌트, 클라이언트 컴포넌트, SQLite3 데이터베이스를 활용하여 사용자 인증 구현

### Part 1. 개발 환경 세팅

1. `Node.js` 환경 세팅

- `Node.js` 다운로드 및 환경 변수 설정
```bash
./download_nodejs.sh
source activate_nodejs.sh
```

- `Node.js` 버전 확인
```bash
node --version #v24.11.1
```


### Part  2. Project 생성

1. `Next.js` 프로젝트 생성

- 기본값 사용(Yes, use recommended defaults)
```bash
npx create-next-app@latest nextjs-auth
cd nextjs-auth
mkdir src
mv app/ src/
```

- 루트 디렉터리를 `app/` 에서 `src/app/` 으로 변경
  - `tsconfig.json`
```
{
  "compilerOptions": {
  "paths": {
    "@/*": [
      "./src/*"
    ]
  }
}
```

- 실행 확인 (`src/` 루트 디렉터리 적용 여부 확인)
  - 데모 페이지 접속 [링크](http://localhost:3000/)
```bash
npm run dev
```

2. `sqlite3` 어댑터 및 `better-auth` 설치

```bash
npm install --save-dev prisma tsx
npm install dotenv @prisma/client @prisma/adapter-better-sqlite3 better-auth
```

3. `Prisma`-`SQLite3` 연결 설정

- [Prisma-CLI](https://www.prisma.io/docs/orm/reference/prisma-cli-reference#init)
```bash
npx prisma init --datasource-provider sqlite --output ../src/generated/prisma
```

4. `prisma.config.ts` 파일 수정

- [prisma.config.ts](https://www.prisma.io/docs/orm/reference/prisma-config-reference)
- [multi-file-prisma-schema](https://www.prisma.io/docs/orm/prisma-schema/overview/location#multi-file-prisma-schema)
```bash
import 'dotenv/config';
import { defineConfig, env } from 'prisma/config';

export default defineConfig({
  schema: 'prisma/',
  migrations: {
    path: 'prisma/migrations',
    seed: 'tsx prisma/seeds/index.ts'
  },
  datasource: { 
    url: process.env['DATABASE_URL'],
  }
});
```

5. 싱글톤 `PrismaClient` 선언

- `src/lib/prisma.ts`
```typescript
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
```

- `Prisma` 관련 로그 레벨을 `PRISMA_LOG_LEVELS`를 활용하여 설정할 수 있음: `query,error,warn`


### Part 3. 회원가입, 로그인을 위한 테이블 준비

1. Secret 준비
- 토큰 및 Session 생성을 위한 Secret 준비
- 생성된 `BETTER_AUTH_SECRET` 복사 및 `.env`로 복사
```bash
npx @better-auth/cli@latest secret
```

- 현재까지의 `.env` 내용
```
DATABASE_URL="file:./dev.db"
BETTER_AUTH_SECRET="ac4c9fa9c5c63763500707e408b7579100c80bcf2aa8a8c499152eff833a8576"
BETTER_AUTH_URL="http://localhost:3000"
BETTER_AUTH_ORIGINS="https://localhost:3000"
```

2. Auth 어댑터 생성
- `src/lib/auth.ts`
- `betterAuth` 어댑터 옵션 [링크](https://www.better-auth.com/docs/reference/options)
```typescript
import { betterAuth } from 'better-auth'
import { prismaAdapter } from 'better-auth/adapters/prisma'
import { prisma } from '@/lib/prisma'

export const auth = betterAuth({
  database: prismaAdapter(prisma, {
    provider: 'sqlite',
  }),
  emailAndPassword: {
    enabled: true,
  },
  trustedOrigins: process.env.BETTER_AUTH_ORIGINS
    ? process.env.BETTER_AUTH_ORIGINS.split(',').map((x) => x.trim())
    : [],
})
```

3. Prisma Client 소스코드 생성
  - `prisma/schema.prisma` 가 수정 됨
```bash
npx prisma generate
npx @better-auth/cli generate
```

4. `prisma/schema.prisma` 수정
  - `npx prisma init --datasource-provider sqlite --output ../src/generated/prisma` 에서 생성된 내용만 남겨야 함
```prisma
// This is your Prisma schema file,
// learn more about it in the docs: https://pris.ly/d/prisma-schema

generator client {
  provider = "prisma-client"
  output   = "../src/generated/prisma"
}

datasource db {
  provider = "sqlite"
}
```

5. `prisma/models/better-auth.prisma` 생성 및 수정
```prisma
model User {
  id            String    @id
  name          String
  email         String
  emailVerified Boolean   @default(false)
  image         String?
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt
  sessions      Session[]
  accounts      Account[]

  @@unique([email])
  @@map("user")
}

model Session {
  id        String   @id
  expiresAt DateTime
  token     String
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  ipAddress String?
  userAgent String?
  userId    String
  user      User     @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@unique([token])
  @@index([userId])
  @@map("session")
}

model Account {
  id                    String    @id
  accountId             String
  providerId            String
  userId                String
  user                  User      @relation(fields: [userId], references: [id], onDelete: Cascade)
  accessToken           String?
  refreshToken          String?
  idToken               String?
  accessTokenExpiresAt  DateTime?
  refreshTokenExpiresAt DateTime?
  scope                 String?
  password              String?
  createdAt             DateTime  @default(now())
  updatedAt             DateTime  @updatedAt

  @@index([userId])
  @@map("account")
}

model Verification {
  id         String   @id
  identifier String
  value      String
  expiresAt  DateTime
  createdAt  DateTime @default(now())
  updatedAt  DateTime @updatedAt

  @@index([identifier])
  @@map("verification")
}
```

6. Database 생성 및 초기화
  - 테이블 스키마 재생성 (데이터베이스 초기화 됨!)
```bash
npx prisma generate
npx prisma db push --force-reset
```

  - `sqlite3 dev.db` 로 데이터베이스 확인
```bash
sqlite> .table
account       session       user          verification
```

### Part 4. 회원가입, 로그인 기능 구현

1. `src/app/api/auth/[...all]/route.ts` 작성
- [Next.js integration](https://www.better-auth.com/docs/integrations/next)
```typescript
import { auth } from '@/lib/auth';
import { toNextJsHandler } from 'better-auth/next-js';
 
export const { POST, GET } = toNextJsHandler(auth);
```

2. `src/lib/auth-client.ts` 작성
```typescript
import { createAuthClient } from 'better-auth/react'

export const { signIn, signUp, signOut, useSession } = createAuthClient()
```

3. `src/app/sign-up/page.tsx` 작성
```typescript
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { signUp } from '@/lib/auth-client';

export default function SignUpPage() {
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setError(null);

    const formData = new FormData(e.currentTarget);

    const res = await signUp.email({
      name: formData.get('name') as string,
      email: formData.get('email') as string,
      password: formData.get('password') as string,
    });

    if (res.error) {
      setError(res.error.message || 'Something went wrong.');
    } else {
      router.push('/dashboard');
    }
  }

  return (
    <main className='max-w-md mx-auto p-6 space-y-4 text-white'>
      <h1 className='text-2xl font-bold'>Sign Up</h1>

      {error && <p className='text-red-500'>{error}</p>}

      <form onSubmit={handleSubmit} className='space-y-4'>
        <input
          name='name'
          placeholder='Full Name'
          required
          className='w-full rounded-md bg-neutral-900 border border-neutral-700 px-3 py-2'
        />
        <input
          name='email'
          type='email'
          placeholder='Email'
          required
          className='w-full rounded-md bg-neutral-900 border border-neutral-700 px-3 py-2'
        />
        <input
          name='password'
          type='password'
          placeholder='Password'
          required
          minLength={8}
          className='w-full rounded-md bg-neutral-900 border border-neutral-700 px-3 py-2'
        />
        <button
          type='submit'
          className='w-full bg-white text-black font-medium rounded-md px-4 py-2 hover:bg-gray-200'
        >
          Create Account
        </button>
      </form>
    </main>
  );
}
```

4. `src/app/sign-in/page.tsx` 작성
```typescript
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { signIn } from '@/lib/auth-client';

export default function SignInPage() {
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setError(null);

    const formData = new FormData(e.currentTarget);

    const res = await signIn.email({
      email: formData.get('email') as string,
      password: formData.get('password') as string,
    });

    if (res.error) {
      setError(res.error.message || 'Something went wrong.');
    } else {
      router.push('/dashboard');
    }
  }

  return (
    <main className='max-w-md h-screen flex items-center justify-center flex-col mx-auto p-6 space-y-4 text-white'>
      <h1 className='text-2xl font-bold'>Sign In</h1>

      {error && <p className='text-red-500'>{error}</p>}

      <form onSubmit={handleSubmit} className='space-y-4'>
        <input
          name='email'
          type='email'
          placeholder='Email'
          required
          className='w-full rounded-md bg-neutral-900 border border-neutral-700 px-3 py-2'
        />
        <input
          name='password'
          type='password'
          placeholder='Password'
          required
          className='w-full rounded-md bg-neutral-900 border border-neutral-700 px-3 py-2'
        />
        <button
          type='submit'
          className='w-full bg-white text-black font-medium rounded-md px-4 py-2 hover:bg-gray-200'
        >
          Sign In
        </button>
      </form>
    </main>
  );
}
```

5. `src/app/dashboard/page.tsx` 작성
```typescript
'use client';

import { useRouter } from 'next/navigation';
import { useSession, signOut } from '@/lib/auth-client';
import { useEffect } from 'react';

export default function DashboardPage() {
  const router = useRouter();
  const { data: session, isPending } = useSession();

  useEffect(() => {
    if (!isPending && !session?.user) {
      router.push('/sign-in');
    }
  }, [isPending, session, router]);

  if (isPending)
    return <p className='text-center mt-8 text-white'>Loading...</p>;
  if (!session?.user)
    return <p className='text-center mt-8 text-white'>Redirecting...</p>;

  const { user } = session;

  return (
    <main className='max-w-md h-screen flex items-center justify-center flex-col mx-auto p-6 space-y-4 text-white'>
      <h1 className='text-2xl font-bold'>Dashboard</h1>
      <p>Welcome, {user.name || 'User'}!</p>
      <p>Email: {user.email}</p>
      <button
        onClick={() => signOut()}
        className='w-full bg-white text-black font-medium rounded-md px-4 py-2 hover:bg-gray-200'
      >
        Sign Out
      </button>
    </main>
  );
}
```

6. `src/app/page.tsx` 작성
```typescript
'use client';

import { useRouter } from 'next/navigation';

export default function Home() {
  const router = useRouter();

  return (
    <main className='flex items-center justify-center h-screen bg-neutral-950 text-white'>
      <div className='flex gap-4'>
        <button
          onClick={() => router.push('/sign-up')}
          className='bg-white text-black font-medium px-6 py-2 rounded-md hover:bg-gray-200'>
          Sign Up
        </button>
        <button
          onClick={() => router.push('/sign-in')}
          className='border border-white text-white font-medium px-6 py-2 rounded-md hover:bg-neutral-800'>
          Sign In
        </button>
      </div>
    </main>
  );
}
```

### Part 5. JWT (Json Web Token) 생성 및 인증 추가

**개선 목표**
  - 웹(Web/브라우저): 지금 그대로 쿠키 세션 사용 (Better Auth 기본 흐름)
  - 앱(Capacitor):
    - refresh token 역할 = Better Auth가 발급하는 세션 토큰(set-auth-token) 을 Secure Storage에 저장
    - access token 역할 = Better Auth JWT 플러그인으로 발급받는 JWT를 일반 Storage에 저장
    - 만료 시: refresh(=세션 토큰)로 /api/auth/token 호출해서 새 JWT 재발급

1. `src/lib/auth.ts` 수정
  - 웹 세션 유지 + JWT 발급 기능 추가
```typescript
import { betterAuth } from 'better-auth'
import { jwt, bearer } from 'better-auth/plugins'
import { prismaAdapter } from 'better-auth/adapters/prisma'
import { prisma } from '@/lib/prisma'

export const auth = betterAuth({
  database: prismaAdapter(prisma, {
    provider: 'sqlite',
  }),
  emailAndPassword: {
    enabled: true,
  },
  trustedOrigins: process.env.BETTER_AUTH_ORIGINS
    ? process.env.BETTER_AUTH_ORIGINS.split(',').map((x) => x.trim())
    : [],
  plugins: [
    jwt(),
    bearer(),
  ],
})
```

2. Prisma Client 소스코드 재생성
```bash
npx prisma generate
npx @better-auth/cli generate
```


3. `prisma/schema.prisma` 수정
  - `npx prisma init --datasource-provider sqlite --output ../src/generated/prisma` 에서 생성된 내용만 남겨야 함
```prisma
// This is your Prisma schema file,
// learn more about it in the docs: https://pris.ly/d/prisma-schema

generator client {
  provider = "prisma-client"
  output   = "../src/generated/prisma"
}

datasource db {
  provider = "sqlite"
}
```

5. `prisma/models/better-auth.prisma` 생성 및 수정
```prisma
model User {
  id            String    @id
  name          String
  email         String
  emailVerified Boolean   @default(false)
  image         String?
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt
  sessions      Session[]
  accounts      Account[]

  @@unique([email])
  @@map("user")
}

model Session {
  id        String   @id
  expiresAt DateTime
  token     String
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  ipAddress String?
  userAgent String?
  userId    String
  user      User     @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@unique([token])
  @@index([userId])
  @@map("session")
}

model Account {
  id                    String    @id
  accountId             String
  providerId            String
  userId                String
  user                  User      @relation(fields: [userId], references: [id], onDelete: Cascade)
  accessToken           String?
  refreshToken          String?
  idToken               String?
  accessTokenExpiresAt  DateTime?
  refreshTokenExpiresAt DateTime?
  scope                 String?
  password              String?
  createdAt             DateTime  @default(now())
  updatedAt             DateTime  @updatedAt

  @@index([userId])
  @@map("account")
}

model Verification {
  id         String   @id
  identifier String
  value      String
  expiresAt  DateTime
  createdAt  DateTime @default(now())
  updatedAt  DateTime @updatedAt

  @@index([identifier])
  @@map("verification")
}

model Jwks {
  id         String    @id
  publicKey  String
  privateKey String
  createdAt  DateTime
  expiresAt  DateTime?

  @@map("jwks")
}
```


## References
- [Session Management](https://www.better-auth.com/docs/concepts/session-management)
